# SKYLER V2 — LOT 103 : boucle continue — barème de liquidité figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-103`
(base : `integration/vertex-skyler-v2` @ `afdadd0`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

expected_move et event_risk : déjà figés en direct (test_option_volatility
— 1σ, bornes, niveaux de risque, crush non porté). Trou réel :
`vertex/options/liquidity.py` — `assess()`, le juge de traitabilité d'un
contrat (consommé par le sélecteur ET l'affichage), n'avait qu'UN test
superficiel (`spread_pct >= 0`). Tout le barème n'était figé nulle part.

## 2. Les 8 comportements figés (nés verts, dits)

```text
bid/ask absent ou ≤ 0 → score 0, non traitable, refus NOMMÉ            OK
contrat parfait (spread ≤ 4 %) → 100, traitable, zéro grief            OK
zone grise 4-10 % : pénalité DÉGRESSIVE exacte (7 % → 87.5) SANS
  grief nommé — on paie, on n'accuse pas                               OK
spread > 10 % : −45 nommé ET jamais traitable même à score ≥ 40
  (la double condition tradeable est réelle)                           OK
mid absent → spread inconnu traité comme 100 % (prudence, pas
  d'invention)                                                         OK
OI inconnu (−15 « inconnu ») ≠ OI faible (−30 nommé) : ne pas savoir
  coûte MOINS cher que savoir que c'est illiquide                      OK
volume None → −5 silencieux · volume faible → −10 NOMMÉ                OK
cumul exact des pénalités : 100 − 45 − 30 − 10 = 15, 3 griefs          OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1864 passed, 2 skipped   (1856 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 104 : angle suivant ; lot 105 = mini-bilan tournée 101-105.
