# Règles d'intégrité des données Vertex (règle produit n°4)

1. **Jamais de chiffre inventé** présenté comme réel. Donnée absente → `—` / `n/d`. **Ne jamais masquer une
   absence par `0`.** Distinguer et rendre distinctement : `0` (vrai zéro) · `—`/absent · `N/A` · `Indisponible` ·
   `Estimation` (modèle) · `Retardée` · `Périmée`.
2. **Provenance & fraîcheur visibles.** Toute valeur affichée doit pouvoir répondre : source (IBKR / yfinance /
   stooq / demo / moteur), timestamp, réel vs estimé, live/delayed/stale. Footer standard : `VX.updateIndicator`.
3. **Démo étiquetée.** Toute donnée synthétique → badge `DÉMO/MOCK/SIMULATED`. Le mot « démo » ne s'affiche que si
   le serveur le confirme (`DEMO_MODE`). **Aucun fallback mock silencieux** présenté comme réel.
4. **Statut live honnête.** Le badge « IBKR temps réel » n'est vrai que si le socket est réellement live
   (`/healthz` → `ibkr_live`), pas un flag de config. Idem greeks : broker IBKR vs `MODEL_ESTIMATE` étiquetés.
5. **News/textes externes** : toujours via `news_plus.sanitize_news()` avant de servir (XSS — rendus en innerHTML).
6. **Vertex peut dire « je ne sais pas ».** « Pas assez de données fiables pour cette analyse » est préférable à
   une recommandation incorrecte. Une recommandation sans données suffisantes ne doit pas être produite.
7. **Enveloppe de donnée cible (IBKR/marché)** — porter en interne : `value · source · timestamp · quality ·
   latency · environment · accountId · currency · isEstimated · isDelayed · isStale · error`. États UI exposés :
   live / delayed / stale / disconnected / partial / estimated / unavailable.
8. **Clés de sync desk** : toute nouvelle clé localStorage synchronisée doit figurer dans **les 4 listes**
   (`__DESK_KEYS` terminal.py, sSyncPush/Pull, `vertex/ui/journal.py`, `DESK_KEYS` de `vx_kit.py`) — sinon un push
   l'efface. Gardien : `tests/test_production.py::test_desk_sync_keys_single_source_of_truth`.
9. **desk_data.json** : ne jamais l'écraser à la main ; backups `desk_backup_*.json` + `/api/desk/restore`.
