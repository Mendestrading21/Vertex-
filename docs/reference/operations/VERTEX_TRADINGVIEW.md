# Vertex — TradingView

- Webhook `POST /api/tradingview/webhook` : secret obligatoire, validation
  de schéma, anti-replay 15 min, event_id + déduplication 10 min, borne de
  taille, journalisation (`tradingview_signal_store`).
- Pipeline : signal → stockage → validation → (confirmation IBKR quand
  connecté) → analyse Vertex → hard gates → décision. **Un signal TV ne
  produit JAMAIS directement ACHETER** — décision max REEVALUATE
  (`test_tradingview_never_directly_buys`).
- États du signal : REÇU → À CONFIRMER → CONFIRMÉ / REJETÉ / EXPIRÉ / INVALIDÉ.
- UI : « Ouvrir dans TradingView » (URL réelle encodée symbole/timeframe),
  signaux visibles sur la fiche Analyse, secret absent → 503 honnête.
- Scripts Pine : `tradingview/vertex_signals.pine` + guide README.
