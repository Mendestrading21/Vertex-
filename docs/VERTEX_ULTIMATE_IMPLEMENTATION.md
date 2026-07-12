# VERTEX ULTIMATE INSTITUTIONAL OS — État d'implémentation

Passe du 2026-07-11, interrompue proprement en fin de session (règle de
vérité : ce document liste EXACTEMENT ce qui est livré et prouvé, et ce
qui reste). Base de départ : fin d'Experience OS (`ef6bf06`, 543 tests).

## Livré, testé et committé dans cette passe

### Phases 1-2 — Baseline & audit
- `docs/VERTEX_ULTIMATE_BASELINE.md`, `docs/VERTEX_ULTIMATE_AUDIT.md`
  (15 écarts identifiés, chacun avec décision).

### Phases 3-5 — Hard gates (commit `d52d837`)
- **R:R 2:1** : nouvelle règle bloquante `RR_BELOW_MINIMUM` dans
  l'ExecutiveEngine (reward_risk < 2 → jamais ACHETER/RENFORCER) ;
  `MIN_REWARD_RISK` contrats 1.5 → 2.0.
- **Régime UNKNOWN** : `new_risk_allowed=False`, priorité ATTENDRE,
  taille 0, 3 confirmations — l'UI ne peut plus afficher « autorisé » à
  confiance nulle ; règle `REGIME_BLOCKS_NEW_RISK` (le paquet de décision
  embarque désormais le régime courant).
- **Denylist étendue** : `auto_close_position`, `auto_rebalance`,
  `one_click_trade` (gardes statiques + registre d'outils IA).

### Phases 6-12 — Runtime (commit `2223e48`)
- `.env.example` complet (§11) + `vertex/app/config_validation.py`
  (CONFIGURED/MISSING/INVALID, conséquence exacte, zéro valeur exposée)
  → `GET /api/system/config`.
- `vertex/services/startup.py` : séquence ordonnée (config → Claude →
  IBKR → TradingView → stockage → moteurs → scheduler → live), rapport
  → `GET /api/system/startup-report` — vérifié en réel (statuts honnêtes
  MISSING/OFFLINE/CONNECTED en mode cloud démo).
- `vertex/ai/health.py` : santé Claude déduite de la config + du dernier
  appel réel (jamais « connecté » sans preuve). Les providers demandés
  par §10 existaient déjà (`provider.py`, `anthropic_provider.py`,
  `fallback.py`, `tool_registry.py`, `response_validator.py`,
  `prompt_builder.py`) — health.py complète la façade.
- `vertex/scheduler/registry.py` : 17 jobs canoniques (§24), battements
  émis par les boucles historiques (scan, alertes, calendrier, hebdo,
  fondamentaux, backup desk) → `GET /api/system/automations`.
- **SSE** : `vertex/services/live_stream.py` (pub/sub, rejeu
  Last-Event-ID) + `GET /api/live/events` + client
  `live-updates.js` (reconnexion, déduplication, repli polling,
  ralenti onglet masqué) chargé par le shell — vérifié en Chromium :
  `VX.liveStatus() === 'LIVE'`, 0 erreur console.

## Vérifications reproduites en fin de passe
- `python -m pytest tests/ -q` → **543 passed, 0 failed**.
- 8 pages en Chromium : **0 erreur console**, `GET /api/client-log` → 0.
- SSE actif (statut LIVE côté client), startup report exposé, registre de
  jobs alimenté.
- Aucun chemin d'ordre (gardiens verts), aucun nom personnel.

## Seconde passe (même session, commits suivants) — TOUT LIVRÉ

1. **P13 News & Brief** ✅ — pipeline validation/dédup/impact + brief
   PRE_MARKET/INTRADAY/CLOSE/WEEKLY sourcé, rien d'inventé (tests).
2. **P14 Company Intelligence** ✅ — `vertex/companies` (jumeau honnête,
   change_detector → recalc_required) + `/api/company/twin/<sym>`.
3. **P16-19 Options** ✅ — Options Command Center (`/portfolio?view=options`,
   CALLS/PUTS séparés), drawer d'analyse par position (§20-21, décision via
   `/api/position-decision`), comparateur 3 contrats Pareto (§22).
4. **P21-35 Obsidian Copper Deep** ✅ — palette §30 complète, zéro bleu
   identitaire (liens cuivre, séries cuivre/beige/gris/violet), tests
   no-blue ; vues `?view=automations` et `?view=impacts`.
5. **P27 Impacts** ✅ (flux SSE + chaîne d'impact ; propagation automatique
   partielle — voir VERTEX_LIMITATIONS.md).
6. **P36-41** ✅ — tests nommés (556 verts), parcours 9/9 trois tailles,
   SW v9, 16 documents §57, rapport final.
