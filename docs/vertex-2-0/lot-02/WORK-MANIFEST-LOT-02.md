# WORK_MANIFEST — Lot 2 · Frontière IBKR market-data-only

## Objectif

Retirer du produit **toute** capacité de lecture du compte courtier — comptes,
soldes, NAV, marge, positions, portefeuille, P&L — et prouver par le scanner
en mode `--enforce` qu'aucun appel interdit ne subsiste ni ne peut réapparaître.
IBKR devient exclusivement un fournisseur de **données de marché** ; le
portefeuille reste saisi manuellement dans Vertex.

`readonly=True` empêche l'ordre ; il ne protège pas la confidentialité du
compte. C'est cette seconde frontière que ce lot ferme.

## Non-objectifs

- Ne touche pas aux flux de **marché** IBKR : cotations, chaînes, historiques,
  Greeks, état de connexion par preuve de socket — tout cela reste.
- Ne supprime aucune donnée utilisateur : les positions **déclarées** du desk
  sont la seule source de portefeuille et ne sont pas modifiées.
- Ne crée pas encore le `MarketDataGateway` complet (façade typée) : ce lot
  ferme la frontière ; la façade est consolidée au lot 6 avec les snapshots.

## SHA et branche

| | |
|---|---|
| Branche | `agent/vertex-2-0-integration-20260828` |
| SHA de départ | `ac2708d` (lot 1) |
| Dirty state | propre |

## Inventaire d'audit — les 13 appels et leurs consommateurs

| Site | Capacité | Consommateur aval |
|---|---|---|
| `terminal.py:1341` | `ib.positions()` (worker `kind='positions'`) | `opt_job('positions')` → `positions_api._ibkr_positions()`, `desk./api/ibkr/positions` |
| `terminal.py:2201/2208/2220` | `accountSummary`, `managedAccounts`, `positions` | `_ibkr_snapshot()` → route `/ibkr` → carte « COMPTE IBKR » du legacy V3 (net_liq, cash, buying power, P&L latent, liste de positions) |
| `ibkr_compte.py` (5 sites) | `managedAccounts`, `accountSummary`, `portfolio` ×2, `reqPnL` | `/api/positions/pnl-reconciliation` → carte « Rapprochement du P&L » de Portefeuille |
| `ibkr_positions.py:36` | `positions` | `from_ibkr_positions` (`portfolio/models.py`) — **aucun appelant runtime** |
| `ibkr_replay.py:507` | `positions` | fixtures de rejeu G5 (`positions_brutes`) |
| `tools/vertex_1_0/mesurer_g5_live.py:337` | `positions` | outil de mesure hors produit |

Consommateurs UI : `portfolio_page.py` (fetch `/api/ibkr/positions`,
`/api/positions/pnl-reconciliation`, bandeau « IBKR hors ligne », pied
« N position(s) broker ») ; legacy `terminal.py` (6 × `fetch('/ibkr')`, dont
une carte de compte complète).

Tests qui épinglent le comportement actuel : `test_real_data.py` (la route
DOIT exister et être consommée), `test_vertex_1_0_reconciliation_pnl.py`,
`test_vertex_1_0_positions_memoire.py`, `test_vertex_1_0_g5_adaptateurs.py`,
`test_vertex_1_0_legacy_zero_parity.py`, `tools/vertex_1_0/_sonde_http.py`,
`mesurer_surfaces_vides.py`.

## Fichiers autorisés

`terminal.py` (worker + `_ibkr_worker`/`_ibkr_snapshot` + carte legacy) ·
`vertex/data_sources/ibkr_compte.py` (suppression) ·
`vertex/data_sources/ibkr_positions.py` (suppression) ·
`vertex/data_sources/ibkr_replay.py` · `vertex/portfolio/models.py` ·
`vertex/app/routes/positions_api.py` · `vertex/app/routes/desk.py` ·
`vertex/app/routes/live_state_api.py` (doc) ·
`vertex/ui/pages/portfolio_page.py` · `vertex/app/routes/system.py` (bump SW) ·
`tools/vertex_1_0/mesurer_g5_live.py` · `tools/vertex_1_0/_sonde_http.py` ·
`tools/vertex_1_0/mesurer_surfaces_vides.py` ·
`tests/**` (bancs épinglant l'ancien comportement + nouveau gardien) ·
`docs/vertex-2-0/lot-02/**`.

## Données à préserver

- `desk_data.json` et toutes les positions déclarées : intouchés.
- Les positions historiques marquées `source_reference: "ibkr:*"` dans le desk
  restent lisibles — on retire la **capacité d'importation**, pas les données
  que l'utilisateur a déjà acceptées.
- Aucune écriture de donnée de compte dans les logs pendant la migration.

## Ordre de migration (contrat du skill, §Migration obligatoire)

1. **Gardien d'abord** : test qui exécute `check_ibkr_boundary.py` et échoue
   sur tout appel interdit — rouge au départ (13 hits), vert à la fin.
2. UI : retirer les deux consommations de Portefeuille et la carte de compte
   legacy ; dire l'absence (« IBKR = données de marché uniquement »).
3. Routes : retirer `/api/positions/pnl-reconciliation` et
   `/api/ibkr/positions` ; `positions_api` cesse de demander les positions
   broker (`ibkr=None` partout).
4. Worker : retirer `kind == 'positions'` ; réduire `_ibkr_worker` à la preuve
   de socket (connected/mode/error).
5. Modules : supprimer `ibkr_compte.py`, `ibkr_positions.py`,
   `from_ibkr_positions` ; purger `positions_brutes` du rejeu et de l'outil G5.
6. Tests : réécrire les bancs qui épinglaient la capacité — l'intention
   inverse (la route N'EXISTE PLUS, le worker NE répond PLUS) — et brancher le
   gardien en `--enforce`.
7. Rejouer : mode sans IBKR, suite complète, navigateur sur Portefeuille et
   Système, captures.

## Tests

- rouge → vert : `tests/test_frontiere_ibkr_lot02.py` (gardien `--enforce`)
- `python -m pytest -q` complet
- `python -m pytest tests/test_no_orders.py -q`
- navigateur : `/portfolio` (positions, vue performance), `/system`
  (connexions), 0 erreur console, captures 1600/1024/390.

## Migration / Rollback

Migration : décrite ci-dessus, un commit cohérent.
Rollback : `git revert` du commit du lot — aucun schéma de données modifié,
aucune migration de store, donc le revert restaure la capacité sans perte.

## Critères d'arrêt

1. `check_ibkr_boundary.py --enforce` → **0 appel sensible**, code 0 ;
2. plus aucune route ne sert compte/positions/P&L broker ;
3. l'UI dit l'absence au lieu de la masquer ;
4. suite verte hors échec environnemental connu ;
5. captures après, aux trois largeurs, sans erreur console.
