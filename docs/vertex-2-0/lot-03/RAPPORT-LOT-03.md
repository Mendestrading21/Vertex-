# Rapport — Lot 3 · Portefeuille manuel souverain

## Le défaut trouvé, et corrigé

Deux portes déclarent une position ; elles n'écrivaient pas le même objet.

Le modal 2.0 ne demandait **ni objectif, ni devise, ni stratégie, ni frais**.
Or `positions/models.py` lit `snap.tgt || myTgt` pour `tp1` : une position
déclarée depuis le 2.0 n'avait **jamais** d'objectif, dans tout le pipeline —
et sa devise était un USD implicite, ce que le contrat interdit (une valeur
non saisie n'est pas une valeur).

Le schéma historique du desk est le propriétaire canonique (le skill interdit
un modèle parallèle). Le formulaire 2.0 est monté à parité : il demande
objectif, devise, stratégie et frais, et écrit `myStop`/`myTgt`/`target1`/
`fees`/`currency`/`strategy` **et** `entrySnap.{stop,tgt,date}` — les deux
chemins que les lecteurs consultent, dans le même ordre que le legacy.

## Preuves

- gardien `tests/test_declaration_position_lot03.py` — **rouge d'abord**
  (2 échecs mesurés), vert après ;
- **preuve navigateur** : position déclarée via le vrai modal sur `/portfolio`,
  relue depuis `localStorage.myTrades` :
  `{sym NVDA, qty 10, cost 5000, entryPrice 500, myStop 450, myTgt 600,
  target1 600, fees 2.5, currency CHF, strategy 'swing 6 sem.'}` +
  `entrySnap {stop, tgt, date}` ;
- matrice des propriétaires des 17 clés publiée
  (`MATRICE-PROPRIETAIRES-DESK.md`), avec sa lecture honnête : le
  double-écrivain caché de `vx_kit`, les trois doubles legacy restants
  (lot 9), les cinq clés dormantes (décision humaine).

## Préservé

Aucune migration : les positions existantes gardent leur forme, les lecteurs
tolèrent l'absence des nouveaux champs (`_f(...) → None`). Le changement
n'affecte que les écritures futures. `desk_data.json` intouché.

## Rollback

Revert du commit. Les positions écrites entre-temps portent des champs
supplémentaires que tous les lecteurs actuels savent lire (superset).

## Prochain lot

Lot 4 — sécurité privée et exposition (démarrage non-loopback, CSRF, headers).
