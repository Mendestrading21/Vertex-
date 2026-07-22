# Design system Vertex V4 — aide d'implémentation

Le design system est un ensemble de tokens CSS, classes `vx-*`, primitives
`VXCharts` et formats `VX.fmt.*`. Ce n'est pas une bibliothèque React.

Sources de vérité : `.interface-design/system.md`,
`docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md` et
`docs/vertex-v4/DECISIONS.md`.

## Identité

Obsidian Prism : canvas noir froid, surfaces graphite, marque
violet–magenta–corail, verre localisé et hiérarchie nette. General Sans pour
l'interface, JetBrains Mono pour les valeurs.

## Sémantique

| Rôle | Usage |
|---|---|
| Prism / violet / magenta / corail | marque, sélection, action principale, série neutre mise en avant |
| Vert | gain, amélioration, validation favorable |
| Rouge | perte, baisse, risque, blocage, erreur |
| Ambre | attente, incertitude, retard, prudence |
| Bleu | comparaison secondaire rare |
| Gris | benchmark, structure, donnée neutre |

Une page ne code jamais son propre hex. Un `state_col` moteur est toujours mappé
vers un token sémantique et jamais rendu brut.

## Composants cibles

- `HeroPanel` : message ou graphique majeur.
- `AnalyticalPanel` : graphique, table ou explication principale.
- `MetricTile` : KPI, delta, sparkline.
- `InspectorPanel` : verdict, risque, niveaux et détails.

Toutes les variantes dérivent d'une primitive partagée, avec mêmes rayons,
espacements, états et règles responsive.

## Densité et formats

Confortable pour la décision, standard pour l'analyse, compact pour les tables.
Centraliser devise, %, prix, P&L, market cap, volatilité, greeks et dates dans
`VX.fmt.*`. Distinguer strictement zéro, absent, indisponible, estimation,
retardé et périmé.

## Legacy

`glass.css`, `polish.css`, `control-surface.css`, `cockpit.css`, `premium.css`
et le thème Copper sont des dépendances transitoires. Ne pas les traiter comme
sources de vérité ; suivre `docs/vertex-v4/MIGRATION_MAP.md`.
