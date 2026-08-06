# SKYLER V2 — LOT 101 : boucle continue — entonnoir de chaîne options figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-101`
(base : `integration/vertex-skyler-v2` @ `2f31ca5`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage honnête

market_clock : déjà figé (frontières 4h/9h30/16h/20h, week-end, forme).
Trou réel : `vertex/options/chain_loader.py` — la logique §14 qui
garantit qu'on ne demande JAMAIS toute la chaîne au broker n'avait
qu'UN test indirect (bornes de funnel_plan). Bornes DTE inclusives,
priorité fenêtre préférée, tri par distance au centre, fenêtre ±35 %,
échantillonnage : figés nulle part.

## 2. Les 8 comportements figés (nés verts, dits — date injectée)

```text
bornes DTE constitution INCLUSIVES (60 et 540 gardés, 59/541 exclus) ·
  dates pourries ignorées sans erreur                                  OK
préférées (90-210) D'ABORD, triées par distance au centre 150, la
  non-préférée la plus proche ferme la marche · cap MAX_EXPIRIES=4 ·
  champ interne _dist jamais fui                                       OK
expirations vides ou None → plan vide                                  OK
fenêtre de strikes ±35 % EXACTE (bornes incluses), triée               OK
spot ≤ 0 → [] (jamais une fenêtre inventée)                            OK
> 14 strikes → échantillonnage à 14 PILE gardant les DEUX extrêmes
  (ITM léger ET très OTM ultra-convexe), croissant, sans doublon       OK
une expiration sans strike plausible ne part JAMAIS au broker ·
  right propagé                                                        OK
contrat d'entrée du plan : {expiry, dte, preferred, strikes, right}    OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1847 passed, 2 skipped   (1839 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 102 : angle suivant ; lot 105 = mini-bilan tournée 101-105.
