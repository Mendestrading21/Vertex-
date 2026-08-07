# SKYLER V2 — LOT 156 : caractérisation de la structure par pivots

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-156`
(base : `integration/vertex-skyler-v2` @ `d5e4d92`, lot 155 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/quant/pivots.py` (124 lignes, ratio 0.65) — `structure()`
est appelée par analysis.py : détection des sommets/creux fractals,
classement de tendance (UP/DOWN/RANGE) et LOGIQUE d'entrée — c'est
elle qui fournit le stop STRUCTUREL du plan de trade.

## 2. Ce qui est figé (`tests/test_pivots_lot156.py`, 8 tests)

```text
Les 5 signaux, chacun atteint par un zigzag déterministe :
  EN_TENDANCE — UP en milieu de mouvement → PAS d'entrée
    (« attendre » la cassure ou le repli)
  REFUS_DOWNTREND — tendance baissière → jamais d'achat, aucun
    niveau émis (« un rebond ici = piège »)
  RANGE — ni sommets ni creux directionnels → « cassure
    confirmée » exigée
  BREAKOUT — franchissement RÉCENT du dernier sommet (≤ 1.2 ATR,
    sous le sommet il y a < 7 séances — anti-chasse) → entrée,
    stop SOUS le dernier creux, cible = EXTENSION (measured move :
    sommet + (sommet − creux)), rr cohérent
  REPLI_REPRIS — repli ≤ 1.8 ATR sur le dernier creux PUIS
    reprise (clôture > veille) → cible = le dernier sommet
Gardes — série < 2k+5 barres → None ; entrée sans colonnes → None
Repli ATR — atr None → 1 % du dernier cours (jamais de ÷0)
Contrat — 16 clés exactes ; fenêtres swing bornées à 4 ;
  last_high/low == dernier de chaque fenêtre ; zigzag UP →
  sommets rendus croissants
```

## 3. Preuves

```text
python -m pytest tests/test_pivots_lot156.py -q → 8 passed
python -m pytest tests/ -q → 2186 passed, 2 skipped (2178 + 8)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 157 : file restante — live_engine (0.64, moteur SSE),
indicators (0.83), market_clock (1.12) ; mini-bilan 156-160 au
lot 160.
