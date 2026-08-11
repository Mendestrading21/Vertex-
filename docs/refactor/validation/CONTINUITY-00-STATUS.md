# CONTINUITY — État d'avancement (refonte navigation & circulation des données)

Objectif : faire de Vertex une **application continue** — navigation instantanée,
données conservées, prix live cohérents, snapshots persistants, identité claire des
données, bascule atomique de session. Invariants tenus partout : **READONLY**, données
réelles (absent → `n/d`), moteurs inchangés, **tests 100 %**.

## Lots livrés (branche `agent/vertex-neon-glass-graphs`)

| Lot | Contenu | Preuve |
|---|---|---|
| **1** | Audit navigation & contrats + métriques de base | `CONTINUITY_01_NAVIGATION_AUDIT.md` |
| **2** | **Shell persistant** : rendu de fragment serveur + routeur client (progressive-enhancement), cycle de vie de page (teardown), `VX.store`, police non bloquante | `CONTINUITY-02.md` |
| **3** | **Cache persistant + stale-while-revalidate** : hydratation sessionStorage, `VX.swr`, annulation anti-hors-ordre, invalidation ciblée, `peek` | `CONTINUITY-03.md` |
| **4** | **Navigation instantanée** : préchargement survol/focus/idle, navigation ticker SPA, transitions | `CONTINUITY-04.md` |
| **5·1** | **Session atomique serveur** : manifest (`session_id`), `/api/session/manifest`, bascule client + notification « Analyse mise à jour » | `CONTINUITY-05.md` |
| **5·b** | **Identité de fraîcheur** (`VX.freshness`, seuils unifiés) + **mode offline/dégradé** | `CONTINUITY-05.md` |
| **5·c** | **Source de prix centrale** (`VX.prices`) : un ticker = un prix partout ; live / référence snapshot / prix d'achat distincts | `CONTINUITY-05.md` |

**Mécaniques transverses en place** (dans `vx-core.js` / `vx-router.js` / `vx-shell.js`) :
`VX.store`, `VX.page` (cycle de vie), `VX.fetch` (persistant + dédup + invalidation +
`peek`), `VX.swr`, `VX.router` (SPA + préchargement), `VX.freshness`, `VX.prices`.
Serveur : rendu de fragment, `session_snapshot` (manifest), `session_digest`.

**État mesuré** : navigation SPA (shell jamais reconstruit), endpoints shell 8× → 1× par
tour, données conservées entre pages ET après reload, préchargement consommé (clic sans
round-trip), session atomique + notification, offline sans écran vide. **1041 tests
verts**, 0 erreur console, READONLY intact.

| **6** | **Observabilité** : `VX.fetch.stats()` + panneau « Continuité » dans Système (navigation/cache/session/connexion/prix) | `CONTINUITY-00` |
| **5·2 (pilote)** | **Aujourd'hui** branché en stale-while-revalidate (peinture immédiate du cache puis revalidation) — modèle des autres pages | commit `ae75bd3` |

**Acquis global** : grâce au cache mémoire partagé + persistant (LOT 3), TOUTES les pages
bénéficient déjà de la revisite instantanée (les données déjà chargées ne sont pas
re-téléchargées lors d'une navigation SPA), du shell persistant (LOT 2), du préchargement
(LOT 4), de la bascule de session (LOT 5), du mode offline et de l'identité de fraîcheur.

## Reste — polish optionnel par page (piloté par l'usage)

L'infrastructure est complète et validée (**1045 tests verts**). Le reste est de la
finition par page, à prioriser après essai de l'app en conditions réelles :

- Généraliser le pattern SWR d'Aujourd'hui (peinture immédiate) aux autres vues par
  défaut (Portefeuille, Opportunités, Marchés) — gain marginal, le cache mémoire les
  sert déjà instantanément en SPA.
- Poser les **badges de fraîcheur** `VX.freshness` sur les en-têtes de widgets (live/
  snapshot/stale) là où c'est utile.
- Alimenter `VX.prices` depuis les pages par-ticker (Analyse, Portefeuille, Options) pour
  la cohérence de prix visible (§9).

Ces éléments sont indépendants et se posent widget par widget, sans risque structurel.
