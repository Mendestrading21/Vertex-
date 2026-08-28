# WORK_MANIFEST — Lot 6 · Gateway et snapshots (tranche : servir sans attendre)

## Objectif

Qu'une requête UI ne paie plus la latence fournisseur quand une cotation
existe déjà : `/api/pos-quotes` sert immédiatement ce qu'il tient — frais ou
**périmé et étiqueté** — et rafraîchit en arrière-plan. L'attente bornée ne
subsiste que pour une clé jamais cotée, et elle est resserrée.

## Constat d'audit (mesuré)

- **Un seul worker IBKR** (`_ibkr_opt_worker`, file `_optq`) — imposé par
  ib_async non thread-safe. Chaîne 75 s, fondamentaux 90 s, scan 45 s,
  cotations 45 s **se sérialisent** derrière lui.
- `/api/pos-quotes` : cache TTL 45 s ; au-delà, la requête UI **bloque
  jusqu'à 45 s** derrière la file — mesuré 20/33/56 s dans les commentaires
  du code. Une cotation vieille de 46 s existe pourtant en mémoire et
  vaudrait mieux, étiquetée, qu'une attente.
- Le repli hors-broker (`completer_par_repli` + mid du board) existe et est
  étiqueté SECONDARY — conservé tel quel.

## Décisions

1. **Servir le périmé, étiqueté** : entre TTL et 20×TTL (la purge), la
   cotation en cache part immédiatement avec `stale` + âge ; un
   rafraîchissement part en arrière-plan (thread détaché sur la même file).
2. **Clé jamais cotée** : attente bornée **12 s** (au lieu de 45) puis repli
   honnête existant. C'est la dette résiduelle, déclarée.
3. La réponse porte `stale: [clefs]` — l'UI peut étiqueter ; aucun champ
   existant ne change.

## Hors lot, et dit

La refonte de la file unique (un worker par domaine, coalescence, circuit
breakers) et les snapshots atomiques complets : c'est le vrai corps du lot 6
du programme, qui exige un banc de charge — consigné comme dette
d'architecture, pas absorbé dans cette tranche.

## Fichiers autorisés

`vertex/app/routes/desk.py` · `tests/test_pos_quotes_lot06.py` (neuf) ·
`docs/vertex-2-0/lot-06/**`.

## Tests

Rouge d'abord : cache périmé + worker lent → la route répond immédiatement
avec la valeur étiquetée. Clé absente → borne 12 s. Suite complète.

## Rollback

Revert — le comportement bloquant revient.
