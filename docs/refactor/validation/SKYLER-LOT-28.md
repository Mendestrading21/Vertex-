# SKYLER V2 — LOT 28 — DÉCOUPE BY_CATALYST + PROPAGATION 3 SAUTS GARDÉE

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-28-catalyst-hops`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `59f298f`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Décisions

### (a) `by_catalyst` — découpe d'OBSERVATION uniquement

- Dérivée du champ `catalyst` DÉJÀ figé dans le record (aucun nouveau champ) :
  cellules `avec_catalyseur` / `sans_catalyseur`, mêmes règles d'échantillon
  (≥ 20 sinon `INSUFFISANT`, valeur `None`).
- **PAS consommée par la sélection du facteur** : `calibration_factor_for`
  garde sa signature (niveau → régime → global) — testé par inspection ET par
  scénario (25 mesures avec catalyseur, niveaux tous insuffisants → scope
  `global`, jamais `catalyst`). **Aucun bump de moteur** : aucune règle de
  décision ne change, c'est une lentille d'observation dans
  `/api/skyler/memory` (dit dans la note de l'API).

### (b) Propagation 3 sauts avec garde de volume

- `propagate(graph, node, max_hops=..., max_paths=None)` : garde dure
  **`MAX_PATHS` = 200** (surchargeable), troncature DÉTERMINISTE (parcours
  trié) — le défaut 2 sauts reste inchangé (compatibilité lot 11 testée).
- Route `/api/skyler/graph/<sym>?hops=1..3` (défaut 2, clampé, invalide →
  défaut) ; la réponse porte TOUJOURS `truncated` et une note explicite quand
  la garde a tronqué — jamais silencieux.

## 2. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/decision_memory.py` | `_measured_hits` 5-uplet (+catalyseur), `by_catalyst` | faible |
| `vertex/engines/knowledge_graph.py` | `MAX_PATHS`, garde dans `propagate` | faible |
| `vertex/app/routes/analysis_api.py` | `?hops=`, `truncated`, note | faible |
| `tests/test_catalyst_hops_lot28.py` | 7 tests rouges→verts | faible |

## 3. Tests rouges avant correction

```text
python -m pytest tests/test_catalyst_hops_lot28.py -q
3 failed, 4 passed    (les 4 verts = comportements existants préservés,
                       dont le défaut 2 sauts et la non-consommation)
```

## 4. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_catalyst_hops_lot28.py -q → 7 passed
python -m pytest tests/ -q → 1515 passed, 2 skipped in 8.35s
```

Couverture : cellules avec/sans catalyseur (25 mesures → hit rate 0,80 ;
3 → INSUFFISANT) ; non-consommation prouvée deux fois ; déterminisme ;
3 sauts atteignent des chemins de profondeur 4 sans jamais dépasser ; étoile
dense (25 sociétés × 3 catalyseurs) → garde à `max_paths=10` exacte, garde
par défaut `MAX_PATHS` atteinte, déterministe ; défaut 2 sauts inchangé ;
route : `hops` par défaut/explicite/clampé/invalide + `truncated` toujours
présent.

## 5. Invariants vérifiés

- [x] découpe d'observation ≠ règle moteur (aucun bump — dit et testé) ;
- [x] troncature JAMAIS silencieuse (champ + note) ; déterministe ;
- [x] aucun nouveau champ figé (dérivation du ledger existant) ;
- [x] READONLY, aucun ordre, `main` intacte ; suite 1515/2 ; SW v100 inchangé
      (aucun shell modifié).

## 6. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1508/2 | 1515/2 |
| Découpes calibration | niveau, décision, régime | + catalyseur (observation) |
| Propagation | 2 sauts, sans garde explicite | 1–3 sauts, garde 200 dite |

## 7. Risques et limites restantes

1. `by_catalyst` binaire (présence d'un catalyseur daté) — le type de
   catalyseur (earnings vs macro) serait une découpe future.
2. La garde de volume borne l'API ; une exploration complète au-delà reste
   possible côté moteur via `max_paths` explicite.

## 8. Rollback

`git revert` du commit du lot.

## 9. Verdict

`GO`

## 10. Prochaine étape autorisée

Backlog honnête restant ou RC courte périodique.

**Arrêt après ce lot — validation humaine requise.**
