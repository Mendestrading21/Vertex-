# Lot 29 — Vérification PEUPLÉE (mode démo réel) et défauts révélés (RAPPORT)

Date : 2026-08-28

## La découverte qui ouvre le lot

La « réserve d'environnement » de l'audit (vues peuplées invérifiables sans
réseau) était FAUSSE en partie : le mode démo existe précisément pour cela,
mais la variable est `DEMO=1` (ou `NO_IBKR=1`) — pas `VERTEX_DEMO`, que
toutes mes vérifications précédentes utilisaient. Avec `DEMO=1` : scan
synthétique de 20 titres, zéro réseau requis. La réserve est LEVÉE.

## Mesures peuplées

- 12 pages × 2 largeurs (1600/390), données réelles de scan démo :
  **24/24 sans erreur console ni débordement** ; bannière « Mode DÉMO —
  données synthétiques, clairement identifiées » présente sur les vues de
  données.
- Opportunités : screener 20 titres, nuage avantage × proba, entonnoir
  réel (20→…→1) avec « Premier scan — pas encore de comparaison » (delta
  lot 12 VISIBLE), carte secteur × statut, donut des verdicts, cartes Top.
- Marchés : régime peuplé (6 dimensions), série de référence argent,
  leadership sectoriel. Correctif lot 17 (médiane « — ») vivant.

## Défauts RÉVÉLÉS par le mode peuplé (invisibles en mode dégradé) — corrigés

1. **20 classes orphelines rendues sans règle servie** : mesure DOM
   automatisée sur les 12 pages peuplées — vx-mk-chip(s),
   vx-mk-regime-*, vx-mk-lead-* (Marchés), an-identity/main-column/
   scorecard-note (Analyse), vx-greek(s), vx-scenario-* (Options).
   Effet le plus visible : « Nouveau risqueAutorisé », « Confiance42 % »
   — libellés collés aux valeurs. → **34 règles rapatriées** au mérite
   (§29 de vertex-2-0.css), jetons neon remplacés, zéro glow. Vérifié en
   direct : puces en colonne, identité en grille.
2. **Jeton moteur anglais brut** : « aussi YIELD_CURVE_INVERTED » dans la
   carte régime. → `SECONDARY_LABEL` (5 signaux secondaires en français,
   repli honnête pour un jeton inconnu). Vérifié : « Courbe des taux
   inversée ».
3. **États vides écrasant leur colonne** (dossier Analyse) : 4 chemins
   remplaçaient `host.className`, effaçant `vx-col-*` → cartes à 95 px
   (« Chaîne — meilleurs contrats », quadrant, trimestres). → helper
   `_gardeSpan` unique. Vérifié : 1312/500/869 px.

Service worker **v271**. Bancs : 8 nés rouges → verts.

## Preuves

- Suite complète : **4408 passés · 152 ignorés · 0 échec**.
- Captures peuplées 1600 px des 12 pages : `captures-peuplees/`.

## Enseignement consigné

Les vérifications d'états dégradés NE COUVRENT PAS les chemins peuplés :
toute vérification navigateur future se fait dans LES DEUX modes
(`DEMO=1` et sans données). Ajouté au protocole des rapports.
