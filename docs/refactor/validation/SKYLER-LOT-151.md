# SKYLER V2 — LOT 151 : caractérisation du « cerveau physique »

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-151`
(base : `integration/vertex-skyler-v2` @ `f907276`, lot 150 fusionné).
Nouvelle direction : modules minces HORS engines/. Lot TESTS
uniquement, aucun code moteur ni UI modifié.

## 1. Inventaire (nouvelle file, par ratio croissant)

```text
0.00  vertex/market/context.py          105 l · 0 test
0.00  vertex/market/news_impact.py       61 l · 0 test
0.00  vertex/market/news_pipeline.py     51 l · 0 test
0.00  vertex/market/regime_features.py  179 l · 0 test  ← CHOISI
0.00  vertex/market/sectors.py           83 l · 0 test
0.00  vertex/quant/ml_calibration.py     92 l · 0 test
0.34  vertex/market/editorial.py · 0.59 vertex/quant/scoring.py ·
0.64  services/live_engine.py · 0.65 quant/pivots.py …
```

Choix : `regime_features.py` — LE plus critique des six à zéro test :
analysis.py l'importe (`physics`) et sa rétroaction `score_adjust`
MODIFIE le score Vertex (composante du struct_adj [-12, +10] figé au
lot 146). Hurst, entropie de Shannon, efficience de Kaufman, demi-vie
d'Ornstein-Uhlenbeck, synthèse d'état.

## 2. Ce qui est figé (`tests/test_regime_features_lot151.py`, 15 tests)

```text
hurst — incréments persistants (bruit lissé, graine fixe) > 0.56 ;
  retour-moyenne OU < 0.2 ; LIMITE DOCUMENTÉE : une droite PURE n'a
  PAS d'exposant (différences décalées constantes → variance nulle →
  None) ; gardes série courte (< 2×max_lag) et constante
entropy — rendements constants → 0.0 ; < 30 points → None ;
  concentré < 0.3 < dispersé ≤ 1.0
efficiency — monotone → 1.0 exact ; aller-retour pur → 0.0 ;
  série plate → None (chemin nul) ; < n+1 barres → None
half_life — rappel fort → demi-vie courte (< 10 j) ; série
  TENDANCIELLE → None honnête (β ≥ 0, pas de rappel) ; < 40 → None
analyze — persistant → TENDANCE FRACTALE (note avec Hurst) ;
  OU → RETOUR MOYENNE (note avec demi-vie) ; LIMITE : droite pure →
  NEUTRE malgré efficience 1.0 (la synthèse exige H ET E) ;
  < 80 points → None ; contrat 7 clés exact
score_adjust — valeurs EXACTES : TF +4 (+3 si E ≥ 0.45 → +7),
  CHAOS -7, RM -3 (-3 si ext_atr ≥ 3 → -6), entropie ≥ 0.92 → -2 ;
  extrêmes RÉELS +7 / -9 (les bornes [-10, +8] gardent une marge) ;
  physique absente (None OU {}) → (0, '')
```

Séries déterministes : graines fixes `np.random.default_rng`
(PCG64, flux garanti stable par numpy).

## 3. Preuves

```text
python -m pytest tests/test_regime_features_lot151.py -q → 15 passed
python -m pytest tests/ -q → 2113 passed, 2 skipped (2098 + 15)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 152 : file hors engines/ — `vertex/market/sectors.py` (83 l,
0 test) ou `vertex/quant/ml_calibration.py` (92 l, 0 test) ou
`vertex/market/context.py` (105 l, 0 test), selon les appelants
produit ; puis editorial (0.34) et scoring (0.59).
