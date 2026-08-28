# WORK_MANIFEST — Lot 1 · Autorité Claude unique

## Objectif

Prouver que `/vertex-2-0` est la seule autorité active, que les doctrines
historiques ne peuvent pas réapparaître silencieusement, et produire le
`GITHUB_CLEANUP_MANIFEST` — l'inventaire **en lecture seule** des 748
références distantes, avec SHA, état de préservation et action proposée.
**Aucune suppression n'est exécutée dans ce lot.**

## Non-objectifs

- Ne supprime aucune branche, aucun tag, aucun fichier, aucun agent.
- Ne réécrit pas d'historique, ne force-push pas.
- Ne touche ni au produit, ni aux moteurs, ni aux stores.

## SHA et branche

| Élément | Valeur |
|---|---|
| Branche | `agent/vertex-2-0-integration-20260828` |
| SHA de départ | `71d8214` (lot 0) |
| Dirty state | propre |

## Constat d'audit — la fusion porte déjà l'autorité unique

Mesuré au dépôt, pas supposé :

- **1 seul skill** : `.claude/skills/vertex-2-0/` — plus de `vertex-1-0`,
  `vertex-maximum`, `vertex-skyler-v2` ni `vertex-total-rebuild` ;
- **6 auditeurs** en lecture seule (`permissionMode: plan`), tous liés au
  skill maître ;
- **4 règles** consolidées (`vertex-invariants`, `vertex-data`, `vertex-ui`,
  `vertex-tests`) remplaçant les trois anciennes ;
- `CLAUDE.md` désigne `/vertex-2-0` et n'admet aucun alias.

**Le test de non-réapparition existe déjà** — il n'y a rien à écrire :

- `test_vertex_1_0_contract.py` : `skills == ["vertex-2-0"]` (un répertoire de
  skill et un seul) et `"/vertex-1-0" not in CLAUDE.md` ;
- `test_vertex_2_0_governance.py::test_only_six_subordinate_read_only_auditors_remain` :
  la liste exacte des six auditeurs, épinglée, chacun en `plan`.

Réintroduire un skill ou un agent concurrent fait donc échouer la suite.

## Fichiers autorisés

**Écriture :** `docs/vertex-2-0/lot-01/**` uniquement.
**Lecture seule :** tout le reste.

## Données à préserver

Toutes — le lot n'écrit que de la documentation.

## Tests

- `python -m pytest tests/test_vertex_2_0_governance.py tests/test_vertex_1_0_contract.py -q`
- `python .claude/skills/vertex-2-0/scripts/audit_claude_surface.py`

## Mesures

Inventaire distant : `git ls-remote --heads` (748 références), familles,
état de fusion dans `main` vérifié par `git branch -r --merged` après un
fetch sans blobs.

## Migration / Rollback

Aucune migration. Rollback : `git revert` du commit de lot — documentation
seule.

## Critères d'arrêt

1. Preuve versionnée que l'autorité est unique et gardée par des tests ;
2. `GITHUB_CLEANUP_MANIFEST` publié : chaque famille de références avec SHA,
   preuve de préservation, action proposée, risque et rollback ;
3. La liste des suppressions distantes proposées est **soumise, pas exécutée** ;
4. Suite de gouvernance verte.
