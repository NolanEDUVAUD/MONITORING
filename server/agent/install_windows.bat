@echo off
REM HyperMonitor Agent Windows Registry Setup Script
REM This script adds the agent to Windows startup via Registry

setlocal enabledelayedexpansion

REM Colors (using for display)
color 0A

REM Get admin rights
net session >nul 2>&1
if errorlevel 1 (
    echo [!] This script requires Administrator privileges
    echo [*] Requesting elevation...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "AGENT_PATH=%SCRIPT_DIR%start_agent_windows.bat"

echo.
echo ============================================================
echo   HyperMonitor Agent - Windows Startup Setup
echo ============================================================
echo.

REM Check if agent script exists
if not exist "%AGENT_PATH%" (
    echo [!] Error: start_agent_windows.bat not found
    echo [*] Expected at: %AGENT_PATH%
    timeout /t 5
    exit /b 1
)

REM Set registry path
set "REG_PATH=HKLM\Software\Microsoft\Windows\CurrentVersion\Run"
set "REG_NAME=HyperMonitorAgent"

echo [*] Setting up Windows Registry entry...
echo [*] Registry Path: %REG_PATH%
echo [*] Value Name: %REG_NAME%
echo [*] Agent Path: %AGENT_PATH%
echo.

REM Create registry entry
reg add "%REG_PATH%" /v "%REG_NAME%" /t REG_SZ /d "cmd /c start /min %AGENT_PATH%" /f
if errorlevel 1 (
    echo [!] Error: Failed to create registry entry
    timeout /t 5
    exit /b 1
)

echo [OK] Registry entry created successfully!
echo.
echo [*] The agent will start automatically on next system boot.
echo [*] Or start now: %AGENT_PATH%
echo.
echo [*] To remove from startup:
echo [*] reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v HyperMonitorAgent /f
echo.
timeout /t 10
set /p API_URL="URL du serveur: "
if "!API_URL!"=="" (
    set API_URL=http://192.168.1.109:8888
    echo Utilisation de l'URL par defaut: !API_URL!
)

echo.
echo [3/3] Demarrage de l'agent...
echo.
python agent.py --url !API_URL!

echo.
echo ========================================
echo Options de demarrage:
echo ========================================
echo.
echo OPTION A - Demarrage manuel :
echo    python agent.py --url http://192.168.1.109:8888
echo.
echo OPTION B - Service Windows (requiert droits admin) :
echo    1. Ouvrir Planificateur de taches
echo    2. Creer une tache de base
echo    3. Demarrage: Au demarrage du PC
echo    4. Action: Demarrer un programme
echo    5. Programme: python.exe
echo    6. Arguments: %CD%\agent.py --url http://192.168.1.109:8888
echo.
echo OPTION C - Batch de lancement (simple) :
echo    Creer un fichier run.bat dans le meme dossier avec:
echo    @echo off
echo    python agent.py --url http://192.168.1.109:8888
echo    pause
echo.

pause
