@echo off
title RI ENTERPRISES - Enable Auto Start
cd /d "%~dp0"

set "START_SCRIPT=%~dp0START_WEBSITE.bat"
set "SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\RI_ENTERPRISES_Website.lnk"

echo Adding website to Windows Startup...
powershell -NoProfile -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT%'); $s.TargetPath='%START_SCRIPT%'; $s.WorkingDirectory='%~dp0'; $s.WindowStyle=7; $s.Description='RI ENTERPRISES Website'; $s.Save()"

if exist "%SHORTCUT%" (
    echo.
    echo SUCCESS: Website will start automatically when Windows turns on.
    echo Shortcut created at:
    echo %SHORTCUT%
) else (
    echo.
    echo ERROR: Could not create startup shortcut.
)

echo.
pause
