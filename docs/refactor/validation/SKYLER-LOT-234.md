# SKYLER LOT 234 — Menu contextuel d'entité : constat comportemental + vérif READONLY (0 défaut)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-234` (base : lot 233 fusionné)

## Objet

Le DERNIER composant interactif jamais testé en navigateur : le menu
contextuel d'entité (`data-entity-menu` → `VXEntities.openMenu`),
avec une vérification READONLY explicite — aucune action d'ORDRE ne
doit y figurer.

## Calibrage préalable (lui-même instructif)

Les déclencheurs `[data-entity-menu]` vivent dans le DOM HYDRATÉ de
`/` (3), `/markets` (20) — pas sur /opportunities en démo à 1440 (les
lignes du radar utilisent d'autres délégués). Le test s'exécute sur
`/` (déclencheur réel : bouton ACN).

## Protocole et résultat — 0 défaut

| Étape | Mesuré |
|---|---|
| Clic sur le déclencheur ACN | menu ouvert (data-open=1), **11 actions**, focus DANS le menu, menu entièrement dans le viewport ✔ |
| Flèches ↓↓ | data-active suit (idx 2), focus sur l'item actif ✔ |
| Clic hors du menu | fermé (data-open=0) ✔ |
| **READONLY** | **0 action d'ordre** — balayage des libellés contre {acheter, vendre, ordre, buy, sell, transmettre, passer} → vide ✔ |
| Erreurs console | 0 ✔ |

Les 11 actions : Ouvrir l'analyse · Ajouter aux favoris · Ajouter à la
watchlist · Créer un suivi · Créer une alerte · Ajouter une position ·
Ouvrir les options · Ajouter une note/thèse · Ouvrir le journal ·
Copier le ticker · Ouvrir TradingView. Classification honnête :
« Ajouter une position » est un ENREGISTREMENT au journal personnel
(localStorage/desk sync) — pas un ordre ; l'invariant READONLY est
respecté jusque dans le vocabulaire du menu.

Avec ce lot, TOUS les composants interactifs du shell sont prouvés en
conditions réelles : drawer + modal (229), palette (231), menu
contextuel (234).

Aucun correctif nécessaire — **constat honnête, aucun code touché**.

## Décision SW

**Pas de bump** (`td-shell-v173` inchangé) : constat pur.

## Preuves

- JSON du parcours complet dans ce rapport.
- Suite complète : **2486 passed / 2 skipped** (référence maintenue).

## Suite

LOT 235 : MINI-BILAN 231-235. Purge terminal.py toujours EN ATTENTE
d'accord humain explicite.
