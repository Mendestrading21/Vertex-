# Catalogue des widgets trading Vertex

## Principe

Ce catalogue sert à choisir des formes et, exceptionnellement, des briques
visuelles. Une bibliothèque ne devient jamais moteur financier ni source de
vérité. Réutiliser les composants présents, puis adopter une dépendance
seulement dans un lot dédié, mesuré et réversible.

Avant toute dépendance : vérifier version, licence, attribution, maintenance, poids, CSP, vulnérabilités, accessibilité, responsive, lifecycle, fallback, compatibilité Flask/JavaScript et coût de retrait. L'adoption d'une bibliothèque est une décision séparée et documentée.

## Sources auditées

| Source | Licence constatée | Valeur pour Vertex | Règle |
|---|---|---|---|
| [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts) | Apache-2.0 + attribution TradingView | chandeliers, volume, panes, crosshair, plugins heatmap/volume profile/session/tooltips | candidat principal pour prix si déjà présent ou adopté après audit |
| [Perspective](https://github.com/perspective-dev/perspective) | Apache-2.0 | datagrid temps réel, virtualisation, heatmaps, treemaps, streaming | candidat pour tables massives ; mesurer le poids avant adoption |
| [Apache ECharts](https://github.com/apache/echarts) | Apache-2.0 | heatmaps, treemaps, calendriers, Sankey, barres et visualisations riches | candidat pour widgets non-price si le moteur existant ne suffit pas |
| [Plotly.js](https://github.com/plotly/plotly.js) | MIT | surfaces 3D, smile/skew, heatmaps, scénarios scientifiques | candidat ciblé pour volatilité 3D ; bundle partiel obligatoire |
| [Grid.js](https://github.com/grid-js/gridjs) | MIT | table VanillaJS légère, recherche, tri et pagination | candidat simple, mais vérifier sticky/virtualisation/accessibilité requises |
| [D3FC](https://github.com/d3fc/d3fc) | MIT | séries financières très personnalisables, annotations, WebGL | réserve experte ; coût de maintenance supérieur |
| [Lab49 Value Flash](https://github.com/lab49/react-value-flash) | MIT | motif de flash temporaire à la variation | reprendre le motif en JS/CSS natif ; pas React dans Vertex |
| [lightweight-charts-python](https://github.com/louisnw01/lightweight-charts-python) | MIT + obligations du moteur TradingView | multi-pane, toolbox, événements et intégration Python | référence d'intégration ; ne pas ajouter un wrapper sans besoin prouvé |
| [QuantStats](https://github.com/ranaroussi/quantstats) | Apache-2.0 | tear sheet, equity, drawdown, heatmap mensuelle, distributions | formes seulement ; ne pas importer ses calculs dans l'UI |
| [VolVisualizer](https://github.com/GBERESEARCH/volvisualizer) | MIT | surfaces IV, term structure et skew | formes seulement avec sorties Vertex existantes |
| [Ghostfolio](https://github.com/ghostfolio/ghostfolio) | AGPL-3.0 | allocation, portefeuille, holdings, performance | inspiration visuelle uniquement sans revue juridique dédiée |
| [FreqUI](https://github.com/freqtrade/frequi) | GPL-3.0 | tables de trades, états live, P&L et monitoring | inspiration uniquement ; aucun code copié |
| [NQGEX](https://github.com/joshpanebianco-io/gex-options-flow) | aucune licence trouvée | GEX, gamma flip, walls, session drift et data ledger | inspiration conceptuelle uniquement ; aucun code/asset copié |
| [OpenAlgo](https://github.com/marketcalls/openalgo) | aucune licence trouvée lors de l'audit ; produit transactionnel | chaîne, OI, IV smile, vol surface, GEX, payoff | inventaire d'idées seulement ; rejeter toute logique d'ordre |

## Registre canonique des widgets

### Marché et instrument

- `MarketPulseStrip` : indices, taux, devises, matières premières, état et fraîcheur ; deux lignes maximum.
- `PriceWorkbench` : chandeliers, volume, niveaux existants, timeframe, source, crosshair et panes synchronisés.
- `MiniSpark` : tendance secondaire sans axes, avec valeur de début/fin et delta textuel.
- `VolumeProfile` : profil par prix seulement si les bins existent ou sont calculés par un moteur canonique.
- `SessionMap` : pré/post-market, ouvertures et événements en aplats sobres.
- `MarketHeatmap` : secteurs/instruments, surface = poids ou capitalisation réelle, couleur = variation ou score explicitement nommé.
- `BreadthBoard` : avance/baisse, nouveaux plus hauts/bas, participation et régimes disponibles.

### Opportunités et analyse

- `OpportunityRankTable` : ticker, verdict, score, raisons, gates, catalyseur, risque, source et fraîcheur.
- `DecisionTrace` : Données → Moteur → Décision → Portefeuille, uniquement aux cinq emplacements canoniques.
- `ThesisRail` : thèse, contre-thèse, catalyseur, invalidation et prochaine revue.
- `ScenarioFan` : baissier/central/haussier depuis scénarios existants ; aucune interpolation décorative.
- `EvidenceMatrix` : faits, confirmations, contradictions, manques et provenance.
- `DataLedger` : couverture, source, timestamp, âge, qualité et champs absents.

### Options

- `OptionChainGrid` : CALL à gauche, strike au centre, PUT à droite, ATM neutre, sticky, densité et table empilée mobile.
- `ContractDrawer` : mark, spread, volume, OI, IV, Greeks disponibles, événement, payoff, limites et source.
- `TermStructure` : IV/volatilité par échéance, points réels et gaps visibles.
- `SmileSkew` : call/put ou séries canoniques par strike/moneyness.
- `OpenInterestByStrike` : barres opposées avec ATM et zéro explicites.
- `GexMap` : net GEX par strike, gamma flip/walls uniquement fournis par moteur.
- `PayoffDiagram` : expiration et t+0 si existants, zones de gain/perte et breakevens étiquetés.
- `SpotTimeHeatmap` : spot × temps, légende numérique et table équivalente.
- `VolSurface` : surface 3D optionnelle + vues 2D accessibles ; ne jamais lisser sans moteur canonique.
- `GreeksExposure` : delta/gamma/theta/vega disponibles, unités et niveau d'agrégation visibles.

### Simulateur

- `ScenarioComposer` : classe d'actif, instrument, sens, montant/quantité, horizon et hypothèses.
- `PositionPreview` : exposition, unités/contrats, coût/notionnel et données utilisées.
- `ScenarioCompare` : colonnes Actuel/A/B/C avec variations absolues et relatives.
- `OutcomeRange` : plage de résultats issue du moteur, jamais une probabilité inventée.
- `PortfolioImpact` : poids, secteur, devise, concentration, corrélation et risque disponibles.
- `AssumptionLedger` : saisies, valeurs marché, source, timestamp, données manquantes et limites.

### Portefeuille et risque

- `PortfolioSnapshot` : patrimoine déclaré, valeur estimée, cash volontaire,
  exposition, couverture des cotes et dernière saisie manuelle.
- `AllocationTreemap` : hiérarchie actif/secteur/devise/thème ; labels prioritaires et table fallback.
- `ContributionBars` : contributeurs/détracteurs sur une base commune.
- `ExposureMatrix` : actif × dimension, devise × secteur ou position × risque selon données.
- `CorrelationHeatmap` : diagonale, période, échantillon, clusters et table.
- `RiskConcentration` : top positions, HHI ou limites seulement si déjà calculés.
- `PositionTable` : valeurs alignées, colonnes configurables, sticky, drawer et états complets.

### Performance et journal

- `PerformanceTearsheet` : rendement, benchmark, échantillon, equity et drawdown synchronisé.
- `MonthlyReturnHeatmap` : mois × année, chiffres visibles et palette divergente sobre.
- `RollingMetric` : métrique canonique, fenêtre et minimum d'échantillon explicités.
- `ReturnDistribution` : histogramme, zéro et tails ; aucune courbe théorique inventée.
- `WinLossSequence` : séquence chronologique, durée et population clairement nommées.
- `SetupBreakdown` : table/barres par setup, régime, secteur ou erreur déclarée.
- `JournalTimeline` : décision, exécution déclarée, résultat, notes et pièces liées.

### Calendrier, alertes et système

- `SessionTimeline` : maintenant, prochain, fuseau et importance.
- `CalendarHeatmap` : densité d'événements, pas prévision de volatilité.
- `AlertRail` : sévérité, cause, objet, source, timestamp et action sûre.
- `SourceHealthGrid` : source, couverture, latence, fraîcheur et statut.
- `ValueFlash` : flash tonal 300–600 ms sur valeur réellement mise à jour ; pas de glow permanent, pas de son, reduced motion respecté.

## Astuces de terminal premium

- Lier crosshair, période et sélection entre graphiques comparables sans modifier leurs données.
- Conserver une `CompareTray` pour épingler jusqu'à trois instruments, contrats ou scénarios.
- Ouvrir le détail en drawer sans perdre filtres, scroll ni sélection.
- Afficher la provenance au survol puis en clair dans le DataLedger.
- Utiliser progressive disclosure : conclusion d'abord, preuves ensuite, méthode en profondeur.
- Mémoriser densité, colonnes et vue uniquement avec les mécanismes existants.
- Proposer des raccourcis clavier découvrables pour recherche, période, drawer et retour.
- Afficher `ce qui a changé` depuis le dernier snapshot seulement si cette donnée existe.
- Synchroniser equity/drawdown, spot/volume et chaîne/volatilité par contexte, pas par recopie.
- Remplacer les gauges décoratives par barres, seuils et valeurs comparables.
- Garder une table jumelle pour chaque graphique important.
- Rendre les états de fraîcheur localement, pas seulement dans la topbar.
- Utiliser le flash de valeur comme événement court, jamais comme couleur persistante.
- Préserver le contexte lorsqu'on passe Analyse → Options → Simulateur → Portefeuille.
- Mettre la conclusion et le risque dans le titre/rail, pas sous le graphique.

## Mapping page → widgets dominants

| Page | Widget dominant | Preuves secondaires |
|---|---|---|
| Aujourd'hui | DecisionTrace + SessionTimeline | MarketPulseStrip, AlertRail, PortfolioSnapshot |
| Calendrier | SessionTimeline / AgendaTable | CalendarHeatmap, filtres, DataLedger |
| Marchés | MarketHeatmap ou BreadthBoard | PriceWorkbench, RankedBars, DataLedger |
| Opportunités | OpportunityRankTable | funnel, MiniSpark, EvidenceMatrix |
| Analyse | PriceWorkbench + ThesisRail | DecisionTrace, ScenarioFan, EvidenceMatrix |
| Options | OptionChainGrid | TermStructure, SmileSkew, GexMap, ContractDrawer |
| Simulateur | ScenarioComposer + ScenarioCompare | Payoff, SpotTimeHeatmap, PortfolioImpact, AssumptionLedger |
| Portefeuille | PortfolioSnapshot + PositionTable | AllocationTreemap, CorrelationHeatmap, ContributionBars |
| Suivi | ReviewTable + AlertRail | SessionTimeline, MiniSpark, DataLedger |
| Performance | PerformanceTearsheet | MonthlyReturnHeatmap, distribution, breakdowns |
| Vertex IA | conversation + DecisionTrace | EvidenceMatrix, DataLedger, historique |
| Système | SourceHealthGrid | jobs, AlertRail, stockage et audit |

## Interdits

- widget purement décoratif sans question ;
- donut ou gauge répété pour remplir une carte ;
- 3D lorsqu'une vue 2D est plus lisible ;
- cellule rouge/verte sans signe, texte ou valeur ;
- animation continue, ticker illisible ou flash agressif ;
- mélange trades réels, signaux, hypothèses et simulations ;
- import d'un dashboard entier ou d'un framework pour un seul widget ;
- copie de code/asset depuis AGPL, GPL ou dépôt sans licence sans décision juridique explicite ;
- ajout de calcul, signal, niveau, Greek, score, probabilité ou prédiction dans la couche visuelle.
