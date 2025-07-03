@echo off
title Push To Talk For Everything
echo Starting Push To Talk For Everything...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import pyaudio, keyboard" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install required packages
        pause
        exit /b 1
    )
)


echo Starting the application...
echo.
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Program exited with an error.
    pause
) 