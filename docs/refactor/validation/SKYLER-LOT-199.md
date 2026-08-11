# SKYLER LOT 199 — Tournée TV : barres — la dominante porte sa valeur en chip

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-199` (base : lot 198 fusionné)

## Livré

### `C.bars` (builder partagé) — dominante en évidence

La règle transverse de la tournée (consensus 191, heatmap 194,
staleness 196) appliquée au builder de barres Chart.js, donc héritée
par TOUS les appelants (sensibilité IV Options, barres S+/S/A/B
Portefeuille, leadership Marchés, discipline Journal, movers Système,
recherche Intelligence) :

1. **Barre DOMINANTE** = |valeur| max, calculée seulement s'il y a
   ≥ 2 barres (jamais une dominante inventée sur un singleton) ;
2. elle porte un **liseré appuyé** (couleur pleine, 1.6 px vs 1 px et
   alpha 80 pour les autres) ;
3. et sa **VALEUR en chip pleine couleur** (texte sombre, plugin
   canvas dans la grammaire tvEdgeChip) posée au bout de la barre —
   au-dessus/en-dessous en vertical, à droite/gauche en horizontal,
   bornée à la zone de tracé.

Matière verre des autres barres, survol, axes et formats STRICTEMENT
inchangés. Valeurs réelles uniquement (le chip affiche la donnée du
moteur, formatée par le yFmt de l'appelant).

## Accros

- `#vx-brain-movers` absent de la vue Système en démo (la carte movers
  ne se rend pas sans mouvements) — constat rapporté sans agir, la
  preuve visuelle vient de la sensibilité IV.

## Preuves

- `node --check` OK (chart-core.js).
- Serveur DEMO port 5002, contrat GOOGL ouvert :
  `lot199-iv-card.png` — la barre du choc IV −20 % (pire P&L −23.4 %)
  porte le chip rouge « −23.4 % » et le liseré appuyé, les autres
  restent en verre — **0 erreur console** ; pages Système 1440 + 390.
- SW `td-shell-v162` → `v163` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## Suite

LOT 200 : MINI-BILAN 196-200 + suivant de l'inventaire (price-chart
niveaux, vol cone, discipline Journal — ✔ partiel par héritage à
constater, aires indices, GEX, radar).
