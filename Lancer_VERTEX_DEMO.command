#!/bin/bash
# ════════════════════════════════════════════════════════════════
#   ▲ VERTEX — mode DÉMO (macOS)
#   Données synthétiques réalistes mais FICTIVES (marquées 🎭 DÉMO).
#   Aucun réseau, aucun TWS : ça marche tout de suite, pour découvrir.
# ════════════════════════════════════════════════════════════════
cd "$(dirname "$0")"
clear
echo "════════════════════════════════════════"
echo "   ▲  VERTEX  —  mode 🎭 DÉMO"
echo "════════════════════════════════════════"

if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ Python 3 manquant → https://www.python.org/downloads/"
  read -p "Entrée pour fermer…"; exit 1
fi
if [ ! -d ".venv" ]; then
  echo "⏳ Première installation (1 à 2 min)…"
  python3 -m venv .venv || { echo "❌ Échec création de l'environnement."; read -p "Entrée…"; exit 1; }
  ./.venv/bin/python -m pip install --upgrade pip
  ./.venv/bin/python -m pip install -r requirements.txt || { echo ""; echo "❌ Échec installation des dépendances (voir erreurs ci-dessus)."; read -p "Entrée…"; exit 1; }
  echo "✅ Installation terminée."
fi

echo ""
echo "✅ VERTEX (démo) démarre…  GARDE CETTE FENÊTRE OUVERTE."
echo "   Le navigateur s'ouvrira TOUT SEUL dès que c'est prêt (~10 à 30 s)."
echo "   Sinon, ouvre : http://localhost:5002    (Ctrl+C pour arrêter)"
echo ""

# Ouvre le navigateur SEULEMENT quand le serveur répond vraiment (sonde /healthz).
( for i in $(seq 1 120); do
    if curl -sf "http://localhost:5002/healthz" >/dev/null 2>&1; then open "http://localhost:5002" >/dev/null 2>&1; break; fi
    sleep 1
  done ) &

export DEMO=1 NO_IBKR=1
exec ./.venv/bin/python terminal.py
