@echo off
REM Playwright Test Framework - Windows Installation Script
REM Run this script to set up the test environment

echo ========================================
echo Playwright UI Automation Setup
echo ========================================
echo.

REM Check Python installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if exist playwright_venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv playwright_venv
    echo Virtual environment created successfully!
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call playwright_venv\Scripts\activate.bat
echo.

REM Install Python dependencies
echo [4/6] Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Install Playwright browsers
echo [5/6] Installing Playwright browsers...
playwright install chromium
echo.

REM Create .env file
echo [6/6] Setting up environment configuration...
if exist .env (
    echo .env file already exists, skipping...
) else (
    copy .env.test .env
    echo .env file created from template!
)
echo.

echo ========================================
echo Setup Complete! ✅
echo ========================================
echo.
echo Next steps:
echo 1. Review and update .env file if needed
echo 2. Update selectors in constants/selectors.py
echo 3. Update test data in constants/test_data.py
echo 4. Start your application (Flask backend + Frontend)
echo 5. Run tests: pytest -m smoke
echo.
echo For more information, see:
echo - QUICKSTART.md
echo - README.md
echo - SETUP_COMPLETE.md
echo.
echo Happy Testing! 🎭
echo.
pause
