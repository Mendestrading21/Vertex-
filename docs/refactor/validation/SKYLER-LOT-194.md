# SKYLER LOT 194 — Tournée TV : heatmap alignée + part du treemap en chip

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-194` (base : lot 193 fusionné)

## Livré

### 1. Heatmap alignée sur la grammaire TV (builder partagé)

`vertex/static/vertex/js/charts/heatmap.js` — deux signatures TV sur
`C.heatmapCard`, héritées par TOUS les appelants (secteurs Marchés,
P&L mensuel Portefeuille, scénarios/IV Options) :

1. **Texte des cellules coloré par intensité** : chaque valeur porte
   la couleur de sa tonalité (positive/négative) avec un alpha fondu
   sur |t| (.45 → 1) et gras 700 — comme les cartes secteurs TV, la
   grille se lit sans regarder les fonds.
2. **Cellule DOMINANTE en évidence** : la cellule au |t| maximal de
   TOUTE la grille (une seule, comptes réels) reçoit un liseré appuyé
   (1.6 px, alpha .75) et gras 800 — les autres restent adoucies,
   même langage que la barre dominante du consensus (lot 191).

Tuiles verre, tokens rgb dérivés de C.colors, cellules nulles
(surface neutre) et navigation data-hm inchangés.

### 2. Treemap — part du total en chip pleine couleur

`chart-core.js` (`C.treemap`) : sur les grandes tuiles (l > 90), le
« x % » translucide devient un **chip `tvEdgeChip`** pleine couleur de
la tuile (texte sombre) en haut-droit — LE chiffre éducatif du treemap
dans la grammaire des chips de bord (cône lot 190, runway lot 193).

## Accros

Aucun. Constat démo (rendu honnête) : les tuiles du treemap
portefeuille sont neutres (gris) car le P&L démo est absent — la
couleur ne s'invente pas.

## Preuves

- `node --check` OK sur heatmap.js + chart-core.js.
- Serveur DEMO port 5002 : `lot194-heatmap-card.png` (Marchés secteurs
  — +1,28 % vert / −1,58 % rouge en texte coloré, dominante liserée),
  `lot194-treemap-card.png` (chips 65 %/35 %), `lot194-markets-1440.png`,
  `lot194-markets-390.png` — envoyées, **0 erreur console**.
- SW `td-shell-v157` → `v158` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## Suite

LOT 195 : MINI-BILAN 191-195 + suivant de l'inventaire (sparklines
KPI, equity/drawdown, GEX, scénarios options, discipline Journal,
staleness Système, aires indices).
