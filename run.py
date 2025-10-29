#!/usr/bin/env python3
"""
Universal runner for media-analysis skill
Ensures all scripts run with the correct virtual environment
"""

import os
import sys
import subprocess
from pathlib import Path


def get_venv_python():
    """Get the virtual environment Python executable"""
    skill_dir = Path(__file__).parent
    venv_dir = skill_dir / "venv"

    if os.name == 'nt':  # Windows
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:  # Unix/Linux/Mac
        venv_python = venv_dir / "bin" / "python"

    return venv_python


def ensure_venv():
    """Ensure virtual environment exists and dependencies are installed"""
    skill_dir = Path(__file__).parent
    venv_dir = skill_dir / "venv"
    requirements_file = skill_dir / "requirements.txt"

    # Check if venv exists
    if not venv_dir.exists():
        print("[*] First-time setup: Creating virtual environment...")
        print("    This may take a few minutes...")

        # Create venv
        result = subprocess.run([sys.executable, "-m", "venv", str(venv_dir)])
        if result.returncode != 0:
            print("[!] Failed to create virtual environment")
            sys.exit(1)

        print("[+] Virtual environment created")

        # Install dependencies
        print("[*] Installing dependencies...")
        venv_python = get_venv_python()

        # Upgrade pip first
        subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Install requirements
        result = subprocess.run([str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)])
        if result.returncode != 0:
            print("[!] Failed to install dependencies")
            sys.exit(1)

        print("[+] Dependencies installed")
        print("[+] Environment ready!")

    return get_venv_python()


def main():
    """Main runner"""
    if len(sys.argv) < 2:
        print("Usage: python run.py <file_path>")
        print("\nAnalyzes media files (PDF, images, audio, video) using Gemini + OCR")
        print("\nExample:")
        print("  python run.py ticket.pdf")
        print("  python run.py screenshot.png")
        print("  python run.py recording.mp3")
        sys.exit(1)

    file_path = sys.argv[1]

    # Check if file exists
    if not Path(file_path).exists():
        print(f"[!] File not found: {file_path}")
        sys.exit(1)

    # Ensure venv exists and get Python executable
    venv_python = ensure_venv()

    # Get main.py path
    skill_dir = Path(__file__).parent
    main_script = skill_dir / "main.py"

    if not main_script.exists():
        print(f"[!] main.py not found in {skill_dir}")
        sys.exit(1)

    # Build command
    cmd = [str(venv_python), str(main_script), file_path]

    # Run the script
    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
