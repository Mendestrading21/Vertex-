# Archive Vertex

> **Status: ACTIVE INDEX — contenu archivé hors de l'arbre courant**
> Last verified: 2026-07-22

La consolidation V4 a retiré les documents et captures Black Glass, Signal
Green, Obsidian Copper, UI V3 et les audits historiques. Ils ne sont plus des
instructions actives et ne doivent pas être restaurés dans une session V4.

## Points de récupération Git

| Tag | Contenu protégé |
|---|---|
| `vertex-pre-v4-main-2026-07-22` | `main` avant consolidation |
| `vertex-pre-v4-glass-2026-07-22` | base technique Glass avancée et ses 981 tests |
| `vertex-v4-docs-2026-07-22` | première documentation V4 |
| `vertex-v4-references-2026-07-22` | commit orphelin contenant les 24 images brutes |

L'historique Git reste la sauvegarde. Il est inutile de conserver des copies
dupliquées dans `docs/archive/`, car elles redeviendraient visibles dans les
recherches de Claude Code.

## Ce qui a été retiré

- anciens plans et contrats visuels ;
- 121 captures `docs/redesign/` ;
- audits, baselines et rapports « ultimate » périmés ;
- skills Claude page-par-page liés à Black Glass ;
- anciens documents V3, Copper et Signal Green.

## Ce qui n'est pas encore supprimé

Les CSS et scripts legacy encore chargés par le runtime restent temporairement
dans `vertex/static/vertex/`. Ils sont suivis par
[`../vertex-v4/MIGRATION_MAP.md`](../vertex-v4/MIGRATION_MAP.md) et ne seront
retirés qu'après migration visuelle, tests, captures et vérification navigateur.
