# Vertex Development Framework V1

## Lecture obligatoire

1. `.claude/manifesto/VERTEX.md`
2. `.claude/skills/vertex-total-rebuild/SKILL.md`
3. `CLAUDE_VERTEX_REBUILD.md`
4. Les agents spécialisés dans `.claude/agents/`
5. Les documents de `docs/refactor/`

## Agents

- Product Auditor : inventaire, pages, routes, doublons et contradictions.
- Graph Designer : choix, cohérence et reconstruction des graphiques.
- UI Designer : design system, composants, responsive et motion.
- Trading Engine : asymétrie, scénarios, risque et cohérence financière.
- QA Tester : tests, navigateur, données manquantes, mobile et READONLY.

## Séquence de travail

### Lot 0 — Baseline

Product Auditor et QA Tester établissent l’état initial sans modifier le runtime.

### Lot 1 — Cartographie

Product Auditor, Graph Designer et Trading Engine relient pages, endpoints, moteurs, sources et graphiques.

### Lot 2 — Fondations

UI Designer, Graph Designer et QA Tester consolident tokens, composants et chart shell.

### Refonte page par page

Pour chaque page :

1. définir la mission ;
2. vérifier la logique financière ;
3. choisir les visualisations utiles ;
4. reconstruire la hiérarchie ;
5. valider tous les scénarios.

## Priorité en cas de conflit

1. Justesse et honnêteté des données.
2. Sécurité IBKR READONLY.
3. Compréhension utilisateur.
4. Maintenabilité.
5. Esthétique.

## Définition de terminé

Un lot est terminé uniquement lorsque les tests passent, qu’aucune erreur console réelle ne subsiste, que les états absent/périmé/démo fonctionnent, que desktop et mobile sont validés et que la documentation est à jour.