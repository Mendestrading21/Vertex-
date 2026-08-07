# ANNEXE É1 — Liste exacte des retraits de l'Étape 1 (générée, 0 purge)

> Générée au lot 253 par `tools/purge_e2_sizing.py --e1` (rejouable —
> régénérer cette liste après tout changement de terminal.py).
> Périmètre = la **borne basse certaine** du chiffrage (lot 249) :
> 82 définitions injoignables SANS toucher aux boucles d'injection par
> chaîne. **Rien n'est purgé** : ce document rend le « GO purge
> étape 1 » exécutable sans ambiguïté.

## Triage des 82 défs en 3 catégories d'action

| Cat. | Action É1 | Contenu |
|---|---|---|
| **A — retrait sec** | Supprimer la déf | Toute déf non référencée par tests/ (la majorité : fonctions de rendu orphelines, gros blocs JS/CSS morts) |
| **B — retrait avec leurs tests** | Supprimer déf + test de caractérisation | Défs épinglées par les tests écrits POUR ce moment : `test_dead_functions_lot185.py` (29 réfs), `test_legacy_layers_life_lot184.py` (20), `test_legacy_pages_life_lot183.py` (13), épingles `test_nav.py`/`test_options_lab.py`/`test_journal_page.py`/`test_home_art_lot181.py` |
| **C — re-cibler le test, PUIS retirer l'alias** | Le test garde sa valeur, seul l'import change | Alias de compatibilité re-exportant des moteurs VIVANTS : `_rsi`/`_atr`/`_adx` → `vertex.engines.indicators` (test_indicators.py), `_demo_one` → `vertex.data.demo` (test_demo.py), `_vehicle_of` → `vertex.engines.strategy_fit` (test_strategy_fit.py), `_swing_project` → module swing (test_swing.py) |

Faux positifs connus du grep ci-dessous (à ignorer au triage) :
`home` dans `test_auth_routes.py` (fonction locale du test) et
`test_live_engine.py` (mot dans un commentaire) — aucun de ces deux
tests ne référence réellement la fonction `home` de terminal.py.

Filet É1 (rappel du dossier) : pytest 100 % + serveur DEMO + balayage
navigateur 8 pages + 0 erreur console ; PR séparée ; rollback = revert.

<!-- généré par tools/purge_e2_sizing.py --e1 — rejouable -->

## Liste exacte des retraits É1 (borne basse, 82 défs)

