# SKYLER LOT 227 — Dette TODO + perf serveur : double constat mesuré (0 défaut)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-227` (base : lot 226 fusionné)

## Constat 1 — Dette documentée : ZÉRO marqueur

Balayage `TODO|FIXME|XXX|HACK` (mot entier) sur TOUT le code produit —
`terminal.py` + `vertex/**` (*.py, *.js, *.css, vendor exclu) :

**0 occurrence.** Aucune dette auto-documentée n'attend dans le code.
(La dette CONNUE vit ailleurs, là où elle doit vivre : la purge de
terminal.py cartographiée dans les rapports, EN ATTENTE d'accord
humain — pas en commentaires éparpillés.)

## Constat 2 — Perf serveur en démo : SAIN, très large marge

Chronométrage réel (urllib, 5 passes/route, serveur DEMO chaud) des
8 routes HTML + 8 API critiques :

| Route | méd. (ms) | max (ms) | | Route API | méd. (ms) | max (ms) |
|---|---:|---:|---|---|---:|---:|
| / | 1,9 | 8,0 | | /healthz | 1,2 | 1,2 |
| /markets | 1,7 | 1,9 | | /api/command | 2,9 | 3,8 |
| /opportunities | 1,5 | 1,5 | | /api/market/summary | 1,5 | 1,8 |
| /portfolio | 1,4 | 1,8 | | /api/market/regime | 1,3 | 1,4 |
| /journal | 1,5 | 1,6 | | /api/briefing/editorial | 2,0 | 3,1 |
| /options | 1,2 | 1,4 | | /api/system-status | 1,3 | 1,7 |
| /system | 1,4 | 1,4 | | /cal-feed | 1,3 | 1,4 |
| /tracking | 1,4 | 1,5 | | /api/live/status | 1,2 | 1,4 |

16/16 routes en 200, **médianes 1,2 à 2,9 ms, pire cas 8 ms** (le
premier hit de `/`). La génération serveur des pages (HTML en chaînes
Python) est négligeable devant le budget DCL < 300 ms du lot 72 — le
coût du chargement est côté navigateur (JS/CSS), déjà budgété et gardé
(lot 72 + mesure de dérive lot 226).

Aucun correctif nécessaire — **double constat honnête, aucun code
touché**.

## Décision SW

**Pas de bump** (`td-shell-v172` inchangé) : constat pur.

## Preuves

- Tableaux chiffrés ci-dessus (protocole reproductible : urllib,
  5 passes, min/méd/max).
- Suite complète : **2482 passed / 2 skipped** (référence maintenue).

## Suite

LOT 228 : entretien suivant ou directive. Purge terminal.py toujours
EN ATTENTE d'accord humain explicite.
