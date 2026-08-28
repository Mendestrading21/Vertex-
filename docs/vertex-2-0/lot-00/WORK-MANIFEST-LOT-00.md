# WORK_MANIFEST — Lot 0 · Baseline reproductible

## Objectif

Figer, **par la mesure et non par la lecture**, l'état réel du dépôt consolidé :
routes, pages, collisions, moteurs, jobs, stores, tests, dépendances, styles,
latences, payloads et captures avant. Publier la matrice vérité → cible et
interdire de traiter une redirection ou une 404 comme une page livrée.

## Non-objectifs

- Ne corrige **aucun** défaut produit. Un écart mesuré devient un ticket, pas
  un correctif.
- Ne migre aucun consommateur, ne retire aucun doublon, ne touche aucun moteur,
  aucun store, aucune donnée utilisateur.
- Ne fusionne rien vers `main`. #838 et #839 restent en brouillon.
- N'ajoute aucune dépendance.

## SHA et branches

| Élément | Valeur |
|---|---|
| Branche de travail | `agent/vertex-2-0-integration-20260828` |
| SHA de départ | `cb33d90` (fusion de consolidation) |
| Base commune | `main` @ `eff337f` |
| Programme maître | `agent/vertex-design-2-0-master-20260827` @ `682c201` — PR #838 |
| Travail graphique | `checkpoint/vertex-2-0-graphique-20260828` @ `cfec714` — PR #839 |
| Dirty state au départ | propre |

## Fichiers autorisés dans ce lot

**Écriture autorisée — et rien d'autre :**

- `docs/vertex-2-0/lot-00/**` — tous les livrables du lot ;
- `tools/vertex_2_0_capture.py` — les largeurs de capture étaient figées à
  1440/390 alors que le skill maître exige **1600/1024/390**. Sans ce
  changement, la tablette n'est jamais capturée — or c'est exactement la
  largeur où deux fautes ont été trouvées. Le changement rend les largeurs
  paramétrables ; il ne touche pas au produit.

**Lecture seule :** tout le reste, `vertex/`, `terminal.py`, `tests/`,
`.claude/` inclus.

## Routes, composants, stores, moteurs

Aucun modifié. Les 12 routes cibles sont **mesurées** :
`/`, `/calendar`, `/markets`, `/opportunities`, `/analysis`, `/options`,
`/simulator`, `/portfolio`, `/follow-up`, `/performance`, `/intelligence`,
`/system`.

## Données à préserver

Toutes. Ce lot n'écrit dans aucun store. En particulier :
`desk_data.json` et ses sauvegardes ne sont ni lus en écriture ni écrasés ;
les positions saisies, thèses, enveloppes et clôtures restent intactes ;
aucune clé `localStorage` n'est ajoutée, renommée ou retirée.

## Dépendances

Aucune ajoutée, aucune retirée, aucune version modifiée.

## Tests

- `python -m compileall -q terminal.py vertex`
- `python -m pytest -q` — attendu : 1 échec environnemental connu
  (`test_la_classification_est_discriminante` exige plus de 100 références git ;
  ce clone en porte 4). Il passe sur la CI.
- `python -m pytest tests/test_no_orders.py -q`

## Mesures produites

| Mesure | Outil |
|---|---|
| Routes, endpoints, blueprints, collisions, shell | `scripts/audit_runtime.py` |
| Autorité Claude unique | `scripts/audit_claude_surface.py` |
| Dette de confidentialité IBKR | `scripts/check_ibkr_boundary.py` |
| Inventaire du dépôt | `scripts/inventory_repo.py` |
| Latence et payload des 12 pages | `curl`, médiane de trois passes |
| Poids et propriété des feuilles CSS | mesure directe |
| Palette servie contre palette canonique | mesure directe + contraste WCAG |

## Captures

12 pages × 3 largeurs (**1600 / 1024 / 390**) →
`docs/vertex-2-0/lot-00/captures-avant/`, avec `rapport.json` portant erreurs
console et débordement horizontal par largeur.

## Migration

Aucune. Ce lot est en lecture seule sur le produit.

## Rollback

`git revert` du commit de lot 0. Il ne touche que de la documentation et un
outil d'audit ; aucun chemin de rollback produit n'est requis.

## Critères d'arrêt

Le lot 0 est terminé quand :

1. les quatre scripts du skill ont tourné et leur sortie est versionnée ;
2. la matrice vérité → cible des 12 pages est publiée avec le HTTP réel ;
3. les latences et payloads des 12 pages sont mesurés ;
4. les captures avant existent aux trois largeurs ;
5. le `DESIGN_CONVERGENCE_REPORT` liste palettes, Design Systems, feuilles CSS
   et bibliothèques graphiques, avec un propriétaire canonique proposé pour
   chacun ;
6. chaque écart trouvé porte un numéro de lot cible — aucun n'est corrigé ici ;
7. la suite de tests est verte hors échec environnemental connu.
