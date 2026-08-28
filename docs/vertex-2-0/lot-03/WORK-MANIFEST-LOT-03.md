# WORK_MANIFEST — Lot 3 · Portefeuille manuel souverain

## Objectif

Un seul schéma de déclaration de position, aligné sur le contrat
`DeclaredPosition` du skill (quantité, coût, **devise**, dates, statut,
**stratégie**, objectif, invalidation), quel que soit l'écrivain. Publier la
matrice des propriétaires des 17 clés du desk.

## Constat d'audit (mesuré)

Deux écrivains de `myTrades` coexistent :

| Champ | Legacy `vx_kit.addPosition` | 2.0 `VXEntities.openAddModal` | Lecteur aval |
|---|---|---|---|
| `entrySnap.stop` | ✅ (via `tSnapOf`) | ✅ | `positions/models.py:112` |
| `entrySnap.tgt` / `myTgt` | ✅ demandé | **absent — jamais demandé** | `models.py:113` → `tp1` |
| `currency` | ✅ demandé | **absent** (USD implicite) | enrichment, contrat |
| `strategy` | ✅ demandé | **absent** | contrat `DeclaredPosition` |
| `fees` | ✅ demandé | **absent** | coût réel déclaré |
| `entryPrice` | ✅ | ✅ | `models.py:93` |

**Conséquence :** une position déclarée depuis l'interface 2.0 n'a **jamais**
d'objectif (`tp1 = None` dans tout le pipeline de positions), pas de devise
déclarée, pas de stratégie — alors que la même déclaration depuis le legacy
les porte. Deux positions « identiques » divergent selon la porte d'entrée.

## Décision de convergence

Le **schéma historique du desk est le propriétaire canonique** (contrat du
skill : « ne pas créer un nouveau modèle parallèle »). Le formulaire 2.0 est
enrichi à parité ; le legacy n'est pas touché (strangler au lot 9).

## Fichiers autorisés

`vertex/static/vertex/js/vx-entities.js` · `vertex/app/routes/system.py`
(bump SW) + gardiens SW · `tests/test_declaration_position_lot03.py` (neuf) ·
`docs/vertex-2-0/lot-03/**`.

## Données à préserver

Toutes les positions existantes : le changement n'ajoute que des champs à la
**future** écriture ; aucune migration des entrées passées (les lecteurs
tolèrent déjà l'absence — `_f(...) or None`).

## Tests

- rouge → vert : gardien source sur le formulaire et l'écriture ;
- preuve navigateur : déclarer une position via le VRAI modal, relire
  `myTrades` dans le localStorage, vérifier le schéma complet ;
- suite complète.

## Rollback

Revert du commit — les positions écrites entre-temps gardent leurs champs
supplémentaires, que les lecteurs actuels savent lire (schéma superset).
