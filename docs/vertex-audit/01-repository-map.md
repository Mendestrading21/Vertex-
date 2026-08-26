# 01 — Cartographie du dépôt (réelle)

`terminal.py` = **11 020 lignes** (monolithe : HTML/JS en chaînes Python + JSON/API + PWA). Autour, le package
`vertex/` (strangler). **Pas de frontend JS componentisé** ; les statiques sont du CSS + JS vanilla.

## Racine
- `terminal.py` — app Flask, workers IBKR, scan, caches, routes legacy `@app.route`.
- `ib_reader.py` / `test_connection.py` — accès IBKR lecture seule / diagnostic.
- `docs/` — ~40 docs + `docs/claude/` (contrats) + `docs/vertex-audit/` (cet audit).
- `tests/` — **81 fichiers** de tests (`python -m pytest tests/ -q` → 919 passés, 2 skipped).
- `static/` (racine, legacy) + `vertex/static/vertex/` (canonique : `css/glass.css`, `js/charts/chart-core.js`, `vx-core.js`).
- Runtime **gitignoré** : `desk_data.json`, `*_cache.json`, `breadth_history.json`, `.env`, `.vertex_secret`, `edge_ledger`, `desk_backup_*`.
- Lanceurs : `Lancer_VERTEX*.bat/.command` (+ `_DEMO`), `render.yaml` (déploiement).

## Package `vertex/` (sous-systèmes)
| Domaine | Modules | Rôle |
|---|---|---|
| **app** | `app/routes/*` (20 blueprints), `app/state.py`, `app/config.py` | routage, `scan_state` (muté en place), `READONLY=True` |
| **ui** | `ui/pages/*` (12 pages), `ui/shell/`, `ui/nav.py` (legacy) | rendu HTML des 8 espaces + shell |
| **engines** | `decision_stack`, `recommendation`, `executive`/`decide`, `evidence`, `reasoning`, `scorecard`, `committee`, `quant_engine`, `backtest`, `analysis`, `indicators`, `track_record`, `options_lab`, `multileg_lab`, `swing`, `timeframes`, `market_lens`, `strategy_fit`, `stats`, `performance_ledger`, `context` | pipeline déterministe de décision |
| **options** | `options/` (`on_demand.py`…) | chaînes, greeks, IV, scénarios |
| **market / quant / anomalies / catalysts** | features de marché, régime, signaux, événements | contexte & détection |
| **data_sources / data** | IBKR / yfinance / stooq / demo | acquisition + provenance |
| **ai** | `ai/tool_registry.py` (17 outils d'ordre **interdits**), `ai/health.py`, agents | analyste IA (lecture seule) |
| **portfolio / positions / tracking / planning** | positions, suivis, tickets de préparation | exposition & prep |
| **scheduler / services / observability** | jobs, services, `observability/metrics.py` (`METRICS`) | orchestration & mesure |
| **research / companies / company / alerts / validation / visualization / scanner** | recherche, fondamentaux, alertes, garde-fous, viz, screener | support |

## Routes (2 familles)
- **Blueprint `redesign`** (`app/routes/redesign.py`) → sert les 8 pages via `ui/pages/*` + shell.
- **API blueprints** (`ai_api`, `analysis_api`, `decision_api`, `opportunities_api`, `options_intel_api`,
  `options_lab_api`, `planning_api`, `positions_api`, `tracking_api`, `live_api`, `live_events`, `feeds`,
  `content`, `command`, `system`, `desk`, `strategy_os_api`, `auth`) → JSON.
- **Legacy `@app.route`** dans `terminal.py` (`/options/<sym>` JSON, `/scan`, `/healthz`, `/api/*`, PWA/SW).
  ⚠️ Certaines collisionnent avec le blueprint (voir `02` : `/options/<sym>`).

## Points d'entrée de vérification
`GET /healthz` · `GET /api/client-log` (=0) · `GET /api/live/status` · `GET /api/system/connections` ·
serveur démo : `DEMO=1 NO_IBKR=1 python terminal.py`.
