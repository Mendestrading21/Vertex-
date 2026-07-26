# CONTINUITY — LOT 5 (part 1) · Session atomique serveur + bascule client

**But** : identifier une session d'analyse cohérente (`session_id`) et **basculer
atomiquement** vers une nouvelle session quand elle est prête, avec une notification
discrète — sans jamais recalculer les moteurs.

**Invariants** : READONLY, données réelles, moteurs inchangés, tests 100 %.

---

## Livré

### Serveur (enrobage sans recalcul)
1. **`vertex/engines/session_snapshot.py`** — moteur PUR `build(scan_state)` → manifest
   d'intégrité : `session_id` (dérivé de `scan_ts` → **stable pour tout un cycle**,
   change exactement quand le scan republie = point de bascule atomique), `status`
   (`analyzing`/`ready`/`error`), `as_of`, `age_s`, `coverage_pct` (scannées/univers),
   `quality_pct` (couverture des détails moteur), `error`, `source`. Aucun calcul
   financier — lecture/agrégation de l'état déjà produit.
2. **`/api/session/manifest`** (`session_api.py`) — expose le manifest. Lecture seule.

### Client (bascule + notification)
3. **`vx-shell.js` — surveillance de session** (tâche persistante `session-watch`,
   60 s + `vx:data-refreshed`) :
   - suit `active_session_id` en continu (silencieux, base des futurs badges) ;
   - à un **changement de `session_id`** : met à jour `previous/active` dans le store,
     émet `vx:session-changed` ;
   - **bascule visible throttlée** (≤ 1 / 10 min, car le scan republie ~toutes les 2 min) :
     invalide le cache snapshot (garde le desk perso), affiche la notification
     « **Analyse mise à jour · Session HH:MM · N sociétés · qualité X %** », émet
     `vx:data-refreshed{reason:'session-switch'}` → les pages se rafraîchissent ensemble.
4. **`vx-core.js` / `VX.store`** : `active_session_id`, `previous_session_id`,
   `session_status`.

SW `td-shell-v67 → v68`.

---

## Validation (navigateur réel, DÉMO)

| Vérification | Résultat |
|---|---|
| `/api/session/manifest` | `{session_id:'S…', status:'ready', coverage_pct:100, quality_pct:100, scanned:20, universe:20}` |
| Suivi au chargement | `store.active_session_id` renseigné, `session_status='ready'` |
| **Bascule atomique** (nouvelle session simulée) | `active` → nouvel id, `previous` → ancien, `vx:session-changed` émis, `vx:data-refreshed(session-switch)` émis |
| **Notification** | toast « **Analyse mise à jour · Session 00:19:01 · 20 sociétés · qualité 100 %** » |
| Console | **0 erreur** |

Suite complète : **1030 passed / 2 skipped**. compileall OK. READONLY intact.

---

## Tests
`tests/test_continuity_session.py` (8 gardiens) : manifest honnête (vide/ready),
`session_id` stable par cycle, pas de chemin d'ordre, endpoint, surveillance client +
bascule + notification, throttle, store.

---

## Reste du LOT 5 (part 2 — intégration des pages, à valider)
- Brancher les 8 pages sur `VX.swr` (rendu immédiat du cache + revalidation) et sur le
  `session_id` (toutes lisent le même instantané).
- **Source de prix live centrale** : un ticker = un prix partout (shell/Analyse/
  Portefeuille/Options), distinct du prix de référence du snapshot et du prix d'achat.
- **Identité visuelle** discrète : badges live / snapshot / sauvegardé / stale /
  recalcul / erreur (basés sur `VX.fetch.peek` + `session_status`).

Cette part 2 touche les 8 pages (risque de régression le plus élevé) → à faire en
passe dédiée, page par page, avec validation navigateur.

Prochaine étape proposée : **LOT 5 part 2** puis **LOT 6 — Polish** (offline/dégradé,
observabilité Système, accessibilité, mesures finales).
