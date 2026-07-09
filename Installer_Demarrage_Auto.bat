@echo off
REM ================================================================
REM   VERTEX - Demarrage automatique avec Windows (optionnel)
REM   Double-clic = VERTEX se lancera tout seul (silencieux) a chaque
REM   ouverture de session Windows. Pour retirer : relance ce fichier.
REM ================================================================
cd /d "%~dp0"
title VERTEX - Demarrage auto
schtasks /query /tn "VertexAutoStart" >nul 2>nul
if %errorlevel%==0 (
  echo VERTEX est deja en demarrage automatique.
  choice /m "Le RETIRER du demarrage automatique ?"
  if errorlevel 2 exit /b 0
  schtasks /delete /tn "VertexAutoStart" /f >nul
  echo Retire. VERTEX ne se lancera plus tout seul.
  pause & exit /b 0
)
echo Installation du demarrage automatique...
schtasks /create /tn "VertexAutoStart" /sc onlogon /rl limited ^
  /tr "cmd /c cd /d \"%~dp0\" ^&^& \".venv\Scripts\pythonw.exe\" terminal.py" >nul
if errorlevel 1 ( echo [X] Echec ^(lance en tant qu'administrateur ?^). & pause & exit /b 1 )
echo.
echo OK : VERTEX demarrera automatiquement a chaque session Windows.
echo      (silencieux, en arriere-plan -> http://localhost:5002)
echo      Ouvre TWS pour le live IBKR ; sans TWS, donnees differees.
pause
