# Lot 40 — Refonte de la file worker IBKR (RAPPORT)

Date : 2026-08-28 · Le « vrai corps du lot 6 », consigné comme dette
d'architecture depuis le lot 25.

## Constat (mesuré au lot 6, toujours vrai avant ce lot)

Un seul worker IBKR (imposé par ib_async, non thread-safe) derrière une
FIFO nue : chaîne 75 s, fondamentaux 90 s, scan 45 s, news 40 s et
cotations du desk (12 s de patience) se sérialisaient dans l'ordre
d'arrivée. Quatre défauts distincts :

1. une cotation UI attendait un lot de fondamentaux de 90 s ;
2. deux demandes identiques coûtaient deux jobs courtier ;
3. un job dont le demandeur avait abandonné (timeout échu) s'exécutait
   quand même — du temps courtier payé pour personne ;
4. en panne de connexion, CHAQUE job re-sondait tous les ports
   (6 s × ports × jobs en attente) avant de rendre None.

## Livré

`vertex/services/file_ibkr.py` — file PURE (horloge injectable, zéro
dépendance ib_async), consommée par le worker unique de `terminal.py` :

- **Priorités par domaine** : posq (0) < meta (1) < chain (2) <
  news/scan (3) < fund (4) — FIFO conservée à priorité égale. La cotation
  du desk double les lots de fond.
- **Coalescence** : une demande identique en vol (en file OU en cours)
  s'attache au job existant ; un seul appel courtier, résultat partagé.
- **Péremption** : chaque dépôt porte `expire = now + timeout` (une
  attache prolonge) ; le worker solde sans exécuter tout job échu — plus
  aucun travail pour des demandeurs partis.
- **Circuit breaker de connexion** : un échec de `conn()` ouvre une
  fenêtre de 30 s pendant laquelle les jobs rendent None immédiatement ;
  fenêtre échue, UN essai repart (demi-ouvert) et son issue referme ou
  rouvre.

Contrat de `_opt_job(kind, args, timeout)` inchangé (None au timeout) —
aucune route modifiée, le worker reste UNIQUE.

## Hors périmètre du code, réglé au passage

- `tests/test_js_syntax_sweep_lot182.py` et `test_static_js_assets_lot186.py`
  échouaient en rouge sur une machine sans node : ils SKIPPENT désormais en
  le disant (« node absent — parse JS impossible ici »). Les environnements
  outillés continuent de mesurer.
- Résidu de workspace du package personnel legacy (`__pycache__` de
  bytecode laissé par d'anciennes branches) supprimé — il faisait mentir
  le gardien du namespace.

## Preuves

- Banc du lot : `tests/test_file_ibkr_lot40.py` — 13 bancs (priorités,
  FIFO à priorité égale, coalescence file ET partage de résultat entre
  threads, non-coalescence de clés différentes, libération de clé,
  péremption, prolongation par attache, breaker ouvert/demi-ouvert/refermé,
  intégration terminal). Rouge d'abord (module absent), vert ensuite.
- Suite complète : **4415 passés · 173 ignorés · 0 échec** (231 s).
- Runtime (live IBKR, TWS 7496, compte réel lecture seule) :
  `demo=false`, `/api/pos-quotes` répond en **26 ms**, aucun traceback,
  le scan tourne (jobs `scan`/`fund`/`chain` traités par la file).

## Dette résiduelle (dite, pas absorbée)

- Snapshots atomiques complets de l'état scan (l'autre moitié du lot 6
  historique) — exige un banc de charge dédié.
- Le banc de charge lui-même (saturation de la file, mesure des latences
  par priorité sous contention) reste à construire.

## Rollback

Revert du lot — la FIFO nue revient, avec ses quatre défauts.
