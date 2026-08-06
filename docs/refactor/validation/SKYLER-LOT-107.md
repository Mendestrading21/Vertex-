# SKYLER V2 — LOT 107 : boucle continue — courbe de taux figée

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-107`
(base : `integration/vertex-skyler-v2` @ `4745e62`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

double_prob : déjà figé à la main (golden N(−0.3177) ≈ 0.375, modèle
documenté, confiance RÉDUITE — dit). Trou réel :
`vertex/data_sources/rates.py` — RateCurve sert de FIXTURE à une dizaine
de fichiers de tests, mais la courbe ELLE-MÊME (interpolation, clamps,
fallback plat documenté §6.6, rate_sensitivity) n'avait AUCUN test
direct.

## 2. Les 8 comportements figés (nés verts, dits)

```text
courbe vide → repli plat 0.045 qui SE DIT (fallback_used True, note
  « documenté », source FALLBACK) — jamais présenté comme du marché    OK
interpolation linéaire EXACTE (30→0.04, 90→0.05 : 60 j → 0.045 pile,
  45 j → 0.0425)                                                       OK
clamp aux extrémités : 5 j → premier point, 3000 j → dernier —
  JAMAIS d'extrapolation                                               OK
points fournis en désordre → triés en interne, interpolation juste     OK
tenor exact sur un point → ce taux exact                               OK
contrat to_dict complet (7 clés)                                       OK
rate_sensitivity : ±50 bp par défaut, valeurs et pente exactes
  (documente à quel point le taux compte — exigence §6.6)              OK
bump bas plafonné à 0 (jamais un taux négatif) · prix indisponible →
  sensibilité None, pas 0                                              OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1896 passed, 2 skipped   (1888 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 108 : angle suivant ; lot 110 = mini-bilan 106-110.
