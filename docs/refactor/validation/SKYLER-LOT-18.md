# SKYLER V2 — LOT 18 — ROBUSTESSE MESURÉE PAR PERTURBATION (MOTEUR 0.5.0)

> Date : 2026-08-05  
> Branche : `agent/skyler-v2-lot-18-perturbation`  
> Base : `integration/vertex-skyler-v2`  
> SHA avant : `091e009`  
> SHA après : (tête de la branche du lot)  
> PR : brouillon vers `integration/vertex-skyler-v2`

## 1. Constat

Le facteur `robustness` de la confiance (lot 13) était un PROXY (blocs
insuffisants /8) — dit comme tel dans sa base, mais il ne mesurait pas ce que
DECISION_ENGINE §7 demande : « la stabilité du résultat aux hypothèses ».

## 2. Décision

- **`perturbation_analysis()`** : re-décide sous une liste FIXE de 11
  variations documentées (`PERTURBATIONS`) : score technique ±10, R:R ±0,5,
  confiance du régime ±0,2 (bornées), et un contexte retiré à la fois
  (market/events/anomaly/options/portfolio). `robustness` = fraction des
  perturbations APPLICABLES qui laissent la décision inchangée — les
  perturbations sans donnée d'entrée sont `not_applicable`, listées, EXCLUES
  de la fraction (jamais comptées stables par défaut). Sortie : valeur bornée,
  stables/applicables, liste exacte des bascules (perturbation → décision),
  base. Déterministe — aucun aléatoire (gardien : `import random` interdit).
- **Anti-divergence** : le cœur du verdict est extrait en `_decision_label()`,
  PARTAGÉ entre `decide()` et l'analyse — les règles ne peuvent pas diverger.
- **`confidence(packet, score, robustness=...)`** : consomme la robustesse
  mesurée ; le proxy blocs insuffisants ne reste qu'en secours explicite quand
  aucune perturbation n'est applicable (dit dans la base).
- **`ENGINE_VERSION` 0.4.0 → 0.5.0** ; `decide()` expose le bloc
  `perturbation` complet + étape d'audit ; la mémoire fige la nouvelle
  confiance sous 0.5.0, séparée des versions précédentes (mécanisme lot 10).

## 3. Implémentation

| Fichier | Modification | Risque |
|---|---|---|
| `vertex/engines/skyler_core.py` | `PERTURBATIONS`, `perturbation_analysis`, `_decision_label` partagé, `confidence(robustness=)`, version 0.5.0 | faible |
| `tests/test_perturbation_lot18.py` | 11 tests rouges→verts | faible |
| `tests/test_red_team_producer_lot14.py` | gardien de version rendu prospectif (≥ 0.4.0) | faible |

## 4. Tests rouges avant correction

```text
python -m pytest tests/test_perturbation_lot18.py -q
9 failed, 2 passed
```

## 5. Tests après correction

```text
python -m compileall -q terminal.py vertex → exit 0
python -m pytest tests/test_perturbation_lot18.py -q → 11 passed
python -m pytest tests/ -q → 1438 passed, 2 skipped in 9.89s
```

Cas prouvés : un ACHETER frontière (28/40 exactement) bascule en ATTENDRE
sous `score_technique_-10` — fragilité détectée, robustesse < 1 ; un REFUSER
de dossier vide est robuste (≥ 0,8, seules les perturbations applicables
comptées) ; sans plan, R:R ±0,5 est `not_applicable` et
`n_applicable + not_applicable = 11` ; le facteur robustness de la confiance
égale exactement la fraction mesurée et sa base liste les bascules ;
déterminisme et absence d'aléatoire testés ; gel mémoire sous 0.5.0.

## 6. Validation runtime (`DEMO=1 NO_IBKR=1`)

`/api/skyler/ACN` : moteur 0.5.0, décision REFUSER, robustesse **1.0
(11/11 stables, 0 bascule, 0 non applicable)** — un refus de dossier faible
est massivement robuste, exactement ce qu'on attend ; confiance 0,5 (plafond
structurel : calibration 0,50 × facteurs pleins). `/api/client-log` : 0.

## 7. Invariants vérifiés

- [x] liste de perturbations FIXE, déterministe, sans aléatoire (testé) ;
- [x] non applicable ≠ stable — exclu de la fraction, listé ;
- [x] cœur de verdict partagé — aucune divergence de règles possible ;
- [x] version bumpée, historique séparé, gardiens prospectifs ;
- [x] READONLY, aucun ordre, `main` intacte ; suite 1438/2 skipped ; SW v96
      inchangé (aucune UI touchée).

## 8. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Tests | 1427/2 | 1438/2 |
| ENGINE_VERSION | 0.4.0 | 0.5.0 |
| robustness | proxy blocs insuffisants | MESURÉE (11 perturbations, bascules listées) |

## 9. Risques et limites restantes

1. Coût : chaque décision exécute jusqu'à 11 pipelines légers supplémentaires
   (dicts purs) — négligeable à l'unité ; le sweep X1 multiplie par l'univers,
   à surveiller si l'univers grandit fortement.
2. Les amplitudes (±10, ±0,5, ±0,2) sont des choix documentés de la liste
   fixe — les faire varier serait une nouvelle version du moteur.

## 10. Rollback

`git revert` du commit du lot.

## 11. Verdict

`GO`

## 12. Prochaine étape autorisée

Bloc suivant du travail continu : calibration réelle branchée sur le facteur
`calibration` quand la mémoire contient des résultats mesurés.

**Arrêt après ce lot — validation humaine requise.**
