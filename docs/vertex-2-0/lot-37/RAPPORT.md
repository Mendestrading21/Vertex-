# Lot 37 — Cleanup prouvé : dix modules UI orphelins retirés

## Problème

Après le retrait de la couche pages de terminal.py (lot 36), dix modules de
`vertex/ui/` n'avaient plus UN SEUL consommateur de production :

`nav.py`, `home_art.py`, `sync_center.py`, `vx_kit.py`, `design_system.py`,
`signals.py`, `journal.py`, `options_lab.py`, `strategy_os.py`, `vault.py`.

Preuves relevées AVANT suppression (règle de convergence) :
- **imports** : grep sur vertex/ + terminal.py — zéro import de production
  (seuls des bancs de caractérisation les importaient) ;
- **routes** : toutes les URL héritées (/vault, /archive, /strategy-os,
  /signals…) appartiennent à `vertex.app.routes.redesign` — pages 2.0 ou 301 ;
- **capacités** : chaque capacité a un propriétaire canonique SERVI —
  navigation → `vertex/ui/shell` ; desk/entités (DESK_KEYS, journal, suivis,
  favoris, notes, vault, alertes) → `vx-entities.js` (+ repli inline
  system_page, égalité gardée) ; design system → `vertex-2-0.css` +
  `pages/design_system_page.py` ; stratégie → `strategy_os_api` + pages 2.0 ;
  synchronisation → `live-updates.js` + `/api/live/*` ;
- **données** : aucun de ces modules ne possédait de données (générateurs de
  chaînes JS/CSS) ; les clés localStorage qu'ils citaient restent servies par
  vx-entities.js (ancre littérale des 17 clés désormais dans
  test_production) ;
- **rollback** : git revert du lot.

Le lot 381 avait déjà mesuré le danger de l'ancien montage : les gardiens des
clés de sync s'ancraient sur `vx_kit.py`, module **jamais servi** (0/8 pages).

## Changement

- Suppression des dix fichiers (`git rm`).
- 11 bancs remaniés vers la vérité servie, jamais neutralisés :
  - `test_ui_orphelins_retires_lot37.py` (nouveau, né rouge) : les modules ne
    ressuscitent pas, personne ne les importe, les URL héritées redirigent,
    vxVault reste dans le contrat servi ;
  - `test_production` : l'ancre littérale des 17 clés comparée à
    `vx-entities.js` (le SERVI), plus aucune référence à vx_kit/journal ;
  - `test_desk_keys_servies_lot381`, `test_redesign_ui`,
    `test_strategy_os_final_guards` : repointés sur vx-entities.js ;
  - `test_nav`, `test_journal_page`, `test_strategy_os_routes`,
    `test_live_engine`, `test_js_syntax_sweep_lot182` : la partie module
    remplacée par la vérité 2.0 (coque, 301, API) ;
  - `test_vault.py` et `test_home_art_lot181.py` supprimés AVEC leurs modules
    (leurs vérités survivantes — 301 de /vault et /archive, schéma vxVault —
    déplacées dans le banc lot 37) ; retraits signalés dans les documents
    vivants (gardien lot 364 vert).
- `vx-entities.js` : le commentaire « MIROIR EXACT de __DESK_KEYS
  (terminal.py) » (périmé — terminal n'a plus de liste) devient « SOURCE
  UNIQUE servie du contrat desk ». SW v276 → **v277** + épingles + empreinte.

## Preuves

- Suite complète : **4414 passés · 152 ignorés · 0 échec**.
- Runtime DEMO : pages 200, coque présente, console vide, client-log 0.
- `vertex/ui/` ne contient plus que la surface vivante : `shell/`, `pages/`,
  `vx2.py`, `__init__.py`.

## Rollback

`git revert` du commit unique restaure modules et bancs à l'identique.
