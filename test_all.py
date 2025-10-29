#!/usr/bin/env python3
"""
BMAD-EDI Media Analysis Skill - Master Test Suite
Version: 1.0.0
Date: 2025-10-29

Runs all tests across the system:
- Component tests (OCR, Gemini, Workflow)
- Integration tests (Phase 0 end-to-end)
- Archive tests (Phase 7)
- Watcher tests (optional)
"""

import sys
import os
from pathlib import Path
import subprocess
import time

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
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.END}\n")

def run_test(test_name, test_script):
    """Run a single test script"""
    print(f"{Colors.BOLD}Running: {test_name}{Colors.END}")
    print(f"Script: {test_script}")
    print("-" * 70)

    if not Path(test_script).exists():
        print(f"{Colors.YELLOW}[!] SKIP: {test_script} not found{Colors.END}\n")
        return "SKIP", 0

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, test_script],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        elapsed = time.time() - start_time

        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print(f"{Colors.GREEN}[+] PASS{Colors.END} ({elapsed:.1f}s)\n")
            return "PASS", elapsed
        else:
            print(f"{Colors.RED}[X] FAIL{Colors.END} (exit code: {result.returncode})\n")
            return "FAIL", elapsed

    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}[X] TIMEOUT{Colors.END} (exceeded 5 minutes)\n")
        return "TIMEOUT", 300
    except Exception as e:
        print(f"{Colors.RED}[X] ERROR: {e}{Colors.END}\n")
        return "ERROR", 0

def main():
    """Run all tests"""
    print_header("BMAD-EDI MEDIA ANALYSIS - MASTER TEST SUITE")

    # Define test suite
    tests = [
        # Component Tests
        ("OCR Verification", "verify_ocr.py"),
        ("OCR Test Suite", "test_ocr.py"),

        # Integration Tests
        ("Phase 0 Integration", "test_phase0.py"),
        ("Phase 0 Integration (Extended)", "test_phase0_integration.py"),
        ("Integration Tests", "test_integration.py"),

        # Workflow Tests
        ("Archival Workflow", "test_archival_workflow.py"),
        ("Archive Verification", "verify_archive.py"),

        # Automation Tests (Optional)
        ("Watcher Tests", "test-watcher.py"),
    ]

    results = {}
    total_time = 0

    print(f"{Colors.BOLD}Test Suite:{Colors.END} {len(tests)} tests")
    print(f"{Colors.BOLD}Location:{Colors.END} {Path.cwd()}")
    print(f"{Colors.BOLD}Python:{Colors.END} {sys.version.split()[0]}")

    # Run all tests
    for test_name, test_script in tests:
        status, elapsed = run_test(test_name, test_script)
        results[test_name] = status
        total_time += elapsed

    # Summary
    print_header("TEST SUMMARY")

    passed = sum(1 for status in results.values() if status == "PASS")
    failed = sum(1 for status in results.values() if status == "FAIL")
    skipped = sum(1 for status in results.values() if status == "SKIP")
    errors = sum(1 for status in results.values() if status == "ERROR")
    timeouts = sum(1 for status in results.values() if status == "TIMEOUT")

    print(f"{Colors.BOLD}Results:{Colors.END}")
    for test_name, status in results.items():
        if status == "PASS":
            symbol = f"{Colors.GREEN}[+]{Colors.END}"
        elif status == "SKIP":
            symbol = f"{Colors.YELLOW}[!]{Colors.END}"
        else:
            symbol = f"{Colors.RED}[X]{Colors.END}"
        print(f"  {symbol} {test_name:40s} {status}")

    print(f"\n{Colors.BOLD}Statistics:{Colors.END}")
    print(f"  Total Tests:     {len(tests)}")
    print(f"  {Colors.GREEN}Passed:{Colors.END}          {passed}")
    print(f"  {Colors.RED}Failed:{Colors.END}          {failed}")
    print(f"  {Colors.YELLOW}Skipped:{Colors.END}         {skipped}")
    print(f"  Errors:          {errors}")
    print(f"  Timeouts:        {timeouts}")
    print(f"  Total Time:      {total_time:.1f}s")

    if failed + errors + timeouts == 0:
        if skipped > 0:
            print(f"\n{Colors.YELLOW}[!] ALL AVAILABLE TESTS PASSED{Colors.END} ({skipped} skipped)")
            success_rate = (passed / (len(tests) - skipped)) * 100
        else:
            print(f"\n{Colors.GREEN}[+] ALL TESTS PASSED{Colors.END}")
            success_rate = 100.0
    else:
        success_rate = (passed / len(tests)) * 100
        print(f"\n{Colors.RED}[X] SOME TESTS FAILED{Colors.END}")

    print(f"{Colors.BOLD}Success Rate:{Colors.END} {success_rate:.1f}%")

    # Exit code
    if failed + errors + timeouts > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Test suite interrupted{Colors.END}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}[X] Test suite error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
