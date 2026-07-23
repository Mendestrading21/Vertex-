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
  echo.
  echo [X] Python n'est pas installe ^(ou pas dans le PATH^).
  echo     Telecharge-le : https://www.python.org/downloads/  ^(coche "Add Python to PATH"^)
  echo     Puis relance ce fichier.
  echo.
  pause & exit /b 1
)

if not exist ".venv" (
  echo.
  echo Premiere installation ^(1 a 2 min, une seule fois^)...
  python -m venv .venv || ( echo [X] Echec creation de l'environnement. & pause & exit /b 1 )
  call ".venv\Scripts\python.exe" -m pip install --upgrade pip
  call ".venv\Scripts\python.exe" -m pip install -r requirements.txt || ( echo. & echo [X] Echec installation des dependances ^(voir les erreurs ci-dessus^). & pause & exit /b 1 )
  echo Installation terminee.
)

echo.
echo VERTEX ^(demo^) demarre...  GARDE CETTE FENETRE OUVERTE.
echo Le navigateur s'ouvrira TOUT SEUL des que c'est pret ^(~10 a 30 s^).
echo Sinon, ouvre toi-meme : http://localhost:5002     ^(Ctrl+C pour arreter^)
echo.

REM Ouvre le navigateur SEULEMENT quand le serveur repond vraiment (sonde /healthz).
REM Evite le "site inaccessible" du navigateur ouvert avant que le serveur ecoute.
start "" powershell -NoProfile -WindowStyle Hidden -Command "for($i=0;$i -lt 120;$i++){try{$null=Invoke-WebRequest -UseBasicParsing 'http://localhost:5002/healthz' -TimeoutSec 2;Start-Process 'http://localhost:5002';break}catch{Start-Sleep -Seconds 1}}"

set DEMO=1
set NO_IBKR=1
".venv\Scripts\python.exe" terminal.py

echo.
echo VERTEX s'est arrete. Tu peux fermer cette fenetre.
pause
