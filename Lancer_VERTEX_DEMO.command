#!/bin/bash
# Vertex 1.0 — mode démo, données fictives explicitement marquées.
set -e
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 est requis: https://www.python.org/downloads/"
  read -r -p "Entrée pour fermer…"
  exit 1
fi

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  ./.venv/bin/python -m pip install --quiet --upgrade pip
  ./.venv/bin/python -m pip install --quiet -r requirements.txt
fi

export DEMO=1 NO_IBKR=1 START_ON_IMPORT=0
( sleep 5; open "http://localhost:5002" >/dev/null 2>&1 ) &
exec ./.venv/bin/python -m vertex
