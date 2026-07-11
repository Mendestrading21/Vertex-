# TradingView → Vertex Strategy — installation

Les signaux TradingView sont de l'**information** : le webhook Vertex les
valide, les stocke et déclenche une **réévaluation**. Aucun signal ne peut
produire un achat — c'est garanti par le code et testé
(`tests/test_tradingview.py::test_tradingview_never_directly_buys`).

## 1. Côté serveur Vertex

1. Définir le secret dans `.env` :
   ```
   TRADINGVIEW_SECRET=une-longue-chaine-aleatoire
   ```
2. Redémarrer Vertex. Sans secret configuré, le webhook répond 503 (désactivé).
3. Vérifier : `GET /api/tradingview/signals` doit répondre `{"signals": [...]}`.

## 2. Côté TradingView

1. Ouvrir un graphique du titre voulu (unité **journalière** recommandée).
2. Pine Editor → coller `vertex_signals.pine` → « Ajouter au graphique ».
3. Créer une alerte (⏰) :
   - **Condition** : `Vertex Signals` → choisir le signal (ex. `VX BREAKOUT_CONFIRMED`).
   - **Webhook URL** : `https://<votre-hote>/api/tradingview/webhook`
   - **Message** (adapter le secret et le signal) :
     ```json
     {"secret": "une-longue-chaine-aleatoire",
      "symbol": "{{ticker}}",
      "signal": "BREAKOUT_CONFIRMED",
      "timestamp": {{timenow}},
      "price": {{close}}}
     ```
     ⚠️ `{{timenow}}` est en **millisecondes** chez TradingView : le webhook
     accepte les secondes ; divisez par 1000 (`{{timenow}}` → utiliser
     `"timestamp": {{time}}` sur les alertes de clôture de barre, ou laisser
     le payload du script Pine qui envoie déjà des secondes).
4. Répéter pour chaque signal utile. Les signaux acceptés :
   `CORRECTION_DEEP, SUPPORT_RECLAIM, BREAKOUT_CONFIRMED, BREAKOUT_RETEST,
   MOMENTUM_ACCELERATION, VOLUME_EXPANSION, VOLATILITY_COMPRESSION,
   VOLATILITY_EXPANSION, TREND_ALIGNMENT, FAILED_BREAKOUT, THESIS_INVALIDATION`.

## 3. Garanties du webhook

- secret obligatoire (comparaison en temps constant) ;
- symbole (≤ 8 alphanumériques) et signal (liste fermée) validés ;
- timestamp validé, fenêtre anti-replay de 15 minutes ;
- déduplication (même symbole+signal sous 10 minutes = rejeté) ;
- réponse immédiate (le traitement est asynchrone) ;
- l'événement stocké porte `action: "REEVALUATE"` — jamais un ordre.
