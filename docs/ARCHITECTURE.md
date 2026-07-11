# VERTEX — Architecture & Plan de migration

> **Note — Vertex vNext Production Baseline (2026-07-08)** : les scripts hérités de l'ère « bot » décrits dans ce document (bot_cockpit, paper_bot, paper_live_bot, dashboard, gex_dashboard, mnq_backtest, stock_backtest, daily_opportunities, notion_sync, _daily_check) ont été **supprimés** — aucun n'était importé par l'application. Ce document reste comme audit historique.


## 1. État actuel (audité)

| Zone | LOC | État |
|---|---|---|
| `terminal.py` | ~9 500 | Monolithe : routes Flask + HTML/CSS/JS embarqués + logique + données. À dégraisser progressivement. |
| moteurs quant migrés (ex-package personnel, 23 modules, désormais sous `vertex/quant`, `vertex/engines`, `vertex/options`, `vertex/market`…) | ~4 300 | scoring, noyau quant, options (legacy_engine), stratégie (legacy_adapter), comité, validateur hors échantillon, régime physique, timeframes, chart_read, anomalies, pivots, contexte marché, weekly, fondamentaux, risque portefeuille, scorecard, briefs IA, daily, secteurs, décision, config, calibration ML. |
| `vertex/` (nouveau) | — | Package institutionnel en construction : `data/`, `app/`, `services/`. |
| `tests/` | — | `test_no_orders`, `test_foundation`, `test_smoke`, `test_vertex`. |
| Scripts racine | ~2 000 | `mnq_backtest`, `stock_backtest`, `paper_bot`, `bot_cockpit`, `gex_dashboard`, `dashboard`, `notion_sync`, `daily_opportunities`, `ib_reader`… (outils/legacy). |

**Audit sûreté** : ✅ aucun appel d'exécution d'ordre dans tout le dépôt ; ✅ IBKR `readonly=True`.

## 2. Cible

```
vertex/
  app/       factory, config, extensions, routes/
  services/  scanner, market_data, ibkr, option_chain, cache, universe,
             fundamentals, news, status, logging
  engines/   decision_stack, scoring, vertex, options, strategy, risk,
             validator, regime, data_quality
  models/    schemas, market, stock, option, decision, portfolio, risk, health
  data/      universe, sectors, constants, thresholds, mappings
  ui/        templates/, static/{css,js,charts,components}
tests/  docs/
```

`terminal.py` devient un **lanceur mince** puis disparaît.

## 3. Principe de migration : le « strangler pattern »

On n'exécute **jamais** de « big bang ». À chaque PR :
1. on extrait une responsabilité de `terminal.py` vers un module dédié ;
2. `terminal.py` **importe** le nouveau module (comportement identique) ;
3. tests + smoke verts avant de continuer.

Les moteurs de l'ancien package ont été migrés sous `vertex/*`
(migration réalisée par la refonte Strategy OS).

## 4. Ce qui a été fait (PR fondation)

- `vertex/data/universe.py` — univers extrait (1054 tickers, indices, GICS, industries).
- `vertex/data/constants.py` — constantes nommées (BENCH, R, BUILD, seuils de fraîcheur).
- `vertex/app/config.py` — configuration centralisée + invariants de sûreté.
- `vertex/services/status_service.py` + route `/api/system-status`.
- `tests/test_no_orders.py`, `tests/test_foundation.py`, `tests/conftest.py`.
- CI durcie (compile + tests + job sûreté bloquant).
- Docs : sûreté, architecture, feuille de route.

`terminal.py` : 279 lignes de données inline remplacées par 5 lignes d'import. Zéro régression (32 tests verts).
