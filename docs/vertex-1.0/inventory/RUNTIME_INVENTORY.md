# Vertex 1.0 · #779 — Inventaire exécutable du runtime

SHA : `c06b5d767944` · généré par `tools/vertex_1_0/inventaire_runtime.py`

> Ce document est **régénéré**, jamais édité à la main. Un chiffre qui
> change sans que le code ait bougé est un défaut de l'instrument.

## Monolithe — ce qu'il reste à extraire

| mesure | valeur |
| --- | --- |
| lignes | 7169 |
| octets | 809795 |
| fonctions | 76 |
| plus longue fonction | `_ibkr_opt_worker` (306 lignes) |
| **routes LEGACY** | **7** |
| blueprints enregistrés | 7 |
| workers démarrés | 15 |
| boucles de service | 13 |
| stores de module | 3 |

## Matrice de propriété des routes

| statut | nombre |
| --- | --- |
| CANONIQUE (blueprint du paquet) | 147 |
| LEGACY (`terminal.py`) | 7 |

**L'objectif de #779 est que la ligne LEGACY tombe à 0.** Supprimer
`terminal.py` n'est pas le but ; lui retirer toute responsabilité l'est.

### Routes encore servies par `terminal.py`

| chemin | vue | méthodes | ligne |
| --- | --- | --- | --- |
| `/scan` | `scan_ep` | * | 1741 |
| `/api/rescan` | `api_rescan` | POST, GET | 1754 |
| `/api/ticker/<sym>` | `api_ticker` | * | 1799 |
| `/api/correlations/<sym>` | `api_correlations` | * | 1876 |
| `/desc/<sym>` | `desc_ep` | * | 1970 |
| `/options/<sym>` | `opt_ep` | * | 2050 |
| `/weekly-regen` | `weekly_regen_ep` | POST, GET | 2327 |

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
| fichiers Python | 345 |
| routes canoniques | 147 |

### Blueprints enregistrés par le monolithe

- `_decision_api.make_blueprint`
- `_desk.make_blueprint`
- `_live_state_api.make_blueprint`
- `_positions_api.make_blueprint`
- `_redesign.make_blueprint`
- `_strategy_os_api.make_blueprint`
- `_tv_webhooks.make_blueprint`

