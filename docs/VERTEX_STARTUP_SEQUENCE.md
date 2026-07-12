# Vertex — Séquence de démarrage (§10)

`vertex/services/startup.py` — exécutée dans un thread au lancement,
jamais bloquante, rapport exposé (`/api/system/startup-report`) et affiché
dans Système → Automatisations.

1. **configuration** — validation .env (CONFIGURED/MISSING/INVALID + conséquence)
2. **claude** — santé du runtime (jamais « connecté » sans appel réel observé)
3. **ibkr** — passerelle readonly (OFFLINE si NO_IBKR=1)
4. **tradingview** — secret présent ?
5. **storage** — écriture desk + backups
6. **engines** — constitution chargée, moteurs importés
7. **scheduler** — registre des jobs
8. **live_stream** — diffuseur SSE prêt

Le rapport porte toujours `readonly: true` et
`order_execution: disabled-by-design`.
