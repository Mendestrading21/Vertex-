# SKYLER V2 — LOT 157 : caractérisation des indicateurs techniques purs

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-157`
(base : `integration/vertex-skyler-v2` @ `9e19c1e`, lot 156 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/market/indicators.py` (155 lignes, §12 — SMA/EMA/RSI/ATR/
Bollinger/VWAP purs, sans pandas). Les 11 tests existants couvrent
les bases (alignement, valeurs simples) — ce lot ne fige QUE les
lacunes réelles, conformément au canevas.

## 2. Ce qui est figé (`tests/test_market_indicators_lot157.py`, 9 tests)

```text
Robustesse — valeur non numérique → None traversant (jamais
  d'exception) ; fenêtre nulle/négative → tout None
ASYMÉTRIES de trous de données (comportements limites DOCUMENTÉS,
  deux philosophies assumées) :
  · SMA se RÉINITIALISE sur un trou (honnêteté de fenêtre)
  · EMA TRAVERSE depuis sa valeur précédente (pas de fenêtre à
    invalider)
  · ATR RECOPIE la dernière valeur sur un true-range incalculable
    (pas de None au milieu, pas d'invention : la dernière mesure)
  · VWAP resservi tel quel sur volume nul (le cumul n'avance pas)
  Les unifier = décision explicite future
Longueurs H/L/C différentes → tronquées au minimum (jamais
  d'IndexError)
RSI — valeur GOLDEN de la série classique de Wilder : 70.5 au
  premier point (prouve le lissage de Wilder, pas une SMA) puis
  57.9 ; toutes pertes → 0.0
Bollinger — le multiplicateur écarte les bandes, la médiane n'en
  dépend pas, écart symétrique exact
```

## 3. Preuves

```text
python -m pytest tests/test_market_indicators_lot157.py -q → 9 passed
python -m pytest tests/ -q → 2195 passed, 2 skipped (2186 + 9)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 158 : `live_engine.py` (258 l, 0.64 — moteur live SSE) puis
`market_clock.py` (1.12). Mini-bilan 156-160 au lot 160.
