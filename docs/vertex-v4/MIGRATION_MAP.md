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
| `css/glass.css` | vérité runtime historique chargée en dernier | tokens/components V4 | Lot 15 |
| `js/charts/chart-theme-obsidian-copper.js` | thème global Chart.js | `chart-theme-v4.js` | Lot 04 |

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
