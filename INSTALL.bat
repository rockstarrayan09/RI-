@echo off
title RI ENTERPRISES - Setup
cd /d "%~dp0"

echo ============================================
echo   RI ENTERPRISES - First Time Setup
echo ============================================
echo.

py --version >nul 2>&1
if errorlevel 1 (
    echo Python not found!
    pause
    exit /b 1
)

echo Python Found:
py --version
echo.

echo Creating Virtual Environment...
py -m venv venv

if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

echo Activating Virtual Environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
py -m pip install --upgrade pip

echo.
echo Installing requirements...
py -m pip install -r requirements.txt

echo.
echo ============================================
echo Setup Completed!
echo ============================================
pause