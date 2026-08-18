# ▲ VERTEX 1.0

**Système d'intelligence de marché et d'aide à la décision — analyse uniquement.**

Vertex centralise le régime de marché, le brief quotidien, les opportunités,
l'analyse d'entreprises, le portefeuille et l'intelligence options. Il est
conçu pour produire des décisions structurées, mesurables, traçables et
explicables. **Aucun chemin d'exécution d'ordre n'est autorisé.**

> Version active: **Vertex 1.0 RC1** (`1.0.0rc1`). Le statut RC signifie que
> l'architecture canonique est installée, mais que la release finale dépend
> encore de la CI complète et de l'acceptation humaine documentée.

## Lancer

```bash
python -m venv .venv
# macOS/Linux
. .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
python -m vertex
```

Ouvrir ensuite `http://localhost:5002`.

Les lanceurs `Lancer_VERTEX` et `Lancer_VERTEX_DEMO` restent disponibles.
`python terminal.py` est encore compatible, mais constitue un mode legacy de
rollback et n'est plus l'entrée canonique.

## Mandats de décision

| Mandat | Cadre |
|---|---|
| Options tactiques longues | détention typique 2/4/6 semaines; DTE préféré 120–240 jours; cible 180 jours |
| Actions | horizons de décision 3/6/12 mois |
| WMB Brief | contexte macro quotidien, daté et sourcé; jamais une source de prix |

Le profil de release exécutable est
`vertex/strategy/release_profiles/vertex_strategy_v4.json`. Les profils V1–V3
restent disponibles pour l'historique et le rollback, mais le runtime
canonique active V4 avant de charger l'application.

## Sources et intégrations

- **IBKR**: cours, options et portefeuille, connexion forcée en lecture seule;
- **TradingView**: signaux authentifiés qui demandent une réévaluation, jamais
  un achat;
- **WMB Brief**: contexte macro quotidien avec provenance;
- **yfinance**: repli différé explicitement étiqueté;
- **Claude**: synthèse et explication uniquement; les calculs, scores, Greeks,
  probabilités, hard gates et verdicts restent déterministes.

## Huit espaces canoniques

1. Aujourd'hui
2. Marchés
3. Opportunités
4. Analyse
5. Portefeuille
6. Options
7. Journal
8. Système

## Architecture

```text
sources réelles
  → normalisation / qualité / fraîcheur / provenance
  → moteurs déterministes
  → packet immuable
  → hard gates
  → scénarios / score / portefeuille
  → décision canonique
  → explication IA
  → interface / journal / audit
```

`vertex.runtime` est l'entrée WSGI canonique. Il active le profil de release
avant d'importer `terminal.py`. Le monolithe reste un adaptateur historique
pendant sa décomposition progressive; aucune nouvelle fonctionnalité ne doit y
être ajoutée.

## Développement

```bash
python -m compileall -q terminal.py vertex
python -m pytest -q
python -m pytest tests/test_no_orders.py -q
```

Claude Code doit utiliser exclusivement `/vertex-1-0` et les documents sous
`docs/vertex-1.0/`.

## Documentation active

Commencer par [`docs/vertex-1.0/README.md`](docs/vertex-1.0/README.md).
Les anciens documents et branches restent consultables comme archives de
preuve, mais ne sont plus des sources d'instruction.

## Sécurité

- `READONLY=True` et `ANALYSIS_ONLY=True`;
- aucune route ni fonction d'ordre;
- secrets dans `.env`, jamais dans Git;
- données absentes, différées, rassies, démo ou hors ligne explicitement
  signalées;
- aucune promesse de performance ou conseil financier personnalisé.
