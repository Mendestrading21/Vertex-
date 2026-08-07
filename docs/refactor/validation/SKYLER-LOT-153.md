# SKYLER V2 — LOT 153 : caractérisation du contexte marché (la « météo »)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-153`
(base : `integration/vertex-skyler-v2` @ `4aded4c`, lot 152 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/market/context.py` (105 lignes, 0 test direct) — la « météo »
marché avant de regarder un titre : régime du SPY lui-même, bandes
VIX, Risk-On/Off (cycliques vs défensifs), breadth des 45 leaders,
verdict du jour. Servie par decision_api et terminal.

## 2. Ce qui est figé (`tests/test_market_context_lot153.py`, 15 tests)

```text
Robustesse — TOUT dégradé (5 × None) → contrat complet à 10 clés,
  valeurs None, breadth {}, et un verdict quand même émis avec
  « participation ?% » (honnête — pas un chiffre inventé) :
  comportement limite DOCUMENTÉ
Régime SPY — rampe pure → TREND, ADX 100, texte « au-dessus
  MM20 & MM50 » ; oscillation bruitée (graine fixe) → CHOP
Bandes VIX — bornes EXACTES : 15.9 calme / 16.0 normal /
  21.9 normal / 22.0 stress ; un seul point → None honnête
  (la variation exige ≥ 2 points)
Breadth — participation réelle : above50/above200 en %, avancées/
  reculs, nouveaux sommets (pos52 ≥ 98) / creux (≤ 5), % BUY
RORO — bornes EXACTES ±8 : gap 8 → RISK-ON, 7 → NEUTRE,
  -7 → NEUTRE, -8 → RISK-OFF ; sans secteurs → défauts 50/50 →
  NEUTRE gap 0
Verdict — la phrase complète composée : « MARCHÉ EN TENDANCE ·
  RISK-ON · participation 50% au-dessus MM50 · VIX 14.0 (calme) »
```

## 3. Preuves

```text
python -m pytest tests/test_market_context_lot153.py -q → 15 passed
python -m pytest tests/ -q → 2141 passed, 2 skipped (2126 + 15)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 154 : `news_impact.py` (61 l, 0 test) + `news_pipeline.py`
(51 l, 0 test — servis par daily_brief, à combiner) ; puis
editorial (0.34), scoring (0.59). Mini-bilan 151-155 au lot 155.
