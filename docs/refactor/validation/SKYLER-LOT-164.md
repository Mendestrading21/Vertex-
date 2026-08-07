# SKYLER V2 — LOT 164 : caractérisation du risque de panier (legacy VIVANT)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-164`
(base : `integration/vertex-skyler-v2` @ `c9ba378`, lot 163 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/portfolio/legacy_basket_risk.py` (99 lignes, 0 test) —
VIVANT malgré son nom (vérifié au lot 163 : servi par analysis_api,
command ET risk_engine). Le « no-trade de concentration » :
corrélations du panier, HHI, exposition sectorielle, sizing
inverse-vol capé, drapeau `no_new_risk`.

## 2. Ce qui est figé (`tests/test_legacy_basket_risk_lot164.py`, 8 tests)

```text
Gardes — panier < 2 séries exploitables → note honnête, PAS de
  blocage ; série < 40 points EXCLUE (le titre disparaît du panier)
Drapeau corrélation — paire quasi identique (corr 0.92) →
  'correlation_panier_elevee' + no_new_risk True + top_pair
  expliquée ; panier 5 titres décorrélés → aucun drapeau,
  diversification ≥ 80
TROIS LIMITES DOCUMENTÉES :
  · cap infaisable — n × 15 % < 100 % → les poids restent au cap,
    la somme vaut n × cap (75 % pour 5 titres) : le sizing n'est
    PAS renormalisé au-delà du cap
  · concentration sectorielle NON détectée sur petit panier —
    2 titres 100 % Semiconducteurs mais poids capés sommant 30 %
    → sous le seuil 40 %, pas de drapeau (renormaliser = décision
    explicite)
  · FAIL-OPEN sur erreur — entrée illisible → dict d'erreur avec
    no_new_risk False : l'analyse ne bloque pas le risque quand
    elle ne peut pas conclure, l'erreur est exposée
_cap_weights — redistribution somme 1 quand faisable (tolérance
  d'itération ≤ 1 %), poids tous nuls → nuls
```

## 3. Preuves

```text
python -m pytest tests/test_legacy_basket_risk_lot164.py -q → 8 passed
python -m pytest tests/ -q → 2263 passed, 2 skipped (2255 + 8)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 165 : dernier de la tournée + MINI-BILAN 161-165 obligatoire.
Candidats : ai/briefs (0.33), portfolio/risk_engine (0.52),
legacy_adapter (272 l — à découper).
