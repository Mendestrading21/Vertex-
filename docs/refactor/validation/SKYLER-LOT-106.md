# SKYLER V2 — LOT 106 : boucle continue — score contextuel des contrats figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-106`
(base : `integration/vertex-skyler-v2` @ `9c7df4e`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

`vertex/options/contract_scorer.py` (§20 — le score qui CLASSE les
contrats candidats, 125 lignes) n'avait qu'UNE assertion de constante
(MIN_REWARD_RISK == 2.0). Les principes anti-défauts — score
MULTIPLICATIF, aucun facteur ne rachète un défaut fatal — n'étaient
figés nulle part.

## 2. Les 8 comportements figés (nés verts, dits — 1 sonde ajustée : score non arrondi, approx)

```text
R:R 2.5 + tout au vert → 90 pile, raisons NOMMÉES                      OK
R:R 1.0 < minimum → plafonné à 10 (« un OI élevé ne rachètera pas
  ça »)                                                                OK
R:R non calculable → plancher 5, jamais un score flatteur              OK
liquidité = MULTIPLICATEUR ≤ 1 (50/100 → ×0.65, jamais un bonus)       OK
DTE 60 (minimum absolu, hors fenêtre préférée 90-210) → ×0.75 nommé    OK
IV rank ≥ 85 → ×0.6 « payer la peur coûte cher, DTE long ou pas »      OK
ULTRA_CONVEX : setup STANDARD → score 0 SANS APPEL (rare_setup_only)
  · EXCEPTIONAL mais convexité < 80 % → moitié · sinon raison nommée   OK
prime < 0.10 → ×0.3 « le prix bas n'est pas un argument »              OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1888 passed, 2 skipped   (1880 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 107 : angle suivant ; lot 110 = mini-bilan 106-110.
