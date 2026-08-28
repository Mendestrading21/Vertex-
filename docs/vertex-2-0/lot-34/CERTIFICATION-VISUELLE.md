# Lot 34 — Certification visuelle de la refonte (mode PEUPLÉ)

Date : 2026-08-28 · SHA : main après #848

## Certificat

**12 pages × 7 largeurs (390/430/768/1024/1280/1440/1600) = 84
combinaisons, EN MODE PEUPLÉ (DEMO=1, scan réel de 20 titres) :
0 débordement horizontal · 0 erreur console · 0 échec de navigation.**

Le certificat du lot 21 ne couvrait que le mode dégradé ; celui-ci couvre
le mode qui révèle (données, graphiques, tables, cartes remplies).

## Ce que la campagne visuelle (lots 29→33) a redressé, au total

| Défaut mesuré | Racine | Correctif |
|---|---|---|
| Libellés collés (« Nouveau risqueAutorisé ») | 20 classes rendues sans règle servie | 34 règles rapatriées au mérite (§29) |
| « YIELD_CURVE_INVERTED » à l'écran | jeton moteur brut | SECONDARY_LABEL français |
| Cartes à 95 px (dossier Analyse) | états vides effaçant `vx-col-*` | `_gardeSpan` |
| Question de graphique à 3,84:1 | opacité posée par 3 couches | opacité annulée + gardien anti-opacité |
| Scorecard Portefeuille à moitié vide | grille figée `auto 1fr` sans jauge | grille conditionnelle |
| Pied de treemap sur le bloc suivant | hôte figé pour le SVG seul | primitive libère la hauteur (chart-core) |
| Scénarios fusionnés | motif sans base servie (jamais existé) | base §31 (libellé/valeur/note) |
| Prime « — » à côté de 3 443 $ | mid absent, coût ignoré | dérivation exacte coût/100 |

Plus : a11y Lighthouse **100/100/100** sur les 3 pages corrigées, bundle
CSS (19 requêtes → 1), heading-order h2, cibles tactiles 24 px.

## Vues inspectées à l'œil (captures dans les dossiers de lots)

Aujourd'hui, Calendrier, Marchés (+ régime mobile), Opportunités
(+ cartes mobiles), Analyse/dossier ACN (+ scénarios, chaîne), Options
Structure GOOGL (verdict, payoff, Greeks — capture jointe), Simulateur
(résultats + provenance du prix), Portefeuille (scorecard + treemap),
Suivi, Performance, Vertex IA, Système.

## Ce qui reste par nature hors de ce certificat

Le rendu sur VRAIES données de marché (formes de courbes réelles,
volumes) — même moteurs, mêmes gabarits ; à regarder sur ton poste.
