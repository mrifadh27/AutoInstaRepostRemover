@echo off
title Instagram Repost Remover - Automation Runner
color 0B
cls

echo ======================================================================
echo           INSTAGRAM REPOST REMOVER - ONE-CLICK RUNNER
echo ======================================================================
echo  Speed Mode  : Configurable (Recommended: SAFE Mode)
echo  Notice      : Adjust mode into your internet speed!
echo  Tip         : Use Safe mode if your internet is slow.
echo ======================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    color 0C
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Ensure selenium is installed
echo [*] Checking dependencies...
python -c "import selenium" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [*] Installing required 'selenium' package...
    if exist "requirements.txt" (
        python -m pip install -r requirements.txt
    ) else (
        python -m pip install --upgrade selenium
    )
    if %ERRORLEVEL% neq 0 (
        color 0C
        echo [ERROR] Failed to install required packages.
        pause
        exit /b 1
    )
)

echo [OK] Dependencies verified.
echo.
echo [*] Starting automation engine...
echo ======================================================================
echo.

python repost_remover.py

echo.
echo ======================================================================
echo  Process completed or stopped.
echo ======================================================================
pause
