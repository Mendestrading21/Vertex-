# Vertex — Architecture

## Vue d'ensemble
- **Backend** : Flask. Monolithe historique `terminal.py` (boucles de fond +
  13 routes legacy) en cours d'extinction par blueprints
  `vertex/app/routes/` (auth, feeds, content, desk, analysis_api, command,
  options_lab_api, live_api, live_events, system, strategy_os, decision_api,
  tv_webhooks, redesign).
- **Moteurs** : `vertex/{strategy, options, portfolio, market, scanner,
  anomalies, data_sources, research, validation, ai, alerts, engines,
  observability, catalysts, quant, companies, scheduler, services, data}`.
- **Frontend** : shell unique (`vertex/ui/shell`) + 8 pages
  (`vertex/ui/pages`), design system Obsidian Copper
  (`vertex/static/vertex/css`, 13 feuilles), 25 modules graphiques Chart.js,
  client SSE (`live-updates.js`).

## Sources de vérité uniques
Stratégie : `vertex/strategy/profiles/vertex_strategy_v1.json` ·
Décision : `vertex/strategy/executive_engine.py` ·
Positions : localStorage `myTrades` (17 clés sync `/api/desk`) ·
Connexions : séquence de démarrage + `/api/live/status` ·
Routes : `VERTEX_ROUTE_MATRIX.md` · Couleurs : `tokens.css` ·
Jobs : `vertex/scheduler/registry.py` · États de données : `states.css`.

## Migration progressive
Aucun déplacement aveugle : les paquets `companies/` et `scheduler/`
enveloppent l'existant (adaptateurs), les routes legacy restent servies
avec redirections (42 × 301).
