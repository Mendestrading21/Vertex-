@echo off
REM ================================================================
REM   VERTEX — lanceur du demarrage automatique.
REM
REM   Ce fichier existe pour UNE raison : `schtasks /tr` ne sait pas
REM   recevoir une commande composee. L'installeur passait
REM
REM       /tr "cmd /c cd /d \"%~dp0\" ^&^& \"...pythonw.exe\" -m vertex"
REM
REM   et Windows repondait « Argument ou option non valide - '^&^&' ».
REM   La tache n'etait donc JAMAIS creee — alors que l'installeur
REM   affichait « OK : VERTEX demarrera automatiquement ».
REM
REM   Un seul fichier a lancer, aucun echappement : la tache pointe
REM   ici, et c'est ici qu'on se place dans le bon dossier.
REM ================================================================
cd /d "%~dp0"
if not exist ".venv\Scripts\pythonw.exe" (
  REM  Sans environnement, on ne lance rien plutot que de laisser une
  REM  tache echouer en silence a chaque ouverture de session.
  exit /b 1
)
start "" ".venv\Scripts\pythonw.exe" -m vertex
exit /b 0
