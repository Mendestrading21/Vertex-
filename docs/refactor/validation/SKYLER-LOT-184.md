# SKYLER V2 — LOT 184 : vie/mort des couches JS/CSS du monolithe

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-184`
(base : `integration/vertex-skyler-v2` @ `b560cdd`, lot 183 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié — RIEN supprimé.

## 1. CONSTAT (extension du lot 183)

Par analyse AST de terminal.py + recoupement empirique sur les pages
servies :

```text
Les 35 chaînes de couche (_*_JS/_*_CSS : _BASE_CSS, _HEATMAP_JS,
_SI_JS, _TRADES_JS, _DESK_COCKPIT_JS…) ne nourrissent QUE les 25
pages mortes du lot 183 : chaque assignation module-niveau qui les
consomme vise une PAGE_* morte ou une autre couche ; les seuls
helpers qui les touchent sont _vpage (20 appels, tous au niveau
module, tous assignés à des PAGE_* mortes) et _rail — qui n'est
lui-même appelé NULLE PART (helper mort). Empiriquement, les
marqueurs signés de ces couches (hmHost du heatmap, artBoard de la
couche artistique) n'apparaissent dans AUCUNE des pages réellement
servies.
```

Bilan cumulé du poids mort de terminal.py (lots 183+184) : 25 pages
(~2 265 l) + 35 couches + 2 helpers — la purge reste une DÉCISION
HUMAINE (question ouverte au STATUS depuis le lot 183).
Note : la caractérisation home_art (lot 181) reste valide en tant
que caractérisation de chaînes — leur seule consommation est morte.

## 2. Ce qui est figé (`tests/test_legacy_layers_life_lot184.py`, 5 tests)

```text
Inventaire EXACT des 35 couches — en ajouter/retirer une = mise à
  jour explicite ; aucune couche utilisée dans une fonction sauf les
  assembleurs (_vpage, _rail) ; toutes les cibles d'assemblage sont
  mortes (PAGE_* du lot 183 ou autres couches) ; _vpage → 20 pages
  mortes exclusivement, _rail appelé nulle part ; recoupement
  empirique : hmHost/artBoard absents des 11 pages servies
```

## 3. Preuves

```text
python -m pytest tests/test_legacy_layers_life_lot184.py -q → 5 passed
python -m pytest tests/ -q → 2440 passed, 2 skipped (2435 + 5)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 185 : dernier lot de la tranche + MINI-BILAN 181-185 obligatoire
(181 home_art, 182 gardien JS global, 183 vie/mort pages, 184
vie/mort couches, 185 à livrer). Candidat naturel : compléter la
cartographie de mort de terminal.py (fonctions Python jamais
appelées ?) ou nouvelle direction.
