# Vertex — Connexions

| Connexion | Config (.env) | Statuts | Dégradé honnête |
|---|---|---|---|
| IBKR | NO_IBKR, IBKR_HOST/PORT/CLIENT_ID/ACCOUNT_ID/MARKET_DATA_MODE | LIVE/DELAYED/FROZEN/OFFLINE | marques desk/EOD, Greeks MODEL_ESTIMATE, Actionnable bloqué |
| TradingView | TRADINGVIEW_WEBHOOK_SECRET (+_DEFAULT_TIMEFRAME) | CONFIGURED/MISSING | webhook 503, « non configuré » affiché |
| Claude | ANTHROPIC_API_KEY, ANTHROPIC_MODEL | MISSING/CONFIGURED/CONNECTED/DEGRADED (`vertex/ai/health.py`) | synthèse déterministe étiquetée |
| Stockage | — | CONNECTED/DEGRADED | backups quotidiens desk_backup_* |
| Flux live | — | LIVE/DELAYED/FALLBACK/OFFLINE (client) | repli polling adaptatif |

Vérité : `GET /api/system/startup-report`, `GET /api/system/config`
(statuts sans valeurs), `GET /api/live/status`, drawer Connexions (topbar).
