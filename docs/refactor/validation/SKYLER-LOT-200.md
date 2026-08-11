# SKYLER LOT 200 — Tournée TV : série de référence à chips Max/Min + MINI-BILAN 196-200

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-200` (base : lot 199 fusionné)

## Livré

### 1. Aires indices (Marchés) — chips Max/Min sur la série de référence

- **`line-area-chart.js`** : passthrough `extremes` de `C.areaCard` vers
  `C.area` (opt-in — aucun autre appelant modifié).
- **`markets_page.py`** : la carte « série de référence » (SPY ou proxy,
  120 séances) active `extremes: true` — les chips **Max/Min** (plugin
  lot 195, grammaire tvEdgeChip) se posent sur le plus haut et le plus
  bas RÉELS de la série, en plus de la pilule de dernière valeur. Les
  bornes de la période se lisent sur la courbe, comme sur TV.

### 2. Discipline Journal — ✔ par HÉRITAGE structurel

Les barres du Journal/Performance (répartition des décisions, P&L par
mois, progression) appellent `VXCharts.bars` directement
(performance_page L281/417/461) → elles ont hérité du lot 199 (barre
dominante : liseré + chip de valeur) SANS modification. En démo le
journal est vide (localStorage) → états vides honnêtes, l'héritage est
prouvé par le chemin de code unique.

## Accros

Aucun.

## Preuves

- `node --check` OK ; import Python OK.
- Serveur DEMO port 5002 : `lot200-spy-card.png` — chips « Max 443,69 »
  au sommet, « Min 351,41 » au creux, pilule « 413,00 » en fin de
  série (120 séances réelles du scan) ; pages Marchés 1440 + 390 +
  Journal — envoyées, **0 erreur console**.
- SW `td-shell-v163` → `v164` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## MINI-BILAN 196-200

Voir STATUS.md — 5 lots, PR #229 → #233, SW v159 → v164, suite stable
2461/2. La règle « dominante en évidence » et les chips de
valeur/extrêmes désormais transverses : staleness (196), théta hachuré
+ scénarios héritage (197), rails à chip (198), barres dominantes
(199), série de référence à Max/Min + discipline héritage (200).

## Suite

LOT 201 : suivant de TV-CHARTS-INVENTORY.md — price-chart niveaux,
radar, vol cone, GEX, double probabilité, sparklines KPI.
