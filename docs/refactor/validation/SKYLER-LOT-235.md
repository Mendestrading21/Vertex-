# SKYLER LOT 235 — MINI-BILAN 231-235 (le shell interactif prouvé de bout en bout)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-235` (base : lot 234 fusionné)

## MINI-BILAN de la tranche 231 → 235 (5 lots, PR #264 → #268)

| Mesure | Avant (fin lot 230) | Après (fin lot 235) |
|---|---|---|
| Tests verts | 2486 / 2 skipped | **2486 / 2 skipped** (stable) |
| Service worker | v173* | **v173** — 1 seul bump dans la tranche (v172→v173), porté par le seul correctif réel |
| PR fusionnées | — | **5** (#264 → #268) |

\* v172 en début de tranche ; le bump v173 est arrivé au lot 232.

### Réalisations

1. **Palette de commande prouvée** (231) : Ctrl+K (input focusé,
   11 items, 3 groupes — la position réelle du store y figure),
   filtrage live, flèches suivies par aria-selected, Échap, clic sur
   la barre de recherche, Entrée qui NAVIGUE réellement.
2. **Vues internes balayées + 1 défaut réel soldé** (232) : 10 vues à
   390 px — la ligne de fraîcheur `.vx-update` (nowrap) débordait de
   201 px sur /portfolio?view=risk → elle REPLIE (ellipse refusée sur
   une info d'honnêteté). Bump v173.
3. **Couverture responsive COMPLÈTE** (233) : 8 racines (390+768) +
   6 secondaires + 13 vues — tout le produit navigable balayé au
   protocole discriminant. Campagne totale : 3 défauts réels
   corrigés, 2 bumps justifiés, 0 faux correctif.
4. **Menu contextuel prouvé + READONLY vérifié** (234) : 11 actions,
   flèches, clic-dehors, et **0 action d'ordre** dans les libellés —
   l'invariant READONLY tient jusque dans le vocabulaire.

### Le fait marquant de la tranche

**TOUS les composants interactifs du shell sont désormais prouvés en
conditions réelles** — drawer/modal (229), palette (231), menu
contextuel (234) — et tout le produit navigable est passé au
protocole responsive discriminant. Le shell de Vertex n'est plus
« supposé correct » : il est MESURÉ correct, défaut par défaut.

### Doctrine

4 lots de constat sans code produit (dits honnêtement), 1 correctif
mesuré-minimal-vérifié. Chaque balayage discriminant (off-canvas
voulu ≠ défaut), chaque observation classée (voulu / limitation /
défaut), chaque chiffre publié.

## Décision SW

**Pas de bump** (`td-shell-v173` inchangé) : lot de bilan, docs
seulement.

## Preuves

- Suite complète : **2486 passed / 2 skipped** (référence maintenue).
- Diff limité aux docs.

## Suite

LOT 236 : entretien suivant utile ou directive. Purge terminal.py
toujours EN ATTENTE d'accord humain explicite.
