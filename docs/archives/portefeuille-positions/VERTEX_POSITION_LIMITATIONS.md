# Vertex — Limitations positions

1. **Cotations en démo/cloud** : sans TWS, les positions sont en
   AWAITING_DATA / AWAITING_CONTRACT_DATA (honnête) — market_value, P&L,
   Greeks restent None. Avec IBKR branché, `/api/positions/state` les
   remplit via le worker posq (lecture seule).
2. **Greeks agrégés du portefeuille** : calculés seulement si TOUTES les
   options ont des Greeks broker — jamais une somme de modèles présentée
   comme exposition réelle.
3. **Scénarios spot×temps×IV par position** : rendus via le desk options
   (`/api/options/simulate`, exige IV + spot frais) ; le payoff (arithmétique)
   est disponible partout.
4. **Snapshots/historique** : `change_detector` compare au dernier snapshot
   persisté par position ; l'historisation longue (MAE/MFE série, Track
   Record) reste portée par les snapshots EOD existants.
5. **Sync desk ↔ serveur** : `/api/positions/state` lit le blob serveur
   (`desk_data.json`) ; l'UI locale lit localStorage. En usage réel le
   navigateur pousse vers `/api/desk` (last-writer-wins) et les deux
   convergent ; hors sync, seuls les ids correspondants reçoivent un statut.
