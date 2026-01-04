@echo off
REM Automated startup script for Word Frequency Mini Project (Windows)

echo ============================================================
echo Word Frequency Mini Project - Quick Start
echo ============================================================
echo.

REM Run the Python setup and start script
python start.py

REM If Python script fails, pause to show error
if errorlevel 1 (
    echo.
    echo ============================================================
    echo Error occurred. Please check the messages above.
    echo ============================================================
    pause
)
