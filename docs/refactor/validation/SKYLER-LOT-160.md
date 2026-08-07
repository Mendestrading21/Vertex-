# SKYLER V2 — LOT 160 : famille risque portefeuille + bilan de tournée

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-160`
(base : `integration/vertex-skyler-v2` @ `ee044d2`, lot 159 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cibles

Les deux modules les plus SERVIS de la famille risque (zéro test) :
`vertex/portfolio/correlation.py` (42 l — consommé par risk_engine →
drapeau « correlation_panier_elevee » du Command Center) et
`vertex/portfolio/stress_tests.py` (85 l — servi par la route
strategy_os, §26). factor_exposure et replacement_engine (dépendants
de research/team_engine) restent en file.

## 2. Ce qui est figé (`tests/test_portfolio_risk_lot160.py`, 11 tests)

```text
correlation — bornes ±1.0 exactes (identité/opposition) ; gardes
  < 30 points → None et variance nulle → None ; matrice à paires
  TRIÉES (A/B, A/C, B/C), seuil high_pairs ≥ 0.8, avertissement
  « diversification illusoire » ≥ 0.7 ; matrice vide honnête ;
  corrélation moyenne du candidat (rien à comparer → None)
stress_tests — hypothèse DOCUMENTÉE : bêta inconnu vaut 1.0
  (SPY -5 % → -4.17 % exact sur le snapshot 2 positions + cash) ;
  secteur dominant -15 × poids ; CORRELATIONS_TO_ONE ne choque
  QUE les actions (le cash protège : -6.67 %) ; sensibilité taux
  inconnue → None honnête (« non estimé »), fournie → ±symétrique ;
  équité incalculable → stress REFUSÉS avec avertissement ;
  worst_case exact + alerte drawdown quand le pire scénario
  dépasse le max du profil ; les 10 scénarios déclarés tous
  présents quand les entrées le permettent
```

## 3. Preuves

```text
python -m pytest tests/test_portfolio_risk_lot160.py -q → 11 passed
python -m pytest tests/ -q → 2230 passed, 2 skipped (2219 + 11)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. MINI-BILAN tournée 156-160 (voir aussi STATUS.md)

5 lots, PR #189 → #193, suite 2178 → 2230 passed (+52 tests), SW
stable v151. Couverts : pivots (5 signaux du plan), indicators
(asymétries de trous), live_engine (bornes de fraîcheur strictes),
market_clock (+ limite jours fériés), famille risque portefeuille
(corrélations + stress). Découvertes verrouillées : anti-chasse
1.2 ATR du breakout ; SMA/EMA/ATR/VWAP à quatre philosophies de
trous ; à la borne de fraîcheur on bascule déjà ; pas de calendrier
NYSE ; bêta inconnu = 1.0 ; le cash protège quand les corrélations
tendent vers 1. Nouveau périmètre inventorié (11 modules zéro-test).

## 5. Suite

LOT 161 : file du périmètre — data/constituents (112 l), ai/audit
(37 l), ai/strategy_context (25 l), portfolio/team_roles (19 l) ;
factor_exposure + replacement_engine ; legacy à vérifier.
