# Matrice des propriétaires du desk — lot 3

17 clés synchronisées (les 4 listes concordent, gardien vert). Pour chaque
clé : qui l'écrit, qui la lit — mesuré par recherche exhaustive, fichiers
de sync exclus (ils portent toutes les clés par construction).

| Clé | Écrivains | Lecteurs (hors sync) |
|---|---|---|
| `myTrades` | vx-entities.js | ai_api.py, copilot.py, opportunities_api.py, positions_api.py, redesign.py, terminal.py, vx-entities.js |
| `myTradesClosed` | vx-entities.js | vx-entities.js |
| `myTradesEquity` | — | vx-entities.js |
| `myRecos` | signals.py, terminal.py, vx-entities.js | signals.py, terminal.py, vx-entities.js |
| `myRecosClosed` | — | — |
| `myCapital` | — | vx-entities.js |
| `simCash` | — | — |
| `simStart` | — | — |
| `simTrades` | — | — |
| `simClosed` | — | — |
| `myFavs` | terminal.py, vx-entities.js | analysis_page.py, terminal.py, vx-entities.js |
| `myNotes` | terminal.py, vx-entities.js | terminal.py, vx-entities.js |
| `vxJournal` | vx-entities.js | vx-entities.js |
| `myTradeLog` | vx-entities.js | vx-entities.js |
| `vxVault` | system_page.py, vault.py | system_page.py, vault.py |
| `vxAlerts` | vx-entities.js | terminal.py, vx-entities.js |
| `vxWatchlist` | vx-entities.js | vx-entities.js |

## Lecture honnête de cette matrice

- **`vx_kit.py` est exclu comme fichier de sync, mais il porte AUSSI un vrai
  écrivain** : `addPosition` (legacy V3) écrit `myTrades` ligne 188. La ligne
  `myTrades` ci-dessus se lit donc « vx-entities.js **+ vx_kit legacy** ».
  C'est le double-écrivain traité par ce lot : les deux écrivent désormais le
  **même schéma** ; la porte legacy sera étranglée au lot 9, pas avant.
- **Doubles écrivains restants** — `myRecos`, `myFavs`, `myNotes` : chacun a
  un écrivain 2.0 (`vx-entities`) et un écrivain legacy (`terminal.py`,
  `signals.py`). Même situation, même destin : lot 9.
- **Clés dormantes** — `simCash`, `simStart`, `simTrades`, `simClosed`,
  `myRecosClosed` : aucun lecteur ni écrivain hors sync. Elles restent dans
  les 4 listes (les retirer effacerait les données serveur d'un utilisateur
  qui en a) ; candidates au nettoyage **après** décision humaine.
- `vxVault` a son propriétaire propre (`vault.py`), hors VXEntities : à
  converger ou déclarer domaine séparé au lot 9.
