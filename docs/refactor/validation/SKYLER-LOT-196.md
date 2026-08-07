# SKYLER LOT 196 — Tournée TV : fraîcheur des données (Système) — dominante en évidence

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-196` (base : lot 195 fusionné)

## Livré

### Staleness par domaine alignée sur la grammaire TV (system_page, vue Données)

Le lot 142 avait déjà les barres de staleness RELATIVE (échelle = âge
max connu). Le lot 196 y ajoute la règle « dominante en évidence »
commune à toute la tournée (consensus 191, heatmap 194) :

1. **Le domaine le PLUS RASSIS** (âge max connu, calculé uniquement
   s'il y a ≥ 2 âges connus — jamais un « pire » inventé sur un
   singleton) devient la dominante de la vue :
   - sa **tuile** de la heatmap de fraîcheur porte un liseré appuyé
     (1.6 px vs 1 px) dans sa couleur d'état ;
   - dans la table, son **âge passe en CHIP pleine couleur** (fond de
     l'état, texte sombre `--vx-graphite-850`, gras 800) — la
     grammaire tvEdgeChip, à côté de sa barre pleine.
2. Les autres domaines restent adoucis (barre + texte simples) ;
   domaine sans âge → pas de barre ni chip (honnêteté du lot 142
   préservée).

Comptes et âges STRICTEMENT réels (payload `/api/live/status`), aucun
seuil inventé, états `frais/différé/hors ligne` inchangés.

## Accros

Aucun. (Première tentative d'édition rejetée — ancre textuelle
incomplète sur le template multi-lignes ; repris en deux éditions
exactes, aucun impact.)

## Preuves

- Import du module + `render()` OK ; le gardien de syntaxe JS inline
  (lot 182) couvre la page dans la suite.
- Serveur DEMO port 5002 : `lot196-fresh-card.png` — « companies »
  (20 952 min, hors ligne) porte le chip rouge et la tuile liserée,
  les domaines à 22 s restent adoucis ; `lot196-system-1440.png`,
  `lot196-system-390.png` — envoyées, **0 erreur console**.
- SW `td-shell-v159` → `v160` + 5 gardiens de version.
- Suite complète : **2461 passed / 2 skipped**.

## Suite

LOT 197 : suivant de TV-CHARTS-INVENTORY.md — GEX / scénarios / théta /
IV options, sparklines KPI, barres leadership, price-chart niveaux,
radar, vol cone, barres S+/S/A/B, discipline Journal. Prochain
mini-bilan au lot 200.
