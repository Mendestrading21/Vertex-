# SKYLER V2 — LOT 190 : TOURNÉE TV — le cône de projection

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-190`
(base : `integration/vertex-skyler-v2` @ `0ab9bcb`, lot 189 fusionné).
Lot UI (tournée graphique TV). Moteurs INTACTS, READONLY intact.

## 1. Livré

```text
NOUVEAU BUILDER charts/projection-cone.js — VXCharts.projectionCone :
  la signature « prix cible » TradingView nourrie par les niveaux
  RÉELS du plan moteur. Trait blanc = clôtures réelles récentes →
  point actuel ; éventail HAUSSIER hachuré (tvHatch positif) entre
  TP1 et TP3 avec médiane pointillée vers TP2 ; faisceau de RISQUE
  hachuré (négatif) vers le stop ; frontière « PROJECTION — plan
  moteur » ; chips de bord (tvEdgeChip) : TP3 +x %, TP2, TP1,
  Actuel, Stop −x % — pourcentages CALCULÉS du plan. Sans plan
  complet → VX.states.empty (jamais un niveau inventé). Pied
  honnête : « une carte de risque, pas une prévision de marché ».
  Aucun littéral couleur : C.colors + fallbacks de l'inventaire.
BRANCHÉ fiche Analyse (analysis_page.py) : <script src> + hôte
  #an-cone en tête de la carte « Plan & niveaux clés », alimenté
  par d.price/plan.stop/tp1-3 + les 60 dernières clôtures réelles.
Ajustement après 1re capture : marge droite 96 → 118 (chips
  entiers). SW v153 → v154 + 5 gardiens de version.
```

## 2. Preuves

```text
node --check projection-cone.js → OK (+ sweep lot 186 en suite)
Serveur DEMO 5002 · captures /analysis/ACN 1440+390 + carte cadrée —
  0 erreur console — ENVOYÉES à l'utilisateur
python -m pytest tests/ -q → 2461 passed, 2 skipped
TV-CHARTS-INVENTORY.md : cône ✔
```

## 3. Suite

LOT 191 : barres de consensus du comité (Intelligence — verdicts
RÉELS du committee-review, style barres Strong Buy TV) + regimeAura
aligné (Aujourd'hui).
