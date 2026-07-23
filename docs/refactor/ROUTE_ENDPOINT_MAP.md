# VERTEX — Carte Routes → Pages → Endpoints → Moteurs (Phase 2)

> Branche `agent/vertex-total-rebuild` @ `362c7d4`. 163 règles dans `app.url_map`.
> Deux systèmes de navigation coexistent ; **un seul est canonique**.

## 0. Deux registres de navigation

- **CANONIQUE** — `vertex/ui/shell/__init__.py:13` `PRIMARY_NAV` (9 espaces),
  rendu par le shell du redesign, figé par `tests/test_redesign_ui.py:30`
  (`test_primary_navigation_has_nine_items`). Routes dans le blueprint
  `vertex/app/routes/redesign.py`.
- **LEGACY / MORT de facto** — `vertex/ui/nav.py:10` `ITEMS` (10 libellés
  anglais) encore consommé seulement par `terminal.py:6517-6518` pour injecter
  `var NAV`/`var VSEC` dans d'anciennes pages HTML dont les routes sont
  commentées. Superseded par `PRIMARY_NAV`.

> ⚠️ Contradiction documentaire : le docstring du shell dit « EXACTEMENT huit
> espaces » (`shell/__init__.py:12`) et `redesign.py:122-124` insiste « Options…
> PAS un 9e espace », mais `PRIMARY_NAV` liste **9** entrées et le test fige 9.
> (Voir `CONTRADICTIONS_REGISTER.md` C-01.)

## A. Espaces principaux (`PRIMARY_NAV`)

Source : `vertex/ui/shell/__init__.py:13-23` ; routeur `vertex/app/routes/redesign.py:79-138`.

| # | id | label | route | module de page | sous-vues `?view=` | mission inférée |
|---|----|-------|-------|----------------|--------------------|-----------------|
| 1 | briefing | Briefing | `/` | `vertex/ui/pages/briefing.py:645` | *(page unique ; brief PRE_MARKET/INTRADAY/CLOSE/WEEKLY)* | Brief éditorial sourcé : ce qui a changé, risque/opportunité, action du jour |
| 2 | markets | Marchés | `/markets` | `markets_page.py:788` | `overview`·`macro`·`sectors`·`breadth`·`volatility` (l.16-23) | Macro/indices/secteurs/breadth/vol du marché global |
| 3 | opportunities | Opportunités | `/opportunities` | `opportunities_page.py:467` | `radar`·`stocks`·`options`·`anomalies`·`calendar` (l.12) | Entonnoir d'idées : signaux, univers, contrats, anomalies, catalyseurs |
| 4 | portfolio | Portefeuille | `/portfolio` | `portfolio_page.py:635` | `team`·`positions`·`options`·`risk`·`watchlist` (l.13) | Positions IBKR, options détenues, risque, watchlist |
| 5 | analysis | Analyse | `/analysis` (+ `/analysis/<sym>`) | `analysis_page.py:16 / 670` | fiche canonique par ticker | Fiche titre unique (fonda, catalyseurs, technique, sentiment, scénarios, options, décision) |
| 6 | options | Options | `/options` | `options_intel_page.py:200` | `overview`·`volatility`·`radar`·`scenarios`·`events` (l.17) | Options Intelligence : environnement, vol, radar contrats, scénarios, risque événement |
| 7 | performance | Performance | `/performance` | `performance_page.py:463` | `overview`·`journal`·`track-record`·`learnings` (l.20) | Journal de trades, track record auto-mesuré, enseignements |
| 8 | intelligence | Intelligence | `/intelligence` | `intelligence_page.py:633` | `analyst`·`committee`·`strategy`·`impacts`·`research`·`memory` (l.15) | Cerveau : analyste, comité, profil stratégique, impacts, recherche, mémoire |
| 9 | system | Système | `/system` | `system_page.py:987` | `connections`·`data`·`automations`·`settings`·`archive` (l.15) | Connexions, qualité données, jobs, réglages, archive |

Pages secondaires routées : `/tracking` (`tracking_page.py:61`),
`/system/design-system` (`design_system_demo.py:162`),
`/design-system` (`design_system_page.py:245`).

## B. Endpoints `/api` par domaine

> Détail complet des ~90 endpoints ci-dessous (extrait des blueprints).

