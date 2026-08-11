# SKYLER V2 — ARCHITECTURE CANONIQUE

## Objectif

Skyler est une couche d’orchestration et d’explication. Il n’est ni une seconde base de données, ni un second moteur de décision, ni un calculateur libre piloté par un LLM.

## Pipeline canonique

```text
Sources réelles
  ↓
Normalisation + provenance
  ↓
Moteurs déterministes par domaine
  ↓
SkylerPacket immutable
  ↓
Hard gates
  ↓
Score /40 + scénarios
  ↓
SkylerDecision
  ↓
Rédaction déterministe ou Claude
  ↓
Interface + audit trail
```

## Séparation des responsabilités

### Sources

Exemples : IBKR, yfinance, TradingView, caches locaux, calendrier, news, données déclarées du desk.

Chaque source doit produire une provenance explicite :

- `source_id`
- `as_of`
- `received_at`
- `status`
- `latency_seconds`
- `is_demo`
- `is_estimated`

### Normalisation

La normalisation convertit unités, types, symboles, dates et conventions. Elle ne crée pas de décision.

Règles :

- IV stockée avec unité explicite ;
- prix en devise explicite ;
- rendements en fraction ou pourcentage explicitement typé ;
- DTE entier non négatif ;
- quantité et multiplicateur séparés ;
- timestamps UTC en transport, timezone locale seulement à l’affichage ;
- aucune conversion heuristique silencieuse après la frontière de normalisation.

### Moteurs déterministes

Chaque moteur répond à une question précise et retourne des faits, mesures ou diagnostics.

- `market` : régime, breadth, volatilité, liquidité, leadership ;
- `company` : qualité, croissance, valorisation, révisions ;
- `technical` : tendance, momentum, niveaux, invalidation ;
- `catalysts` : événements, nouveauté, impact, horizon ;
- `anomalies` : écarts statistiques et structurels ;
- `options` : chaîne, volatilité, Greeks, payoff, GEX, liquidité ;
- `portfolio` : exposition, concentration, corrélation, drawdown, compatibilité ;
- `scenarios` : pessimiste, probable, exceptionnel ;
- `calibration` : résultat ex post et qualité probabiliste.

Un moteur ne doit pas publier la décision finale s’il n’est pas le moteur exécutif canonique.

## Contrats de données

### FactValue

```json
{
  "value": 42.5,
  "unit": "PERCENT",
  "source": "IBKR",
  "as_of": "2026-08-04T20:15:00Z",
  "status": "LIVE",
  "estimated": false,
  "method": null,
  "warnings": []
}
```

Statuts minimum :

- `LIVE`
- `DELAYED`
- `STALE`
- `OFFLINE`
- `MISSING`
- `DEMO`
- `ESTIMATED`
- `INSUFFICIENT`
- `CONFLICTED`

### MarketContext

Doit pouvoir porter :

- indices et tendances ;
- breadth MM20/MM50/MM200 ;
- VIX et structure à terme ;
- volatilité réalisée ;
- taux 2Y/10Y/30Y et pente ;
- dollar ;
- spreads de crédit ;
- liquidité ;
- dispersion ;
- leadership cyclique/défensif ;
- secteurs ;
- cross-asset ;
- régime principal, secondaires, confiance et transition.

### CompanyContext

- identité et secteur ;
- croissance CA/EPS/FCF ;
- marges ;
- bilan ;
- valorisation ;
- révisions ;
- surprise historique ;
- moat/qualité ;
- comparaison aux pairs ;
- qualité des données.

### TechnicalContext

- tendance multi-horizon ;
- moyennes ;
- momentum ;
- RSI/ADX/ATR ;
- relative strength ;
- volume ;
- support/résistance ;
- entrée ;
- invalidation ;
- extension ;
- breakout/pullback ;
- anomalies techniques.

### CatalystContext

Un événement n’est pas un catalyseur positif par défaut.

Champs :

- type ;
- date ;
- délai ;
- nouveauté ;
- direction possible ;
- amplitude ;
- confiance ;
- consensus ;
- déjà pricé ou non ;
- risque binaire ;
- sources ;
- faits confirmants et contradictoires.

### OptionsContext

- univers `TACTICAL`, `SWING` ou `LEAPS` ;
- spot ;
- expiration/DTE ;
- strike/right ;
- bid/ask/mid/last ;
- spread ;
- volume/OI ;
- IV, IV rank, IV percentile ;
- skew/term structure ;
- delta/gamma/theta/vega/vanna/vomma/charm ;
- expected move ;
- payoff ;
- max profit/loss et flags illimités ;
- breakevens ;
- PoP ;
- probabilité de doublement ;
- GEX, walls, zero gamma ;
- earnings/IV crush ;
- liquidité et exécutabilité ;
- modèle et hypothèses.

### PortfolioContext

- positions et provenance ;
- capital/cash ;
- poids ;
- niveaux S+/S/A/B ;
- concentration HHI ;
- secteurs/facteurs ;
- corrélations ;
- bêta ;
- drawdown ;
- stress ;
- budget de risque ;
- quota options ;
- compatibilité du candidat ;
- position à remplacer ;
- gagnant renforçable ;
- perdant non renforçable.

### ScenarioSet

Trois scénarios obligatoires :

```json
{
  "bear": {
    "probability": 0.25,
    "target": 88,
    "return_pct": -12,
    "option_return_pct": -35,
    "trigger": "...",
    "invalidation": "...",
    "horizon_days": 90,
    "assumptions": [],
    "unknowns": []
  },
  "base": {},
  "bull": {}
}
```

Contraintes :

- probabilités entre 0 et 1 ;
- somme proche de 1 selon tolérance documentée ;
- aucune cible sans méthode ;
- EV séparée action/option ;
- modèle et date de calibration conservés ;
- données insuffisantes → scénarios indisponibles, jamais probabilités arbitraires.

### SkylerPacket

Agrège les contextes sans muter les sources. Il inclut :

- identifiant et version de schéma ;
- symbole ;
- timestamp de génération ;
- contextes ;
- contradictions ;
- inconnues ;
- freshness floor ;
- provenance summary ;
- profil stratégique actif.

### SkylerDecision

- décision finale autorisée ;
- score /40 ;
- niveau ;
- confiance ;
- hard gates ;
- scénario set ;
- risque maximum ;
- catalyseur ;
- invalidation ;
- prochaine action analytique ;
- raison principale ;
- objection la plus forte ;
- inconnues ;
- audit trail.

## Rôle de Claude

Claude peut :

- résumer ;
- expliquer ;
- comparer ;
- rendre les contradictions lisibles ;
- proposer des questions de recherche ;
- reformuler selon le niveau utilisateur.

Claude ne peut pas :

- inventer un chiffre ;
- créer une probabilité ;
- modifier un score ;
- contourner un hard gate ;
- choisir une prime absente ;
- fabriquer une source ;
- prétendre qu’une donnée estimée vient du broker ;
- exécuter ou préparer un ordre transmissible.

## Mode dégradé

Skyler doit fonctionner sans Claude et sans IBKR.

- sans Claude : récit déterministe ;
- sans IBKR : données disponibles seulement, statut explicite ;
- démo : badge et provenance `DEMO` ;
- stale : décision plafonnée selon criticité ;
- conflit : score de qualité réduit et hard gate si critique ;
- absence : `INSUFFICIENT`, jamais valeur par défaut trompeuse.

## Versioning

Tous les packets et décisions portent :

- `schema_version`
- `engine_version`
- `profile_version`
- `model_version` si estimation
- `generated_at`

Une modification incompatible exige une nouvelle version de schéma et des tests de migration.
