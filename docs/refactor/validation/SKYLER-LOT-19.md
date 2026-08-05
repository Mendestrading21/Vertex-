# SKYLER V2 — LOT 19 — CALIBRATION RÉELLE DE LA CONFIANCE (MOTEUR 0.6.0)

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-19-real-calibration`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `f08c8e8`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Depuis le lot 13, le facteur `calibration` de la confiance était figé à 0,50
(« aucun historique ») — honnête, mais la boucle décision → mémoire →
confiance n'était pas fermée : les résultats mesurés de la mémoire (lots
10/15) n'alimentaient rien.

## 2. Décision

- **`decision_memory.calibration_factor(memory, engine_version)`** : depuis
  les résultats MESURÉS de la mémoire pour CETTE version de moteur UNIQUEMENT —
  scenario hit rate = part des décisions mesurées dont le résultat était
  contenu par les scénarios (`DECISION_CORRECTE` ou `VARIANCE_NORMALE` au plus
  long horizon mesuré, via `classify_error`). Facteur = 0,50 + 0,40 × hit
  rate, **borné [0,50, 0,90]** — jamais 1,0.
- **Seuil d'échantillon** : `MIN_CALIBRATION_SAMPLE = 20` mesures minimum —
  en dessous, facteur 0,50 avec raison « échantillon insuffisant (n/20) » :
  un facteur ne s'invente pas sur 3 mesures.
- **`confidence(..., calibration=)`** consomme le facteur documenté ;
  `decide(..., calibration=)` le transporte ; la route `/api/skyler/<sym>` le
  calcule fail-safe depuis la mémoire persistée avant chaque décision.
- **`ENGINE_VERSION` 0.5.0 → 0.6.0** — les décisions 0.6.0 sont figées
  séparément ; leur PROPRE calibration ne s'alimentera que de résultats 0.6.0
  (aucun recyclage inter-versions, prouvé par test).

## 3. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/decision_memory.py` | `calibration_factor` + `MIN_CALIBRATION_SAMPLE` | faible |
| `vertex/engines/skyler_core.py` | `confidence(calibration=)`, `decide(calibration=)`, version 0.6.0 | faible |
| `vertex/app/routes/analysis_api.py` | calcul fail-safe du facteur avant `decide` | faible |
| `tests/test_real_calibration_lot19.py` | 12 tests rouges→verts | faible |

## 4. Tests rouges avant correction

```text
python -m pytest tests/test_real_calibration_lot19.py -q
11 failed, 1 passed
```

## 5. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_real_calibration_lot19.py -q → 12 passed
python -m pytest tests/ -q → 1450 passed, 2 skipped in 9.55s
```

Couverture : mémoire vide → 0,50 raison dite ; 3 mesures parfaites → toujours
0,50 (jamais gonflé) ; 20 mesures à 75 % → 0,80 exact avec hit rate documenté ;
100 % → plafond 0,90, 0 % → plancher 0,50 ; une autre version n'alimente
JAMAIS le facteur (0 mesure comptée) ; `VARIANCE_NORMALE` compte comme hit
(le scénario pessimiste avait contenu la perte) ; déterminisme ; `decide`
consomme le facteur (0,80 visible avec sa base) ; défaut sans historique
inchangé ; route en client Flask réel : mémoire vide → 0,50 « insuffisant »
dans la décision servie.

Aucun gardien cassé par le bump — tous les gardiens de version sont désormais
prospectifs (`>=`).

## 6. Invariants vérifiés

- [x] jamais un facteur inventé sous l'échantillon minimum (raison dite) ;
- [x] borné [0,50, 0,90] — jamais 1,0 ;
- [x] versions JAMAIS mélangées (test dédié) ;
- [x] `VARIANCE_NORMALE` = hit (cohérent avec la taxonomie du lot 10) ;
- [x] fail-safe route (mémoire illisible → défaut honnête) ;
- [x] READONLY, aucun ordre, `main` intacte ; suite 1450/2 skipped ; SW v96
      inchangé (aucune UI).

## 7. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1438/2 | 1450/2 |
| ENGINE_VERSION | 0.5.0 | 0.6.0 |
| calibration | 0,50 figé | scenario hit rate réel, borné, par version |
| Boucle décision→mémoire→confiance | ouverte | FERMÉE (avec seuil d'échantillon) |

## 8. Risques et limites restantes

1. Le hit rate agrège tous les régimes/niveaux — la calibration par contexte
   (SCENARIO_CALIBRATION §13) reste une granularité future.
2. En pratique, le facteur restera 0,50 jusqu'à ce que 20 décisions 0.6.0
   soient MESURÉES (séances réelles du lot 15) — la confiance ne montera
   qu'avec des preuves, c'est le but.
3. La pondération 0,50 + 0,40 × hit rate est un choix documenté ; la modifier
   = nouvelle version du moteur.

## 9. Rollback

`git revert` du commit du lot.

## 10. Verdict

`GO`

## 11. Prochaine étape autorisée

Bloc suivant du travail continu : drill-down mémoire par décision
(`GET /api/skyler/memory/<decision_id>`) + repricing options pour la red-team.

**Arrêt après ce lot — validation humaine requise.**
