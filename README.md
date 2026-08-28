# ▲ VERTEX 1.0

**Système d'intelligence de marché et d'aide à la décision — analyse uniquement.**

Vertex centralise le régime de marché, le brief quotidien, les opportunités,
l'analyse d'entreprises, le portefeuille déclaré et l'intelligence options. Il est
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

- **IBKR**: contrats, cours, historiques, chaînes, IV et Greeks de marché
  uniquement, connexion forcée en lecture seule; aucun compte, solde, position
  ou P&L broker ne fait partie du contrat Vertex 2.0;
- **Portefeuille**: enveloppes, cash et positions saisis volontairement par
  l'utilisateur dans Vertex;
- **TradingView**: signaux authentifiés qui demandent une réévaluation, jamais
  un achat;
- **WMB Brief**: contexte macro quotidien avec provenance;
- **yfinance**: repli différé explicitement étiqueté;
- **Claude**: synthèse et explication uniquement; les calculs, scores, Greeks,
  probabilités, hard gates et verdicts restent déterministes.

## Espaces du runtime actuel

La navigation principale réellement servie contient Dashboard, Opportunités,
Analyse, Portefeuille, Options, Journal et Système. Intelligence et Suivis sont
des pages secondaires. Calendrier redirige vers Opportunités, Marchés vers le
Dashboard ; Simulateur et la future route Suivi n'existent pas encore.

La cible Vertex 2.0 comporte douze pages, livrées par migration progressive :
Aujourd'hui, Calendrier, Marchés, Opportunités, Analyse, Options, Simulateur,
Portefeuille, Suivi, Performance, Vertex IA et Système. La matrice exacte vit
dans le skill maître ; elle ne constitue pas une promesse de pages déjà prêtes.

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

Claude Code doit utiliser exclusivement `/vertex-2-0`. Le skill maître est
`.claude/skills/vertex-2-0/SKILL.md`; il fait converger progressivement le
runtime 1.0 vers la plateforme 2.0 sans présenter la cible comme déjà livrée.
Il contient désormais la composition des douze pages et de leurs widgets, le
laboratoire de stratégies reproductible, la matrice de connexions/résilience
et le protocole Autopilot lot par lot. Ces références définissent des contrats
et des portes d'adoption ; elles n'installent aucune dépendance ni ne déclarent
une capacité absente comme disponible.

## Documentation active

Commencer par le skill maître. [`docs/vertex-1.0/README.md`](docs/vertex-1.0/README.md)
reste une archive technique du runtime actuel ; les anciens documents et
branches sont des preuves historiques, pas des instructions concurrentes.

## Sécurité

- `READONLY=True` et `ANALYSIS_ONLY=True`;
- aucune route ni fonction d'ordre;
- secrets dans `.env`, jamais dans Git;
- données absentes, différées, rassies, démo ou hors ligne explicitement
  signalées;
- aucune promesse de performance ou conseil financier personnalisé.
