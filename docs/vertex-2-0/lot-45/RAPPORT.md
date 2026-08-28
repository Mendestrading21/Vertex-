# Lot 45 — Les rows publiés sont immuables : le board republie une copie

## Problème (dette nommée au lot 42)

Deux sites mutaient la liste `rows` DÉJÀ publiée dans `scan_state` :

1. `_publish_board` (boucle options) : `_attach_vehicle(scan_state['rows'])`
   injectait le verdict véhicule dans les dicts publiés, et posait
   `options_board` / `options_as_of` / `option_tracking_snapshot` par
   écritures à l'unité — un lecteur pouvait voir un board sans horodatage,
   ou son snapshot du cycle précédent changer sous ses yeux.
2. Le chemin démo de `_scan_once` remutait `rows` APRÈS la publication
   partielle (verdict véhicule sur le board synthétique).

## Correctif

- `_publish_board` : bloc unique `{options_board, options_as_of,
  option_tracking_snapshot, rows}` passé à `_publier` — atomique, MÊME cycle
  (génération et phase conservées : un refresh de board n'est pas un nouveau
  scan) ; le verdict est attaché sur une **copie ligne à ligne** des rows,
  l'objet déjà publié reste figé.
- Chemin démo : `rows = [dict(r) for r in rows]` avant `_attach_vehicle`,
  copie republiée dans le bloc démo (`'rows': rows`).
- Vérifié : le reste de `_scan_once` ne fait que LIRE `rows` après ces
  points (recommandations, stratégie, comité — aucune écriture dans `r`).

Pas de bump SW : terminal.py ne sert aucun octet navigateur.

## Preuves

- `tests/test_rows_publies_immuables_lot45.py` — 3 bancs nés rouges :
  l'objet publié avant reste figé + la republication porte le verdict sur
  une NOUVELLE liste + même cycle (gen/phase) ; plus d'écriture à l'unité
  dans `_publish_board` (statique) ; le chemin démo copie et republie
  (statique).
- Suite complète : **4467 passés · 152 ignorés · 0 échec**.

## Dette résiduelle (dite)

Les moteurs amont (daily, anomalies, sectors) reçoivent encore les listes
publiées en lecture ; les figer structurellement (tuples/MappingProxy) est
le dernier cran du programme « snapshots immuables » et changerait les
signatures — passage dédié si un défaut de lecture est un jour mesuré.

## Rollback

git revert du commit unique.
