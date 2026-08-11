# SKYLER LOT 359 — `/analysis` : la seule page servie que les gardiens JS ne voyaient pas

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-359` (base : lot 358 fusionné,
82f3a3a)

## Piste calibrée

Le lot 358 a montré qu'une règle critique peut décrire correctement **une**
famille et ignorer l'autre. Même question appliquée à la **règle n°2** (« tout
JavaScript généré depuis Python doit être syntaxiquement valide — deux
SyntaxError silencieuses ont déjà vécu ») : ses gardiens (lots 182 et 186)
travaillent sur une **liste de routes figée**. Cette liste couvre-t-elle encore
les pages réellement servies ?

## Mesure — inventaire complet de l'`url_map`

Chaque règle GET sans paramètre, hors préfixes d'API, appelée **sans suivre les
redirections** : seul un `200 text/html` est une page servie.

```text
40 routes hors liste  →  301 vers une page canonique (/analyse, /vault,
                          /watchlist, /settings, /sectors, /performance…)
PAGES HTML 200 SERVIES ET NON GARDÉES : 1
  /analysis              22 248 o · 2 bloc(s) JS inline
```

**Un seul trou, précis.** `/analysis` (index) est rendu par
`analysis_page.render_index()` — une fonction **distincte** de
`analysis_page.render(sym)` qui sert `/analysis/<sym>`. Les gardiens listaient
`/analysis/AAPL` et pas `/analysis` : les **2 blocs `<script>` inline** de la
page d'accueil d'Analyse n'ont jamais été passés au parseur, et ses liens
d'assets jamais vérifiés (gardien 186).

`/analysis` est par ailleurs bien testée ailleurs (`test_continuity_shell`,
`test_redesign_ui`, `test_ui_v3`, `test_full_system_integration`…) : le trou
portait précisément sur la **syntaxe JS** et les **liens d'assets**, rien
d'autre. C'est aussi l'une des 8 pages de la référence smoke — d'où l'intérêt.

## Correction

Ajout de `/analysis` aux deux listes de routes :
`tests/test_js_syntax_sweep_lot182.py` et
`tests/test_static_js_assets_lot186.py`, avec la note d'audit expliquant
pourquoi elle manquait et que les 40 autres routes hors liste sont des 301.

## Preuve ROUGE — le bug historique, rejoué

Injection dans le JS de `render_index` de la faute exacte que la règle n°2
décrit : une apostrophe française non échappée dans une chaîne JS simple
(`'Aucun titre consulté récemment.'` → `'…aujourd'hui.'`).

```text
NOUVELLE liste (avec /analysis) : ROUGE OK — la faute est attrapée
ANCIENNE LISTE : 0 erreur(s)
restauration : identique
```

L'ancienne liste est **totalement aveugle** à la faute ; la nouvelle l'attrape.
Fichier restauré MD5 identique. C'est la démonstration que l'ajout n'est pas
cosmétique : une troisième SyntaxError silencieuse aurait pu vivre sur cette
page.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 358, 82f3a3a) ; arbre propre.
- Suite complète : **2506 passed / 2 skipped** — verte (le balayage couvre
  désormais 17 routes au lieu de 16, et 14 au lieu de 13 pour les assets).

## Décision SW

**Pas de bump** (`td-shell-v187`) : aucun octet servi n'a changé — le lot ne
touche que `tests/` et `docs/`.

## Portée — ce que ce lot ne prétend pas

Aucune faute de syntaxe n'existait : `/analysis` parse correctement aujourd'hui.
Le lot ferme une **fenêtre de non-détection**, il ne répare rien. L'audit porte
sur les routes **sans chaîne de requête** ; les variantes `?view=…` (vers
lesquelles les 301 pointent) partagent le même squelette de page mais n'ont pas
été balayées séparément — piste possible pour un lot ultérieur. Les routes
`/memory/<id>` et `/memory/cell/<g>/<k>` servent du HTML mais exigent un
identifiant réel (404 avec un identifiant factice) : non couvertes, signalé.

## Suite

LOT 360 : checkpoint périodique complet (serveur DEMO + smoke + MD5 des 8 pages
+ bilan de la tranche 350-359).