### Marché / feeds
| endpoint | src | but | moteur/source |
|---|---|---|---|
| `/api/market/summary` | feeds.py:27 | résumé marché widgets | `scan_state.market_ctx` |
| `/api/market/regime` | strategy_os_api.py:84 | classification régime | `vertex.market.regime_engine.classify_regime` |
| `/api/cockpit` | feeds.py:47 | action du jour + top opps | `scan_state.recommendations` |
| `/api/watchlist` | feeds.py:62 | rows + secteurs | `scan_state.rows/sectors` |
| `/api/options` | feeds.py:69 | board options global | `scan_state.options_board` |
| `/api/search` | feeds.py:74 | autocomplete | `UNIVERSE` |
| `/api/weekly` | feeds.py:81 | sélection hebdo | `weekly_state` |
| `/api/comite` | feeds.py:92 | comité (snapshot) | `scan_state.committee` |

### Décision / analyse titre
| endpoint | src | but | moteur |
|---|---|---|---|
| `/api/decision/<sym>` | decision_api.py:79 | décision stack (vérité unique) | `engines/decision_stack` (+recommendation, context, market_lens) |
| `/api/position-decision/<sym>` | decision_api.py:97 | gestion d'une position détenue | `engines/decision_stack` |
| `/api/options-for/<sym>` | decision_api.py:129 | meilleurs contrats | `engines/options_lab` |
| `/api/brief` | decision_api.py:138 | morning brief | `engines/committee` + `decision_stack` |
| `/api/committee-review` | decision_api.py:160 | revue comité univers | `engines/committee` |
| `/api/vertex/<sym>` | analysis_api.py:22 | deep-dive quant explicable | `engines/quant_engine` |
| `/api/validator` | analysis_api.py:36 | walk-forward, DSR/PSR/PBO | `engines/quant_engine` |
| `/api/risk` | analysis_api.py:46 | risk manager portefeuille | `engines/quant_engine` |
| `/api/strategy/profile` | strategy_os_api.py:33 | profil stratégique canonique | `strategy/constitution` |
| `/api/strategy/decision/<sym>` | strategy_os_api.py:41 | décision finale exécutive | `strategy/executive_engine` |
| `/api/command` | command.py:35 | Command Center | `strategy/legacy_adapter` + `market_lens` |

### Options
| endpoint | src | but |
|---|---|---|
| `/api/options/overview` | options_intel_api.py:33 | vue d'ensemble |
| `/api/options/environment` | options_intel_api.py:44 | score long-option |
| `/api/options/volatility/<sym>` | options_intel_api.py:56 | interprétation vol |
| `/api/options/scenarios/<sym>` | options_intel_api.py:77 | scénarios spot×temps×IV |
| `/api/options/vol-charts/<sym>` | options_intel_api.py:123 | datasets graphiques vol |
| `/api/options/event-risk/<sym>` | options_intel_api.py:141 | risque événement |
| `/api/options/simulate` | redesign.py:178 | simulation d'un contrat |
| `/api/options-lab` | options_lab_api.py:19 | Options Research Center |
| `/api/options/strategies/<sym>` | options_lab_api.py:30 | stratégies multi-jambes |
| `/api/options/analyze` (POST) | options_lab_api.py:60 | analyse stratégie arbitraire |

### Positions IBKR (réelles, readonly)
| endpoint | src | but |
|---|---|---|
| `/api/positions/state` | positions_api.py:51 | état recalculé |
| `/api/positions/report` | positions_api.py:64 | rapport démarrage |
| `/api/positions/audit` | positions_api.py:71 | intégrité HEALTHY/DEGRADED/CRITICAL |
| `/api/positions/reconcile` | positions_api.py:78 | réconciliation locale↔IBKR |
| `/api/positions/alerts` | positions_api.py:88 | alertes consolidées |
| `/api/ibkr/positions` | desk.py:119 | portefeuille TWS lecture seule |
| `/api/pos-quotes` (POST) | desk.py:134 | cote live des trades saisis |

### Desk / tracking / IA / live / système
| endpoint | src | but |
|---|---|---|
| `/api/desk` (GET/POST) | desk.py:70 | sync desk perso → `desk_data.json` |
| `/api/desk/backups`, `/restore` | desk.py:86/95 | snapshots + restauration |
| `/api/tracking*` (8 routes) | tracking_api.py | suivis hypothétiques → `vertex.tracking.*` |
| `/api/opportunities/funnel` | opportunities_api.py:37 | entonnoir | 
| `/api/ai/enrichment\|status\|refresh` | ai_api.py:75-90 | cerveau Claude étiqueté |
| `/api/live/status\|refresh\|report\|events(SSE)` | live_api.py / live_events.py | live engine + flux SSE |
| `/api/planning/ticket` (POST) | planning_api.py:17 | ticket d'ordre **analyse, non transmis** |
| `/api/system/config\|connections\|automations\|startup-report\|diagnostics` | system.py / strategy_os_api.py | diagnostics & réglages |
| `/api/client-log` (GET/POST) | system.py:52/65 | journal erreurs JS (0-erreur) |
| `/api/data-quality` | strategy_os_api.py:154 | qualité/fraîcheur |
| `/news-feed`, `/cal-feed`, `/weekly-feed` | content.py | fils éditoriaux (news sanitizées) |

