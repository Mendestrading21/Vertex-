# SKYLER V2 — LOT 20 — DRILL-DOWN MÉMOIRE ET POST-MORTEM PAR DÉCISION

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-20-postmortem-drilldown`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `bee14fb`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

La mémoire décisionnelle n'exposait que des agrégats — impossible d'inspecter
UNE décision figée avec son résultat et sa lecture post-mortem (mode
Post-Mortem du comité, ADVERSARIAL_COMMITTEE §7).

## 2. Décision

- **`post_mortem(record, outcome)`** (pur, déterministe) : décision vs
  résultat observé — classification par horizon mesuré (`classify_error`),
  **scénario ayant CONTENU le résultat** (`HORS_FOURCHETTE_BASSE` /
  `PESSIMISTE` / `PROBABLE` / `EXCEPTIONNEL_ATTEINT`), MFE/MAE, résumé.
  Rien de mesuré → `available: false` avec raison ; scénarios absents à la
  décision → containment non évaluable, dit ; **erreur de discipline
  inobservable sans trades réels — dit, jamais deviné**.
- **`GET /api/skyler/memory/<decision_id>`** : record figé complet + outcome +
  post-mortem ; id inconnu → **404 structuré** (`error: decision_inconnue`).
- **Carte Mémoire (Performance)** : tableau « Dernières décisions figées »
  (5 dernières — titre, décision, moteur, séance) avec lien « détail → » vers
  le post-mortem. Shell modifié → **SW `td-shell-v96` → `td-shell-v97`** +
  gardiens (celui du lot 17 rendu prospectif ≥ 96).

## 3. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/decision_memory.py` | `find_decision`/`find_outcome`/`post_mortem` | faible |
| `vertex/app/routes/analysis_api.py` | route drill-down 200/404 | faible |
| `vertex/ui/pages/performance_page.py` | tableau dernières décisions + liens | faible |
| `vertex/app/routes/system.py` + 4 gardiens + gardien lot 17 | SW v97, prospectifs | faible |
| `tests/test_postmortem_lot20.py` | 13 tests rouges→verts | faible |

## 4. Tests rouges avant correction

```text
python -m pytest tests/test_postmortem_lot20.py -q
13 failed
```

## 5. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_postmortem_lot20.py -q → 13 passed
python -m pytest tests/ -q → 1463 passed, 2 skipped in 10.48s
```

Couverture : non mesuré honnête ; containment PROBABLE (+14 % ∈ [12, 18)),
PESSIMISTE (−4 % ∈ [−6, 12) → VARIANCE_NORMALE), HORS_FOURCHETTE_BASSE
(−15 % → ERREUR_*), EXCEPTIONNEL_ATTEINT (+22 % ≥ 18) ; scénarios absents →
note honnête ; discipline inobservable dite ; MFE/MAE + résumé ; déterminisme ;
route 200 complète et 404 structuré (client Flask réel) ; liens dans la carte ;
SW ≥ 97.

## 6. Validation navigateur (Playwright, `DEMO=1 NO_IBKR=1`)

| Vue | Taille | Résultat |
|---|---:|---|
| /journal (Performance) | 1440×900 | 2 liens post-mortem rendus, drill-down suivi → 200, `available: false` honnête (décision figée le jour même, aucun horizon mesuré) ; 0 overflow |
| /journal | 390×844 | idem ; 0 overflow |

- erreurs console : **0** ; `/api/client-log` : 0 ;
- captures : `docs/skyler/baseline/lot20-performance-{desktop,mobile}.png`.

## 7. Invariants vérifiés

- [x] post-mortem = LECTURE des données figées — ne réécrit jamais le record ;
- [x] non mesuré → indisponible avec raison ; discipline jamais devinée ;
- [x] 404 structuré sur id inconnu ;
- [x] SW v97 + gardiens prospectifs ;
- [x] READONLY, aucun ordre, `main` intacte ; suite 1463/2 skipped.

## 8. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1450/2 | 1463/2 |
| Inspection par décision | impossible | record + outcome + post-mortem |
| SW | v96 | v97 |

## 9. Risques et limites restantes

1. Le lien « détail → » ouvre le JSON brut de l'API — une vue formatée du
   post-mortem est une amélioration future (le contenu est déjà complet).
2. Le containment utilise le plus long horizon séance mesuré — le containment
   par horizon de scénario déclaré viendra quand le moteur déclarera des
   horizons de thèse.

## 10. Rollback

`git revert` du commit du lot.

## 11. Verdict

`GO`

## 12. Prochaine étape autorisée

Bloc suivant du travail continu : repricing spot×temps×IV branché sur les
questions options de la red-team (Q05/Q08).

**Arrêt après ce lot — validation humaine requise.**
