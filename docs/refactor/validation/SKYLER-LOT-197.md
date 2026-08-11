# SKYLER LOT 197 — Tournée TV : théta hachuré (projection modèle) + scénarios par héritage

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-197` (base : lot 196 fusionné)

## Livré

### 1. `C.hatchPattern(color)` — motif d'estimation réutilisable (chart-core)

Équivalent CANVAS du `tvHatch` SVG (teinte .08 + rayures 45° .38),
désormais disponible pour TOUS les builders Chart.js. Nouvelle option
`hatch: true` de `C.area` : le remplissage passe du dégradé au motif
hachuré — la texture qui dit « estimation/projection, pas un réel ».
Défaut inchangé (aucun graphique modifié sans opt-in).

### 2. Théta (Options) — la projection assume sa texture

`option-theta.js` (`C.thetaCard`) : `hatch: true` + `extremes: 'min'` —
la décroissance temps vient du `scenario_pricer` (un MODÈLE) : l'aire
est hachurée comme le payoff (lot 192) et le cône (lot 190), et le chip
Min marque la valeur la plus basse de la projection. Données de la
simulation moteur inchangées.

### 3. Scénarios (Options) — ✔ par HÉRITAGE constaté

`option-scenarios.js` passe par `C.heatmapCard` → il a hérité du lot
194 sans modification : texte des cellules coloré par intensité, pire
cellule (−66 % BEAR J+28 sur la capture) en dominante liserée, pied
« estimation modèle, pas une promesse » déjà en place. Constaté en
navigateur, marqué ✔ à l'inventaire.

## Accros

Aucun.

## Preuves

- `node --check` OK (chart-core.js, option-theta.js).
- Serveur DEMO port 5002, contrat GOOGL ouvert (clic tr[data-ct]) :
  `lot197-theta-card.png` (aire jaune HACHURÉE, chip « Min 23,3 » +
  pilule dernière valeur), `lot197-scenarios-card.png` (héritage TV
  constaté), pages 1440 + 390 — envoyées, **0 erreur console**.
- SW `td-shell-v160` → `v161` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## Suite

LOT 198 : suivant de TV-CHARTS-INVENTORY.md — sensibilité IV / GEX
(Options), sparklines KPI, barres leadership, price-chart niveaux,
radar, vol cone, barres S+/S/A/B, discipline Journal, aires indices.
Mini-bilan au lot 200.
