# Vertex — Rapport de tests (Ultimate)

`python -m pytest tests/ -q` → **556 passed, 0 failed** (état au commit
final ; relancer pour re-vérifier).

## Suites
30 fichiers de tests — gardiens de sûreté (test_no_orders, readonly IBKR,
registre IA sans outil d'ordre), constitution/décision (executive engine,
hard gates R:R 2:1 + UNKNOWN), provenance/qualité, options (scénarios,
sélecteur, PUT rare, multiplicateur, conventions %), portefeuille (risque
réel, 11e position), TradingView (secret/replay/dédup/jamais ACHETER),
runtime IA (whitelist, repli), golden numériques (31), UI canoniques
(routes/boutons/liens/valeurs invalides/états/SW), thème Obsidian
(zéro bleu), brief (sources/timestamp/rien d'inventé/dédup), startup,
companies (jumeau honnête, détecteur de changement).

## Vérifications navigateur (Chromium réel)
- 10 pages/vues × 3 tailles (1600/768/390) : **0 erreur console,
  0 débordement** ; `/api/client-log` → 0.
- Parcours A-I : 9/9 PASS (dégradés IBKR/TV/Claude inclus).
- SSE : statut client LIVE, rejeu après reconnexion.
