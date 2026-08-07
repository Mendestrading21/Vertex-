# SKYLER V2 — LOT 183 : vérification de vie des pages legacy

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-183`
(base : `integration/vertex-skyler-v2` @ `8636daf`, lot 182 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié — RIEN supprimé.

## 1. CONSTAT STRUCTUREL (décision humaine requise pour agir)

Par introspection des vues Flask ACTIVES (url_map + co_names) :

```text
Les 25 blobs PAGE_* de terminal.py (~2 265 lignes de HTML/JS, plus
leurs chaînes CSS/JS associées) ne sont plus servis par AUCUNE route
active. La refonte (vertex/ui/pages + redesign.py) a tout repris ;
les 39 anciennes URLs (/daily, /strategie, /watchlist, /vault,
/options-desk, /ma-page, /brief…) redirigent toutes vers les 8
espaces canoniques (/, /markets, /opportunities, /portfolio,
/analysis, /journal, /intelligence, /system). Aucun module de
vertex/ n'importe terminal.PAGE_* — mortes ET orphelines.
```

Conséquence pratique : ces ~2 265+ lignes sont du POIDS MORT dans le
monolithe (allongent l'import, le grep, la maintenance). La
SUPPRESSION serait sûre au regard des routes — mais c'est une
décision humaine explicite (hors périmètre de ce lot, conformément
au canevas). Note : la « couche artistique » (lot 181) s'applique à
PAGE_DAILY/PAGE_STRATEGIE — donc à des chaînes mortes ; ses tests de
câblage restent valides en tant que caractérisation des chaînes.

## 2. Ce qui est figé (`tests/test_legacy_pages_life_lot183.py`, 5 tests)

```text
Inventaire EXACT des 25 pages mortes — ressusciter (re-router) ou
  supprimer une page doit mettre à jour l'inventaire, jamais un
  changement silencieux ; aucune vue active ne référence un PAGE_*
Orphelines — aucun module de vertex/ n'importe terminal.PAGE_*
Redirections — les 39 URLs legacy redirigent (301/302/308) vers leur
  cible EXACTE ; les destinations = les 8 espaces canoniques et rien
  d'autre, toutes répondent 200 (aucun vieux lien ne tombe dans le
  vide) ; aucune cible n'est elle-même une URL legacy (pas de
  chaînes de redirections)
```

## 3. Preuves

```text
python -m pytest tests/test_legacy_pages_life_lot183.py -q → 5 passed
python -m pytest tests/ -q → 2435 passed, 2 skipped (2430 + 5)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 184 : candidats — vx_kit/DESK_KEYS (règle n°1, vérifier le
gardien existant), ou nouvelle direction. MINI-BILAN 181-185 au
lot 185. Question OUVERTE pour l'utilisateur : autoriser un futur
lot de PURGE des 25 pages mortes de terminal.py (~2 265 lignes) ?
