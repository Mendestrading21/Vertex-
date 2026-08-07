# SKYLER V2 — LOT 171 : honnêteté HTTP de Position Intelligence

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-171`
(base : `integration/vertex-skyler-v2` @ `c01eaa4`, lot 170 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible — NOUVELLE DIRECTION : durcissement d'honnêteté des routes

Survey préalable : `vertex/options/` (27 modules) et `vertex/research/`
(14 modules) sont déjà couverts (lot6, lot95, lot115, lot117, lot118,
dealer_synthesis, gex_scan, gex_history, tv_confluence…). Le survey des
routes (`vertex/app/routes/`, endpoint par endpoint) a révélé la vraie
lacune : **`positions_api.py` (249 lignes) — 4 endpoints à ZÉRO test**
(`/api/positions/state`, `/report`, `/audit`, `/reconcile`) plus
`/api/positions/<id>/changes`. Les moteurs sous-jacents (repository,
recalculator, audit, reconciler — 41 tests directs) étaient couverts ;
la COUCHE HTTP qui les sert ne l'était pas.

## 2. Ce qui est figé (`tests/test_positions_api_lot171.py`, 10 tests)

```text
/state — desk vide → live False DIT, positions [], P&L None (jamais
  un 0 inventé), delta/theta None ; position réelle → recalcul au prix
  RÉEL du scan ((200−150)×10 = 500), cible dépassée → TARGET_REACHED
  avec action DESCRIPTIVE « SÉCURISER » mais décision ATTENDRE (Vertex
  n'exécute JAMAIS) ; myTrades corrompu → 200 + vide honnête, pas de
  crash
/report + /reconcile — IBKR hors ligne : « positions locales
  conservées, aucune clôture automatique », issues [] et 0 réparation
  (l'absence du broker ne clôture JAMAIS une position locale)
/audit — desk vide → HEALTHY, 0 vérifiée, 0 finding
/<id>/changes — introuvable → HTTP 200 + {error: 'position
  introuvable', changed: False} DOCUMENTÉ tel quel (pas 404 — le
  client UI lit `error` sans casse réseau) ; 1er appel = baseline
  (before None, source 'scan') + snapshot persisté ; 2e appel après
  +5 % → before/after exacts, change_pct 5.0, matérialité MAJOR
/api/portfolio/stress — myTrades corrompu → empty True + raison
  « aucune position action avec prix réel », generator deterministic
Invariant — la source du module ne contient AUCUN verbe d'ordre
  (placeOrder/place_order/submit_order/transmit)
```

## 3. Preuves

```text
python -m pytest tests/test_positions_api_lot171.py -q → 10 passed
python -m pytest tests/ -q → 2338 passed, 2 skipped (2328 + 10)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 172 : continuer le durcissement des routes par lacune réelle —
candidats au survey : `analysis_api.py` (744 l, 0 test direct),
`decision_api.py`, `tracking_api.py`, `ai_api.py`, `feeds.py`.
