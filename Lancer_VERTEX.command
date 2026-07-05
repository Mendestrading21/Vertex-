#!/bin/bash
# ════════════════════════════════════════════════════════════════
#   ▲ VERTEX — Terminal d'analyse (macOS)
#   Double-clic = installe (1re fois) puis lance. Ouvre le navigateur.
#
#   MODE DIRECT (données live) : ouvre TWS ou IB Gateway AVANT,
#   avec l'API en LECTURE SEULE (Read-Only API + 127.0.0.1 en Trusted).
#   Sans TWS, VERTEX fonctionne quand même en données différées.
#
#   ⛔ Analyse uniquement — VERTEX ne passe JAMAIS d'ordre.
# ════════════════════════════════════════════════════════════════
cd "$(dirname "$0")"
clear
echo "════════════════════════════════════════"
echo "   ▲  V E R T E X   —  démarrage"
echo "════════════════════════════════════════"

if ! command -v python3 >/dev/null 2>&1; then
  echo ""
  echo "❌ Python 3 n'est pas installé sur ce Mac."
  echo "   Télécharge-le ici :  https://www.python.org/downloads/"
  echo "   Puis relance ce fichier."
  echo ""
  read -p "Appuie sur Entrée pour fermer…"
  exit 1
fi

# Première fois : environnement isolé + installation des dépendances.
if [ ! -d ".venv" ]; then
  echo ""
  echo "⏳ Première installation (1 à 2 minutes, une seule fois)…"
  python3 -m venv .venv || { echo "❌ Échec création de l'environnement."; read -p "Entrée…"; exit 1; }
  ./.venv/bin/python -m pip install --quiet --upgrade pip
  ./.venv/bin/python -m pip install --quiet -r requirements.txt || { echo "❌ Échec installation des dépendances."; read -p "Entrée…"; exit 1; }
  echo "✅ Installation terminée."
fi

echo ""
echo "✅ VERTEX démarre…  →  http://localhost:5002"
echo "   (le navigateur s'ouvre tout seul dans 5 s · Ctrl+C pour arrêter)"
echo ""

# Ouvre le navigateur quand le serveur est prêt.
( sleep 5; open "http://localhost:5002" >/dev/null 2>&1 ) &

# Lancement. Par défaut : DIRECT (live si TWS ouvert, sinon différé).
exec ./.venv/bin/python terminal.py
