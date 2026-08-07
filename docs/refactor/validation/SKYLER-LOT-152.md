# SKYLER V2 — LOT 152 : caractérisation rotation sectorielle + calibration ML

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-152`
(base : `integration/vertex-skyler-v2` @ `88a9cd3`, lot 151 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié. Deux modules
zéro-test combinés (minces).

## 1. Cibles

`vertex/market/sectors.py` (83 lignes, 0 test) — rotation
sectorielle : appelée par le comité (`engines/committee.py`) et la
fiche Analyse (`routes/analysis_api.py`). `vertex/quant/
ml_calibration.py` (92 lignes, 0 test) — probabilité de gain
calibrée consommée par `engines/quant_engine.py` (chaîne du score).

## 2. Ce qui est figé (`tests/test_sectors_mlcalib_lot152.py`, 13 tests)

```text
sectors — agrégation exacte (avg_score, pct_buy, breadth b50/b200
  depuis les signaux) et tri par score moyen décroissant ; symbole
  hors mapping exclu silencieusement ; membres classés par (score,
  sigcount) ; bornes risk_band EXACTES : <3 Low, 3.0-5.0 Med,
  >5 High ; delta vs veille ignore les scores None (sans baseline
  → None honnête) ; sans détail moteur → défauts neutres (score 0,
  atr 2 → Low, rs 50, rvol 1) ; rows vides → [] ; contrat de la
  carte secteur et des membres
ml_calibration — point NEUTRE exact : edge 54 → p_win 0.500 ;
  calibration annoncée figée : edge 86 → 0.736, edge 30 → 0.317 ;
  bornes HUMBLES [0.05, 0.85] (jamais une promesse, jamais un zéro
  absolu) ; ajustement Monte-Carlo first-touch (+0.4 net → 0.525) ;
  nuance structure trend_quality (0.574) ; DEUX LIMITES
  DOCUMENTÉES : bloc None → repli edge 50 → proba quasi neutre
  0.468, MAIS edge non numérique → prédiction entière None (pas de
  repli partiel) ; meta_score == round(p_win × 100) partout
```

## 3. Preuves

```text
python -m pytest tests/test_sectors_mlcalib_lot152.py -q → 13 passed
python -m pytest tests/ -q → 2126 passed, 2 skipped (2113 + 13)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 153 : file hors engines/ — `vertex/market/context.py` (105 l,
0 test, servi par decision_api + terminal) puis news_impact/
news_pipeline (0 test, servis par daily_brief), puis editorial
(0.34), scoring (0.59).
