# Rapport — Lot 1 · Autorité Claude unique

## Numéro et nom

Lot 1 — Autorité Claude unique (+ `GITHUB_CLEANUP_MANIFEST` en lecture seule).

## Constat central : la fusion portait déjà le lot

Le travail demandé par le programme — activer uniquement `/vertex-2-0`,
retirer les skills et agents concurrents, consolider les règles, garder le
tout par un test de non-réapparition — **était déjà accompli par PR #838** et
est entré dans la branche d'intégration avec la fusion du lot 0. Ce lot n'a
donc **rien modifié** : il a prouvé.

| Exigence du lot | Preuve mesurée |
|---|---|
| Un seul skill actif | `ls .claude/skills/` → `vertex-2-0` seul |
| Six auditeurs lecture seule | liste exacte épinglée par `test_only_six_subordinate_read_only_auditors_remain`, chacun `permissionMode: plan` |
| Règles consolidées | `vertex-invariants` · `vertex-data` · `vertex-ui` · `vertex-tests` |
| `CLAUDE.md` sans alias | désigne `/vertex-2-0`, interdit `/vertex-1-0` |
| Test de non-réapparition | **existait déjà** : `skills == ["vertex-2-0"]` + liste d'agents épinglée. Réintroduire un concurrent fait échouer la suite |
| Archives explicitement historiques | `CLAUDE.md` §« preuves historiques, jamais des instructions » |

## Tests exacts

```
python -m pytest tests/test_vertex_2_0_governance.py tests/test_vertex_1_0_contract.py -q
    17 passed
python .claude/skills/vertex-2-0/scripts/audit_claude_surface.py
    OK: 1 skill Vertex, 6 auditeurs, références résolues, audit 001–150.
```

## Fichiers modifiés

`docs/vertex-2-0/lot-01/**` uniquement — trois documents. Aucun fichier
produit, aucun test, aucun agent, aucune règle.

## Le GITHUB_CLEANUP_MANIFEST

748 références distantes inventoriées après un fetch **sans blobs** ; l'état
de fusion dans `main` est mesuré, pas supposé :

- **30 branches fusionnées** — contenu prouvé dans `main`, suppression sûre
  (tranche A, **proposée, non exécutée**) ;
- **636 branches `agent/skyler-v2-*`** non fusionnées — le *résultat* du
  programme vit dans `main`, les branches gardent le *déroulé* ; proposition
  d'archive puis suppression (tranche B, **en attente d'autorisation**) ;
- le reste — prototypes design abandonnés, `feature/*`, `claude/*` — listé
  branche par branche avec SHA et état, décision différée (tranche C).

**Aucune suppression exécutée. Aucun historique réécrit. Aucun force-push.**

## Erreurs restantes / limites

- La preuve de fusion s'appuie sur `git branch -r --merged origin/main` : elle
  établit qu'une branche est *contenue* dans `main`, pas qu'une PR GitHub la
  référence. Pour la tranche A c'est équivalent (le contenu est préservé).
- Les 717 branches non fusionnées n'ont **pas** été examinées commit par
  commit — c'est précisément pourquoi les tranches B et C ne proposent rien
  d'automatique.

## Migration / Rollback

Aucune migration. Rollback : revert du commit (documentation seule).

## Prochain lot

Lot 2 — **Frontière IBKR market-data-only** : firewall de capacités typé,
retrait des 13 appels sensibles relevés au lot 0, `check_ibkr_boundary.py
--enforce` obligatoire en fin de lot.
