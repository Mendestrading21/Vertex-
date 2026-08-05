# SKYLER V2 — LOT 22 — CALIBRATION PAR CONTEXTE (MOTEUR 0.7.0)

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-22-context-calibration`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `528caaf`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

La calibration réelle (lot 19) agrégeait tous les contextes — un moteur peut
pourtant être bien calibré sur ses refus et mal calibré sur ses achats.
SCENARIO_CALIBRATION §13 exige la découpe par contexte, avec la discipline
d'échantillon par cellule.

## 2. Décision

- **`calibration_by_context(memory, engine_version)`** : découpe les mesures
  par NIVEAU (S_PLUS/S/A/B/REFUS_WATCH) et par DÉCISION (ACHETER/ATTENDRE/
  REFUSER). Chaque cellule reçoit SON hit rate et SON facteur (0,50 + 0,40 ×
  hit rate, borné) UNIQUEMENT si `n_cellule ≥ MIN_CALIBRATION_SAMPLE` (20) —
  sinon `INSUFFISANT` avec compte exact, valeur `None`, jamais inventée.
  Versions jamais mélangées.
- **`calibration_factor_for(memory, version, level=)`** : sélection à portée
  explicite (`scope`) — cellule du niveau courant si `MESURE` →
  `context:level=X` ; sinon agrégat global ; sinon 0,50 « insuffisant ».
- **Route** : `/api/skyler/<sym>` calcule le niveau préliminaire
  (`score40(packet0)`) et sert le facteur CONTEXTUEL de ce niveau —
  **`ENGINE_VERSION` 0.6.0 → 0.7.0** (règle de consommation changée).
- **`/api/skyler/memory`** expose `calibration_by_context` complet.

## 3. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/decision_memory.py` | `_measured_hits`, `_context_cell`, `calibration_by_context`, `calibration_factor_for` | faible |
| `vertex/engines/skyler_core.py` | version 0.7.0 (commentaire versionné) | faible |
| `vertex/app/routes/analysis_api.py` | facteur contextuel du niveau courant + exposition API | faible |
| `tests/test_context_calibration_lot22.py` | 9 tests rouges→verts | faible |

## 4. Tests rouges avant correction

```text
python -m pytest tests/test_context_calibration_lot22.py -q
8 failed, 1 passed
```

## 5. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_context_calibration_lot22.py -q → 9 passed
python -m pytest tests/ -q → 1481 passed, 2 skipped in 12.95s
```

Couverture : cellule A à 25 mesures obtient SON hit rate (0,80 → facteur 0,82)
pendant que la cellule B à 3 mesures reste INSUFFISANTE (valeur None) ; une
autre version n'alimente rien ; mémoire vide honnête ; déterminisme ;
sélection contextuel → global → 0,50 avec `scope` ; moteur ≥ 0.7.0 ; `decide`
porte la base contextuelle ; endpoint mémoire sert la découpe ; route en
client Flask réel : 25 mesures REFUS_WATCH parfaites sous la version courante
→ la décision démo (dossier faible → REFUS_WATCH) reçoit **0,90 avec la base
« cellule niveau=REFUS_WATCH »** — la boucle contextuelle est prouvée de bout
en bout.

## 6. Invariants vérifiés

- [x] discipline d'échantillon PAR CELLULE (jamais un facteur inventé) ;
- [x] versions jamais mélangées ; portée du facteur explicite (`scope`) ;
- [x] secours global préservé ; défaut 0,50 raisonné ;
- [x] READONLY, aucun ordre, `main` intacte ; suite 1481/2 skipped ; SW v97
      inchangé (aucune UI).

## 7. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1472/2 | 1481/2 |
| ENGINE_VERSION | 0.6.0 | 0.7.0 |
| Calibration | agrégat global | par niveau ET décision, cellule autonome, secours global |

## 8. Risques et limites restantes

1. Le niveau utilisé pour la sélection est celui du packet préliminaire (avant
   red-team) — cohérent avec la construction, dit ici.
2. Découpes futures possibles (§13) : régime, type de catalyseur, IV
   percentile — mêmes mécanismes, échantillons encore plus exigeants.

## 9. Rollback

`git revert` du commit du lot.

## 10. Verdict

`GO`

## 11. Prochaine étape autorisée

Bloc suivant du travail continu : vue lisible du post-mortem + index des
rapports de lots.

**Arrêt après ce lot — validation humaine requise.**
