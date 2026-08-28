# ADR — Le registre d'essais reste en mémoire (pas de persistance)

Date : 2026-08-28 · Statut : ACCEPTÉ (lot 25)

## Contexte
`vertex/research/registry.py` conserve les expériences (rejetées comprises)
en mémoire de processus. Le skill exige un ADR avant toute persistance.

## Décision
PAS de persistance tant qu'aucun usage réel ne la justifie. Critères de
révision (l'un suffit) : 1) un utilisateur mène des essais sur plusieurs
sessions et perd son compte d'essais (la correction de multiplicité devient
fausse) ; 2) une UI de labo (phase D future) doit afficher l'historique ;
3) le replay d'un manifeste exige de retrouver un essai passé.

## Conséquences
- `n_essais()` ne compte que la session courante — dit dans la docstring.
- Le jour venu : persistance via `vertex.services.persist` (JSON borné),
  jamais une nouvelle infrastructure (ADR anti-infrastructure du lot 9).
