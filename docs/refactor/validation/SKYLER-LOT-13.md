# SKYLER V2 — LOT 13 — ÉTATS OPÉRATIONNELS ET CONFIANCE FACTORISÉE (MOTEUR 0.3.0)

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-13-operational-confidence`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `9d97299`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Deux champs du ledger institutionnel (lot 10) restaient honnêtement vides parce
que le moteur ne les produisait pas : `operational_state` (None, « non émis par
le moteur ») et `confidence`/`confidence_factors` (None, « aucun modèle de
confiance calibré »). DECISION_ENGINE §2.2 définit les 8 états opérationnels et
§7 la forme `confidence = data_quality × agreement × robustness × calibration`
avec plafonds obligatoires.

## 2. Problème

- Une décision servie ne disait pas SON CONTEXTE OPÉRATIONNEL (surveiller ?
  déclenchement conditionnel ? données insuffisantes ?) alors que toutes les
  informations nécessaires existaient déjà dans la sortie.
- Aucune confiance n'accompagnait la décision — pas même une estimation
  déterministe étiquetée avec ses plafonds.

## 3. Périmètre

Inclus : `skyler_core.py` (deux fonctions pures + branchement dans `decide()`,
`ENGINE_VERSION` 0.2.0 → 0.3.0), `decision_memory.py` (le gel utilise les
champs quand le moteur les produit, sinon None honnête), 19 tests. Hors
périmètre : UI, Constitution, `main`, ordres.

## 4. Décision

- **`operational_state(decision, gates, plan)`** : dérivation déterministe
  ordonnée — DATA_QUALITY_CRITICAL → `DONNEES_INSUFFISANTES` ; THESIS_BROKEN →
  `THESE_A_REEVALUER` ; ACHETER/RENFORCER → `PREPARER` ; ATTENDRE plafonné par
  gate → `CONFIRMATION_REQUISE` ; ATTENDRE avec plan complet →
  `DECLENCHEMENT_CONDITIONNEL` ; sinon → `SURVEILLER`. Base explicite à chaque
  état ; jamais une décision finale de plus (testé). `SECURISATION_PARTIELLE`
  et `RUNNER` restent dans l'énumération mais sans producteur (le moteur
  n'émet pas REDUIRE) — jamais inventés.
- **`confidence(packet, score)`** : produit de 4 facteurs bornés [0,1] avec
  base chacun — data_quality (bloc score /4), agreement (−0,20 par
  contradiction), robustness (proxy : blocs insuffisants /8, aucune analyse de
  perturbation encore — dit), calibration (0,50 fixe : aucun historique,
  jamais supposé calibré). Plafonds §7 appliqués et LISTÉS : régime UNKNOWN
  ≤ 0,55 ; conflit de sources ≤ 0,50 ; contradiction ≤ 0,60. Sortie étiquetée
  `estimated: true` + `method` — jamais 100 % (calibration 0,50 l'interdit
  structurellement).
- **`ENGINE_VERSION` 0.3.0** : changement de règle = changement de version ;
  la mémoire sépare 0.2.0/0.3.0 sans recalcul (mécanisme lot 10).

## 5. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/skyler_core.py` | `OPERATIONAL_STATES`, `operational_state()`, `confidence()`, branchement decide(), version 0.3.0 | faible |
| `vertex/engines/decision_memory.py` | gel des champs quand produits, fallback None honnête inchangé | faible |
| `tests/test_operational_confidence_lot13.py` | 19 tests rouges→verts | faible |
| `tests/test_red_team_lot12.py` | gardien de version assoupli (≥ 0.2.0 : la règle exige un bump, pas une valeur figée) | faible |

## 6. Tests rouges avant correction

```text
python -m pytest tests/test_operational_confidence_lot13.py -q
18 failed, 1 passed        (fonctions absentes, version 0.2.0, champs non exposés)
```

Gardiens ayant réagi en cours de lot (corrigés) :
- `test_single_decision_source` : la branche REDUIRE→SECURISATION_PARTIELLE
  introduisait le vocabulaire décisionnel complet dans skyler_core — branche
  SUPPRIMÉE (code mort : le moteur n'émet jamais REDUIRE) ;
- `test_engine_version_bumped_for_red_team_rule` épinglait `== '0.2.0'` —
  assoupli en `>= (0,2,0)` + existence de la règle (l'intention du test).

## 7. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_operational_confidence_lot13.py -q → 19 passed
python -m pytest tests/ -q → 1386 passed, 2 skipped in 8.82s
```

## 8. Validation runtime (`DEMO=1 NO_IBKR=1`)

| Vérification | Résultat |
|---|---|
| `/api/skyler/ACN` | `engine_version: 0.3.0` ; `operational_state: SURVEILLER` avec base ; `confidence: 0.438` (facteurs 1,0 × 1,0 × 0,875 × 0,5), caps vides listables |
| Ledger mémoire | `op_state=SURVEILLER`, `conf=0.438`, `version=0.3.0` figés |
| `/api/client-log` | 0 erreur |

## 9. Invariants vérifiés

- [x] READONLY, aucun ordre, `main` intacte, Constitution intouchée ;
- [x] état opérationnel ≠ décision finale (testé) ;
- [x] confiance ESTIMÉE avec méthode, plafonds §7 appliqués, jamais 100 % ;
- [x] version bumpée, historique séparé par version ;
- [x] anciens records sans champs → None honnête (testé) ;
- [x] suite complète verte (1386/2 skipped) ; SW v94 inchangé.

## 10. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1367/2 | 1386/2 |
| ENGINE_VERSION | 0.2.0 | 0.3.0 |
| Champs ledger vivants | 29/31 | 31/31 (op_state + confiance) |

## 11. Risques et limites restantes

1. `robustness` est un proxy (blocs insuffisants) — une vraie analyse de
   perturbation (hypothèses variées) reste à construire ; dit dans la base.
2. `calibration` fixe à 0,50 tant que le journal n'a pas d'historique noté —
   son branchement futur sur les résultats réels exigera validation humaine.
3. `SECURISATION_PARTIELLE`/`RUNNER` sans producteur (pas de décision REDUIRE
   ni de suivi de gagnants dans le moteur) — états déclarés, jamais émis.

## 12. Rollback

`git revert` du commit du lot. Les décisions 0.3.0 figées restent liées à leur
version.

## 13. Verdict

`GO`

## 14. Prochaine étape autorisée

Bloc suivant du travail continu : producteur red-team déterministe
(10 questions du comité) — puis série datée par séance pour les horizons de la
mémoire.

**Arrêt après ce lot — validation humaine requise.**
