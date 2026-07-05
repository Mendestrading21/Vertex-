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
  python3 -m venv .venv
  ./.venv/bin/python -m pip install --quiet --upgrade pip
  ./.venv/bin/python -m pip install --quiet -r requirements.txt
fi

echo ""
echo "✅ VERTEX (démo) démarre…  →  http://localhost:5002"
echo "   (navigateur auto dans 5 s · Ctrl+C pour arrêter)"
( sleep 5; open "http://localhost:5002" >/dev/null 2>&1 ) &
export DEMO=1 NO_IBKR=1
exec ./.venv/bin/python terminal.py
