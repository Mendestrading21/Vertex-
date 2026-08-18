---
name: rebuilding-vertex-visual-system
description: Reconstruit l’interface Vertex page par page avec le système Signal OS : shell, navigation, cartes, widgets, tableaux, icônes, micro-copy, graphiques de type terminal/TradingView, responsive et validation. Utiliser pour toute création, refonte, audit ou correction UI/UX de Vertex, sans modifier les moteurs financiers ni introduire d’exécution d’ordre.
---

# Rebuilding Vertex Visual System

## Mission
Transformer Vertex en terminal d’investissement premium, dense mais simple, lisible en moins de 10 secondes, cohérent de bout en bout et immédiatement identifiable.

La cible n’est pas « joli ». La cible est : **décision plus rapide, risque plus visible, information plus hiérarchisée, interface plus calme**.

Chaque écran doit répondre dans cet ordre :
1. Quel est le signal ?
2. Pourquoi maintenant ?
3. Quelles preuves le soutiennent ?
4. Quel est le risque maximum ?
5. Quelle asymétrie est disponible ?
6. Qu’est-ce qui invalide la thèse ?
7. Quelle action analytique vient ensuite ?

Vertex reste READONLY. Ne jamais créer de chemin d’achat, vente, transmission, modification ou annulation d’ordre.

## Avant toute modification
Lire seulement les références nécessaires à la tâche, toutes accessibles directement depuis ce fichier :

- [VISUAL_SYSTEM.md](VISUAL_SYSTEM.md) — identité, palette, typographie, espaces, surfaces, icônes, densité.
- [COMPONENTS.md](COMPONENTS.md) — primitives UI, cartes, KPI, tableaux, boutons, badges, formulaires, drawers, modales.
- [CHARTS.md](CHARTS.md) — grammaire graphique Vertex + TradingView, choix de graphiques, annotations, tooltips, états.
- [COPY.md](COPY.md) — micro-copy, vocabulaire, titres, labels, décisions, textes interdits.
- [PAGES.md](PAGES.md) — spécification des 8 espaces et ordre de reconstruction.
- [WORKFLOW.md](WORKFLOW.md) — procédure exacte audit → design → code → tests → validation.
- [VALIDATION.md](VALIDATION.md) — Definition of Done, matrices desktop/mobile, tests et contrôle visuel.
- [REPO_MAP.md](REPO_MAP.md) — fichiers canoniques et zones à ne pas casser.

Lire aussi `docs/design/VERTEX_SIGNAL_OS.md` lorsque la modification touche la philosophie globale ou la hiérarchie décisionnelle.

## Doctrine de design

### 1. Une interface, pas un assemblage de widgets
Les cartes ne doivent jamais ressembler à des blocs indépendants achetés sur dix templates différents. Toute page utilise la même grammaire de rayons, bordures, ombres, espacements, titres, contrôles et états.

### 2. La hiérarchie gagne contre la quantité
Ne pas afficher dix KPI avec le même poids. Chaque zone choisit :
- 1 information primaire ;
- 2 à 4 preuves secondaires ;
- 1 risque ou invalidation ;
- 1 action analytique.

### 3. Le texte doit être plus court que le calcul
Tout texte UI doit être supprimé, raccourci ou déplacé dans une aide si l’utilisateur peut comprendre sans lui.

### 4. Couleur = sens
- Violet Vertex : identité, sélection, série primaire, niveau premium.
- Vert : résultat favorable / validation / gain réel.
- Rouge corail : risque / perte / invalidation.
- Jaune : attente / prudence / donnée à surveiller.
- Cyan : comparaison ou couche technique.
- Blanc/gris : structure, données neutres, benchmark.
Ne jamais utiliser le vert comme décoration de marque.

### 5. Les chiffres sont l’interface
Un chiffre important doit être grand, bien aligné, accompagné de son unité et de son contexte. Ne jamais compenser une mauvaise hiérarchie par des illustrations décoratives.

### 6. Dense, jamais tassé
Vertex est un terminal. La densité est autorisée, mais chaque bloc doit respirer. Préférer des gaps constants, des lignes de séparation fines et une structure de grille stable plutôt que des marges arbitraires.

### 7. Un seul shell
Navigation, recherche, command palette, compte, état des connexions et actions universelles restent au même endroit sur toutes les pages.

### 8. Responsive réel
Ne pas simplement réduire les dimensions. Mobile doit re-prioriser : signal, score, risque, scénario, action. Les données secondaires passent dessous ou en drawer.

## Règles d’exécution obligatoires

