#!/usr/bin/env bash
# Relance Vertex en mode démo pour les preuves visuelles 2.0.
# Port fixe 8099 — même adresse pour toutes les captures avant/après.
set -u
SP="${VX2_SCRATCH:-/tmp/vertex-2-0}"
mkdir -p "$SP"
if [ -f "$SP/server.pid" ]; then
  kill "$(cat "$SP/server.pid")" 2>/dev/null
  sleep 2
fi
cd /home/user/Vertex-
DEMO=1 NO_IBKR=1 nohup python -c "
from vertex.runtime import app
app.run(host='127.0.0.1', port=8099, debug=False, use_reloader=False, threaded=True)
" > "$SP/server.log" 2>&1 &
echo $! > "$SP/server.pid"
for i in $(seq 1 30); do
  code=$(curl -s -o /dev/null -w '%{http_code}' --noproxy '*' http://127.0.0.1:8099/healthz 2>/dev/null)
  if [ "$code" = "200" ]; then echo "vertex prêt (pid $(cat "$SP/server.pid")) — /healthz 200"; exit 0; fi
  sleep 1
done
echo "ÉCHEC de démarrage :"; tail -25 "$SP/server.log"; exit 1
