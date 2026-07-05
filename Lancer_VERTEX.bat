@echo off
REM ================================================================
REM   VERTEX - Terminal d'analyse (Windows)
REM   Double-clic = installe (1re fois) puis lance. Ouvre le navigateur.
REM
REM   MODE DIRECT (donnees live) : ouvre TWS ou IB Gateway AVANT,
REM   avec l'API en LECTURE SEULE (Read-Only API + 127.0.0.1 Trusted).
REM   Sans TWS, VERTEX fonctionne quand meme en donnees differees.
REM
REM   Analyse uniquement - VERTEX ne passe JAMAIS d'ordre.
REM ================================================================
cd /d "%~dp0"
title VERTEX
cls
echo ============================================
echo    V E R T E X   -  demarrage
echo ============================================

where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo [X] Python n'est pas installe ^(ou pas dans le PATH^).
  echo     Telecharge-le ici : https://www.python.org/downloads/
  echo     IMPORTANT : coche "Add Python to PATH" pendant l'installation.
  echo     Puis relance ce fichier.
  echo.
  pause
  exit /b 1
)

REM Premiere fois : environnement isole + installation des dependances.
if not exist ".venv" (
  echo.
  echo Premiere installation ^(1 a 2 minutes, une seule fois^)...
  python -m venv .venv || ( echo [X] Echec creation environnement. & pause & exit /b 1 )
  call ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
  call ".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt || ( echo [X] Echec installation dependances. & pause & exit /b 1 )
  echo Installation terminee.
)

echo.
echo VERTEX demarre...  ^>  http://localhost:5002
echo ^(le navigateur s'ouvre tout seul · Ctrl+C pour arreter^)
echo.

REM Ouvre le navigateur apres un court delai (sous-processus).
start "" cmd /c "timeout /t 5 >nul & start http://localhost:5002"

REM Lancement. Par defaut : DIRECT (live si TWS ouvert, sinon differe).
".venv\Scripts\python.exe" terminal.py
pause
