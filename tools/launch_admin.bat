@echo off
:: Crimson Desert Trainer launcher — must run as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~fn0' -Verb RunAs"
    exit /b
)
cd /d "%~dp0.."
python -m crimson_trainer.bootstrap
pause