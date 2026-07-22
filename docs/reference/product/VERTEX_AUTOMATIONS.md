# Vertex — Automatisations (§24)

`vertex/scheduler/registry.py` : 17 jobs canoniques — battements émis par
les boucles historiques (aucun re-threading risqué). Vue :
Système → Automatisations (`/api/system/automations`).

Priorité produit (jamais sacrifier la surveillance des positions pour
scanner plus large) : STARTUP_HEALTH_CHECK · POSITION_REFRESH ·
OPTION_POSITION_REFRESH · MARKET_DATA_REFRESH · PORTFOLIO_RECALCULATION ·
DECISION_RECALCULATION · CATALYST_REFRESH · NEWS_REFRESH ·
PREMARKET/INTRADAY/CLOSE_BRIEF · EOD_SNAPSHOT · WEEKLY_REVIEW ·
SYSTEM_AUDIT · DATA_BACKUP · TRACK_RECORD_UPDATE · ALERTS_EVALUATION.

Chaque job affiche : statut (OK/erreur/jamais exécuté), dernière exécution,
prochaine estimée, nombre d'exécutions, durée. Les jobs « sur événement »
(briefs, recalculs) n'ont pas de cadence propre. Flux temps réel :
SSE `/api/live/events` (rejeu Last-Event-ID, heartbeat 25 s) + client
reconnect/dédup/repli polling.
