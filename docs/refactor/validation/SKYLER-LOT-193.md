# SKYLER LOT 193 — Tournée TV : catalystRunway aligné (piste dégradée + hachures + chip)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-193` (base : lot 192 fusionné)

## Livré

### Catalyst Runway (Aujourd'hui) aligné sur la grammaire TV

`vertex/static/vertex/js/charts/catalyst-runway.js` — trois signatures
de la grammaire (lots 189-192) appliquées à la piste DTE :

1. **Piste en dégradé CONTINU** : l'axe passe du trait uniforme
   border-soft à un dégradé userSpaceOnUse imminence rouge
   (`--vx-negative`) → moyen terme jaune (`--vx-warning`, ancré à la
   frontière ≤ 5 j réelle de l'horizon) → horizon éteint
   (`--vx-border-soft`) — la lecture du risque temporel est dans la
   matière même de la piste.
2. **Zone ≤ 5 j HACHURÉE** : par-dessus la teinte existante, un rect
   `tvHatch` négatif — la texture « estimation/risque » commune à
   toute la tournée (cône lot 190, payoff lot 192).
3. **Chip J-x sur le PROCHAIN catalyseur** : le premier événement
   porte son échéance en `tvEdgeChip` pleine couleur d'impact (texte
   sombre), les suivants gardent le texte simple — l'œil sait où
   regarder, même grammaire que les chips du cône.

Anti-collision d'étiquettes (lot 61), anneau de focus, halos d'impact,
verdict tonal et état vide honnête (calendrier vide → `states.empty`)
STRICTEMENT inchangés. Usage de `C.tvHatch`/`C.tvEdgeChip` gardé par
test d'existence (dégradation propre si chart-core absent).

## Accros

Aucun.

## Preuves

- `node --check` OK.
- Serveur DEMO port 5002 : `lot193-runway-card.png` (piste dégradée
  rouge→jaune, hachures ≤ 5 j, chip rouge « J-0 » sur Emploi US (NFP),
  chips J-3/J-5/J-6/J-7 textuels, verdict imminent rouge),
  `lot193-today-1440.png`, `lot193-today-390.png` — envoyées,
  **0 erreur console**.
- SW `td-shell-v156` → `v157` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## Suite

LOT 194 : suivant de TV-CHARTS-INVENTORY.md — sparklines KPI
(Aujourd'hui) OU heatmap secteurs / bandes linéaires (Marchés).
MINI-BILAN 191-195 au lot 195.
