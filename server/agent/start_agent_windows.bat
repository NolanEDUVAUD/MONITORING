@echo off
REM HyperMonitor Agent Startup Script for Windows
REM This script runs at system startup

setlocal enabledelayedexpansion

REM Get the directory of this script
cd /d "%~dp0"

REM Change to agent directory
cd agent

REM Get the server URL (can be configured or use default)
set API_URL=http://localhost:8888
if exist "..\config\agent-config.txt" (
    for /f "tokens=*" %%i in (..\config\agent-config.txt) do set API_URL=%%i
)

REM Run the agent
python3 agent.py --url !API_URL! --interval 3

REM Keep window alive if there's an error
if errorlevel 1 (
    echo [ERROR] Agent failed to start
    timeout /t 5
)
