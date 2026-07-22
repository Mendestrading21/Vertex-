# Vertex V4 — carte de migration visuelle

> **Status: ACTIVE**
> Last verified: 2026-07-22

Les couches ci-dessous restent chargées uniquement parce que l'interface actuelle
les consomme. Leur nom historique ne leur donne aucun statut canonique.

| Fichier legacy | Rôle actuel | Destination V4 | Retrait prévu |
|---|---|---|---|
| `css/polish.css` | ajustements tardifs | tokens + components/pages | Lot 15 |
| `css/control-surface.css` | contrôles et états sélectionnés | `controls.css` + components | Lot 15 |
| `css/cockpit.css` | mise en page cockpit | `layout.css` + pages | Lot 15 |
| `css/premium.css` | overrides premium | components + pages | Lot 15 |
| `css/glass.css` | ex-vérité runtime, désormais re-mappée sur les tokens V4 par le pont | tokens/components V4 | Lot 15 |
| `js/charts/chart-theme-obsidian-copper.js` | thème global Chart.js | `chart-theme-v4.js` | Lot 04 |

## Pont de compatibilité V4 (Lot 01)

`css/tokens-v4-bridge.css` est **chargé en dernier** (après `glass.css`) et
re-mappe les tokens `--vx-*` consommés par le runtime historique sur les valeurs
canoniques `--vx-v4-*` de `tokens.css`. Il applique l'identité Obsidian Prism aux
pages/shell/graphiques existants **sans les reconstruire**. Ce n'est pas une source
de vérité : c'est une couche de migration transitoire, retirée au Lot 15 une fois
`glass.css` et les couches legacy migrées et prouvées inutiles. Il n'introduit
aucune règle métier.

## Couche shell V4 (Lot 02)

`css/shell.css` est **chargé en dernier** (après `tokens-v4-bridge.css`) et
restyle le shell existant (sidebar, topbar, recherche, item de nav actif, logo,
nav mobile, drawers) vers la spec V4 §4-5 : dimensions (sidebar 180px, topbar
58px), verre localisé, accent prism violet sur l'item actif et le logo. Il bat
les règles shell historiques de `glass.css` sans modifier structure, routes ni
comportements. Couche de migration transitoire → consolidée dans `layout.css`
au Lot 15 (mêmes conditions de retrait que ci-dessus). Aucune règle métier.

## Couche composants V4 (Lot 03)

`css/components-v4.css` est **chargé en dernier** (après `shell.css`) et affine
les composants partagés (cartes 4 niveaux, onglets, chips/filtres, segmented,
boutons) vers la spec V4 §4.2-4.4 : la **sélection** passe en violet prism
(carte active, onglet actif, chip/filtre actif, option segmented), accent hero
prism, rayons de contrôle V4. La sémantique pos/neg/warn des tuiles reste
inchangée. Bat les règles composant historiques de `glass.css` sans modifier
structure ni données. Consolidée dans `components.css` au Lot 15. Aucune règle métier.

## Condition de retrait d'un fichier

Un fichier ne peut être supprimé que si :

1. ses sélecteurs/exports utiles ont une destination documentée ;
2. aucun import ou chargement ne le référence ;
3. les tests complets sont verts ;
4. les neuf espaces et leurs sous-vues ont été contrôlés ;
5. desktop, tablette et mobile sont capturés ;
6. `/api/client-log` et la console restent sans erreur ;
7. le service worker est bumpé si le shell change ;
8. `STATUS.md` et ce fichier sont mis à jour.

## Interdictions

- Ne pas supprimer toutes les couches en une opération globale.
- Ne pas copier leurs règles dans un nouveau fichier sans déduplication.
- Ne pas changer une règle métier pendant une migration CSS.
- Ne pas laisser un ancien fichier chargé « au cas où » après preuve de non-usage.
