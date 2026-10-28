@echo off
setlocal
cd /d "%~dp0"
title Clean My Fire TV - Universal Optimization Suite

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] Python is not found in PATH. Please install Python 3.8 or newer.
    pause
    exit /b 1
)

python main.py %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [*] Execution completed with status code %ERRORLEVEL%.
    pause
)
