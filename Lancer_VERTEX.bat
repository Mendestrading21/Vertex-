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
  call ".venv\Scripts\python.exe" -m pip install --upgrade pip
  call ".venv\Scripts\python.exe" -m pip install -r requirements.txt || ( echo. & echo [X] Echec installation des dependances ^(voir les erreurs ci-dessus^). & pause & exit /b 1 )
  echo Installation terminee.
)

echo.
echo VERTEX demarre...  GARDE CETTE FENETRE OUVERTE.
echo Le navigateur s'ouvrira TOUT SEUL des que c'est pret ^(~10 a 30 s^).
echo Sinon, ouvre toi-meme : http://localhost:5002     ^(Ctrl+C pour arreter^)
echo.

REM Ouvre le navigateur SEULEMENT quand le serveur repond vraiment (sonde /healthz).
start "" powershell -NoProfile -WindowStyle Hidden -Command "for($i=0;$i -lt 120;$i++){try{$null=Invoke-WebRequest -UseBasicParsing 'http://localhost:5002/healthz' -TimeoutSec 2;Start-Process 'http://localhost:5002';break}catch{Start-Sleep -Seconds 1}}"

REM Lancement. Par defaut : DIRECT (live si TWS ouvert, sinon differe).
".venv\Scripts\python.exe" terminal.py

echo.
echo VERTEX s'est arrete. Tu peux fermer cette fenetre.
pause
