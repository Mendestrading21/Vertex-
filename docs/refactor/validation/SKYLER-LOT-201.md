# SKYLER LOT 201 — Tournée TV : radar — sommet dominant en évidence

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-201` (base : lot 200 fusionné)

## Livré

### 1. `C.radar` (chart-core) — le sommet dominant porte sa valeur

La règle « dominante en évidence » appliquée au radar (utilisé par la
scorecard d'Analyse) :

- le **sommet à la valeur maximale réelle** reçoit un anneau de focus
  (stroke couleur, opacité .55) ;
- et sa **valeur en chip pleine couleur** (`tvEdgeChip`, texte sombre),
  posée VERS LE CENTRE le long du rayon pour ne jamais gêner les
  libellés d'axes.

Grille dégressive, remplissage radial, points et libellés inchangés.
Le chip affiche la valeur RÉELLE arrondie (ex. « Risque 100 » en démo
ACN). Gardé par test d'existence de `C.tvEdgeChip`.

### 2. Jauge environnement options — héritage STRUCTUREL constaté

`pages/options-intel.js` (mountEnvGauge) appelle `VXCharts.gauge`
directement → chemin de code unique vers la jauge TV du lot 189 (arc
dégradé continu + pointeur blanc). En DEMO l'hôte
`#vx-opt-gauge-radial` n'est pas rendu (données environnement
absentes → état honnête) — l'héritage est prouvé par le code, la
capture visuelle attend des données réelles.

## Accros

Aucun. (1re capture options via `.vx-gauge` puis `#vx-opt-gauge-radial`
— hôte absent en démo, constat rapporté sans agir.)

## Preuves

- `node --check` OK (chart-core.js).
- Serveur DEMO port 5002 : `lot201-radar-card.png` — scorecard ACN,
  sommet « Risque » (100) avec anneau + chip « 100 » vers le centre ;
  pages Analyse 1440 + 390 — envoyées, **0 erreur console**.
- SW `td-shell-v164` → `v165` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## Suite

LOT 202 : suivant de TV-CHARTS-INVENTORY.md — price-chart niveaux,
vol cone, GEX / double probabilité, sparklines KPI. Mini-bilan au
lot 205.
