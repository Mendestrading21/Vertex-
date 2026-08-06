# SKYLER V2 — LOT 94 : boucle continue — contrat des routes POST figé

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-94-post`
(base : `integration/vertex-skyler-v2` @ `31c78ea`, fraîchement fetchée).

## 1. Inventaire et sondes (publiés)

18 routes POST au total. Déjà couvertes par suites dédiées : tradingview
(12 tests), desk/desk-restore (lots 74/84), pos-quotes (lot 74),
memory/import (lot 45), rescan/tracking (suites existantes). Les 12
restantes SONDÉES avec payloads limites (non-JSON, null, vide, 1e308) :

```text
ai/refresh 202 · copilot/ask « question vide » ok:false ·
options/analyze « jambes manquantes » available:false ·
planning/ticket 400 « symbol requis » · portfolio/team 200 ·
pretrade/check honnête (« hors du scan ») · rescan 200 ·
tracking 400 « symbol requis » · live/refresh 200 ·
weekly-regen « scan pas encore prêt » ok:false · login 302
→ 0×5xx, TOUS les refus structurés et honnêtes
```

## 2. Les 4 caractérisations (nées vertes, dites)

`tests/test_post_routes_lot94.py` : jamais 5xx sur payloads limites ·
refus structurés honnêtes (ok:false + raison, jamais un résultat
inventé) · télémétrie client TRONQUÉE exactement (page 120 / msg 300 /
src 160 chars, line non-entier → None) · tampon circulaire PLAFONNÉ à
100 (les anciens évincés, jamais de croissance infinie).

## 3. Preuves

```text
python -m pytest tests/ -q → 1801 passed, 2 skipped   (1797 + 4)
tools/rc_short_audit.js → GO — 0 défaut (SW v127)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
```

## 4. Suite

LOT 95 : angle suivant + MINI-BILAN 91-95 dans STATUS.