### Quand une page est demandée
1. Ouvrir son code actuel et ses dépendances.
2. Inventorier tout ce qui est affiché : sections, widgets, contrôles, tableaux, graphiques, états, actions.
3. Marquer chaque élément `KEEP`, `MERGE`, `MOVE`, `REWRITE`, `REDESIGN`, `DELETE`.
4. Définir la nouvelle hiérarchie avant le CSS.
5. Identifier les primitives communes déjà existantes.
6. Modifier d’abord les primitives si la correction doit bénéficier à plusieurs pages.
7. Reconstruire la page en sections clairement ordonnées.
8. Simplifier toute la micro-copy visible.
9. Refaire les graphiques selon [CHARTS.md](CHARTS.md).
10. Vérifier les états honnêtes : loading, empty, stale, error, demo, offline.
11. Tester interactions, liens, clavier et responsive.
12. Exécuter la checklist [VALIDATION.md](VALIDATION.md).
13. Ne passer à la page suivante que lorsque la page courante est validée.

### Quand un composant est demandé
Ne pas patcher localement avant de vérifier si le comportement doit être canonique. Si plusieurs pages utilisent le même pattern, le corriger dans la primitive commune.

### Quand un graphique est demandé
Toujours commencer par la question décisionnelle. Choisir ensuite le type de graphique. Ne jamais partir d’un type de graphique « parce qu’il est beau ».

### Quand un texte est demandé
Appliquer [COPY.md](COPY.md). Le label doit décrire l’objet ou l’action, pas expliquer le logiciel.

## Architecture visuelle cible

### Shell
- Sidebar sombre, stable, peu large, icônes monolignes cohérentes.
- Navigation primaire limitée aux 8 espaces canoniques.
- Élément actif très lisible, sans glow excessif.
- Topbar avec recherche globale dominante mais calme.
- Command palette accessible clavier.
- État IBKR / données visible sans prendre le dessus.

### Page
Chaque page suit :
`page-header → signal-strip/hero → primary-grid → evidence-grid → detail/table → contextual-actions`

Le header contient au maximum : titre, sous-titre court, fraîcheur, 1 à 3 contrôles utiles.

### Carte
Une carte doit avoir une fonction unique : résumer, comparer, expliquer, surveiller ou agir. Si une carte fait quatre choses, la découper.

### KPI
`label → valeur → delta/contexte → micro-indicateur éventuel`.
Pas de paragraphes dans un KPI.

### Widget de décision
Afficher dans cet ordre :
`Ticker → grade → score → verdict → asymétrie → catalyseur → invalidation`.
Les détails avancés restent accessibles sans encombrer le premier regard.

### Scénarios
Toujours présenter :
- Pessimiste : perte potentielle / condition.
- Probable : gain potentiel / condition.
- Exceptionnel : convexité / condition.
Ne pas donner le même poids visuel aux trois si leurs probabilités diffèrent.

## Grades Vertex
- `S+` : opportunité exceptionnelle, priorité visuelle maximale.
- `S` : très forte opportunité.
- `A` : opportunité solide.
- `B` : observation / petite taille.
Le grade est un raccourci de décision, pas une décoration. Toujours l’accompagner du score ou du motif principal quand l’espace le permet.

## Icônes
- Une seule famille visuelle.
- Stroke cohérent, géométrie simple, pas d’emojis comme icônes produit.
- 16–18 px dans navigation/contrôles, 20–24 px pour points focaux.
- Icône seule uniquement si le sens est universel ou si un tooltip/aria-label existe.
- Ne jamais mélanger pictogrammes remplis, outline, multicolores et emojis dans la même surface.

## États et feedback
- Hover discret : bordure/surface, pas translation spectaculaire.
- Focus visible obligatoire.
- Pressed/selected explicite.
- Skeleton de même géométrie que le contenu final.
- Empty state utile et court.
- Erreur : cause compréhensible + action possible.
- Stale : montrer la dernière donnée connue et son âge, sans la faire passer pour live.

## Ce qu’il faut supprimer activement
- Glow permanent.
- Bordures lumineuses sur toutes les cartes.
- Gradients gratuits.
- Glassmorphism lourd.
- Cartes imbriquées sans raison.
- Titres répétitifs (`Overview`, `Overview of...`, `Your...`).
- Légendes de graphiques qui répètent l’évidence.
- Boutons `View more` partout.
- Trois variantes différentes du même filtre.
- Décorations ne portant aucune information.
- Couleurs multiples pour des catégories arbitraires.
- Paragraphes explicatifs visibles en permanence.

## Qualité du code
- Favoriser variables/tokens et composants existants.
- Aucun style inline nouveau sauf valeur réellement dynamique indispensable.
- Aucun hex éparpillé si un token existe.
- Aucun composant dupliqué pour changer seulement le look.
- Aucun nouveau handler mort.
- Aucun `console.log` de debug livré.
- Aucun réseau ajouté dans la couche purement visuelle.
- Aucun calcul financier déplacé dans le navigateur pour faciliter le rendu.

## Contrat de sortie d’une tâche
À la fin d’une refonte, produire un mini bilan dans le commit/PR :
- page ou composant refait ;
- structure supprimée/fusionnée ;
- nouveaux patterns communs ;
- tests exécutés ;
- responsive vérifié ;
- dette restante explicite.

Ne jamais écrire « terminé » si un test échoue, un breakpoint n’a pas été vérifié ou une interaction reste simulée.
