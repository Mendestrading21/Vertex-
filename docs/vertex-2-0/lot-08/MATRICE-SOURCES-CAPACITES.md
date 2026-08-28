# Matrice source → capacité → snapshot → consommateurs → fallback — lot 8

Mesurée sur la branche d'intégration, après les lots 2 (frontière compte) et
6 (stale-while-revalidate). Une ligne par capacité réellement servie.

| Source | Capacité | Où vit l'état | Consommateurs | Fallback | Mode absent |
|---|---|---|---|---|---|
| IBKR (worker unique) | cotations spot/options (`posq`) | `posq_cache` (TTL 45 s, stale servi étiqueté) | `/api/pos-quotes` → Portefeuille, Suivi | `completer_par_repli` (SECONDARY, étiqueté) puis mid du board | `n/d` honnête |
| IBKR | chaînes d'options (`chain`) | `scan_state['options_chain_full']` (LRU ~200 sym) | Options, Analyse, board | aucune — absence dite | état vide honnête |
| IBKR | méta contrat (`meta`) | mémo worker | fiche Analyse | aucune | `n/d` |
| IBKR | fondamentaux (`fund`) | `scan_state` | Analyse, scan | aucune | `n/d` |
| IBKR | historiques/barres | `ibkr_historical` | graphiques Analyse | stooq/yfinance (SECONDARY) | série absente dite |
| IBKR | news (`news`) | `scan_state` | Aujourd'hui, Marchés | aucune | bloc absent |
| IBKR | état de connexion | `/ibkr` — preuve de socket `{connected, mode}` | Système, legacy | — | `connected:false` |
| ~~IBKR~~ | ~~compte/positions/P&L~~ | **RETIRÉ (lot 2)** — scanner `--enforce` à zéro | — | — | — |
| yfinance/stooq | spot différé, séries EOD | caches TTL par module | scan, repli cotations | l'un l'autre | `STALE`/`EOD` étiquetés |
| FRED / BLS | macro (taux, emploi, inflation) | caches datés | Marchés → Macro, WMB | aucune | daté ou absent |
| SEC EDGAR | dépôts | cache | fiche Analyse | aucune | absent dit |
| TradingView (webhook) | alerte authentifiée de réévaluation | desk/alertes | Alertes, Journal | — | jamais un ordre |
| Desk (utilisateur) | positions, thèses, journal, watchlist, alertes | `localStorage` + `desk_data.json` (backups quotidiens) | tout le produit | `/api/desk/restore` | source souveraine |
| Moteurs (60 modules) | scores, scénarios, verdicts | `scan_state` (muté en place, jamais réassigné) | toutes les pages | — | verdict `Inconnu` honnête |
| Claude | explication du packet | instantanés d'enrichissement | Vertex IA, briefs | instantané `MISSING` honnête | « analyse indisponible » |

## Ce que la matrice montre

- **Un seul point de contention** : la file worker IBKR unique — tous les
  appels broker s'y sérialisent (dette lot 6, consignée).
- **Deux capacités sans aucun fallback** : chaînes et fondamentaux. C'est un
  choix honnête (un fallback inventerait), pas un oubli.
- **L'état du produit vit dans `scan_state`** (muté en place — règle critique
  du dépôt) + le desk. Pas d'autre store caché.
