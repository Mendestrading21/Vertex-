# SKYLER LOT 195 — Tournée TV : équité & drawdown (chips Max/Min) + MINI-BILAN 191-195

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-195` (base : lot 194 fusionné)

## Livré

### Chips Max/Min sur les extrêmes RÉELS (equity & drawdown, Portefeuille)

1. **`chart-core.js` — `C.tvExtremesPlugin(color, yFmt, which)`** :
   nouveau plugin Chart.js qui pose des CHIPS (équivalent canvas du
   tvEdgeChip : fond plein couleur, texte sombre, coins arrondis) sur
   le maximum et le minimum RÉELS de la série — Max au-dessus du
   point, Min en dessous, bornés à la zone de tracé. `which` permet
   de n'afficher qu'un seul extrême. Activation par option
   `extremes: true | 'max' | 'min'` de `C.area` (défaut : inchangé —
   aucun autre graphique n'est modifié sans opt-in).
2. **`equity-chart.js`** : `extremes: true` — le plus haut et le plus
   bas d'équité (les deux chiffres du drawdown) sont désormais lus
   directement sur la courbe, comme les bornes d'un graphique TV.
3. **`drawdown-chart.js`** : `extremes: 'min'` — le chip unique est
   le PIRE drawdown réel de la série (le max vaut 0 par définition).

Arithmétique du drawdown, pilule de dernière valeur, glow, crosshair
et états vides honnêtes (« la courbe se construit au fil des clôtures
déclarées ») STRICTEMENT inchangés.

## Accros

Aucun. Note de preuve : la série d'équité vient de `myTradesEquity`
(localStorage) — vide dans un navigateur neuf. La capture utilise une
série d'exemple SEMÉE LOCALEMENT dans le navigateur de test
(add_init_script), jamais commitée ni servie : la page reste
honnêtement vide sans clôtures déclarées.

## Preuves

- `node --check` OK sur les 3 fichiers.
- Captures : `lot195-equity-card.png` (chips « Max 11510 » au sommet,
  « Min 10040 » au creux + pilule dernière valeur), `lot195-drawdown-card.png`
  (chip « Min −4 % » au pire drawdown), pages 1440 + 390 — envoyées,
  **0 erreur console**.
- SW `td-shell-v158` → `v159` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## MINI-BILAN 191-195

Voir STATUS.md — tranche entièrement consacrée à la TOURNÉE GRAPHIQUE
TV : 5 lots, PR #224 → #228, SW v154 → v159, suite stable 2461/2,
9 signatures livrées (consensus, aura, payoff hachuré, runway,
heatmap, treemap-chips, equity/drawdown-chips) + correctif structurel
__VXVOCAB au shell.

## Suite

LOT 196 : suivant de TV-CHARTS-INVENTORY.md — GEX / scénarios options,
discipline Journal, aires indices, barres leadership, price-chart
niveaux, sparklines KPI, staleness Système.
