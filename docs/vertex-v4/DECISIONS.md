# Vertex V4 — décisions figées

> **Status: ACTIVE**
> Owner: Vertex V4
> Last verified: 2026-07-22
> Branch: `integration/vertex-v4-clean`

Ce journal ferme les ambiguïtés de design et d'organisation. Toute modification
de l'une de ces décisions doit être explicite et reportée dans la Master Spec.

| ID | Décision | Conséquence |
|---|---|---|
| D-001 | **Obsidian Prism** est l'unique identité V4. | Black Glass, Signal Green et Obsidian Copper sont supersédés. |
| D-002 | La marque utilise violet, magenta et corail. | Le vert et le rouge restent exclusivement financiers. |
| D-003 | La référence maître est `reference/00-master-obsidian-prism.jpg`. | Toute revue visuelle commence par cette image et le manifeste. |
| D-004 | General Sans + JetBrains Mono restent les polices officielles. | Aucun CDN ni nouvelle famille à télécharger ; les assets auto-hébergés sont conservés. |
| D-005 | La navigation cible comporte neuf espaces. | Marchés redevient explicite en réutilisant les vues existantes, sans nouveau moteur. |
| D-006 | `integration/vertex-v4-clean` est la branche d'intégration. | `redesign/vertex-v4-master` devient une source historique de docs, pas une base de code. |
| D-007 | Un seul skill Claude actif : `vertex-v4-redesign`. | Les anciens skills page-par-page sont retirés. |
| D-008 | Les fichiers runtime legacy ne sont pas supprimés avant migration prouvée. | Chaque retrait exige tests verts, captures et absence de consommateur. |
| D-009 | Les captures historiques sont retirées de l'arbre actif. | Les tags Git assurent la récupération sans polluer les recherches. |
| D-010 | `main` n'est jamais modifiée directement. | Toute fusion finale nécessite une PR et une autorisation explicite. |

## Navigation cible

1. Briefing
2. Marchés
3. Opportunités
4. Portefeuille
5. Analyse
6. Options
7. Performance
8. Intelligence
9. Système

Marchés est une séparation d'expérience et de navigation. Les données de marché,
routes et moteurs existants restent les sources à réutiliser.

## Hiérarchie des sources

En cas de contradiction :

1. invariants READONLY et tests ;
2. `docs/canonical/*` ;
3. ce journal ;
4. `VERTEX_V4_MASTER_SPEC.md` ;
5. `.interface-design/system.md` ;
6. références du skill ;
7. documents `reference/`.
