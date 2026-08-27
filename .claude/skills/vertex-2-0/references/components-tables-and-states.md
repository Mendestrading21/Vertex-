# Composants, tables et états

## Bibliothèque canonique

Shell : `AppShell`, `SidebarGroup`, `Topbar`, `GlobalSearch`, `DataHealth`, `AlertCenter`, `CommandPalette`.

Structure : `PageHeader`, `ContextBar`, `DecisionZone`, `Section`, `Surface`, `Card`, `HeroCard`, `SplitPanel`, `Drawer`, `Modal`.

Données : `MetricCard`, `MetricStrip`, `DecisionTrace`, `StatusBadge`, `FreshnessBadge`, `SourceStamp`, `DataTable`, `ChartCard`, `InsightPanel`, `RiskPanel`, `ScenarioPanel`, `EventCard`.

Contrôles : `Button`, `IconButton`, `Tabs`, `SegmentedControl`, `FilterChip`, `SearchField`, `DateRange`, `ColumnPicker`, `SavedView`, `DensityControl`.

États : `Skeleton`, `EmptyState`, `PartialState`, `StaleBanner`, `OfflineState`, `ErrorState`, `DemoBadge`.

## Contrat d'un widget de données

```text
id · title · question · content/value · conclusion
source · timestamp · freshness · mode · limits
actions · density · accessibility summary
```

Le widget ne calcule jamais le verdict. Il consomme un modèle de présentation canonique.

## Tables unifiées

Toutes les grandes tables partagent : colonnes configurables, ordre mémorisé, tri, filtres, recherche, saved views, densité, header sticky, colonnes clés sticky, navigation clavier, sélection neutre, drawer de détail, pagination/virtualisation, export autorisé et états complets.

### Règles

- Chiffres à droite, texte à gauche, statuts centrés seulement si scannables.
- Unité dans l'en-tête ; signe conservé ; décimales cohérentes.
- Au-delà de 100 lignes visibles, virtualiser ou paginer selon la tâche.
- Tablette : colonnes prioritaires + drawer, pas réduction illisible.
- Mobile : cartes-lignes structurées ou vue dédiée ; pas de table entière compressée.
- Couleur + signe/label/icône ; jamais couleur seule.
- Sélection argentée ; vert uniquement si la donnée est positive.

## Tables spécialisées

- Opportunités : score, gates, raisons et impact.
- Chaîne options : CALL/strike/PUT, synchronisation horizontale et ATM.
- Positions : mark/source, coût, poids, P&L, thèse et risque.
- Suivi : type, workflow, verdict, revue et événement.
- Journal : contexte, décision, résultat et erreur.
- Calendrier : temps, type, importance, objets et source.
- Système : source, état, latence, fraîcheur et dernier succès.

## États complets

- Loading : squelette fidèle à la forme attendue.
- Empty : absence réelle, explication et action sûre.
- Missing : dimension non fournie, pas zéro.
- Partial : liste des dimensions présentes/manquantes.
- Delayed/Stale : âge et impact sur la lecture.
- Offline : dernière valeur connue explicitement datée ou aucune donnée.
- Demo : confirmé par le serveur.
- Error : propriétaire/service, retry et corrélation de log sans secret.

## Formulaires et feedback

Labels visibles, aide proche, validation inline, résumé d'erreurs si plusieurs champs, focus ramené au problème, action nommée par son résultat. Toast et bouton utilisent le même vocabulaire. Les actions dangereuses sont rares, explicites et confirmées ; aucune action broker.
