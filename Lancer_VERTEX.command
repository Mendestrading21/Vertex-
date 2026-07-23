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
  ./.venv/bin/python -m pip install --upgrade pip
  ./.venv/bin/python -m pip install -r requirements.txt || { echo ""; echo "❌ Échec installation des dépendances (voir erreurs ci-dessus)."; read -p "Entrée…"; exit 1; }
  echo "✅ Installation terminée."
fi

echo ""
echo "✅ VERTEX démarre…  GARDE CETTE FENÊTRE OUVERTE."
echo "   Le navigateur s'ouvrira TOUT SEUL dès que c'est prêt (~10 à 30 s)."
echo "   Sinon, ouvre : http://localhost:5002    (Ctrl+C pour arrêter)"
echo ""

# Ouvre le navigateur SEULEMENT quand le serveur répond vraiment (sonde /healthz).
( for i in $(seq 1 120); do
    if curl -sf "http://localhost:5002/healthz" >/dev/null 2>&1; then open "http://localhost:5002" >/dev/null 2>&1; break; fi
    sleep 1
  done ) &

# Lancement. Par défaut : DIRECT (live si TWS ouvert, sinon différé).
exec ./.venv/bin/python terminal.py
