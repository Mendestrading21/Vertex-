# SKYLER V2 — LOT 170 : caractérisation de l'univers

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-170`
(base : `integration/vertex-skyler-v2` @ `2073713`, lot 169 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/data/universe.py` (324 lignes, ratio 0.56 — dernier module de
la file du périmètre ai/data/strategy/portfolio). Données pures :
l'univers scanné (union des 3 indices US), la watchlist, les
cartographies GICS/industrie, les listes hors-US et l'ensemble
« tendance ». Les tests existants vérifient le câblage ; ceux-ci
figent les INVARIANTS DE COHÉRENCE des données elles-mêmes.

## 2. Ce qui est figé (`tests/test_universe_lot170.py`, 9 tests)

```text
Univers — dédupliqué (aucun doublon), plancher ≥ 400 tickers,
  LIVE_SYMBOLS == UNIVERSE (une seule liste servie au live) ;
  INDEX_SOURCE ∈ {live, cache, cache-stale, static} et
  INDEX_MEMBERS['union'] == UNIVERSE (une seule vérité)
Normalisation yfinance — AUCUN point dans l'univers US ni la
  watchlist (BRK.B → BRK-B) ; les suffixes de place (.PA, .T…)
  vivent exclusivement dans _EUROPE/_ASIA (tous suffixés)
Cartographies — _GICS a exactement 11 secteurs, miroir des 11 ETF
  de _SECTOR_ETFS ; AUCUN ticker dans deux secteurs GICS ni dans
  deux industries ; les aplatis _GICS_SECTOR/_INDUSTRY_MAP couvrent
  exactement les tickers déclarés (une seule vérité par ticker)
Watchlist — 57 tickers sans doublon
Tendance — TREND_SET == set(_TREND_EXTRA) (badge 🔥 de l'UI), ≥ 30
```

## 3. Preuves

```text
python -m pytest tests/test_universe_lot170.py -q → 9 passed
python -m pytest tests/ -q → 2328 passed, 2 skipped (2319 + 9)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

La file du périmètre est ÉPUISÉE (tous les modules de vertex/engines,
market, quant, services, ai, data, strategy, portfolio ont désormais
des tests directs). LOT 171 : nouvelle direction (durcissement
d'honnêteté des routes, revue de sécurité, vertex/options/ ou
vertex/research/ par ratio, ou correctifs utilisateur).
