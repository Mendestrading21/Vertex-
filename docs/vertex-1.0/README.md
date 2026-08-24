# Vertex 1.0 — corpus canonique

Ce dossier est la source documentaire active unique.

| Document | Rôle |
|---|---|
| `PRODUCT_CONTRACT.md` | mission, utilisateurs, mandats, décisions et limites |
| `ARCHITECTURE.md` | composants, flux de données et frontières IA/déterministe |
| `QUALITY_STANDARD.md` | niveau minimum données, décision, UI, sécurité et fiabilité |
| `RELEASE_GATES.md` | gates G0–G7 avant le tag final |
| `REPOSITORY_AUDIT.md` | état mesuré du dépôt et risques de consolidation |
| `MIGRATION_PLAN.md` | extraction du monolithe et convergence par phases |
| `DESIGN_SYSTEM.md` | direction visuelle et règles de consolidation UI |
| `CLEANUP_POLICY.md` | conditions de suppression des fichiers, branches et couches legacy |
| `BRANCH_GOVERNANCE.md` | branches, PR, archives et release |
| `CLAUDE_CODE_RUNBOOK.md` | procédure d'exécution pour Claude Code |
| `CLAUDE_MASTER_PROMPT.md` | prompt unique pour les grands chantiers Claude Code |
| `RELEASE_CHECKLIST.md` | preuves exigées avant Vertex 1.0 final |
| `DECISIONS.md` | registre court des décisions actives |
| `audits/AUDIT-TOTAL-2026-08-24.md` | audit indépendant de la RC, CI, couverture, sources et dette |
| `roadmap/VERTEX-INTELLIGENCE-2.0.md` | programme ordonné de montée en gamme après stabilisation RC |
| `roadmap/SOURCES-APIS-OPEN-SOURCE.md` | sélection des sources officielles, API et références externes |
| `roadmap/STRATEGY-V5-ARBITRAGE.md` | contradictions V4 / doctrine utilisateur à trancher humainement |
| `roadmap/CLAUDE-CODE-EXECUTION.md` | prompt d'exécution du programme pour Claude Code |
| `roadmap/external_references.json` | registre machine-readable des références externes |

## Autorité

En cas de contradiction :

1. invariants de sécurité ;
2. code et tests du commit candidat ;
3. profil stratégique de release ;
4. documents de ce dossier ;
5. archives.

Toute ambiguïté devient une entrée dans `DECISIONS.md`, jamais un nouveau document « master », « ultimate » ou une branche d'intégration concurrente.

Les documents `roadmap/` ne remplacent ni les gates ni la doctrine active. Ils
ordonnent le travail après la RC. Une phase ne devient active que lorsque ses
dépendances et décisions humaines sont satisfaites.
