# SKYLER V2 — LOT 88 : boucle continue — evidence + reasoning figés

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-88-evidence`
(base : `integration/vertex-skyler-v2` @ `bb78cd8`, fraîchement fetchée).
**Moteurs INTACTS — diff = tests + docs uniquement.**

## 1. Constat de couverture

`vertex/engines/evidence.py` (232 lignes, le comité d'analystes) et
`reasoning.py` (97 lignes, les scénarios conditionnels) ont 24 tests
dédiés existants (test_evidence 9, test_reasoning 7, evidence_lab_x2 8)
qui couvrent le nominal. 10 branches limites restaient non couvertes.

## 2. Les 10 comportements figés (nés verts, dits)

```text
gather(None)            → 5 seaux vides + balance 0 + régime None      OK
entrées analyste None   → [] partout (jamais de preuve inventée)       OK
force des preuves       → bornée 0-100 (clamp -50→0, 500→100)          OK
catalyseur              → bornes exactes vol_z 2.5 / |gap| 4           OK
fondamental note 0      → AUCUNE preuve (absent ≠ négatif —
  les gates non branchés ne punissent pas)                             OK
champs manquants        → UNKNOWN prime sur « rassis »                 OK
CHAOS + MM empilées     → CONTRADICTION exposée (Loi 14)               OK
scenarios(None)         → 3 scénarios, move_pct None (jamais un %
  inventé sans prix), poids ~100                                       OK
comité absent           → poids haussier = baissier (aucun biais)      OK
invalidations           → plafonnées à 4, régime marché toujours cité  OK
```

**Aucun résultat malhonnête — les deux moteurs traitent chaque cas
limite proprement. Comportement figé par la suite.**

## 3. Preuves

```text
python -m pytest tests/ -q → 1755 passed, 2 skipped   (1745 + 10)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 89 : angle suivant ; lot 90 = MINI-BILAN 86-90.
