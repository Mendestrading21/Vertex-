# VERTEX — Contrat global des graphiques

## But

Chaque graphique répond à une question métier précise. Un graphique sans question explicite doit être supprimé, fusionné ou transformé.

## Style commun

- fond transparent ;
- carte verre gérée par le conteneur, pas le canvas ;
- série principale argent/blanc ;
- benchmark gris ;
- positif vert ;
- négatif rouge ;
- incertain/seuil orange ;
- grilles fines ;
- axes, unités, période et source visibles ;
- tooltip en verre gris ;
- typographie tabulaire ;
- animations courtes ;
- aucun bleu par défaut.

## Composants existants à conserver et normaliser

Le dépôt dispose de `VXCharts`, Chart.js, TradingView Lightweight Charts et de modules dans `vertex/static/vertex/js/charts/`. Consolider ces éléments sans créer une bibliothèque concurrente.

Familles cibles :

- `Sparkline`
- `TrendChart`
- `BenchmarkComparisonChart`
- `CandlestickChart`
- `AllocationTreemap`
- `AllocationDonut`
- `SignedBars`
- `ConvictionBars`
- `RiskGauge`
- `ParticipationGauge`
- `BreadthTrend`
- `DrawdownChart`
- `EquityCurve`
- `MonthlyHeatmap`
- `DistributionHistogram`
- `RotationQuadrant`
- `Waterfall`
- `Funnel`
- `Radar`
- `Flow`
- `OptionsPayoff`
- `OptionsScenarioHeatmap`
- `TermStructure`
- `VolatilitySmile`
- `OpenInterestByStrike`
- `ThetaDecay`
- `IVSensitivity`

## API de carte graphique

```js
{
  title,
  question,
  conclusion,
  source,
  timestamp,
  mode,
  unit,
  period,
  limits,
  legend,
  explain,
  render
}
```

## Règles d’échelle

- ne pas tronquer un axe de manière trompeuse ;
- zéro visible sur barres signées et drawdown ;
- comparaison normalisée sur une base commune ;
- afficher les seuils métier réellement définis ;
- jauge seulement pour score borné avec seuils ;
- donut limité à cinq catégories puis « Autres » ;
- préférer une barre triée pour une comparaison précise.

## États

### Loading
Skeleton de la forme du graphique, aucune fausse courbe.

### Empty
Expliquer la donnée absente et comment l’obtenir.

### Error
Afficher le moteur ou service indisponible.

### Stale
Afficher l’âge réel et l’impact sur la lecture.

### Partial
Afficher les dimensions présentes et manquantes.

## Validation obligatoire

1. Quelle décision aide-t-il à prendre ?
2. Quelle source réelle l’alimente ?
3. Quelle unité ?
4. Quelle période ?
5. Quelle fraîcheur ?
6. Quelle conclusion est lisible en cinq secondes ?
7. Resize et destruction sont-ils propres ?
8. Le fallback fonctionne-t-il ?
9. Les couleurs respectent-elles la sémantique ?
10. Est-il compréhensible au clavier et sur tablette ?
