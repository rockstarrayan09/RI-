@echo off
title RI ENTERPRISES - Website
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo First time setup required...
    call INSTALL.bat
)

if not exist ".env" (
    copy .env.example .env
)

echo ============================================
echo   RI ENTERPRISES Website Starting...
echo   Open: http://127.0.0.1:5000
echo   Press Ctrl+C to stop the server
echo ============================================
echo.

start "" "http://127.0.0.1:5000"
venv\Scripts\python.exe app.py

if errorlevel 1 (
    echo.
    echo ERROR: Website could not start.
    echo Try running INSTALL.bat first.
    pause
)
