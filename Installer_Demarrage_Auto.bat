@echo off
REM ================================================================
REM   VERTEX - Demarrage automatique avec Windows (optionnel)
REM   Double-clic = VERTEX se lancera tout seul (silencieux) a chaque
REM   ouverture de session Windows. Pour retirer : relance ce fichier.
REM
REM   CE QUI NE MARCHAIT PAS, mesure le 26 aout 2026 :
REM
REM     schtasks /create ... /tr "cmd /c cd /d \"%~dp0\" ^&^& ..."
REM     -> Erreur : Argument ou option non valide - '^&^&'.
REM
REM   `schtasks /tr` ne recoit pas une commande composee. La tache
REM   n'etait donc JAMAIS creee — et l'installeur affichait quand meme
REM   « OK : VERTEX demarrera automatiquement a chaque session ».
REM   Un statut qui s'affirme sans se verifier est un mensonge.
REM
REM   Corrige sur deux plans :
REM     * la tache pointe sur `_vertex_autostart.cmd`, un seul fichier,
REM       aucun echappement ;
REM     * le « OK » n'est affiche QUE si la tache existe reellement.
REM ================================================================
cd /d "%~dp0"
title VERTEX - Demarrage auto

if not exist "_vertex_autostart.cmd" (
  echo [X] `_vertex_autostart.cmd` est introuvable a cote de ce fichier.
  echo     Les deux doivent rester ensemble dans le dossier de VERTEX.
  pause
  exit /b 1
)

schtasks /query /tn "VertexAutoStart" >nul 2>nul
if %errorlevel%==0 (
  echo VERTEX est deja en demarrage automatique.
  choice /m "Le RETIRER du demarrage automatique ?"
  if errorlevel 2 exit /b 0
  schtasks /delete /tn "VertexAutoStart" /f >nul
  echo Retire. VERTEX ne se lancera plus tout seul.
  pause
  exit /b 0
)

echo Installation du demarrage automatique...

REM  DEUX formes de /tr sont tentees, dans cet ordre :
REM    1. chemin entre guillemets echappes — forme documentee, seule a
REM       supporter un dossier dont le nom contient une espace ;
REM    2. chemin nu — plus simple, suffisante sans espace.
REM  La seconde n'est tentee que si la premiere n'a rien cree.
REM
REM  Aucune des deux n'a pu etre verifiee depuis l'environnement de
REM  developpement (shell non eleve : « Acces refuse »). C'est exactement
REM  pourquoi ce script VERIFIE au lieu d'affirmer.
schtasks /create /tn "VertexAutoStart" /sc onlogon /rl limited /f /tr "\"%~dp0_vertex_autostart.cmd\"" >nul 2>nul

schtasks /query /tn "VertexAutoStart" >nul 2>nul
if not %errorlevel%==0 schtasks /create /tn "VertexAutoStart" /sc onlogon /rl limited /f /tr "%~dp0_vertex_autostart.cmd" >nul 2>nul

REM  On ne CROIT aucun code de retour : on VERIFIE que la tache est la.
REM  C'est ce controle qui manquait, et c'est lui qui rendait le « OK »
REM  possible alors que rien n'avait ete cree.
schtasks /query /tn "VertexAutoStart" >nul 2>nul
if not %errorlevel%==0 (
  echo.
  echo [X] Echec : la tache n'a PAS ete creee — et cette fois on te le dit.
  echo.
  echo     1^) relance ce fichier en tant qu'administrateur
  echo        clic droit ^> Executer en tant qu'administrateur
  echo     2^) si cela echoue encore, VERTEX se lance parfaitement a la main :
  echo        double-clic sur Lancer_VERTEX.bat
  echo.
  pause
  exit /b 1
)

echo.
echo OK : la tache VertexAutoStart est en place — verifiee, pas supposee.
echo      VERTEX demarrera a chaque ouverture de session Windows.
echo      silencieux, en arriere-plan  -^>  http://localhost:5002
echo      Ouvre TWS pour le live IBKR ; sans TWS, donnees differees.
echo.
echo      Pour verifier la constitution active, une fois VERTEX lance :
echo         http://localhost:5002/healthz    doit afficher  "version": 4
pause
