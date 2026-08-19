# Vertex 1.0 · #779 — Inventaire exécutable du runtime

SHA : `5513763fa294` · généré par `tools/vertex_1_0/inventaire_runtime.py`

> Ce document est **régénéré**, jamais édité à la main. Un chiffre qui
> change sans que le code ait bougé est un défaut de l'instrument.

## Monolithe — ce qu'il reste à extraire

| mesure | valeur |
| --- | --- |
| lignes | 7175 |
| octets | 809667 |
| fonctions | 81 |
| plus longue fonction | `_ibkr_opt_worker` (306 lignes) |
| **routes LEGACY** | **11** |
| blueprints enregistrés | 6 |
| workers démarrés | 15 |
| boucles de service | 13 |
| stores de module | 3 |

## Matrice de propriété des routes

| statut | nombre |
| --- | --- |
| CANONIQUE (blueprint du paquet) | 143 |
| LEGACY (`terminal.py`) | 11 |

**L'objectif de #779 est que la ligne LEGACY tombe à 0.** Supprimer
`terminal.py` n'est pas le but ; lui retirer toute responsabilité l'est.

### Routes encore servies par `terminal.py`

| chemin | vue | méthodes | ligne |
| --- | --- | --- | --- |
| `/scan` | `scan_ep` | * | 1740 |
| `/api/rescan` | `api_rescan` | POST, GET | 1753 |
| `/api/ticker/<sym>` | `api_ticker` | * | 1798 |
| `/api/correlations/<sym>` | `api_correlations` | * | 1875 |
| `/desc/<sym>` | `desc_ep` | * | 1969 |
| `/options/<sym>` | `opt_ep` | * | 2049 |
| `/quotes` | `quotes_ep` | * | 2325 |
| `/ibkr` | `ibkr_ep` | * | 2332 |
| `/weekly-regen` | `weekly_regen_ep` | POST, GET | 2340 |
| `/api/alerts/status` | `api_alerts_status` | * | 7063 |
| `/api/track-record` | `api_track_record` | * | 7069 |

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

- `_FR_DESC`
- `_IBKR_MODE`
- `_STOOQ_IDX`

## Paquet `vertex/` — surface canonique

| mesure | valeur |
| --- | --- |
| fichiers Python | 342 |
| routes canoniques | 143 |

### Blueprints enregistrés par le monolithe

- `_decision_api.make_blueprint`
- `_desk.make_blueprint`
- `_positions_api.make_blueprint`
- `_redesign.make_blueprint`
- `_strategy_os_api.make_blueprint`
- `_tv_webhooks.make_blueprint`

