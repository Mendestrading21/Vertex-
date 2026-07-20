# 09 — Audit de l'intégration IBKR

Accès via `ib_async` (fork ib_insync). **Invariant : lecture seule.** Détail contrat :
`references/ibkr-data-contract.md`.

## Ce qui est bien fait
- **4 workers `readonly=True`** : `terminal.py:846` (clientId 41), `2378` (17), `2492` (18), `2587` (22) ;
  `clientId` distincts via `_ibkr_cid(default, offset)` (`terminal.py:816`) — base `IBKR_CLIENT_ID`+offset si
  numérique, sinon défauts distincts. **Pas de collision de clientId constatée.**
- **Anti-blocage** : timeouts synchrones bornés + `timeout=6` à la connexion + worker qui « répond None » si
  `ib_async` manque / init échoue (`terminal.py:821-832`) → file jamais figée. **Ne pas retirer.**
- **Statut honnête** : `_sync_ibkr_state()` (`terminal.py:2449`) reflète le **socket réel** dans `scan_state` ;
  garde-fou **fraîcheur 75 s** (`ts` des ticks) → un worker figé n'apparaît plus « connecté » ;
  `ibkr_live = connected AND rt`. `_store_ticker` (`terminal.py:2463`) distingue LIVE (`marketDataType==1`) de
  delayed (`==3`) et filtre les prix non finis/≤0.
- **Surface de vérité** : `GET /healthz` (`ibkr_connected`/`ibkr_live`), `GET /api/system/connections`
  (`app/routes/connections.py` lit `scan_state`), `GET /api/live/status`.

## Findings
- **IBK-01 (P1) — Badge « temps réel » = socket, jamais config.** Reconfirmer sur **toutes** les surfaces que le
  badge live dérive de `ibkr_live` (socket + fraîcheur + `rt`), pas d'un flag `IBKR_*`. Auditer les rendus de
  badge dans les pages (Système, topbar, Portefeuille, Options).
- **IBK-02 (P1) — États complets exposés.** Mapper partout les 7 états : live / delayed / stale / disconnected /
  partial / estimated / unavailable. Aujourd'hui `connected`/`live` sont exposés ; `partial` (certains symboles)
  et `stale` méritent un rendu UI explicite.
- **IBK-03 (révisé P2, lié DAT-01) — Absence ≠ 0.** Vérifié : la couche d'affichage est déjà honnête (chain-grid
  `available:false`, normalisation `None` à `_persist_chain_full`). Résidu étroit : au producteur IBKR **live**
  (`terminal.py:904-905`), OI/volume confondent NaN et vrai `0` — à distinguer **en local** (non testable en cloud).
  Voir `06`.
- **IBK-04 (P2) — Environnement cloud sans IBKR.** Le cloud ne joint pas TWS ; toute vérification live se fait en
  local. En cloud, exécuter/valider en **DEMO** (`DEMO=1 NO_IBKR=1`), sans jamais présenter la démo comme réelle.

## Sécurité des données
Masquer les identifiants de compte dans captures/logs. Ne jamais commiter `.env`, `.vertex_secret`, clés API.
Runtime IBKR (position_inventory, caches) gitignoré. IBKR : `readonly=True` **toujours**.
