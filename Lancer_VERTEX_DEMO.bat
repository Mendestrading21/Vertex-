@echo off
REM ================================================================
REM   VERTEX - mode DEMO (Windows)
REM   Donnees synthetiques realistes mais FICTIVES (marquees DEMO).
REM   Aucun reseau, aucun TWS : ca marche tout de suite, pour decouvrir.
REM ================================================================
cd /d "%~dp0"
title VERTEX - DEMO
cls
echo ============================================
echo    V E R T E X   -  mode DEMO
echo ============================================

where python >nul 2>nul
if errorlevel 1 (
  echo [X] Python manquant -^> https://www.python.org/downloads/  ^(coche "Add to PATH"^)
  pause & exit /b 1
)
if not exist ".venv" (
  echo Premiere installation ^(1 a 2 min^)...
  python -m venv .venv
  call ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
  call ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt
)

echo.
echo VERTEX ^(demo^) demarre...  ^>  http://localhost:5002
start "" cmd /c "timeout /t 5 >nul & start http://localhost:5002"
set DEMO=1
set NO_IBKR=1
".venv\Scripts\python.exe" terminal.py
pause
