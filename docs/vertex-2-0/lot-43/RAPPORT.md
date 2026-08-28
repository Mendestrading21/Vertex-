# Lot 43 — Mémoire datée des refus fournisseur (RAPPORT)

Date : 2026-08-28 · Choisi sur mesure runtime (session live du jour), pas
sur intuition.

## Constat (mesuré)

Le journal du serveur montrait, à CHAQUE cycle de fondamentaux, les mêmes
refus : « Aucune définition de titre » (IBKR) et HTTP 404 (yfinance) sur des
titres morts de l'univers — rachetés (JNPR, ANSS…), renommés, radiés.
`_fund_loop` les voyait « manquants » pour toujours :

1. mêmes symboles redemandés aux DEUX fournisseurs à chaque cycle — bruit
   de log permanent, quota gaspillé ;
2. `batch = missing[:40]` : le cache plein, le lot n'était plus composé QUE
   de morts ;
3. `still_missing` restait vrai à vie → la boucle tournait **toutes les
   45 s pour l'éternité** au lieu de se calmer à 6 h.

## Livré

`vertex/services/refus_fournisseur.py` — `MemoireRefus`, module PUR
(horloge injectable) :

- un refus est **daté**, jamais définitif : TTL 24 h, puis on réessaie (un
  ticker peut renaître — IPO, re-listing) ;
- `filtrer` partitionne sans perdre personne ; la casse est normalisée ;
- **écarté ≠ oublié** : `etat()` nomme chaque écarté et son âge, exporté
  dans `scan_state['fund_refus']` — l'interface peut le dire.

`_fund_loop` : consulte la mémoire avant de composer son lot, note tout
symbole que les deux fournisseurs ont laissé vide, exporte l'état, et
`still_missing` ignore les refus récents — le rythme se calme réellement.

## Preuves

- `tests/test_refus_fournisseur_lot43.py` — 10 bancs (TTL, réessai après
  échéance, partition, casse, état daté, oubli des échus, TTL par défaut,
  et 4 gardiens d'intégration sur `_fund_loop`). Rouge d'abord, vert après.
- Suite complète : **4437 passés · 173 ignorés · 0 échec**.

## Dette résiduelle (dite)

La mémoire vit en RAM : un redémarrage refait UNE tentative sur les morts
(45 s de bruit, une fois) avant de les re-dater. La persister dans un cache
disque n'a pas été fait ici — le gain (silence au premier cycle) ne vaut un
fichier de plus que si les redémarrages deviennent fréquents.
