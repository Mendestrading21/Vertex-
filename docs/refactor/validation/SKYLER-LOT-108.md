# SKYLER V2 — LOT 108 : boucle continue — surface de volatilité figée

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-108`
(base : `integration/vertex-skyler-v2` @ `f0024ea`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**
(Lot démarré sur « Continue » utilisateur, sans attendre le réveil.)

## 1. Repérage honnête

horizon_scanners : déjà bien couvert (LEAPS/TACTICAL/SWING/YOLO, absent
— dit). Trou réel : `vertex/options/vol_surface.py` (210 lignes) n'avait
que 3 tests d'INTÉGRATION (inversion+crush, honnêteté sans historique,
zones de valeur relative). Les formules internes n'étaient figées nulle
part.

## 2. Les 8 comportements figés (nés verts, dits)

```text
realized_vol : prix constants → 0.0 exact · série trop courte → None
  honnête · _median vide → None, pair → moyenne des centraux            OK
spot invalide → surface VIDE + note « spot invalide » (jamais bâtie
  sur du faux)                                                          OK
IV pourries (absente, 0, négative, > 500 %) filtrées — jamais utilisées OK
ATM = IV du strike LE PLUS PROCHE du spot (pas une moyenne) ·
  expected move = atm·√(dte/365)·100 exact                              OK
skew calculé SEULEMENT si un put ~10 % OTM existe à < 6 % du spot —
  sinon aucun skew inventé                                              OK
dislocations NOMMÉES : STRIKE_IV_DISLOCATION (≈3× la médiane) +
  SMILE_DISCONTINUITY (saut adjacent > 35 %)                            OK
IV rank/percentile EXACTS sur historique linéaire (max → 100/100,
  milieu → rank 50)                                                     OK
IV_SPIKE si courante > 1.3× la médiane récente (« payer la peur ») ·
  historique PLAT → rank None (jamais 0 inventé), percentile honnête    OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1904 passed, 2 skipped   (1896 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 109 : angle suivant ; lot 110 = mini-bilan 106-110.
