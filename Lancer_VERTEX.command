#!/bin/bash
# Vertex Test 1.0 — analyse uniquement, aucun ordre.
set -e
cd "$(dirname "$0")"
clear
echo "════════════════════════════════════════"
echo "   ▲  V E R T E X  1.0 — démarrage"
echo "════════════════════════════════════════"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 est requis: https://www.python.org/downloads/"
  read -r -p "Entrée pour fermer…"
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Première installation…"
  python3 -m venv .venv
  ./.venv/bin/python -m pip install --quiet --upgrade pip
  ./.venv/bin/python -m pip install --quiet -r requirements.txt
fi

echo "VERTEX démarre sur http://localhost:5002"
( sleep 5; open "http://localhost:5002" >/dev/null 2>&1 ) &
exec ./.venv/bin/python -m vertex
