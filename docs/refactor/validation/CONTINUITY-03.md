# CONTINUITY — LOT 3 · Cache & stale-while-revalidate (validation)

**But** : conserver les données déjà chargées, revenir sur une page sans nouveau
chargement lourd, ne jamais vider l'écran, protéger contre les réponses hors-ordre.

**Invariants** : READONLY, données réelles, moteurs inchangés, tests 100 %.

---

## Livré (`vertex/static/vertex/js/vx-core.js`)

1. **Cache client PERSISTANT** — le cache mémoire s'archive dans `sessionStorage`
   (`vxDataCache`) et se **réhydrate au démarrage** → revenir sur une page (même après
   un reload dur) affiche les données instantanément, sans réseau. Bornes : gros
   payloads non archivés (`PERSIST_MAX_ENTRY`, ex. `/scan` ~8 Mo exclu), `PERSIST_MAX`
   entrées, écriture throttlée (400 ms).

2. **Stale-while-revalidate** — `VX.swr(url, onData, {ttl})` : rend le cache
   **immédiatement** (même périmé), revalide en fond, ne rappelle `onData` que si la
   donnée a **changé**. Sur erreur → garde l'ancien contenu (jamais de vide, jamais
   remplacer du valide par du vide).

3. **Annulation anti-hors-ordre** — `VX.swr` retourne un annulateur (`cancel()`) :
   au changement de page/ticker, la réponse obsolète est **ignorée** (drapeau `alive`),
   elle ne peut plus écraser l'affichage courant.

4. **Invalidation CIBLÉE** — `VX.fetch.invalidate(clé | préfixe | prédicat)` remplace
   le `cache.clear()` aveugle ; le bouton « Actualiser » (`runAll`) passe désormais par
   l'invalidation (mémoire + persistance).

5. **Lecture synchrone** — `VX.fetch.peek(url)` → `{data, age, ts}` ou `null`
   (fraîcheur sans réseau, base des badges live/snapshot/stale du LOT 5).

6. **Déduplication in-flight** conservée (une requête identique ne part pas deux fois).

SW `td-shell-v65 → v66`.

---

## Validation (navigateur réel, Chromium 1440×900, DÉMO)

| Mécanisme | Résultat |
|---|---|
| **Persistance** | `sessionStorage.vxDataCache` peuplé (7 entrées) ; **après reload dur**, `peek('/api/market/summary')` renvoie la donnée **immédiatement** (hydratée, zéro réseau) |
| **Stale-while-revalidate** | `VX.swr` rappelle `[{cached:true, stale:true}, {cached:false, stale:false}]` — cache d'abord, frais ensuite |
| **Annulation hors-ordre** | après `cancel()`, seul le rappel caché synchrone a lieu ; **le rappel frais ne se déclenche pas** |
| **Invalidation ciblée** | `invalidate('/api/market')` purge le résumé marché **mais garde** le digest de session en cache |
| **Console** | **0 erreur** |

Suite complète : **1015 passed / 2 skipped**. compileall OK. READONLY intact.

---

## Tests
`tests/test_continuity_data.py` (7 gardiens) : API publique (`swr`/`invalidate`/`peek`),
persistance + réhydratation, bornes payloads, sémantique SWR, annulation anti-hors-ordre,
invalidation ciblée (pas de clear aveugle), dédup in-flight.

---

## Reste à faire (LOT 5, intégration pages)
Les pages consomment encore majoritairement `VX.fetch` (fresh-or-network) ; le passage
à `VX.swr` (rendu immédiat du cache + annulation au changement de vue/ticker) et le
branchement de `/api/session/digest` (aujourd'hui `no-store`) sur le store se feront à
l'intégration des pages, avec les badges de fraîcheur (`peek`).

Prochaine étape : **LOT 4 — Navigation instantanée** (préchargement hover/idle/proximité,
transitions, historique & navigation ticker, deep links).
