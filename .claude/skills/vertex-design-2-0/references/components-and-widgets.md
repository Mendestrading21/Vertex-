# Système de composants et widgets

## Principe

Un composant existe pour encoder un comportement et une hiérarchie réutilisables. Une classe créée uniquement pour donner un autre rayon ou une autre couleur à une page est une dette.

## Primitives canoniques

- `AppShell`, `Sidebar`, `Topbar`, `PageHeader`, `Subnav`, `FilterBar`.
- `Surface`, `Card`, `HeroCard`, `Section`, `Divider`.
- `MetricCard`, `MetricStrip`, `StatusBadge`, `FreshnessBadge`, `SourceStamp`.
- `Button`, `IconButton`, `SegmentedControl`, `Tabs`, `Chip`, `SearchField`.
- `DataTable`, `RowActions`, `Pagination`, `ColumnPicker`, `DetailDrawer`.
- `ChartCard`, `InsightPanel`, `DecisionPanel`, `RiskPanel`, `ScenarioPanel`.
- `LoadingState`, `EmptyState`, `PartialState`, `StaleState`, `OfflineState`, `ErrorState`.
- `Modal`, `Drawer`, `Toast`, `Tooltip`, `CommandPalette`.

Faire converger `vx-kpi`, `vx-metric`, `vx-stat` et `vx-stat-xl` vers une seule famille `MetricCard`. Faire converger les redéfinitions de `vx-card` vers une primitive et des variantes documentées.

## Contrat d'un widget

Tout widget de données expose conceptuellement :

```text
title · question · value/content · conclusion · source · timestamp
freshness · state · actions · limits · density
```

Un widget ne calcule pas un verdict métier dans l'UI. Il présente la sortie canonique et son contexte.

## Variantes autorisées

- Surface : `subtle`, `card`, `elevated`, `selected`, `critical`.
- Densité : `compact`, `comfortable`, `dense` ; chaque mode modifie réellement padding, hauteur de ligne et détails secondaires.
- Ton : `neutral`, `positive`, `negative`, `warning`, `option`. Le ton vient de la donnée, jamais de la page.
- Taille : dictée par la grille et le contenu ; éviter des hauteurs fixes sans raison.

## Tables

- Première colonne et colonne de décision restent visibles selon la largeur.
- Chiffres alignés à droite, chiffres tabulaires, unités dans le header.
- Tri actif clairement indiqué en argent ; gain/perte conserve signe et couleur.
- Hover neutre ; sélection argentée, jamais verte.
- Colonnes secondaires masquables ; détail complet dans drawer ou expansion.
- Loading par lignes skeleton ; empty avec cause et action éventuelle.

## Contrôles

- Bouton principal neutre argent/graphite. Vert seulement pour confirmer un état réellement positif, rouge seulement pour une action destructive ou un risque explicite.
- Chaque icône seule possède un nom accessible et un tooltip.
- Le focus clavier est plus visible que le hover.
- Cible tactile au moins 40 px lorsque l'interface passe en mode tablette/mobile.

## États

- Loading : squelette de la forme attendue, jamais une fausse donnée.
- Empty : ce qui manque, pourquoi, et comment l'obtenir si possible.
- Partial : ce qui est disponible et ce qui manque.
- Stale/delayed : âge réel et conséquence sur la lecture.
- Offline : dernière donnée connue clairement datée, ou aucune donnée.
- Demo : badge explicite provenant du serveur.
- Error : service concerné, retry sûr, aucun secret.

## Interdictions

- cartes imbriquées sans nécessité ;
- rangées de badges multicolores décoratifs ;
- icônes différentes pour la même action ;
- style inline répété ;
- contenu factice pour remplir une composition ;
- boutons qui ressemblent à du texte ou texte qui ressemble à un bouton ;
- hover qui déplace la mise en page.

