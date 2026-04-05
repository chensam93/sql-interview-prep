@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Creating .venv and installing dependencies...
  python -m venv .venv
  if errorlevel 1 (
    echo Failed to create venv. Is Python on PATH?
    exit /b 1
  )
  .venv\Scripts\python.exe -m pip install --upgrade pip
  if errorlevel 1 exit /b 1
  .venv\Scripts\python.exe -m pip install -r requirements.txt
  if errorlevel 1 exit /b 1
)

.venv\Scripts\python.exe data\bootstrap.py %*
exit /b %ERRORLEVEL%
