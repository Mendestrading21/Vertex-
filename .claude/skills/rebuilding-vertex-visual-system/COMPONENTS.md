# Vertex Components

## Sommaire
- Principes
- Headers
- KPI
- Cards
- Decision cards
- Scenario cards
- Tables
- Buttons
- Filters
- Inputs
- Badges
- Drawers/modals
- Empty/error states
- Mobile

## Principes
Chaque composant doit avoir un but unique, une hiérarchie stable et des états complets. Préférer une primitive canonique réutilisable à une variante locale.

## Page header
Contenu maximal :
- eyebrow optionnel ;
- titre ;
- sous-titre d’une ligne ;
- fraîcheur/source si utile ;
- 1 à 3 actions/contrôles.

Éviter les énormes hero marketing dans un terminal analytique.

## KPI tile
Anatomie : `label / value / delta / context`.

Exemples :
- `Score Vertex` → `34 / 40` → `S` → `Conviction élevée`.
- `Risque max.` → `-14%` → `Sous invalidation`.
- `Asymétrie` → `1:4.6` → `Probable +52%`.

Ne pas mettre un bouton primaire dans chaque KPI.

## Card standard
Anatomie :
- header : titre + meta/controls ;
- body : 1 contenu principal ;
- footer facultatif : source/fraîcheur/action discrète.

Si le footer contient plus de trois éléments, revoir la carte.

## Decision card
Ordre visuel obligatoire :
1. ticker + nom ;
2. grade + score ;
3. verdict en une phrase ;
4. asymétrie ;
5. catalyseur ;
6. invalidation ;
7. action analytique (`Analyser`, `Comparer`, `Voir options`).

Le verdict doit être compréhensible sans ouvrir la fiche détaillée.

## Scenario card
Présenter pessimiste / probable / exceptionnel dans une grille ou une bande commune. Chaque scénario affiche :
- résultat potentiel ;
- hypothèse déclenchante ;
- horizon ;
- probabilité/confidence si réellement disponible.

Le pessimiste doit être visible sans hover.

## Risk block
Toujours séparer :
- perte planifiée ;
- niveau d’invalidation ;
- événement à risque ;
- concentration/positionnement si pertinent.

Le rouge n’est utilisé que pour le risque réel, pas comme accent décoratif.

## Tables
### Règles
- En-tête sticky si table longue.
- Première colonne sticky seulement si réellement utile.
- Alignement à droite pour nombres.
- `font-variant-numeric: tabular-nums` si possible.
- Row hover subtil.
- Pas de zebra striping fort.
- Actions de ligne dans menu contextuel ou dernière colonne compacte.
- Tri/filtre explicite.

### Mobile
Passer en scroll horizontal contrôlé ou cartes de lignes, selon la tâche. Ne jamais écraser 8 colonnes en 320 px.

## Boutons
### Primary
Une seule action primaire par zone. Violet Vertex, contraste élevé.

### Secondary
Surface/border neutre.

### Ghost
Actions tertiaires, iconiques, menu contextuel.

### Danger
Rouge uniquement pour une action réellement destructive dans l’UI locale. Vertex READONLY : ne jamais créer une action de trading destructive.

### Labels
Verbes directs : `Analyser`, `Comparer`, `Suivre`, `Créer une alerte`, `Ouvrir`, `Exporter`.
Éviter `Click here`, `Learn more`, `View more` génériques.

## Segmented controls / timeframes
Pour 3–6 choix exclusifs courts : `1J 1S 1M 3M 1A` ou vues. Sélection claire. Ne pas utiliser un dropdown si tous les choix tiennent en ligne.

## Filters
- Afficher les filtres les plus utilisés.
- Regrouper les filtres avancés en drawer/popover.
- Montrer le nombre de filtres actifs.
- Bouton `Réinitialiser` seulement si au moins un filtre est actif.

## Inputs
- Label visible sauf recherche évidente.
- Placeholder = exemple, pas remplacement du label.
- États focus/error/disabled.
- Messages d’erreur courts et actionnables.

## Badges
Catégories : grade, statut, fraîcheur, type, timeframe.
Ne pas utiliser des badges pour de simples mots qui pourraient être du texte secondaire.

## Tooltips
Réservés à : icône seule, métrique spécialisée, abréviation non évidente. Un tooltip ne doit pas cacher une information critique.

## Drawer
Pour détails secondaires, explication d’un graphique, filtres avancés, actions contextuelles. Largeur desktop 360–520 px selon contenu.

## Modal
Seulement pour tâche qui exige une décision explicite. Éviter modal pour simple lecture.

## États
### Loading
Skeleton ressemblant au contenu final, pas spinner plein écran.

### Empty
Titre court + cause + prochaine action si possible.
Exemple : `Aucune opportunité S/S+` / `Les filtres actuels ne retournent aucun dossier.`

### Stale
Afficher âge/source et conserver la dernière valeur connue si le produit l’autorise.

### Error
`Impossible de charger les données` + `Réessayer` + chemin Système si la connexion est en cause.

### Demo/offline
Toujours explicites, jamais confondus avec live.

## Cards imbriquées
Autoriser seulement si la sous-carte représente une entité distincte. Sinon utiliser lignes, separators, background bands ou mini-panels.

## Mobile action bar
Sur fiche Analyse : maximum 3 actions prioritaires + overflow. La barre ne doit jamais proposer d’exécution d’ordre.
