@echo off
REM VERTEX 1.0 - analyse uniquement, aucun ordre.
cd /d "%~dp0"
title VERTEX 1.0
cls
echo ============================================
echo    V E R T E X  1.0  -  demarrage
echo ============================================

where python >nul 2>nul
if errorlevel 1 (
  echo [X] Python n'est pas installe ou absent du PATH.
  echo     https://www.python.org/downloads/
  pause
  exit /b 1
)

if not exist ".venv" (
  echo Premiere installation...
  python -m venv .venv || (echo [X] Echec creation environnement. & pause & exit /b 1)
  call ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
  call ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt || (echo [X] Echec dependances. & pause & exit /b 1)
)

echo VERTEX demarre sur http://localhost:5002
start "" cmd /c "timeout /t 5 >nul & start http://localhost:5002"
".venv\Scripts\python.exe" -m vertex
pause