| Définition | Genre | Lignes (spans) | Taille |
|---|---|---|---|
| `_PORTSIM_JS` | const | 8728-9222 | 495 l. |
| `_TRADES_JS` | const | 9224-9662 | 439 l. |
| `_DESK_COCKPIT_JS` | const | 9940-10366 | 427 l. |
| `_SI_JS` | const | 7090-7449 | 360 l. |
| `_SI_CSS` | const | 6764-6969 | 206 l. |
| `_STRAT_PAGE_CSS` | const | 9664-9839 | 176 l. |
| `_RECO_JS` | const | 8577-8726 | 150 l. |
| `_SI_BODY` | const | 6971-7088 | 118 l. |
| `_STRAT_EMBED_JS` | const | 8423-8533 | 111 l. |
| `_SUIVI_JS` | const | 8016-8111 | 96 l. |
| `_SECT_JS` | const | 7517-7606 | 90 l. |
| `_CAT_JS` | const | 7632-7712 | 81 l. |
| `_EQUIPE_JS_UNUSED` | const | 8325-8393 | 69 l. |
| `_COMPARE_JS` | const | 6431-6486 | 56 l. |
| `_WEEKLY_CSS` | const | 3963-4009 | 47 l. |
| `_DESK_COCKPIT` | const | 9896-9939 | 44 l. |
| `_BRIEF_JS` | const | 7727-7766 | 40 l. |
| `_DECJ_JS` | const | 7828-7861 | 34 l. |
| `_STOCKS_JS` | const | 10524-10556 | 33 l. |
| `_BASE_CSS` | const | 3917-3944 | 28 l. |
| `_STRATTOP_JS` | const | 8551-8575 | 25 l. |
| `PAGE_SECTORS` | const | 7608-7629 | 22 l. |
| `_STRAT_EMBED_HEAD` | const | 8395-8409 | 15 l. |
| `_DESK_ADDFORM` | const | 9869-9883 | 15 l. |
| `PAGE_SUIVI` | const | 8113-8125 | 13 l. |
| `_DESK_SIMFORM` | const | 9884-9895 | 12 l. |
| `_STRAT_EMBED_SECTIONS` | const | 8411-8421 | 11 l. |
| `_DESK_MID` | const | 9849-9858 | 10 l. |
| `_BASE_JS` | const | 3945-3953 | 9 l. |
| `PAGE_COMPARE` | const | 8005-8013 | 9 l. |
| `PAGE_CATALYSTS` | const | 7714-7722 | 9 l. |
| `PAGE_BRIEF` | const | 7768-7776 | 9 l. |
| `_DESK_TOP` | const | 9841-9847 | 7 l. |
| `PAGE_DECISIONS` | const | 7863-7869 | 7 l. |
| `PAGE_STOCKS` | const | 10557-10562 | 6 l. |
| `PAGE_STRATEGIE` | const | 10369-10372, 10374-10374 | 5 l. |
| `_rail` | func | 4102-4105 | 4 l. |
| `NAV` | const | 3908-3911 | 4 l. |
| `watchlist_page` | func | 4474-4476 | 3 l. |
| `my_page` | func | 5393-5395 | 3 l. |
| `_RAIL_ITEMS` | const | 4097-4099 | 3 l. |
| `_DESK_TAIL` | const | 9860-9862 | 3 l. |
| `vault_page` | func | 8142-8143 | 2 l. |
| `titre_page` | func | 6507-6508 | 2 l. |
| `suivi_page` | func | 8130-8131 | 2 l. |
| `strategy_os_page` | func | 2073-2074 | 2 l. |
| `strategie_page` | func | 4935-4936 | 2 l. |
| `stocks_page` | func | 10566-10567 | 2 l. |
| `settings_page` | func | 7505-7506 | 2 l. |
| `sectors_page` | func | 10571-10572 | 2 l. |
| `review_page` | func | 7824-7825 | 2 l. |
| `research_page` | func | 7943-7944 | 2 l. |
| `options_lab_page` | func | 10591-10592 | 2 l. |
| `options_desk_page` | func | 2392-2393 | 2 l. |
| `options_desk_alias` | func | 4926-4927 | 2 l. |
| `journal_page` | func | 10582-10583 | 2 l. |
| `home` | func | 2377-2378 | 2 l. |
| `heatmap_page` | func | 8190-8191 | 2 l. |
| `health_page` | func | 7997-7998 | 2 l. |
| `equipe_page` | func | 8546-8547 | 2 l. |
| `entreprises_page` | func | 6497-6498 | 2 l. |
| `decisions_page` | func | 7873-7874 | 2 l. |
| `compare_page` | func | 6491-6492 | 2 l. |
| `catalysts_page` | func | 10577-10578 | 2 l. |
| `brief_page` | func | 7780-7781 | 2 l. |
| `bordel_page` | func | 10496-10497 | 2 l. |
| `anomalies_page` | func | 8136-8137 | 2 l. |
| `_legacy_pages_redirect` | func | 2387-2388 | 2 l. |
| `_vehicle_of` | const | 1060-1060 | 1 l. |
| `_swing_project` | const | 384-384 | 1 l. |
| `_strat_score` | const | 1062-1062 | 1 l. |
| `_rsi` | const | 223-223 | 1 l. |
| `_playbook_of` | const | 1063-1063 | 1 l. |
| `_demo_one` | const | 378-378 | 1 l. |
| `_atr` | const | 224-224 | 1 l. |
| `_adx` | const | 225-225 | 1 l. |
| `_DEMO_BASE` | const | 377-377 | 1 l. |
| `PAGE_VAULT` | const | 7514-7514 | 1 l. |
| `PAGE_TITRE` | const | 7451-7451 | 1 l. |
| `PAGE_OPTIONS_LAB` | const | 10587-10587 | 1 l. |
| `PAGE_JOURNAL` | const | 8002-8002 | 1 l. |
| `PAGE_ANOMALIES` | const | 7511-7511 | 1 l. |

## Fichiers de tests référençant ces définitions (à adapter/retirer)

- `tests/test_auth_routes.py` — 1 réf(s) : `home`
- `tests/test_dead_functions_lot185.py` — 29 réf(s) : `_legacy_pages_redirect`, `_rail`, `anomalies_page`, `bordel_page`, `brief_page`, `catalysts_page`, `compare_page`, `decisions_page` …
- `tests/test_demo.py` — 1 réf(s) : `_demo_one`
- `tests/test_home_art_lot181.py` — 1 réf(s) : `PAGE_STRATEGIE`
- `tests/test_indicators.py` — 3 réf(s) : `_adx`, `_atr`, `_rsi`
- `tests/test_journal_page.py` — 2 réf(s) : `PAGE_JOURNAL`, `_DECJ_JS`
- `tests/test_legacy_layers_life_lot184.py` — 20 réf(s) : `_BASE_CSS`, `_BASE_JS`, `_BRIEF_JS`, `_CAT_JS`, `_COMPARE_JS`, `_DECJ_JS`, `_DESK_COCKPIT_JS`, `_PORTSIM_JS` …
- `tests/test_legacy_pages_life_lot183.py` — 13 réf(s) : `PAGE_ANOMALIES`, `PAGE_BRIEF`, `PAGE_CATALYSTS`, `PAGE_COMPARE`, `PAGE_DECISIONS`, `PAGE_JOURNAL`, `PAGE_OPTIONS_LAB`, `PAGE_SECTORS` …
- `tests/test_live_engine.py` — 1 réf(s) : `home`
- `tests/test_nav.py` — 2 réf(s) : `NAV`, `PAGE_TITRE`
- `tests/test_options_lab.py` — 1 réf(s) : `PAGE_OPTIONS_LAB`
- `tests/test_strategy_fit.py` — 1 réf(s) : `_vehicle_of`
- `tests/test_swing.py` — 1 réf(s) : `_swing_project`
