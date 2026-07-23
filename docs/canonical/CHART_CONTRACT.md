# Vertex — contrat global des graphiques

> **Status: ACTIVE**
> Last verified: 2026-07-22
> Owner: Vertex UI

## But

Chaque graphique doit répondre à une question métier précise. Un graphique sans question explicite doit être supprimé, fusionné ou transformé.

## Style commun

- fond transparent ;
- carte verre gérée par le conteneur, pas par le canvas ;
- série principale violet/prism lorsqu'elle est neutre et mise en avant ;
- benchmark gris ;
- positif vert ;
- négatif rouge ;
- incertain/seuil orange ;
- grilles fines et peu contrastées ;
- axes, unités, période et source visibles ;
- tooltip en verre gris ;
- typographie tabulaire ;
- animations courtes ;
- bleu uniquement comme série de comparaison secondaire et limitée ;
- marque violet/magenta/corail, jamais utilisée comme gain ou perte.

## Composants existants à conserver et normaliser

Le dépôt dispose de `VXCharts`, de Chart.js, de TradingView Lightweight Charts et de modules sous `vertex/static/vertex/js/charts/`. La refonte doit consolider ces éléments, pas créer une seconde bibliothèque concurrente.

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

Toute carte graphique réutilisable doit accepter conceptuellement :

```js
{
  title,
  question,
  conclusion,
  source,
  timestamp,
  mode,        // live | delayed | stale | demo | partial
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
- comparaison de performance normalisée sur une base commune ;
- afficher les seuils métier lorsqu’ils existent réellement ;
- une jauge n’est autorisée que si le score est borné et les seuils sont définis par le moteur ;
- un donut est limité à cinq catégories, puis « Autres » ;
- préférer une barre triée à un donut lorsque la comparaison précise est prioritaire.

## États

### Loading
Skeleton de la forme du graphique ; aucune fausse courbe.

### Empty
Expliquer la donnée absente et comment l’obtenir.

### Error
Afficher le service ou moteur indisponible.

### Stale
Afficher l’âge réel et l’impact sur la lecture.

### Partial
Afficher les dimensions présentes et manquantes.

## Validation obligatoire par graphique

1. Quelle décision aide-t-il à prendre ?
2. Quelle source réelle l’alimente ?
3. Quelle unité ?
4. Quelle période ?
5. Quelle fraîcheur ?
6. Quelle conclusion lisible en cinq secondes ?
7. Le code gère-t-il le resize et la destruction ?
8. Le fallback sans bibliothèque fonctionne-t-il ?
9. Les couleurs respectent-elles la sémantique ?
10. Le graphique reste-t-il compréhensible au clavier et sur tablette ?
