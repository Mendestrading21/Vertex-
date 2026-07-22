# Vertex — IBKR en lecture seule

- `vertex/data_sources/ibkr_gateway.py` : `readonly=True` **codé en dur**,
  worker unique sérialisé (ib_async non thread-safe), RequestTimeout=45.
- Lectures : positions, cotations, historiques, chaînes options, contrats,
  Greeks broker (BROKER_GREEKS prioritaires sur le modèle).
- **Denylist** : placeOrder/submitOrder/bracketOrder/Market-Limit-StopOrder/
  reqGlobalCancel + auto_close_position/auto_rebalance/one_click_trade —
  gardiens `tests/test_no_orders.py` (appels ET définitions, Python + JS).
- Statuts : IBKR LIVE / DELAYED / FROZEN / OFFLINE / FALLBACK — une donnée
  rassise ne produit jamais ACTIONNABLE (`test_stale_data_blocks_actionable`
  via qualité de données).
- Hors ligne : `/api/ibkr/positions` → 200 `{ok:false}` honnête ; l'UI
  affiche « marques indisponibles » plutôt qu'un chiffre inventé.
