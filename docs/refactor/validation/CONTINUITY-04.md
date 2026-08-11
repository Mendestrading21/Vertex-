# CONTINUITY — LOT 4 · Navigation instantanée (validation)

**But** : navigation perçue instantanée — préchargement des pages probables,
navigation ticker fluide, transitions courtes, aucun scan lourd déclenché.

**Invariants** : READONLY, données réelles, moteurs inchangés, tests 100 %.

---

## Livré

1. **Préchargement** (`vertex/static/vertex/js/vx-router.js`)
   - **Survol** (débounce 90 ms) et **focus clavier** d'un lien interne → récupération
     du fragment de la page cible, gardé prêt (cache `PF`, TTL 30 s, max 12).
   - **Idle** : après le chargement et après chaque navigation, préchargement des pages
     probables depuis l'espace courant (carte `NEXT` : Aujourd'hui → Marchés/Opportunités/
     Portefeuille ; Analyse → Opportunités/Options ; etc.).
   - **Concurrence bornée** (2 max, file d'attente `pfQueue`), **dédup** (`pfInflight`),
     GET de lecture uniquement.
   - `navigate()` **consomme** le fragment préchargé si présent → clic sans round-trip.

2. **Navigation ticker fluide** (`vx-core.js`)
   - `VX.openAnalysis(sym)` (utilisé PARTOUT) passe désormais par `VX.router.go()` →
     ouverture de fiche en **SPA** (shell conservé), repli dur si routeur absent.

3. **Transitions** : crossfade discret sur `#vx-content` pendant la navigation,
   **désactivé sous `prefers-reduced-motion`**.

SW `td-shell-v66 → v67`.

---

## Validation (navigateur réel, Chromium 1440×900, DÉMO)

| Vérification | Résultat |
|---|---|
| **Préchargement consommé** | survol de `/journal` → 1 récupération du fragment ; **clic → 0 récupération supplémentaire** (servi depuis le cache de préchargement) |
| **Navigation ticker SPA** | `VX.openAnalysis('AAPL')` → `space=analysis`, `path=/analysis/AAPL`, `store.active_ticker=AAPL`, **shell conservé** (sentinelle) |
| **Latence de swap** | pages légères ~250 ms ; pages lourdes (Marchés, nombreux graphiques) plus longues — le préchargement supprime le round-trip réseau, le rendu des graphiques reste le coût dominant (cible LOT 5/6) |
| **Console** | **0 erreur** |
| **Scan lourd déclenché par navigation** | **aucun** (invariant préservé) |

Suite complète : **1022 passed / 2 skipped**. compileall OK. READONLY intact.

---

## Tests
`tests/test_continuity_nav.py` (7 gardiens) : machinerie de préchargement, déclencheurs
survol/focus/idle, concurrence bornée + dédup, consommation du préchargement par
`navigate`, navigation ticker via routeur, transition reduced-motion, carte idle.

---

## Note
Le rendu des graphiques des pages lourdes (Marchés) domine encore la latence perçue
après le swap ; l'optimisation (rendu progressif, cache de composants) est prévue au
polish (LOT 6). Le gain réseau du préchargement est acquis dès maintenant.

Prochaine étape : **LOT 5 — Session atomique serveur + intégration des pages**
(session_id + snapshot + manifest + bascule atomique ; branchement des 8 pages sur le
store avec SWR ; prix live cohérent partout ; identité visuelle live/snapshot/stale).
