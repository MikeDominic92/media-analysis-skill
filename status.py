#!/usr/bin/env python3
"""
BMAD-EDI Media Analysis Skill - System Status Dashboard
Version: 1.0.0
Date: 2025-10-29

Displays system status including:
- Dependencies installed
- Authentication status
- Recent processing stats
- Error summary
- Performance metrics
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import importlib.util

# Colors for terminal output (Windows compatible)
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}\n")

def print_status(label, status, details=""):
    """Print status line"""
    if status == "OK" or status == "PASS":
        symbol = f"{Colors.GREEN}[+]{Colors.END}"
        status_color = Colors.GREEN
    elif status == "WARNING" or status == "MEDIUM":
        symbol = f"{Colors.YELLOW}[!]{Colors.END}"
        status_color = Colors.YELLOW
    elif status == "ERROR" or status == "FAIL":
        symbol = f"{Colors.RED}[X]{Colors.END}"
        status_color = Colors.RED
    else:
        symbol = f"{Colors.BLUE}[i]{Colors.END}"
        status_color = Colors.BLUE

    print(f"{symbol} {label}: {status_color}{status}{Colors.END} {details}")

def check_dependencies():
    """Check if required dependencies are installed"""
    print_header("DEPENDENCY STATUS")

    dependencies = {
        "patchright": "1.55.2",
        "paddleocr": "2.7.0",
        "paddlepaddle": "2.6.0",
        "cv2": "4.8.1 (opencv-python)",
        "PIL": "10.1.0 (Pillow)",
        "watchdog": "3.0.0",
        "pdf2image": "1.16.3"
    }

    installed_count = 0
    for module_name, expected_version in dependencies.items():
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print_status(f"{module_name:20s}", "OK", f"(expected: {expected_version})")
            installed_count += 1
        else:
            print_status(f"{module_name:20s}", "ERROR", "NOT INSTALLED")

    print(f"\n{installed_count}/{len(dependencies)} dependencies installed")
    return installed_count == len(dependencies)

def check_authentication():
    """Check Gemini authentication status"""
    print_header("AUTHENTICATION STATUS")

    auth_file = Path("data/auth_info.json")
    browser_state = Path("data/browser_state")

    if auth_file.exists():
        try:
            with open(auth_file, 'r') as f:
                auth_data = json.load(f)

            authenticated = auth_data.get("authenticated", False)
            timestamp = auth_data.get("timestamp", "Unknown")

            if authenticated:
                print_status("Gemini Authentication", "OK", f"Last: {timestamp}")
            else:
                print_status("Gemini Authentication", "WARNING", "Not authenticated")
        except Exception as e:
            print_status("Gemini Authentication", "ERROR", f"Failed to read auth file: {e}")
    else:
        print_status("Gemini Authentication", "WARNING", "Not authenticated - run: python gemini_analyzer.py auth")

    if browser_state.exists() and any(browser_state.iterdir()):
        print_status("Browser State", "OK", "Session data present")
    else:
        print_status("Browser State", "WARNING", "No session data")

def check_directories():
    """Check required directories exist"""
    print_header("DIRECTORY STATUS")

    directories = {
        "Skill Directory": Path("."),
        "Data Directory": Path("data"),
        "OCR Cache": Path("data/ocr_cache"),
        "Browser State": Path("data/browser_state"),
        "Prompts": Path("prompts"),
        "Templates": Path("templates"),
        "Incoming": Path(r"C:\Users\sleep\Documents\tickets\incoming"),
        "Processing": Path(r"C:\Users\sleep\Documents\tickets\processing"),
        "Archived": Path(r"C:\Users\sleep\Documents\tickets\archived")
    }

    for name, path in directories.items():
        if path.exists():
            if path.is_dir():
                file_count = len(list(path.iterdir())) if path.is_dir() else 0
                print_status(f"{name:20s}", "OK", f"({file_count} items)")
            else:
                print_status(f"{name:20s}", "WARNING", "Exists but not a directory")
        else:
            print_status(f"{name:20s}", "WARNING", "Not found")

def analyze_logs():
    """Analyze recent logs"""
    print_header("RECENT ACTIVITY")

    log_file = Path(r"C:\Users\sleep\Documents\tickets\media-analysis.log")

    if not log_file.exists():
        print_status("Log File", "INFO", "No logs yet (first run)")
        return

    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()

        total_lines = len(lines)
        recent_lines = lines[-100:] if len(lines) > 100 else lines

        # Count message types
        info_count = sum(1 for line in recent_lines if "INFO" in line)
        warning_count = sum(1 for line in recent_lines if "WARNING" in line)
        error_count = sum(1 for line in recent_lines if "ERROR" in line)

        # Find recent processing
        processed_count = sum(1 for line in recent_lines if "Processing file:" in line)
        success_count = sum(1 for line in recent_lines if "Metadata extracted" in line)

        print_status("Total Log Lines", "INFO", f"{total_lines}")
        print_status("Recent INFO", "OK", f"{info_count}")
        if warning_count > 0:
            print_status("Recent WARNINGS", "WARNING", f"{warning_count}")
        else:
            print_status("Recent WARNINGS", "OK", "0")
        if error_count > 0:
            print_status("Recent ERRORS", "ERROR", f"{error_count}")
        else:
            print_status("Recent ERRORS", "OK", "0")

        print(f"\n{Colors.BOLD}Processing Stats:{Colors.END}")
        print_status("Files Processed", "INFO", f"{processed_count}")
        print_status("Successful Extractions", "INFO", f"{success_count}")
        if processed_count > 0:
            success_rate = (success_count / processed_count) * 100
            if success_rate >= 90:
                print_status("Success Rate", "OK", f"{success_rate:.1f}%")
            elif success_rate >= 70:
                print_status("Success Rate", "WARNING", f"{success_rate:.1f}%")
            else:
                print_status("Success Rate", "ERROR", f"{success_rate:.1f}%")

    except Exception as e:
        print_status("Log Analysis", "ERROR", f"Failed: {e}")

def check_performance():
    """Check performance metrics"""
    print_header("PERFORMANCE METRICS")

    # Check disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage(".")
        free_gb = free // (2**30)
        used_percent = (used / total) * 100

        if free_gb > 1:
            print_status("Disk Space Free", "OK", f"{free_gb} GB")
        else:
            print_status("Disk Space Free", "WARNING", f"{free_gb} GB - running low")
    except Exception as e:
        print_status("Disk Space", "ERROR", f"Failed to check: {e}")

    # Check OCR cache size
    ocr_cache = Path("data/ocr_cache")
    if ocr_cache.exists():
        try:
            cache_size = sum(f.stat().st_size for f in ocr_cache.rglob('*') if f.is_file())
            cache_mb = cache_size / (1024 * 1024)
            if cache_mb < 100:
                print_status("OCR Cache Size", "OK", f"{cache_mb:.1f} MB")
            elif cache_mb < 500:
                print_status("OCR Cache Size", "WARNING", f"{cache_mb:.1f} MB - consider clearing")
            else:
                print_status("OCR Cache Size", "ERROR", f"{cache_mb:.1f} MB - CLEAR RECOMMENDED")
        except Exception as e:
            print_status("OCR Cache", "ERROR", f"Failed to check: {e}")
    else:
        print_status("OCR Cache", "INFO", "Not created yet (first run)")

def check_watcher():
    """Check directory watcher status"""
    print_header("DIRECTORY WATCHER STATUS")

    watcher_script = Path("watch-incoming.py")
    if not watcher_script.exists():
        print_status("Watcher Script", "WARNING", "Not found")
        return

    print_status("Watcher Script", "OK", "Present")

    # Try to check if watcher is running (Windows)
    try:
        import psutil
        watcher_running = False
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and 'watch-incoming.py' in ' '.join(cmdline):
                    watcher_running = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if watcher_running:
            print_status("Watcher Process", "OK", "Running")
        else:
            print_status("Watcher Process", "INFO", "Not running (optional)")
    except ImportError:
        print_status("Watcher Process", "INFO", "Cannot check (psutil not installed)")

def print_summary():
    """Print overall system summary"""
    print_header("SYSTEM SUMMARY")

    print(f"{Colors.BOLD}BMAD-EDI Media Analysis Skill{Colors.END}")
    print(f"Version: 1.0.0")
    print(f"Status: Production Ready")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\n{Colors.BOLD}Quick Commands:{Colors.END}")
    print(f"  Authentication:    python gemini_analyzer.py auth")
    print(f"  Verify OCR:        python verify_ocr.py")
    print(f"  Test Phase 0:      python test_phase0.py")
    print(f"  Process File:      python workflow.py <file_path>")
    print(f"  View Logs:         type C:\\Users\\sleep\\Documents\\tickets\\media-analysis.log")
    print(f"  Start Watcher:     python watch-incoming.py")
    print(f"  Watcher Status:    python watcher-status.py")

    print(f"\n{Colors.BOLD}Documentation:{Colors.END}")
    print(f"  User Guide:        README.md")
    print(f"  Technical Ref:     SKILL.md")
    print(f"  Deployment:        DEPLOYMENT_GUIDE.md")
    print(f"  Quick Reference:   QUICK_REFERENCE.md")

def main():
    """Main status check"""
    print_header("BMAD-EDI MEDIA ANALYSIS SKILL - SYSTEM STATUS")

    # Run all checks
    deps_ok = check_dependencies()
    check_authentication()
    check_directories()
    analyze_logs()
    check_performance()
    check_watcher()
    print_summary()

    # Final status
    print_header("STATUS CHECK COMPLETE")

    if deps_ok:
        print(f"{Colors.GREEN}[+] System Ready{Colors.END}")
    else:
        print(f"{Colors.RED}[X] System NOT Ready - Install dependencies with: pip install -r requirements.txt{Colors.END}")

    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Status check interrupted{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[X] Error during status check: {e}{Colors.END}")
        sys.exit(1)
