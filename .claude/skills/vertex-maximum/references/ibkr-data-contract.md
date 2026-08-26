# Contrat de données IBKR — lecture seule, provenance, fraîcheur

Vertex se place **au-dessus** d'IBKR : IBKR est la source de vérité (comptes, positions, ticks, chaînes
d'options) ; Vertex lit, vérifie la qualité, étiquette la provenance, et n'écrit **jamais**. Ce contrat fixe
comment une valeur venue d'IBKR (ou d'un fallback) doit voyager et s'afficher.

## Invariant lecture seule (jamais enfreint)
- Les **4 workers** `ib_async` se connectent tous en `readonly=True` (`terminal.py:846`, `2378`, `2492`, `2587`).
  Un worker dédié possède la connexion (file de jobs) ; aucun chemin `placeOrder`/`reqExecutions`-écriture.
- `clientId` **distincts** par worker : défaut `41 / 17 / 18 / 22` ; si `IBKR_CLIENT_ID` (`_IBKR_CID_BASE`) est
  numérique → `base+0/1/2/3` (`_ibkr_cid`, `terminal.py:816`). Vérifier qu'aucun nouveau worker ne réutilise un id.
- Anti-blocage : `RequestTimeout` borné + `timeout=6` à la connexion + dégradation « worker répond None » si
  `ib_async` manque ou si l'init échoue (`terminal.py:821-832`) — la file ne se fige jamais. **Ne pas retirer.**
- Config : `READONLY=True` (`vertex/app/config.py`). Gardiens : `test_redesign_ui.py::test_no_order_execution_in_ui`.

## États honnêtes (règle produit n°4 — ne jamais mentir sur le live)
`_sync_ibkr_state()` (`terminal.py:2449`) reflète l'état **réel du socket** dans `scan_state` (muté en place) :
- `fresh = (now - _live_meta['ts']) < 75` s — un worker figé dont les ticks datent de > 75 s **n'est plus
  « connecté »** (garde-fou fraîcheur, répété `terminal.py:2457`, `2552`, `2637`).
- `ibkr_connected = connected AND fresh` ; `ibkr_live = connected AND rt` (`rt` = flux temps réel réel).
- `_store_ticker` (`terminal.py:2463`) ne retient une cotation que si `last`/`close` sont finis et > 0, et
  renvoie `marketDataType == 1` (1 = LIVE ; 3 = delayed) → distinction **live vs retardé** portée jusqu'en UI.

États exposés (badge/tooltip) : **live · delayed · stale · disconnected · partial · estimated · unavailable**.
- `live` = socket ouvert, ticks < 75 s, `marketDataType==1`. `delayed` = `marketDataType==3`.
- `stale` = ticks > 75 s. `disconnected` = pas de socket. `partial` = certains symboles seulement.
- `estimated` = valeur issue d'un **modèle** (greeks `MODEL_ESTIMATE`, MC), pas du broker. `unavailable` = rien de
  fiable → afficher `—`/`n/d`, **jamais `0`**.

## Enveloppe de valeur (cible à porter en interne)
Toute valeur marché doit pouvoir répondre : `value · source · timestamp · quality · latency · environment ·
accountId · currency · isEstimated · isDelayed · isStale · error`. Aujourd'hui l'info existe éclatée
(`_live_meta`, `_live_quotes`, `marketDataType`, caches TTL) ; la consolider en une enveloppe unique
(`ProvenancedValue`) est un chantier d'audit (`docs/vertex-audit/06-data-provenance.md`).

## Fallbacks & provenance (jamais de mock silencieux)
Chaîne de sources : **IBKR** (live/delayed) → **yfinance** → **stooq** → **demo** (si `DEMO_MODE`/`NO_IBKR`).
- Chaque valeur affichée doit dire d'où elle vient ; footer standard `VX.updateIndicator` (source + ts + état).
- **Piège connu** — chaîne d'options vide : une chaîne réellement absente ne doit pas se déguiser en `0`
  (`terminal.py:~900-905`, à durcir → `unavailable`). Voir `docs/vertex-audit/06-data-provenance.md`.
- `DEMO/MOCK/SIMULATED` : badge obligatoire ; le mot « démo » ne s'affiche que si le serveur confirme
  (`DEMO_MODE`). Aucun fallback synthétique présenté comme réel.

## Surfaces de vérification
- `GET /healthz` → `ibkr_connected` / `ibkr_live` (vérité socket, pas un flag de config).
- `GET /api/system/connections` (`vertex/app/routes/connections.py`, lit `scan_state`) → carte Système honnête.
- `GET /api/live/status` → détail live/delayed par flux. `GET /api/client-log` → erreurs JS (doit rester à 0).

## Sécurité des données IBKR dans l'audit / captures
Masquer les **identifiants de compte** ; ne jamais copier `.env`, `VERTEX_SECRET`, `.vertex_secret`, clés API dans
un doc ou une capture. Runtime gitignoré (`edge_ledger`, `desk_backup_*`, `.vertex_secret`) — jamais commité.
