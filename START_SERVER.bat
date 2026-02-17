@echo off
echo ============================================
echo MAXY Chat Backend Server
echo ============================================
echo.
echo Starting server on http://localhost:8000
echo.
echo DO NOT CLOSE THIS WINDOW!
echo Keep this window open while using the chat
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

cd /d "%~dp0\backend"

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Install dependencies quietly
echo Installing dependencies (if needed)...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed
echo.
echo 🚀 Starting server...
echo 🌐 Open http://localhost:8000 in your browser
echo.

:: Start the server
python server.py

if errorlevel 1 (
    echo.
    echo ❌ Server crashed with error code %errorlevel%
    echo.
    pause
)
