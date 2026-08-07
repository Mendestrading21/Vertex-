# SKYLER V2 — LOT 174 : honnêteté HTTP du ticket de préparation + recherche

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-174`
(base : `integration/vertex-skyler-v2` @ `5d612c6`, lot 173 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

Survey des mentions test par endpoint : les plus minces étaient
`/api/planning/ticket` (`planning_api.py`, 43 l — couvert seulement
par un test de robustesse aux grands nombres) et `/api/search`
(`feeds.py` — seule route de feeds à logique propre, couverte
seulement par un smoke 200). Le moteur `order_ticket` a ses tests
directs ; la lacune était le câblage HTTP du ticket — la route la
plus sensible du produit au regard du READONLY (elle prépare un
texte d'ordre à COPIER dans IBKR, sans jamais transmettre).

## 2. Ce qui est figé (`tests/test_planning_search_lot174.py`, 10 tests)

```text
/api/planning/ticket — sans symbole → 400 « symbol requis » ; le plan
  du scan est repris (entrée 100, rr 3.0 transmis tels quels) avec
  dimensionnement EXACT (100 k × 1 % = 1 000 ; risque unitaire 5 →
  200 actions) ; la CONCENTRATION bloque même avec un budget de
  risque correct (20 % projeté > 15 % → blocked + blocker explicite
  — le garde-fou prime sur le budget) ; le body PRIME sur le plan du
  scan (entry/stop → per_unit_risk 10, qty 100) ; refus honnêtes
  (sans compte → qty/sizing None sans blocage ; stop au-dessus de
  l'entrée → « risque non défini » ; option sans prime → « prime
  indisponible ») ; option dimensionnée sur la prime (2.5 × 100 =
  250 par contrat → 4) avec TYPE/STRIKE dans le texte ;
  INVARIANT PRODUIT : chaque copy_text COMMENCE par « PRÉPARATION
  UNIQUEMENT — Vertex est en lecture seule et ne transmet aucun
  ordre », le stop y est « (référence, non transmis) », readonly True
/api/search — sans q → [] ; sous-chaîne insensible à la casse
  (aapl → AAPL) ; plafond dur à 20 résultats
Invariant — aucun verbe d'ordre dans planning_api ni feeds
```

## 3. Preuves

```text
python -m pytest tests/test_planning_search_lot174.py -q → 10 passed
python -m pytest tests/ -q → 2367 passed, 2 skipped (2357 + 10)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 175 : dernier lot de la tranche + MINI-BILAN 171-175 obligatoire
(171 positions_api, 172 decision_api, 173 tracking_api, 174
planning/search, 175 à choisir — candidats : session_api digest/
manifest, opportunities_api funnel, ai_api enrichment, live_api).
