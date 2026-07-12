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

## Restant à faire (phases non entamées — liste exacte)

1. **P13 News & Brief** : `vertex/market/{news_pipeline,news_dedup,
   news_impact,daily_brief}.py` — brancher le fil réel existant
   (`news_state`, assaini) sur un brief PRE_MARKET/INTRADAY/CLOSE/WEEKLY
   150-280 mots sourcé + version compacte + « actualité dominante » dans
   le Briefing. Rien d'inventé : sections actualité absentes quand le
   flux est hors ligne (mode démo).
2. **P14 Company Intelligence** : `vertex/companies/*` (façade sur
   `data/company.py` + fondamentaux + `change_detector`).
3. **P16-18 Options** : Options Command Center (`/portfolio?view=options`
   avec Greeks agrégés et compteurs CALLS/PUTS séparés), analyse par
   position option (drawer §20 + graphiques §21 sur les moteurs
   existants), comparateur 3 contrats (§22).
4. **P21-35 Thème Obsidian Copper Deep** : tokens obsidienne/cuivre §30,
   suppression du bleu identitaire (liens `--vx-info`, série graphique
   n° 2), `chart-theme-obsidian-copper.js`, widgets §44 (What Changed,
   Theta Burn, Data Freshness…), vues `?view=automations` (l'API existe)
   et `?view=impacts`.
5. **P27 Graphe d'impact** (événements → recalculs) — le bus SSE posé
   dans cette passe en est le support.
6. **P36-41** : tests §53 restants (les gardes R:R/UNKNOWN/readonly de
   cette passe sont couverts par les suites existantes ; les tests nommés
   `test_rr_gate_is_two`, `test_unknown_regime_blocks_risk`,
   `test_no_blue_*` sont à écrire), parcours 1-9, bump SW, 19 documents
   §57, rapport final complet.

## Notes techniques pour la reprise
- Le SSE maintient une connexion ouverte : les scripts Playwright doivent
  attendre `domcontentloaded` + délai, plus `networkidle` (les scripts de
  vérification de cette passe ont été adaptés).
- Les battements de jobs s'insèrent dans les boucles historiques — trois
  sites (`_cal_loop`, `_fund_loop`, `_weekly_loop`) ont une indentation
  non triviale : préférer des insertions à points d'ancrage exacts.
