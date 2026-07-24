# Claude Code — Vertex Total Rebuild

## Branche obligatoire

Travaille sur :

```bash
git fetch origin
git checkout agent/vertex-total-rebuild
git pull --ff-only
```

Confirme ensuite :

```bash
git branch --show-current
test -f .claude/FRAMEWORK.md
test -f .claude/skills/vertex-total-rebuild/SKILL.md
test -f .claude/manifesto/VERTEX.md
```

## Lecture obligatoire

Lis intégralement, dans cet ordre :

1. `.claude/FRAMEWORK.md`
2. `.claude/manifesto/VERTEX.md`
3. `.claude/skills/vertex-total-rebuild/SKILL.md`
4. `.claude/agents/product-auditor.md`
5. `.claude/agents/graph-designer.md`
6. `.claude/agents/ui-designer.md`
7. `.claude/agents/trading-engine.md`
8. `.claude/agents/qa-tester.md`
9. les documents existants de `docs/refactor/`.

## Mission immédiate

Exécute uniquement les phases 0, 1 et 2 :

- baseline réelle ;
- inventaire de tous les fichiers ;
- cartographie routes, pages, endpoints et moteurs ;
- inventaire de tous les graphiques ;
- carte des références visuelles ;
- registre des contradictions ;
- liste des doublons et fichiers morts potentiels.

Ne commence pas encore la refonte massive du runtime.

## Exécution réelle

Tu dois réellement lancer les tests, lancer Vertex en mode démo, inspecter toutes les routes dans le navigateur, relever les erreurs console et réseau, tester desktop/tablette/mobile et vérifier les états sans IBKR, données absentes et données périmées.

## Livrables

- `docs/refactor/VERTEX_BASELINE_AUDIT.md`
- `docs/refactor/FILE_INVENTORY.md`
- `docs/refactor/ROUTE_ENDPOINT_MAP.md`
- `docs/refactor/PAGE_DATA_GRAPH_MATRIX.md`
- `docs/refactor/CHART_INVENTORY.md`
- `docs/refactor/CONTRADICTIONS_REGISTER.md`
- `docs/refactor/VISUAL_REFERENCE_MAP.md`
- `docs/refactor/PHASE_0_2_REPORT.md`

## Contraintes absolues

- IBKR reste strictement READONLY.
- Aucun ordre ou chemin d’ordre.
- Aucune donnée inventée.
- Aucun fichier supprimé pendant l’audit.
- Aucun moteur modifié pour une raison esthétique.
- Ne déclare rien terminé sans preuves.

## Rapport final attendu

Présente la branche et le commit, les commandes exécutées, les résultats exacts des tests, le nombre de fichiers/routes/pages/endpoints/moteurs/graphiques, les dix problèmes principaux, les contradictions critiques, les graphiques à garder/fusionner/remplacer/supprimer, les fichiers legacy potentiels, les risques et le plan exact de la prochaine PR.