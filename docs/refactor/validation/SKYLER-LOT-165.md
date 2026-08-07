# SKYLER V2 — LOT 165 : moteur de risque du portefeuille réel + bilan de tournée

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-165`
(base : `integration/vertex-skyler-v2` @ `8c55762`, lot 164 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/portfolio/risk_engine.py` (100 lignes, §26 — servi par
strategy_os) — le risque du portefeuille RÉEL (jamais les candidats
du scanner). Seule l'honnêteté des greeks était couverte
(test_calc_honesty) ; la chaîne du risque est désormais COMPLÈTE :
correlation (lot 160) + stress_tests (160) + basket_risk (164) +
risk_engine (165).

## 2. Ce qui est figé (`tests/test_risk_engine_lot165.py`, 8 tests)

```text
Garde de provenance — snapshot 'SCANNER' → ValueError (le risque
  ne se calcule JAMAIS sur les candidats du scanner)
Poids & concentration — surpoids détecté (66.67 % > 15 %), HHI
  exact 0.4623, secteur Tech 80 % > 40 % averti, bêta PONDÉRÉ par
  les poids (1.07 exact) ; aucun bêta connu → None (jamais un 1.0
  inventé)
Règles de discipline — drawdown -25 % PILE → no_new_risk True
  (borne INCLUSE, ≤) avec « AUCUN nouveau risque » ; titre à
  -23.1 % ≤ -20 % → « revue de position obligatoire »
Exposition options — 4 ouvertes > max 3 → no_new_risk True ;
  agrégat HONNÊTE : somme des seuls deltas connus (1.0), gamma
  absent → None (pas un 0 qui sous-estimerait), greeks_partial
  signalé dès qu'une valeur manque ; sans options → défauts None
Contrat — 14 clés exactes du rapport de risque
```

## 3. Preuves

```text
python -m pytest tests/test_risk_engine_lot165.py -q → 8 passed
python -m pytest tests/ -q → 2271 passed, 2 skipped (2263 + 8)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. MINI-BILAN tournée 161-165 (voir aussi STATUS.md)

5 lots, PR #194 → #198, suite 2239 → 2271 passed (+32 tests), SW
stable v151. Couverts : constituents (démarrage jamais bloqué
PROUVÉ), trio audit/contexte/rôles (rappels READONLY figés mot pour
mot), factor_exposure + replacement_engine (+ vérif : les 2 legacy
VIVANTS), basket_risk (cap infaisable, fail-open), risk_engine
(chaîne du risque complète — bornes -25 %/-20 % incluses, plafond
d'options, provenance gardée). Le périmètre ai/data/strategy/
portfolio n'a plus que 4 modules non caractérisés (briefs, copilot,
company, universe partiels) + legacy_adapter.

## 5. Suite

LOT 166 : ai/briefs (0.33) ou data/company (0.39) ou
legacy_adapter (272 l, à découper) — ou nouvelle direction si
pertinent (durcissement, revue des routes).
