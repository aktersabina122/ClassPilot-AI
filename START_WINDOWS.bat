@echo off
setlocal
cd /d "%~dp0"
title ClassPilot AI - Setup and Run

echo ========================================
echo          ClassPilot AI - Launcher
echo ========================================
echo.

py -3.13 --version >nul 2>&1
if errorlevel 1 (
  echo Python 3.13 was not found.
  echo Install Python 3.13 from python.org and enable "Add python.exe to PATH".
  echo Then double-click this file again.
  echo.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Preparing the project environment. This happens only once...
  py -3.13 -m venv .venv
  if errorlevel 1 goto :failed
)

echo Checking the required Python packages...
.venv\Scripts\python.exe -c "import flask, requests" >nul 2>&1
if errorlevel 1 (
  echo Installing packages. Please wait...
  .venv\Scripts\python.exe -m pip install -r requirements.txt
  if errorlevel 1 goto :failed
)

where ollama >nul 2>&1
if errorlevel 1 (
  echo Ollama was not found. The website can still use its built-in sample answers,
  echo but install Ollama to use the local AI model.
  echo.
  goto :start_app
)

ollama list 2>nul | findstr /I "qwen3:0.6b" >nul
if errorlevel 1 (
  echo The qwen3:0.6b model is not installed yet.
  choice /C YN /M "Download the model now? It is about 523 MB"
  if errorlevel 2 goto :start_app
  ollama pull qwen3:0.6b
  if errorlevel 1 (
    echo Model download did not finish. The app can still answer from its sample data.
    echo You can retry later with: ollama pull qwen3:0.6b
    echo.
  )
)

:start_app
echo.
echo Starting ClassPilot AI. Keep this window open while you use the chatbot.
echo Your browser will open at http://127.0.0.1:5000
echo To stop the app, close this window or press Ctrl+C.
echo.
start "" "http://127.0.0.1:5000"
.venv\Scripts\python.exe app.py
pause
exit /b 0

:failed
echo.
echo Setup did not finish. Check that Python 3.13 is installed and internet is available.
pause
exit /b 1
