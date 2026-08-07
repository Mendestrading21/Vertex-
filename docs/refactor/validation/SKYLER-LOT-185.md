# SKYLER V2 — LOT 185 : cartographie de mort — volet fonctions

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-185`
(base : `integration/vertex-skyler-v2` @ `dbd22e0`, lot 184 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié — RIEN supprimé.

## 1. CONSTAT (clôture de la cartographie 183-185)

Méthode PRUDENTE (un doute = vivant) : racines vivantes = fonctions
décorées, référencées au niveau module (threads/assemblages), vues
Flask actives, références externes de production ; propagation par
les références internes.

```text
91 fonctions top-niveau dans terminal.py : 62 VIVANTES (dont les 9
boucles de fond _loop/_opt_loop/_radar_loop/_news_loop/_cal_loop/
_fund_loop/_edge_loop/_weekly_loop/_indices_loop — garde
anti-faux-positif vérifiée), 29 MORTES (62 lignes seulement) :
presque toutes des STUBS de vues legacy (≤ 4 lignes, `return
PAGE_*`/redirect/render migré) + _rail (lot 184) +
_legacy_pages_redirect (remplacé par redesign). Aucune logique
métier morte — le poids mort de terminal.py est essentiellement
les BLOBS (lots 183/184), pas les fonctions.
```

BILAN FINAL de la cartographie de mort de terminal.py (183+184+185) :
25 pages (~2 265 l) + 35 couches JS/CSS + 29 fonctions stubs
(62 l) + _vpage assembleur — morts, orphelins, inventaires figés par
tests. La PURGE (≈ 25-30 % du monolithe) serait sûre au regard des
routes et références — décision humaine explicite requise (question
ouverte au STATUS depuis le lot 183).

## 2. Ce qui est figé (`tests/test_dead_functions_lot185.py`, 5 tests)

```text
Inventaire EXACT des 29 fonctions mortes (ressusciter/supprimer =
  mise à jour explicite) ; les 9 boucles de fond CLASSÉES VIVANTES
  (la cartographie ne condamne jamais un travailleur de fond) ;
  chaque morte est un stub ≤ 4 lignes retournant une PAGE_* morte,
  une redirection ou un render migré — jamais de la logique ;
  aucune morte n'est un endpoint actif (recoupement inverse) ;
  poids mort fonctions chiffré : 62 lignes exactement
```

## 3. Preuves

```text
python -m pytest tests/test_dead_functions_lot185.py -q → 5 passed
python -m pytest tests/ -q → 2445 passed, 2 skipped (2440 + 5)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

Tranche 181-185 TERMINÉE (mini-bilan dans STATUS.md). LOT 186 :
nouvelle direction au survey — ou, avec accord humain explicite, le
LOT DE PURGE des inventaires morts de terminal.py.
