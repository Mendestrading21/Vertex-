# Vertex Charts — TradingView-grade grammar

## Sommaire
- Principe décisionnel
- Contrat obligatoire
- Palette
- Types de graphiques
- Price chart
- Multi-series
- Bar charts
- Donuts
- Heatmaps
- Options
- Annotations
- Tooltips
- Axes
- États
- Mobile
- Anti-patterns

## Principe décisionnel
Un graphique n’existe que pour répondre à une question. Avant de coder : écrire la question et la conclusion attendue. Si une table répond mieux, utiliser une table.

## Contrat obligatoire de chaque graphique
Conserver le contrat de `chart-core.js` :
- titre ;
- question ;
- conclusion ;
- timeframe ;
- unité ;
- source ;
- timestamp/fraîcheur ;
- légende si nécessaire ;
- état loading/empty/stale/error ;
- aide `Comprendre ce graphique` quand la lecture n’est pas triviale.

## Grammaire TradingView à intégrer
S’inspirer des qualités fonctionnelles de TradingView sans copier son produit :
- grille sombre ultra discrète ;
- ligne/prix primaire nette ;
- dernier prix clairement marqué ;
- crosshair au survol ;
- tooltip compact collé à la donnée ;
- extrema utiles ;
- niveaux horizontaux annotables ;
- zones de risque/support/résistance ;
- projections visuellement distinctes du réalisé ;
- labels de fin de série plutôt qu’une légende éloignée ;
- zoom/timeframe cohérent si supporté par les données ;
- aucune décoration sans information.

## Palette graphique
- Série principale : violet Vertex.
- Comparaison technique : cyan.
- Benchmark : gris clair/neutre.
- Positive : vert.
- Negative : rouge.
- Warning/threshold : jaune.
- Options/volatilité secondaire : violet profond.

Maximum 5–6 séries réellement distinctes. Éviter arc-en-ciel.

## Price / performance chart
Préférer :
- ligne monotone ou candlesticks selon besoin ;
- area gradient très faible ;
- last value dot + label ;
- crosshair ;
- extrema seulement s’ils sont décisionnels ;
- benchmark en ligne plus fine/moins saturée ;
- événements via annotations discrètes.

Ne jamais transformer une série de prix en courbe lissée qui invente des valeurs intermédiaires trompeuses.

## Candlesticks
Utiliser pour Analyse lorsque OHLC est réellement utile. Couleurs positive/négative, corps lisibles, volume séparé si disponible. Ne pas utiliser pour un KPI de tendance simple.

## Multi-series line
- Une série primaire plus épaisse.
- Comparaisons plus fines.
- Labels en bout de ligne si possible.
- Éviter légende distante obligeant des allers-retours visuels.
- Si > 4 séries, envisager small multiples ou sélection interactive.

## Bars
Idéal pour classement, contribution, surprise, flux, P&L par position, facteur. Trier lorsque l’ordre porte du sens. Utiliser positif/négatif selon signe, pas une couleur arbitraire par barre.

## Horizontal bars
Préférer pour labels longs et ranking. La valeur dominante peut recevoir une annotation/chip compacte.

## Donut
Seulement pour composition simple ≤ 5 catégories. Afficher la catégorie dominante et sa part au centre. Pour plus de catégories, préférer barres.

## Heatmap
Pour matrice, secteurs, calendrier ou intensité. Couleur = magnitude/sens ; texte lisible ; pas de heatmap si les valeurs absolues exactes sont plus importantes qu’un pattern.

## Treemap
Seulement pour poids + performance simultanés et si la hiérarchie de surface est utile. Éviter sur mobile si les labels deviennent illisibles.

## Scatter
Pour relation entre deux variables : qualité vs valorisation, rendement vs risque, IV vs liquidité. Mettre quadrants/références si cela aide une décision.

## Options
### Payoff
- spot courant ;
- strike ;
- break-even ;
- zone gain/perte ;
- résultat à échéance clairement distingué de P&L actuel.

### Scenarios
Tracer pessimiste/probable/exceptionnel avec labels cohérents avec les cartes de scénario. Ne jamais masquer la perte maximum.

### Theta
Montrer l’érosion dans le temps avec horizon et hypothèses visibles.

### IV sensitivity
Comparer IV actuelle, compression/expansion et impact estimé sans présenter une estimation comme résultat certain.

### Vol surface
Seulement si données suffisantes et lecture exploitable ; sinon état honnête.

## Projection vs réalisé
Obligatoire : motif hachuré, opacité ou style de ligne distinct pour toute estimation. Ne jamais utiliser la même matière que l’historique réel.

## Annotations
Types :
- événement earnings/Fed/catalyseur ;
- niveau technique ;
- entrée théorique/observée ;
- invalidation ;
- objectif ;
- support/résistance ;
- gap.

Limiter le nombre visible. Regrouper si collisions.

## Niveaux
Une ligne horizontale doit porter un label court sur le bord droit : `Invalidation 172`, `Break-even 205`, `Résistance 221`. La couleur suit son sens.

## Tooltip
Doit afficher seulement : date/x, valeur principale, comparaisons essentielles. Formatage financier cohérent. Pas de texte pédagogique long dans tooltip.

## Axes
- Maximum ~6 ticks Y.
- Unité visible dans le shell ou l’axe, pas répétée partout.
- Dates adaptatives selon timeframe.
- Grille faible contraste.
- Éviter décimales inutiles.

## Freshness
Live/delayed/stale/demo/offline/missing visible au niveau de la carte graphique.

## Mobile
- Hauteur 280–340 px pour graphique principal.
- Réduire ticks et annotations.
- Crosshair tactile si supporté.
- Contrôles timeframe scrollables ou compacts.
- Légende sous le graphe seulement si indispensable.

## Performance
Détruire les instances Chart.js lors du teardown. Ne pas recréer inutilement les charts à chaque micro-interaction. Préserver `C.mount`/registry et les primitives canoniques.

## Anti-patterns
- Graphique 100 px de haut avec 12 séries.
- Donut à 9 catégories.
- Courbe sans source/date.
- Vert pour série principale juste parce que le marché monte.
- Projection pleine identique à l’historique.
- Tooltip géant.
- Gradient opaque.
- Axe avec précision factice.
- Faux points générés pour rendre la courbe plus jolie.
