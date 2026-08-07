# SKYLER LOT 284 — Carte « Application » : version du shell + mise à jour forcée

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-284` (base : lot 283 fusionné)

## Objet (mode développement, directive active)

Douleur documentée dans CHAQUE rapport depuis des dizaines de lots :
« validation physique iPhone — vider le cache pour recevoir SW vNNN ».
Aucun moyen dans l'UI de savoir quelle version du shell est servie, ni
de forcer la mise à jour : il fallait vider le cache navigateur à la
main. Ce lot comble les deux manques.

## Livré — carte « Application » (Système → Réglages)

- **Version du shell (cache local)** : lue des caches RÉELS du
  navigateur (`caches.keys()` → `td-shell-vN`, jamais un numéro codé
  en dur — la vérité vit dans le SW) + état du service worker
  (« actif (hors-ligne prêt) » / « installé, pas encore aux
  commandes » / « indisponible »). Re-lue quand le SW devient prêt
  (premier chargement : le cache s'installe encore — bug de timing
  trouvé au navigateur et corrigé dans le lot).
- **Bouton « Forcer la mise à jour de l'app »** : désinscrit le
  service worker, vide tous les caches CacheStorage, recharge.
  **Ne touche JAMAIS localStorage** — les données desk (positions,
  journal, alertes…) survivent, et le gardien le fige.

## Gardien neuf — `tests/test_app_update_card_lot284.py` (3 tests)

1. Carte présente dans Réglages avec la promesse « Aucune donnée desk
   n'est touchée » ; domicile unique (HTML des autres vues sans la
   carte) ; 2. la version est lue de `caches.keys()` et AUCUN
   `td-shell-vN` en dur dans le JS de page ; 3. `forceAppUpdate` fait
   `unregister()` + `caches.delete` + `reload` et ne contient PAS
   `localStorage`.

## Preuves (navigateur réel, serveur DEMO)

- Carte visible ; après installation du SW : **« td-shell-v175 » +
  « actif (hors-ligne prêt) » affichés** (donnée réelle, pas un
  libellé).
- **Clic RÉEL testé** : page rechargée, caches vidés puis SW
  réinstallé proprement.
- 0 débordement (1416/1440 · 378/390) ; **0 erreur console**.
- 1 faux départ honnête : première mesure « n/d » → cause vérifiée
  (timing d'installation du SW, le cache s'appelait bien
  td-shell-v175) → correctif `serviceWorker.ready` + re-render.
- Capture envoyée (lot284_app_card.png).
- Suite complète : **2492 passed / 2 skipped** (+3).

## Décision SW

**Bump v174 → v175** (nouvelle carte servie) + les 5 gardiens SW.

## Suite

LOT 285 : mini-bilan 281-285 + prochaine piste produit. La purge
attend toujours « GO purge étape 1 » explicite.
