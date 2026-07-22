# Vertex V4 — résultat de la consolidation

> **Status: ACTIVE RESULT**
> Date: 2026-07-22
> Branch: `integration/vertex-v4-clean`

## Verdict

Vertex possède désormais une base unique, testée et compréhensible pour Claude
Code. La branche part de la meilleure baseline technique et n'altère aucun
moteur, calcul, contrat API ou comportement de trading.

## Avant / après

| Axe | Avant | Après |
|---|---:|---:|
| Directions visuelles concurrentes | 3 | 1 — Obsidian Prism |
| Skills Claude actifs | 15 | 1 |
| Règles Claude actives | 3 contradictoires | 3 cohérentes |
| Fichiers sous `.claude/` | 37 | 26 |
| Fichiers sous `docs/` | 216 | 71 |
| Taille de `docs/` | ~20,6 Mo | ~2,6 Mo |
| Captures historiques actives | 121 | 0 |
| Références V4 classées | 0 | 24 + manifeste |
| Fichiers runtime suivis par Git | 2 | 0 |
| Tests baseline | 981 passés, 2 ignorés | 981 passés, 2 ignorés |

## Organisation créée

- `docs/canonical/` : produit, architecture, READONLY, accès, données, charts et routes.
- `docs/reference/` : détails métier et techniques non canoniques.
- `docs/vertex-v4/` : Master Spec, décisions, statut, migration et références.
- `docs/audits/current/` : audit avant consolidation et résultat courant.
- `docs/archive/README.md` : points de récupération Git, sans copies polluantes.
- `.claude/skills/vertex-v4-redesign/` : unique orchestration active.
- `.claude/rules/` : sécurité, intégrité des données et design V4.

## Nettoyage effectué

- anciens plans Black Glass, Copper, Signal Green et V3 retirés ;
- 121 captures historiques supprimées de l'arbre courant ;
- anciens audits et baselines supersédés retirés ;
- 14 workflows Claude concurrents supprimés ;
- 24 images récupérées, renommées et classées MASTER/SECONDARY/REJECTED ;
- `company_cache.json` et `position_inventory.json` retirés du suivi Git ;
- CI étendue à `integration/**` et `redesign/**` ;
- README, démarrage, guide Claude et design system réécrits.

Les couches CSS historiques encore consommées par le runtime restent en place
jusqu'au lot 15. Leur retrait est contrôlé par `docs/vertex-v4/MIGRATION_MAP.md`.

## Preuves

```text
python -m compileall -q terminal.py vertex
python -m pytest tests/ -q
981 passed, 2 skipped
```

Contrôle serveur `DEMO=1 NO_IBKR=1` :

| Contrôle | Résultat |
|---|---:|
| `/` | 200 |
| `/opportunities` | 200 |
| `/portfolio` | 200 |
| `/analysis` | 200 |
| `/options` | 200 |
| `/performance` | 200 |
| `/intelligence` | 200 |
| `/system` | 200 |
| `/markets` | 302 attendu vers la baseline actuelle |
| `/healthz` | `status: ok` |
| `/api/client-log` | `count: 0` |

## Sauvegardes

- `vertex-pre-v4-main-2026-07-22`
- `vertex-pre-v4-glass-2026-07-22`
- `vertex-v4-docs-2026-07-22`
- `vertex-v4-references-2026-07-22`

## Prochaine étape autorisée

Lot 01 — fondations V4 : tokens, typographies, profondeur et primitives. Aucun
travail page-par-page ne commence avant validation de cette consolidation.
