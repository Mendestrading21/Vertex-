# Lot 42 — Publications atomiques générationnées du scan (RAPPORT)

Date : 2026-08-28 · Seconde dette du lot 6 historique (« snapshots
atomiques »), dite aux rapports des lots 40/41.

## Constat

`_scan_once` écrivait dans `scan_state` par petites touches entre ses deux
grandes publications : `titres_en_echec`, board d'options démo,
`analytics_packets`, `reconciliation_by_symbol`, `strat_tilt`, et les deux
chemins d'erreur posaient leurs clés une à une. Les routes Flask lisent le
même dict depuis d'autres threads : un lecteur pouvait observer des `rows`
d'une génération et des dérivés d'une autre — état déchiré, indétectable.

## Livré

- `_publier(etat, phase, gen, bloc)` : UNE publication = UN `dict.update`
  C-level (aucun entrelacement de bytecode entre les clés d'un bloc),
  estampillé `scan_gen` (génération monotone) + `scan_phase`
  (`partiel` → `complet` ; `erreur`).
- `_scan_once` ne pose plus AUCUNE clé à l'unité : publication anticipée
  (cockpit) et publication complète regroupent tout ; les dérivés
  (`analytics_packets`, `reconciliation_by_symbol`, `strat_tilt`,
  `titres_en_echec`) voyagent avec le bloc `complet` — même génération que
  les `rows` dont ils dérivent. Les chemins d'erreur publient d'un bloc.
- `_generation` sans repli chiffré en except (invariant lot 385) : un
  `scan_gen` corrompu repart par typage.
- Le marquage démo (`source: 'demo'`) devient une clé des blocs publiés —
  même invariant, forme saine (gardien lot 391 mis à jour en ce sens).
- Recensement lot 386 : 34 → 33 `except: pass` — celui du tilt stratégie
  est remplacé par une reprise EXPLICITE de la valeur précédente (la
  publication par blocs ne permet plus l'omission silencieuse).

## Gardiens (`tests/test_scan_publication_lot42.py`)

AST : zéro `scan_state[...] =` dans `_scan_once`, zéro `update` direct hors
`_publier`, les trois phases présentes, les dérivés dans le bloc complet ;
comportement : estampillage gen/phase, génération monotone.

## Preuves

Suite complète : **4427 passés · 173 ignorés · 0 échec**.

## Dette résiduelle (dite)

Les OBJETS publiés restent partagés (les listes `rows` sont mutées en place
par `_attach_vehicle` avant publication — et en démo une fois après) : le
programme « snapshots immuables » complet exigerait de figer les structures.
Les publications étant désormais générationnées, un lecteur peut au moins
détecter le mélange — c'était impossible avant.
