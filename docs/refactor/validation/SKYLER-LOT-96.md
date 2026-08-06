# SKYLER V2 — LOT 96 : boucle continue — socle math du lab options figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-96`
(base : `integration/vertex-skyler-v2` @ `ea23ac8`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage (leçon du lot 95 appliquée : grep par nom de module)

chain_loader/dealer_synthesis/gex_history : couverts (1 fichier chacun) ;
context (8), backtest (3), knowledge_graph (6) : couverts. Le vrai trou :
`options_lab.py` (862 lignes) a 26 tests de HAUT niveau mais son **socle
mathématique** (Black-Scholes maison, _ncdf, _pct, _star, _rr) n'était
caractérisé nulle part directement.

## 2. Les 7 comportements figés (nés verts, dits)

```text
_ncdf : vraie CDF (N(0)=0,5 · N(1)=0,8413 table · bornes ±10)          OK
_bs dégénéré (T=0, IV=0, spot/strike invalides) → valeur INTRINSÈQUE,
  jamais NaN ni crash                                                  OK
PARITÉ PUT-CALL exacte : C − P = S − K·e^(−rT) à 1e-9 près             OK
GOLDEN BS : S=K=100, T=1, IV=20 %, r=4,5 % → C ≈ 10,19 — recalculé À
  LA MAIN (d1=0,325, d2=0,125). Mon premier golden « de mémoire »
  (10,27) était FAUX — LE MOTEUR AVAIT RAISON, corrigé et dit          OK
_pct(x, 0) → None (jamais ZeroDivisionError) · _r2 tolérant            OK
_star : qualité d'abord, POP départage, jamais un contrat sans
  qualité · board vide → None                                          OK
_rr : potentiel inconnu → None, jamais inventé                        OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1814 passed, 2 skipped   (1807 + 7)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 97 : angle suivant ; lot 100 = BILAN CONSOLIDÉ n°7 (76-100).
