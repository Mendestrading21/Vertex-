# Matrice QA Vertex (tests & vérification)

## Niveaux de test — baseline de consolidation : `tests/` (981 passés, 2 ignorés)
| Niveau | Couvre | Où / à étendre |
|---|---|---|
| **Unitaires** | calculs financiers, P&L, rendements, drawdown, greeks, conversions, sizing, scores, formats, règles de risque, normalisation IBKR | `tests/test_vertex.py`, `test_calculations_golden.py`, `test_indicators.py`, `test_analysis.py`, `test_options_engine.py` |
| **Intégration** | IBKR simulé, positions/ordres (lecture), synchro, reconnexion, données partielles/retardées, erreurs, multi-comptes | `tests/test_data_sources.py`, `test_real_data.py`, `test_full_system_integration.py` |
| **UI (routes)** | navigation, filtres, tri, drawers, tickets (prep), états vides/erreur/chargement, tableaux | `tests/test_*_routes.py`, `test_ui_v3.py`, `test_no_dead_buttons` |
| **E2E (démo)** | lancer → connexion → compte → positions → fiche → opportunité → scénario → **préparer** ordre → contrôles de risque → **simuler** → Desk → suivi → performance → journal → historique de décision | Playwright/Chromium (démo seedée) |
| **Visuels** | avant/après par page : débordement, tailles, contrastes, cohérence des cartes, graphes, densité | captures Chromium (scratchpad) |

## Contrat de vérification à chaque lot
1. `python -m pytest tests/ -q` → **100 %** (zéro test précision/déterminisme cassé).
2. Serveur démo (`DEMO=1 NO_IBKR=1 python terminal.py`) + Chromium → page rendue, **0 erreur console**,
   `GET /api/client-log` = **0**.
3. Endpoints honnêtes : `/healthz`, `/api/live/status`, `/api/ai/status`, `/api/system/connections`.
4. Byte-identique là où déterministe (hash scan démo inchangé) pour tout changement touchant un calcul.

## Gardiens à préserver / étendre
- Déterminisme : MC/bootstrap seed dérivé du prix ; plafonds Kelly ≤12 %, p_win ≤0,85 ; golden Black-Scholes.
- Cross-page : même entité → mêmes valeurs (`test_cross_page_consistency.py`) ; `scan_state` = même objet (`test_state.py`).
- Sync desk : 4 listes (`test_production.py::test_desk_sync_keys_single_source_of_truth`).
- Version SW épinglée (`test_ui_v3.py`, `test_production_guards_canonical.py`, `test_redesign_ui.py`).
- Lecture seule : aucun verbe d'ordre dans `vertex/ai/*` (`test_ai_api.py`).
- Nouveaux graphiques : contrat `source`+`timestamp` (`test_ui_v3.py`).
