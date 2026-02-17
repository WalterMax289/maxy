@echo off
echo =========================================
echo Starting MAXY Chat Backend
echo =========================================
cd /d "%~dp0\backend"
echo.
echo Installing dependencies (if needed)...
pip install -q -r requirements.txt
echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop
echo.
python server.py
pause
