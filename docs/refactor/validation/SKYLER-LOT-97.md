# SKYLER V2 — LOT 97 : boucle continue — scoring pur figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-97`
(base : `integration/vertex-skyler-v2` @ `202fb5d`, fraîchement fetchée).
**Moteur INTACT — diff = tests + docs uniquement.**

## 1. Repérage

`vertex/quant/scoring.py` (140 lignes — les fonctions PURES du score
/100 que toute l'app affiche : technique, momentum, fondamental, risque,
options, compose) n'avait que 5 tests indirects (test_foundation).

## 2. Les 8 comportements figés (nés verts, dits)

```text
tous les sous-scores bornés 0-100 sur entrées extrêmes                 OK
dict vide → neutres EXACTS figés (tech 18, momentum 50, fond. proxy
  45, risque 64 — les défauts rsi 50/volx 1.0 documentés)              OK
ROC borné ±25 (un ROC extrême ne domine jamais le momentum)            OK
fondamental RÉEL (P/E décoté vs pairs → 62) vs PROXY (formule force
  relative exacte) — les deux figés                                    OK
options_score(None) → None (jamais 0 inventé) ·
  échéance couvrant un earnings → −10 EXACT (IV-crush)                 OK
bucket court + IV chère → double peine ≥ 10                            OK
compose : proxy TOUJOURS signalé (fundamental_is_proxy) · sans option
  aucun sous-score inventé · confiance auto-cohérente (écart-type des
  sous-scores) · grade = barème config sur la moyenne pondérée         OK
vrais fondamentaux → drapeau proxy levé                                OK
```

## 3. Preuves

```text
python -m pytest tests/ -q → 1822 passed, 2 skipped   (1814 + 8)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

Lot 98 : angle suivant ; lot 100 = BILAN CONSOLIDÉ n°7 (76-100).
