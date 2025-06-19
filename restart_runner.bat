@echo off
REM Restart Runner Batch Script for Cradle RDR2
REM This script will continuously restart your runner.py when it stops

setlocal
set ENV_CONFIG=./conf/env_config_rdr2_main_storyline.json
set RESTART_DELAY=5
set RESTART_COUNT=0

echo Starting Cradle RDR2 Auto-Restart Script
echo Command: python runner.py --envConfig "%ENV_CONFIG%"
echo Restart delay: %RESTART_DELAY% seconds
echo Press Ctrl+C to stop the restart loop
echo.

:RESTART_LOOP
set /a RESTART_COUNT+=1
echo === Restart #%RESTART_COUNT% ===
echo %date% %time% - Starting runner.py

python runner.py --envConfig "%ENV_CONFIG%"

echo %date% %time% - Process exited with code %ERRORLEVEL%

if %ERRORLEVEL% EQU 0 (
    echo Process completed successfully
) else (
    echo Process exited with error code %ERRORLEVEL%
)

echo Waiting %RESTART_DELAY% seconds before restart...
timeout /t %RESTART_DELAY% /nobreak >nul

goto RESTART_LOOP 