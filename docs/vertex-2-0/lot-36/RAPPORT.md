# Lot 36 — Strangler : la couche pages morte de terminal.py est retirée (−4650 lignes)

## Problème

La dette nommée « doubles écrivains myRecos/myFavs/myNotes de terminal.py »
cachait un fait plus grand, mesuré au runtime : **la totalité de la couche
pages de terminal.py était morte**.

- Les 5 gabarits bruts (`PAGE_DAILY`, `PAGE_WATCHLIST`, `PAGE_OPTIONS_DESK`,
  `PAGE_ME`, `PAGE_ENTREPRISES`) et les 7 pages `_vpage` (`/settings`,
  `/review`, `/research`, `/health`, `/heatmap`, `/equipe`, `/bordel`)
  n'étaient renvoyés par **aucune route** : `/`, `/daily`, `/watchlist`,
  `/entreprises`, `/options-desk` et les 7 hubs appartiennent tous à
  `vertex.app.routes.redesign` (pages 2.0 ou redirections 301) — mesuré sur
  `app.url_map`.
- AST : **zéro référence** aux 46 noms de la couche depuis le code vivant.
- Les modules `vertex/ui/{nav, home_art, sync_center, vx_kit, design_system}`
  et `recommendation` (alias `_reco`) n'alimentaient QUE cette couche depuis
  terminal.py ; la coque 2.0 servie charge vx-core/vx-entities/vx-shell.
- Conséquence : les « doubles écrivains » étaient inatteignables — le **seul
  écrivain servi** de myRecos/myFavs/myNotes est `vx-entities.js`.

## Changement

Coupe des lignes 2532–7182 de terminal.py (gabarits + machinerie `_extract`,
`_inject_single_nav`, `_inject_vx`, `_vpage`, `_hub_tabs`, blocs nav/kit/scatter)
remplacées par une pierre tombale documentée, et retrait des 6 imports morts.
**7374 → 2724 lignes.** Le code vivant (API, scan, boucles, alertes,
`live_state_api`) est intact — la coupe suit la frontière AST exacte.

Les modules orphelins (`nav`, `home_art`, `sync_center`, `vx_kit`,
`design_system`, `signals`) restent en place : leur retrait est un lot dédié
avec ses propres preuves de convergence (règle : jamais deux chantiers
couplés dans une PR).

## Bancs réécrits vers la vérité nouvelle (jamais neutralisés)

- `test_strangler_couche_pages_lot36.py` (nouveau, né rouge 3/4) : la couche
  ne ressuscite pas, les imports morts non plus, les routes héritées
  redirigent, les 12 pages servent HTTP 200.
- `test_nav.py` : nav inline interdite dans terminal.py ; invariants de forme
  de nav.py conservés.
- `test_script_concatene_lot374.py` : le gardien du `<script>` concaténé de
  `_vpage` n'a plus de support — il garde l'équilibre des balises sur les
  pages SERVIES, les 301 hérités, et interdit le retour de l'assemblage brut.
- `test_live_engine.py`, `test_home_art_lot181.py`, `test_production.py`,
  `test_js_syntax_sweep_lot182.py`, `test_full_system_integration.py` :
  chaque épingle sur le tissu mort remplacée par l'assertion inverse
  (« n'existe plus ») ou déplacée sur la surface réellement servie
  (base.css pour focus-visible/reduced-motion).

## Preuves

- Suite complète : **4428 passés · 152 ignorés · 0 échec**.
- Runtime DEMO : les 12 pages 2.0 → HTTP 200, coque présente, console vide,
  `/api/client-log` = 0 ; les 6 routes héritées sondées → 301 vers leurs
  propriétaires 2.0.
- Aucun octet de `/static` ne change (gardien d'empreinte SW vert, restauré
  au lot 35) — aucun bump SW nécessaire : terminal.py ne sert plus de HTML.

## Rollback

`git revert` du commit unique — la couche revit à l'identique (elle était
inerte, le revert l'est aussi).
