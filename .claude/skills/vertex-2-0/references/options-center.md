# Centre Options

Contrat de présentation uniquement : afficher et composer les capacités existantes ; ne pas créer les données, moteurs, Greeks, scénarios, calculs, états ou persistance décrits.

## Mission

Explorer une exposition optionnelle avec données, volatilité, liquidité, scénarios et risque complets, sans jamais préparer ou transmettre un ordre.

## Chaîne canonique

Sélecteur de sous-jacent et échéance ; quote/fraîcheur ; CALL à gauche, strike au centre, PUT à droite ; mode empilé tablette. Colonnes disponibles : bid, ask, mid, last, spread absolu/%, volume, OI, IV, delta, gamma, theta, vega, valeur intrinsèque/extrinsèque, breakeven, DTE, multiplicateur, qualité et liquidité.

Filtres : DTE, moneyness, type, delta, spread, volume, OI, IV, liquidité et événements. ATM neutre, headers sticky, colonnes configurables, virtualisation/pagination, navigation clavier.

## Détail contrat

Drawer avec source du mark, qualité, spread, Greeks, IV, événement, payoff, sensibilité spot/temps/IV, breakeven, gain/perte max si mathématiquement défini, limites et impact portefeuille. Toute valeur indisponible reste absente.

## Volatilité et marché

- term structure ;
- smile/skew ;
- volume/OI par strike ;
- IV vs historique/percentile si fourni ;
- expected move uniquement depuis données/moteur ;
- lecture cher/neutre/bon marché uniquement si canonique.

## Scénarios

Payoff, matrice spot × temps, theta, sensibilité IV, comparaison de contrats et simulation multi-jambes analytique. Aucun bouton achat/vente, aucun ticket, aucun export broker.

Le bouton sûr `Simuler cette position` ouvre `/simulator` avec le contrat et les hypothèses visibles, uniquement à partir des données déjà reçues. Le simulateur ne complète jamais une Greek, une IV, un mark ou un multiplicateur absent.

## Widgets prioritaires

- `OptionChainGrid` : CALL / strike / PUT, ATM neutre et cellules de liquidité sobres ;
- `ContractDrawer` : provenance, spread, Greeks disponibles, événement et limites ;
- `TermStructure` et `SmileSkew` : lignes précises avec table équivalente ;
- `OpenInterestByStrike` et `GexMap` : barres signées, zéro et murs seulement s'ils viennent d'un moteur existant ;
- `Payoff` et `SpotTimeHeatmap` : scénarios explicitement étiquetés ;
- `DataLedger` : source, heure, couverture et données absentes.

S'inspirer des exemples retenus dans `trading-widget-catalog.md`, sans copier les dépôts sans licence ni leur logique transactionnelle.

## Livre Options

Positions réelles séparées des contrats candidats : coût total, multiplicateur, mark, P&L, Greeks, échéance, événement, concentration, scénario et fraîcheur. Réconcilier les marks et signaler les écarts.