### Routes actives restantes dans le monolithe `terminal.py`
`/scan` (1689), `/api/rescan` (1701), `/api/ticker/<sym>` (1777),
`/api/company/<sym>` (1820), `/api/analyst/<sym>` (1829), `/api/names` (1841),
`/api/correlations/<sym>` (1882), `/desc/<sym>` (1984), `/options/<sym>` (2074),
`/quotes` (2355), `/ibkr` (2362), `/weekly-regen` (2393),
`/api/alerts/status` (10641), `/api/track-record` (10647).

## C. Endpoints appelés par page (grep JS/templates)

- **Briefing** : `/scan`, `/api/briefing/editorial`, `/api/command`, `/api/market/summary`, `/api/market/regime`, `/api/alerts/status`, `/api/pos-quotes`.
- **Marchés** : `/scan`, `/api/market/summary`, `/api/market/regime`.
- **Opportunités** : `/scan`, `/api/opportunities/funnel`, `/api/data-quality`, `/api/options/simulate`.
- **Portefeuille** : `/scan`, `/api/positions/state`, `/api/ibkr/positions`, `/api/pos-quotes`, `/api/position-decision/<sym>`, `/api/portfolio/team`, `/api/options/analyze`.
- **Analyse** : `/api/ticker/<sym>`, `/api/analyst/<sym>`, `/api/names`, `/api/anomalies/<sym>`, `/api/strategy/decision/<sym>`, `/api/options-for/<sym>`, `/api/planning/ticket`, `/api/tradingview/signals`.
- **Options** : `/api/options/overview`, `/environment`, `/volatility/<sym>`, `/scenarios/<sym>`.
- **Performance** : `/api/track-record` (+ journal desk localStorage).
- **Intelligence** : `/api/decision/<sym>`, `/api/committee-review`, `/api/strategy/profile`, `/api/strategy/decision/<sym>`, `/api/validator`, `/api/desk`.
- **Système** : `/api/system/*`, `/api/data-quality`, `/api/ai/*`, `/api/live/status|refresh`, `/api/desk*`, `/api/client-log`, `/api/tradingview/signals`.

## D. Moteurs métier

### `vertex/engines/`
`decision_stack` (décision unique explicable), `recommendation` (façade + vocab),
`quant_engine` (noyau quant : deep-dive/validator/risk), `committee` (comité 4
portes), `options_lab` + `multileg_lab` (options), `track_record` +
`performance_ledger` (auto-mesure), `evidence`, `market_lens`, `context`,
`analysis`, `decide`, `reasoning`, `scorecard`, `strategy_fit`, `indicators`,
`timeframes`, `swing`, `stats`, `backtest`.

### `vertex/options/`
`overview`, `environment`, `interpretation`, `scenario_pricer`, `vol_charts`,
`vol_surface`, `volatility`, `event_risk`, `expected_move`, `pulse`,
`call_selector`, `bearish_tactical`, `contract_scorer`, `contract_filter`,
`chain_loader`, `liquidity`, `recommendation`, `models`, `legacy_engine`.

### `vertex/strategy/`
`executive_engine` (seule couche de décision finale), `constitution` (profil),
`legacy_adapter` (stratégie options perso), `config`, `profiles/`, `memory/`.

## E. Doublons / recouvrements de routes (voir contradictions)

1. **Alias fonctionnels** : `/healthz`≡`/api/healthz` ; `/api/system-status`≡`/api/system/status` ; `/api/system/automations`≡`/api/system/jobs`.
2. **Surface « options » fragmentée sur 4 fichiers** : feeds (`/api/options` board), options_lab_api (`/api/options-lab`, `/strategies`, `/analyze`), options_intel_api (`/overview`, `/environment`, `/volatility`, `/scenarios`…), redesign (`/simulate`) + terminal (`/options/<sym>`).
3. **Comité & stratégie dupliqués** : `/api/comite` (snapshot feeds) vs `/api/committee-review` (moteur) ; `/api/strategie` (snapshot) vs `/api/strategy/profile`+`/decision` (moteurs).
4. **Anciennes pages du monolithe** : constantes `PAGE_*` encore construites au démarrage (`terminal.py` l.7994, 10579…) alors que leurs `@app.route` sont commentés → **code mort coûteux au boot** (à vérifier avant retrait — voir `FILE_INVENTORY.md`).
5. **`/desc/<sym>` et `/options/<sym>`** (terminal) actifs mais non appelés par le redesign → résiduels probables.
