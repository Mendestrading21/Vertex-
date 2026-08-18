# Architecture canonique — Vertex 1.0

## Flux

```text
IBKR / yfinance / TradingView / WMB / calendrier / fondamentaux
  ↓
adapters de source
  ↓
normalisation + provenance + fraîcheur + qualité
  ↓
contextes immuables
  ↓
moteurs déterministes
  ↓
packet de décision versionné
  ↓
hard gates
  ↓
scénarios + score + compatibilité portefeuille
  ↓
décision canonique
  ↓
narration Claude
  ↓
API / UI / journal / calibration
```

## Frontières

### Sources

Chaque source expose un contrat uniforme: valeur, unité, timestamp, source,
qualité, fraîcheur et erreur. Les replis ne remplacent jamais silencieusement
la source primaire.

### Domaines

- `vertex/data*`: acquisition et normalisation;
- `vertex/market`: régime, breadth, secteurs, macro et brief;
- `vertex/companies` / `company`: à converger vers un domaine entreprise;
- `vertex/options`: chaîne, Greeks, liquidité, GEX, flow et contrats;
- `vertex/portfolio` / `positions` / `tracking`: à converger autour d'un
  portefeuille canonique et d'un journal d'état;
- `vertex/engines`: calculs et décisions déterministes;
- `vertex/strategy`: constitution, packet, hard gates et décision exécutive;
- `vertex/app/routes`: API;
- `vertex/ui` et `vertex/static`: présentation;
- `vertex/ai`: narration et enrichissement, jamais vérité numérique.

### Runtime

- `python -m vertex`: entrée locale;
- `vertex.runtime:app`: entrée WSGI;
- `terminal.py`: composition historique, maintenue par adaptateur;
- toute nouvelle capacité doit entrer dans le package, puis être branchée au
  runtime.

## Packet canonique

Le packet doit être immuable et versionné. Il référence:

- version produit et profil stratégique;
- instantané des sources;
- contexte marché, entreprise, technique, catalyseurs, options et portefeuille;
- qualité/fraîcheur;
- résultats moteurs;
- contradictions;
- hard gates;
- scénarios;
- décision et justification.

## Dégradation

Vertex doit fonctionner sans Claude, sans IBKR et en panne partielle. La
capacité diminue; l'honnêteté ne diminue jamais.

## Migration du monolithe

Aucun « big bang ». Extraire dans cet ordre:

1. création d'application et démarrage;
2. registre de routes;
3. workers et scheduler;
4. state stores;
5. caches et persistance;
6. pages encore incorporées;
7. suppression des adaptateurs après preuve de non-usage.
