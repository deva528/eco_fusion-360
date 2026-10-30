@echo off
title Push Eco Fusion 360 to GitHub
echo ========================================================
echo       Pushing Eco Fusion 360 to GitHub Repository...
echo ========================================================
echo.
cd /d "%~dp0"

echo Running: git push -u origin main
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo  SUCCESS! All files pushed to GitHub successfully!
    echo ========================================================
) else (
    echo.
    echo If prompted, click 'Sign in with your browser' to authenticate.
)
pause
