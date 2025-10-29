@echo off
REM BMAD-EDI Media Analysis Skill - Installation Script
REM Version: 1.0.0
REM Date: 2025-10-29

echo ============================================================
echo BMAD-EDI Media Analysis Skill - Installation
echo ============================================================
echo.

REM Check Python installation
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: Python not found. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo [+] Python found
echo.

REM Check pip
echo [2/7] Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: pip not found. Please install pip.
    pause
    exit /b 1
)
echo [+] pip found
echo.

REM Create virtual environment if it doesn't exist
echo [3/7] Setting up virtual environment...
if not exist venv\ (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [!] ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [+] Virtual environment created
) else (
    echo [+] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [4/7] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [!] ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo [+] Virtual environment activated
echo.

REM Upgrade pip
echo [5/7] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [+] pip upgraded
echo.

REM Install dependencies
echo [6/7] Installing dependencies...
echo This may take 2-5 minutes...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [!] ERROR: Failed to install dependencies
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)
echo [+] Dependencies installed successfully
echo.

REM Install Patchright browser
echo [7/7] Installing Chrome browser for Gemini...
patchright install chrome
if %errorlevel% neq 0 (
    echo [!] WARNING: Failed to install Chrome browser
    echo You may need to install it manually with: patchright install chrome
) else (
    echo [+] Chrome browser installed
)
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Next Steps:
echo 1. Authenticate with Google AI Studio:
echo    python gemini_analyzer.py auth
echo.
echo 2. Verify OCR installation:
echo    python verify_ocr.py
echo.
echo 3. Test Phase 0 workflow:
echo    python test_phase0.py
echo.
echo 4. Review documentation:
echo    - README.md (user guide)
echo    - SKILL.md (technical reference)
echo    - DEPLOYMENT_GUIDE.md (deployment instructions)
echo.
echo For help, see: QUICK_REFERENCE.md
echo ============================================================
echo.
pause
