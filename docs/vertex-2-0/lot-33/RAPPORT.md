# Lot 33 — Refonte visuelle : tout mettre droit en mode peuplé (RAPPORT)

Date : 2026-08-28 · Captures avant/après dans ce dossier

## Quatre défauts mesurés au navigateur peuplé, corrigés à la racine

1. **Scorecard Portefeuille boiteuse** : sans marques (pas de jauge), les
   4 tuiles KPI tombaient dans la colonne `auto` (~190 px) d'une grille
   figée `auto minmax(0,1fr)`, laissant la moitié droite VIDE. La grille
   se déclare selon la présence réelle de la jauge → tuiles pleine
   largeur (`portfolio-fix.png`).
2. **Le pied des primitives saignait** : treemap/waterfall ajoutent tête
   et pied DANS un hôte dimensionné pour le SVG seul (260 px figés,
   294 px de contenu) — « Composition du capital » passait SOUS la
   légende du treemap. Corrigé chez le propriétaire (chart-core) : la
   primitive libère la hauteur figée, le SVG porte sa hauteur en pixels,
   le conteneur suit son contenu. Vérifié : 294 = 294, zéro chevauchement.
3. **Scénarios collés** (« Pessimiste-4.2 %cible 189,63 ») : le motif
   `.vx-scenario*` n'a JAMAIS eu de base hors de la variante
   `.an-decision-grid` — même la feuille morte ne portait qu'elle. Base
   posée dans la couche finale (§31) : libellé | valeur sémantique à
   droite, note en pleine largeur (`scenarios-fix.png`).
4. **Prime « — » à côté de son propre montant** : la chaîne affichait
   PRIME — et RISQUE MAX 3 443 $ sur la même ligne, alors que le coût
   par contrat EST la prime × 100. Dérivation exacte (34,43 mesuré) —
   une conversion d'unité, jamais une estimation.

## Vérifications mobiles (390 px, peuplé)

Puces de régime empilées (libellé au-dessus de la valeur), « Courbe des
taux inversée » en français, cartes Top structurées (jauge, rails
stop/entrée/objectif) — captures jointes.

Bancs : 4 nés rouges → verts. SW **v275**.
Suite : **4422 passés · 152 ignorés · 0 échec**.
