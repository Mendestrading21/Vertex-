# ▲ VERTEX — Terminal de décision en lecture seule

Vertex est une application locale Python/Flask qui rassemble marché, opportunités,
portefeuille, analyse, options, performance et intelligence dans un même cockpit.

> **Invariant absolu : ANALYSIS ONLY.** Vertex ne passe aucun ordre. Toute connexion
> IBKR impose `readonly=True`, et la CI bloque l'apparition d'un chemin d'exécution.

## Démarrage rapide

Le guide utilisateur se trouve dans [`DEMARRER_ICI.md`](DEMARRER_ICI.md).

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python terminal.py
```

Puis ouvrir <http://localhost:5002>.

Pour une démonstration hors ligne :

```bash
DEMO=1 NO_IBKR=1 python terminal.py
```

Les lanceurs `Lancer_VERTEX*` proposent les mêmes modes sous Windows et macOS.

## Espaces actuels

| Espace | Route | Rôle |
|---|---|---|
| Briefing | `/` | Vue du jour, régime, alertes et marchés |
| Opportunités | `/opportunities` | Actions, options, anomalies et calendrier |
| Portefeuille | `/portfolio` | Positions, risque, équipe et watchlist |
| Analyse | `/analysis` | Recherche et dossier complet par titre |
| Options | `/options` | Volatilité, scénarios, événements et dossiers options |
| Performance | `/performance` | Journal, track-record et apprentissages |
| Intelligence | `/intelligence` | Analyste, comité, stratégie et mémoire |
| Système | `/system` | Connexions, qualité des données et réglages |

La V4 fera de **Marchés** un neuvième espace explicite en réutilisant les vues et
contrats existants, sans modifier les moteurs financiers.

## Architecture

- `terminal.py` : point d'entrée historique, routes et orchestration encore en migration.
- `vertex/app/` : configuration, état et blueprints Flask.
- `vertex/ui/` : shell et pages componentisées.
- `vertex/engines/`, `vertex/options/`, `vertex/strategy/` : logique analytique.
- `vertex/static/vertex/` : CSS, JavaScript et graphiques.
- `tests/` : garde-fous métier, données, sécurité et interface.
- `docs/` : documentation indexée par statut.
- `ib_reader.py` / `test_connection.py` : diagnostic IBKR local en lecture seule.

La carte technique actuelle est dans
[`docs/canonical/ARCHITECTURE.md`](docs/canonical/ARCHITECTURE.md).

## Développement

```bash
python -m compileall -q terminal.py vertex
python -m pytest tests/ -q
```

Toute modification visible doit aussi être vérifiée dans un vrai navigateur sur
desktop, tablette et mobile, avec `/healthz` vert et `/api/client-log` sans erreur.

## Vertex V4

La seule direction visuelle active est **Obsidian Prism**. Commencer par :

1. [`CLAUDE.md`](CLAUDE.md)
2. [`docs/README.md`](docs/README.md)
3. [`docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md`](docs/vertex-v4/VERTEX_V4_MASTER_SPEC.md)
4. [`docs/vertex-v4/STATUS.md`](docs/vertex-v4/STATUS.md)

Branche d'intégration : `integration/vertex-v4-clean`. `main` ne doit jamais être
modifiée directement.
