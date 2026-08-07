# SKYLER LOT 222 — Responsive 390px : 2 débordements RÉELS du topbar trouvés et soldés

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-222` (base : lot 221 fusionné)

## Objet

Spot-check responsive 390 px EN NAVIGATEUR sur les 8 espaces :
débordement horizontal du document + éléments visibles dépassant le
viewport à droite (hors conteneurs à scroll interne voulu et hors
off-canvas cachés — sidebar/drawer/modal exclus par aria-hidden).

## Mesure (avant correctif)

- `overflowX` document : **0 sur les 8 pages** (le body ne scrolle
  jamais horizontalement — les gardes existantes tiennent) ;
- MAIS 2 dépassements réels d'éléments visibles, découverts en
  discriminant gauche off-canvas (voulu) / droite (défaut) :
  1. **/tracking** : le crumb « Approfondissement du Portefeuille »
     (nowrap, 213 px) finissait à **433 px** — texte passant SOUS les
     boutons du topbar puis coupé ;
  2. **/portfolio en NAVIGATION** (défaut intermittent reproduit en
     visitant 3 pages avant) : le libellé du bouton retour (nowrap,
     155 px) poussait le cluster droit à **403 px** — bouton refresh
     coupé de 13 px. Invisible en visite directe (bouton retour
     caché), d'où l'intermittence.

## Correctif minimal — `responsive.css`, bloc ≤768 px (scopé mobile/tablette)

```css
.vx-breadcrumb{flex:1 1 0;overflow:hidden}
.vx-breadcrumb>*{min-width:0;overflow:hidden;text-overflow:ellipsis}
.vx-back-btn{min-width:0}
.vx-back-btn span{min-width:0;overflow:hidden;text-overflow:ellipsis}
```

Le fil d'Ariane et le libellé retour tronquent en ellipse au lieu de
passer sous les boutons. Aucun changement desktop (>768 px).

## Vérification (après)

- Contexte défaillant rejoué (/portfolio après 3 pages) : bouton
  retour tronqué à 130 px, cluster droit à **378 px ≤ 390** ✔ ;
- balayage complet des 8 pages : **0 dépassement droit partout**,
  0 erreur console ;
- captures avant/après envoyées (/tracking + /portfolio).

## Décision SW

**Bump `td-shell-v171` → `td-shell-v172`** + les 5 gardiens : le CSS
du shell change et le correctif doit se déployer (doctrine : bump car
changement visible).

## Preuves

- Suite complète : **2482 passed / 2 skipped** (gardiens SW mis à
  jour, aucun test ajouté — le défaut est de géométrie navigateur,
  hors de portée de pytest).

## Suite

LOT 223 : entretien suivant ou directive. Purge terminal.py toujours
EN ATTENTE d'accord humain explicite.
