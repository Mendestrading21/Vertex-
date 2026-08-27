# Système final des graphiques

## Verrouillage

Modifier uniquement le conteneur, le thème, les options de rendu, les labels, tooltips, légendes, interactions visuelles, resize et accessibilité. Ne changer ni calcul, série, source, endpoint, agrégation, timeframe canonique ou valeur.

## Règle de sélection

Un graphique répond à une question. Si la comparaison exacte est prioritaire, préférer table/barres. Si la tendance est prioritaire, ligne. Si le temps et le prix interagissent, heatmap/scénario. Si aucune décision n'est aidée, déplacer le graphique en détail ou le masquer visuellement sans supprimer son moteur.

## Contrat ChartCard

```text
title · question · conclusion · source · timestamp
freshness · mode · unit · period · legend · limits
render · resize · destroy · accessibleSummary · fallback
```

## Familles

- `PriceChart` : chandeliers, volume, niveaux et indicateurs existants.
- `TrendChart` / `BenchmarkChart` : tendance et comparaison normalisée existante.
- `SignedBars` / `RankedBars` : contributions et classements.
- `AllocationTreemap` : composition hiérarchique.
- `Donut` : maximum cinq catégories + Autres.
- `EquityCurve` + `Drawdown` : performance et perte sous zéro.
- `Heatmap` : calendrier, corrélation, scénarios ou distribution dense.
- `BreadthTrend` / `RotationQuadrant` : régime et participation.
- Options : `OptionChainGrid`, `Payoff`, `SpotTimeHeatmap`, `TermStructure`, `SmileSkew`, `OpenInterestByStrike`, `Theta`, `IVSensitivity`.

## Palette et encodage

Série principale argent, benchmark gris, positif vert, négatif rouge, prudence ambre, options violet discret. Le cyan des références est réservé au crosshair, focus ou comparaison technique. Pour séries neutres : luminance, épaisseur, dash, marqueur et motif avant une nouvelle teinte. La hausse d'une métrique n'est pas automatiquement positive.

## Honnêteté

Zéro visible sur barres signées/drawdown ; axes non trompeurs ; base commune pour performances ; seuil seulement depuis moteur ; gaps non reliés silencieusement ; univers partiel explicite ; limites et taille d'échantillon visibles.

## Implémentation visuelle

Une couche de thème lit les tokens CSS. Tooltip, axes, grilles, formatters d'affichage, légendes, registry, ResizeObserver, destruction et reduced motion sont centralisés. Canvas transparent ; surface gérée par ChartCard. Détruire instance/listeners/observers avant recréation sans changer la donnée.

## Accessibilité

Résumé textuel, valeurs clés, légende lisible, contraste, motifs/signes et fallback table pour toute visualisation critique. Les interactions clavier donnent accès au point sélectionné ou à une table équivalente.
