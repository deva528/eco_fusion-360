@echo off
title Eco Fusion 360 Web Server
echo ========================================================
echo       Starting Eco Fusion 360 Web Application...
echo ========================================================
echo.
cd /d "%~dp0"

echo Launching browser at http://127.0.0.1:5001/ ...
start "" http://127.0.0.1:5001/

echo Starting Flask Server (Press Ctrl+C to stop)...
python app.py
pause
