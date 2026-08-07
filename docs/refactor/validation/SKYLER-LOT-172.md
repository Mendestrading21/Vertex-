# SKYLER V2 — LOT 172 : honnêteté HTTP des décisions de position

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-172`
(base : `integration/vertex-skyler-v2` @ `379e40b`, lot 171 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

Survey endpoint par endpoint des routes candidates (analysis_api,
decision_api, tracking_api, ai_api, feeds, redesign) : deux endpoints
à ZÉRO test dans `vertex/app/routes/decision_api.py` (182 lignes) —
**`/api/position-decision/<sym>`** et **`/api/options-for/<sym>`** —
alors que les moteurs servis (`recommendation.position_decision` /
`options_for_position`) sont couverts par le lot 87. La lacune était
le câblage HTTP (parsing des paramètres, normalisations, sous-jacent).

## 2. Ce qui est figé (`tests/test_decision_api_lot172.py`, 9 tests)

```text
/api/position-decision/<sym> — symbole inconnu → HOLD avec sous-jacent
  étiqueté DATA_INSUFFICIENT (jamais inventé), symbole normalisé
  majuscules ; stop touché via query params → EXIT 78 « perte au
  stop » ; paramètres corrompus (entry=abc, pl_pct=xyz, dte=) →
  avalés en None, HOLD, JAMAIS un crash ; les seuils de discipline
  traversent la couche HTTP intacts (action -20 % EXIT, option -20 %
  HOLD, option -25 % EXIT) ; thêta commande à ≤14 j en gain →
  TAKE_PROFIT « thêta / expiration »
/api/options-for/<sym> — board vide → suggestions [] + note explicite
  (« Aucun contrat chargé… ») jamais un contrat inventé ; position
  ACTION → 5 rôles exacts (CALL qualité max, PUT, LEAPS ≥300 j,
  COVERED_CALL delta 0.15-0.40, PROTECTIVE_PUT) et JAMAIS un contrat
  d'un autre titre du board ; type ≠ STK → normalisé OPT et les rôles
  revenu/protection disparaissent (on ne vend pas un call couvert
  sans actions)
Invariant — aucun verbe d'ordre dans la source du module
```

## 3. Preuves

```text
python -m pytest tests/test_decision_api_lot172.py -q → 9 passed
python -m pytest tests/ -q → 2347 passed, 2 skipped (2338 + 9)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 173 : poursuivre la tournée des routes — prochaines lacunes
partielles à sonder : analysis_api (18 endpoints, 744 l — mémoire
Skyler import/export/cell), tracking_api (routes POST/DELETE),
feeds (/api/options, /api/comite). MINI-BILAN au lot 175.
