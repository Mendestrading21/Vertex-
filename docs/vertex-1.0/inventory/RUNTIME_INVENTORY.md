# Vertex 1.0 · #779 — Inventaire exécutable du runtime

SHA : `d52a39d4baf1` · généré par `tools/vertex_1_0/inventaire_runtime.py`

> Ce document est **régénéré**, jamais édité à la main. Un chiffre qui
> change sans que le code ait bougé est un défaut de l'instrument.

## Monolithe — ce qu'il reste à extraire

| mesure | valeur |
| --- | --- |
| lignes | 7276 |
| octets | 813212 |
| fonctions | 91 |
| plus longue fonction | `_ibkr_opt_worker` (306 lignes) |
| **routes LEGACY** | **14** |
| blueprints enregistrés | 21 |
| workers démarrés | 15 |
| boucles de service | 13 |
| stores de module | 11 |

## Matrice de propriété des routes

| statut | nombre |
| --- | --- |
| CANONIQUE (blueprint du paquet) | 140 |
| LEGACY (`terminal.py`) | 14 |

**L'objectif de #779 est que la ligne LEGACY tombe à 0.** Supprimer
`terminal.py` n'est pas le but ; lui retirer toute responsabilité l'est.

### Routes encore servies par `terminal.py`

| chemin | vue | méthodes | ligne |
| --- | --- | --- | --- |
| `/scan` | `scan_ep` | * | 1766 |
| `/api/rescan` | `api_rescan` | POST, GET | 1779 |
| `/api/ticker/<sym>` | `api_ticker` | * | 1870 |
| `/api/company/<sym>` | `api_company` | * | 1913 |
| `/api/analyst/<sym>` | `api_analyst` | * | 1922 |
| `/api/names` | `api_names` | * | 1934 |
| `/api/correlations/<sym>` | `api_correlations` | * | 1975 |
| `/desc/<sym>` | `desc_ep` | * | 2080 |
| `/options/<sym>` | `opt_ep` | * | 2163 |
| `/quotes` | `quotes_ep` | * | 2444 |
| `/ibkr` | `ibkr_ep` | * | 2451 |
| `/weekly-regen` | `weekly_regen_ep` | POST, GET | 2460 |
| `/api/alerts/status` | `api_alerts_status` | * | 7183 |
| `/api/track-record` | `api_track_record` | * | 7189 |

### Workers démarrés par `terminal.py`

- `_alerts_loop`
- `_brain_boot`
- `_cal_loop`
- `_edge_loop`
- `_fund_loop`
- `_ibkr_opt_worker`
- `_ibkr_worker`
- `_indices_loop`
- `_loop`
- `_news_loop`
- `_opt_loop`
- `_quotes_worker`
- `_radar_loop`
- `_startup`
- `_weekly_loop`

### Stores de module (état partagé)

- `_CORR_BENCH`
- `_FR_DESC`
- `_IBKR_MODE`
- `_IDX_IBKR`
- `_IDX_META`
- `_SOURCE_BUDGET_STATE`
- `_STOOQ_CACHE`
- `_STOOQ_IDX`
- `_ibkr_cache`
- `_live_meta`
- `_live_quotes`

## Paquet `vertex/` — surface canonique

| mesure | valeur |
| --- | --- |
| fichiers Python | 338 |
| routes canoniques | 140 |

### Blueprints enregistrés par le monolithe

- `_ai_api.bp`
- `_analysis_api.bp`
- `_auth.make_blueprint`
- `_command.bp`
- `_content.bp`
- `_decision_api.make_blueprint`
- `_desk.make_blueprint`
- `_feeds.bp`
- `_live_api.bp`
- `_live_events.bp`
- `_opportunities_api.bp`
- `_options_intel_api.bp`
- `_options_lab_api.bp`
- `_planning_api.bp`
- `_positions_api.make_blueprint`
- `_redesign.make_blueprint`
- `_session_api.bp`
- `_strategy_os_api.make_blueprint`
- `_system.bp`
- `_tracking_api.bp`
- `_tv_webhooks.make_blueprint`

