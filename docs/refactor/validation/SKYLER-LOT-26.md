# SKYLER V2 — LOT 26 — CALIBRATION PAR RÉGIME (MOTEUR 0.8.0, SW v100)

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-26-regime-calibration`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `7c0d33b`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

La calibration par contexte (lot 22) découpait par niveau et par décision —
mais pas par RÉGIME, la découpe la plus demandée par SCENARIO_CALIBRATION §13
(un moteur peut être calibré en TREND_UP et mal calibré en RISK_OFF). Et le
record mémoire ne figeait pas le régime au moment de la décision.

## 2. Décision

- **Régime figé** : `freeze` capture `contexts.market.regime.label` du packet —
  `None` honnête si absent ; anciens records compatibles (`dict.get`).
- **`by_regime`** dans `calibration_by_context` : mêmes règles d'échantillon
  par cellule (≥ 20 sinon `INSUFFISANT`, valeur `None`) ; un régime inconnu
  (`None`) ne crée JAMAIS de cellule.
- **Priorité de sélection documentée** dans `calibration_factor_for(...,
  level=, regime=)` : cellule NIVEAU → cellule RÉGIME → global → 0,50 —
  portée `scope` explicite (`context:level=X` / `context:regime=Y` /
  `global`). Pas de croisement niveau×régime, par choix (échantillons trop
  exigeants) — dit dans la docstring.
- **Route** : passe le régime courant du MarketContext en plus du niveau.
  **`ENGINE_VERSION` 0.7.0 → 0.8.0** (règle de consommation étendue).
- **Carte Mémoire** : bloc « Calibration par contexte (niveau → régime →
  global) » — badges par cellule (valeur + n mesures si MESURE, `insuffisant
  (n)` sinon), base au survol ; bloc masqué tant qu'aucune cellule n'existe
  (honnête). Shell modifié → **SW v99 → v100** + gardiens.

## 3. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/decision_memory.py` | régime figé, `_measured_hits` 4-uplet, `by_regime`, priorité étendue | faible |
| `vertex/engines/skyler_core.py` | version 0.8.0 | faible |
| `vertex/app/routes/analysis_api.py` | régime courant passé à la sélection | faible |
| `vertex/ui/pages/performance_page.py` | bloc badges par cellule | faible |
| SW + 4 gardiens | v100 | faible |
| `tests/test_regime_calibration_lot26.py` | 10 tests rouges→verts | faible |

## 4. Tests rouges avant correction

```text
python -m pytest tests/test_regime_calibration_lot26.py -q → 10 failed
```

## 5. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_regime_calibration_lot26.py -q → 10 passed
python -m pytest tests/ -q → 1508 passed, 2 skipped in 14.53s
```

Couverture : régime figé (RISK_OFF) et None honnête + compatibilité anciens
records ; cellule TREND_UP mesurée (25 mesures, hit rate 0,80) pendant que
RISK_OFF (3) reste INSUFFISANTE ; régime None ≠ cellule ; priorité complète
prouvée (niveau prime → régime en secours à 0,90 → global → 0,50 mémoire
vide) ; versions jamais mélangées ; moteur ≥ 0.8.0 ; endpoint sert
`by_regime` ; page contient le bloc ; SW ≥ 100.

## 6. Validation navigateur (`DEMO=1 NO_IBKR=1`)

390 + 1440 : 0 erreur console, 0 overflow ; le bloc contexte est HONNÊTEMENT
absent (0 cellule mesurée en démo fraîche — il n'apparaît qu'avec des mesures,
comportement voulu, le rendu avec cellules étant prouvé par le test
d'endpoint). Captures `lot26-memory-context-*.png`.

## 7. Invariants vérifiés

- [x] régime figé AU MOMENT de la décision — jamais recalculé après coup ;
- [x] cellule sous-échantillonnée jamais inventée ; régime inconnu ≠ cellule ;
- [x] priorité documentée, portée explicite ; versions jamais mélangées ;
- [x] SW v100 + gardiens ; READONLY, `main` intacte ; suite 1508/2.

## 8. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1498/2 | 1508/2 |
| ENGINE_VERSION | 0.7.0 | 0.8.0 |
| Découpes calibration | niveau, décision | + RÉGIME (avec sélection prioritaire) |
| SW | v99 | v100 |

## 9. Risques et limites restantes

1. Pas de croisement niveau×régime — choix documenté (échantillons).
2. Les anciens records sans régime n'alimentent pas `by_regime` — normal,
   jamais rétro-inventé.

## 10. Rollback

`git revert` du commit du lot.

## 11. Verdict

`GO`

## 12. Prochaine étape autorisée

Bloc suivant du travail continu : audit périodique type RC courte
(compileall + suite + démo complète) + backlog honnête.

**Arrêt après ce lot — validation humaine requise.**
