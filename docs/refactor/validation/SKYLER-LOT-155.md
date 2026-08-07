# SKYLER V2 — LOT 155 : caractérisation du brief éditorial + bilan de tournée

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-155`
(base : `integration/vertex-skyler-v2` @ `19724c7`, lot 154 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible et choix

Le canevas proposait scoring.py OU editorial.py. Vérification :
`scoring.py` a déjà une caractérisation ciblée solide (lot 97 —
8 tests à valeurs exactes : neutres figés, clips, proxy signalé,
confiance auto-cohérente). Choix : **`vertex/market/editorial.py`**
(202 lignes, ratio 0.34) — le narratif de séance §10 affiché en tête
d'Aujourd'hui ; chaque phrase n'est émise que si sa donnée existe.

## 2. Ce qui est figé (`tests/test_editorial_lot155.py`, 17 tests)

```text
Direction des indices — seuils EXACTS ±0.15 (0.15 « en hausse »,
  0.14 « quasi inchangés », symétrique en baisse)
Leadership — écart STRICT > 0.2 : Nasdaq à +0.2 pile ne déclenche
  PAS « leadership technologique » ; S&P dominant → « rotation
  cycliques hors technologie »
VIX — les trois phrases aux bornes 18/25 : 17.9 convexité,
  18.0 et 25.0 médiane, 25.1 renchérit
Breadth — frontière 55 : 55 « participation saine »,
  54.9 « sélectivité »
main_risk — RISK-OFF prioritaire sur la breadth étroite ;
  breadth < 45 STRICT (44.9 « faux départs », 45 pile → None :
  pas de risque déclaré sans franchissement)
calls_impact — branche IV chère (VIX 30 → « coûtent cher »,
  « R:R strict »)
Actualités — titre « À la une » borné à 180 caractères (jamais le
  titre entier) ; sources triées et dédupliquées ; phrase comité
  avec les comptes exacts
Opportunité prioritaire — premier verdict ACHETER/RENFORCER,
  les REFUSER sautés
```

## 3. Preuves

```text
python -m pytest tests/test_editorial_lot155.py -q → 17 passed
python -m pytest tests/ -q → 2178 passed, 2 skipped (2161 + 17)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. MINI-BILAN tournée 151-155 (voir aussi STATUS.md)

5 lots, PR #184 → #188, suite 2098 → 2178 passed (+80 tests), SW
stable v151. Les modules minces HORS engines/ sont couverts : les
SIX zéro-test (regime_features, sectors, ml_calibration, context,
news_impact, news_pipeline) + editorial (0.34). Découvertes clés
verrouillées : droite pure sans exposant de Hurst ; bornes humbles
de la proba [0.05, 0.85] ; verdict météo « ?% » honnête ; limite de
sous-chaîne 'ai' ; bandes VIX 16/22 (données) et 18/25 (narratif) ;
RORO ±8 ; risques priorisés (indéterminé > RISK-OFF > breadth).

## 5. Suite

LOT 156 : file restante par ratio — live_engine (0.64), pivots
(0.65), indicators (0.83), market_clock (1.12) ; ou nouvelle
direction si la couverture est jugée suffisante (durcissement
d'honnêteté, revue des routes).
