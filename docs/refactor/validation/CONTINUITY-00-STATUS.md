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

## Reste à faire

- **LOT 5·2 — Intégration des pages** (le plus gros ; touche les 8 espaces) : brancher
  chaque page sur `VX.swr` (rendu immédiat du cache) + `VX.freshness` (badges live/
  snapshot/stale) + `VX.prices` (prix cohérent), et sur `session_id`. À faire page par
  page avec validation navigateur (risque de régression le plus élevé).
- **LOT 6 — Polish** : observabilité dans Système (métriques nav/cache/session/store,
  §18), accessibilité, mesures finales, documentation, captures.

Les fondations (mécaniques + serveur) étant posées et validées, l'intégration des pages
peut se faire sereinement, une page à la fois.
