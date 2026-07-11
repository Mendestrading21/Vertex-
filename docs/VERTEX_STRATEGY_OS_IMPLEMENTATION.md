# VERTEX STRATEGY OS — Rapport d'implémentation

Date : 2026-07-11 · Branche : `claude/vertex-strategy-os-h17dso`
Baseline : 250 tests → Final : **414 tests verts** (164 nouveaux).

## 1. Architecture avant / après

**Avant** : monolithe `terminal.py` (~10 430 lignes) + ancien package quant à
nom personnel (23 modules à la racine) + `vertex/` embryonnaire (app, engines,
services, ui, data). Six moteurs de verdict concurrents, constantes
contradictoires, provenance non tracée.

**Après** :

```
vertex/
├── ai/              analyste Claude lecture seule (registre d'outils, agent,
│                    validation stricte, fallback déterministe, audit, briefs FR)
├── alerts/          alertes intelligentes (6 niveaux, ACTIONABLE sous conditions)
├── anomalies/       moteurs données / actions / options (format standard)
├── app/             config, état partagé, routes Blueprints (+ strategy_os_api)
├── catalysts/       earnings_engine (modes, dossier hold-through), event_engine
├── data/            univers, constituants, entreprise, calendrier (existant)
├── data_sources/    provenance, qualité, routeur de sources, réconciliation,
│                    scheduler IBKR, passerelle readonly, taux par échéance,
│                    TradingView (store + webhook), fallback EOD, fondamentaux
├── engines/         decision_stack, comité, scorecard, quant_engine, timeframes,
│                    performance_ledger (track record complet), analyse, etc.
├── market/          contexte, secteurs, regime_features, regime_engine (12 régimes)
├── observability/   logging (redaction), metrics, health, traces, diagnostics
├── options/         legacy_engine (migré), chain_loader (entonnoir),
│                    contract_filter, liquidity, vol_surface, scenario_pricer,
│                    contract_scorer, call_selector, bearish_tactical, recommendation
├── portfolio/       models (positions réelles/simulées), team_engine (8-10),
│                    team_roles, replacement_engine, risk_engine (réel),
│                    legacy_basket_risk, factor_exposure, correlation,
│                    stress_tests, portfolio_guard
├── quant/           scoring, pivots, ml_calibration
├── research/        chart_read, factory (cycle de vie + walk-forward),
│                    hypothesis/experiment/dataset/backtest/walk_forward/
│                    calibration/robustness/costs/registry/reporting,
│                    institutional/ (10 modules facteurs → ensemble)
├── scanner/         universe, scan_budget, stages, candidate_pipeline,
│                    daily, weekly
├── services/        live_engine, persist, news_plus, status, market_clock (existant)
├── strategy/        constitution versionnée + profils JSON, config (migré),
│                    legacy_adapter, executive_engine (décision UNIQUE), memory/
├── ui/              pages existantes + strategy_os (hub)
└── validation/      out_of_sample (PSR/DSR/PBO), probability_calibration, drift
tradingview/         vertex_signals.pine + guide d'installation
```

## 2. Migration du namespace

22 modules migrés (`git mv`, historique préservé), imports réécrits dans
`terminal.py`, 6 fichiers de routes/données, tests et CI ; 5 imports morts
supprimés du monolithe. Détail : `docs/NAMESPACE_MIGRATION_AUDIT.md`.
Zéro nom personnel dans l'arbre (`test_no_personal_name_in_current_tree`),
clé localStorage migrée `vxPos` avec reprise automatique des données.

## 3. Fichiers supprimés / créés / modifiés

- **Supprimés** : l'ancien package personnel entier (23 fichiers, déplacés).
- **Créés** : ~70 modules Python + 12 fichiers de tests + 4 documents + 2
  fichiers TradingView (voir `git log --stat`, 12 commits de phases).
- **Modifiés** : `terminal.py` (imports, salutation, clé positions, blueprints
  TradingView + Strategy OS), routes command/analysis_api/content/system,
  `vertex/engines/analysis.py`, `vertex/ui/vault.py`, CI, README, CLAUDE.md, docs.

## 4. Contradictions corrigées

| Défaut | Correction |
|---|---|
| 6 moteurs de verdict concurrents | `executive_engine` = seule couche de décision finale (5 décisions constitutionnelles), gardé par test |
| R:R 1.5 vs 2.0 selon la page | seuil unique `MIN_REWARD_RISK = 1.5` (présentable) / 2.5 (bon) dans le scorer contextuel |
| delta 0.70–0.88 favorisé (§6.2) | catégories BALANCED 0.40-0.60 / DYNAMIC 0.28-0.45 / ULTRA_CONVEX 0.18-0.30 / BEARISH 0.30-0.55, score contextuel |
| DTE 150–400 par défaut (§6.3) | constitution : 60–270 absolu, 90–210 préféré, appliqué par les filtres durs |
| CALLS/PUTS mélangés, covered calls proposés (§6.4) | moteur CALL et module PUT tactique totalement séparés ; vente d'options interdite par constitution + tests |
| une seule horizon de simulation (§6.5) | grille 7 spots × 7 temps (0-28 j) × 5 IV (±20 %) |
| taux fixe global (§6.6) | courbe de taux par échéance + fallback documenté + sensibilité |
| dividendes ignorés (§6.7) | BS avec rendement continu + warning ex-dividende dans le setup |
| BS présenté comme vérité (§6.8) | étiquettes BROKER_GREEKS / MODEL_ESTIMATE / FALLBACK_ESTIMATE, limitations explicites, Greeks IBKR préférés |
| risque sur candidats scanner (§6.9) | `risk_engine` exige positions RÉELLES ou simulées explicites (ValueError sinon) ; l'ancien moteur renommé `legacy_basket_risk` |
| track record signal=trade (§6.10) | `performance_ledger` : 6 types de traces, métriques jamais mélangées |
| provenance absente (§6.1) | `ProvenancedValue` {value, source, source_mode, timestamp, age_seconds, quality, fallback_used} + paquet `as_of` |

## 5. Intégrations

- **IBKR** : passerelle `readonly=True` codé en dur, worker unique,
  RequestTimeout 45 s conservé, scheduler à 7 priorités (dédup, cache TTL,
  retry borné, circuit breaker, annulation des requêtes rassises, limite de
  lignes de marché), entonnoir de chaînes (jamais tout l'univers).
- **TradingView** : `POST /api/tradingview/webhook` (secret en comparaison
  constante, validation symbole/signal/timestamp, anti-replay 15 min, dédup
  10 min, réponse immédiate, `action: REEVALUATE` — jamais un achat),
  Pine Script 11 signaux + guide.
- **Claude** : liste blanche de 22 outils (aucun outil d'ordre — rejet à
  l'enregistrement), prompts interdisant le calcul et la décision, validation
  stricte du schéma de réponse (clés fermées, langage de certitude rejeté),
  rate limit, audit, **fallback déterministe** : Vertex fonctionne sans IA.

## 6. Validation quantitative

Research Factory : cycle IDEA→…→APPROVED verrouillé (définition 11 champs,
12 contrôles de biais, walk-forward obligatoire) ; walk-forward sans
look-ahead (train strict + embargo) ; PSR/DSR/PBO conservés
(`vertex/validation/out_of_sample.py`) ; calibration des probabilités (Brier,
log loss, fiabilité par décile, stabilité) avec affichage « Confiance
insuffisante » ; drift (7 codes) avec désactivation automatique d'un signal
technique permise — la constitution, jamais.

## 7. Tests

414 tests (`python -m pytest tests/ -q`), dont tous les tests obligatoires
§38 (noms canoniques dans `tests/test_strategy_os_final_guards.py`,
`test_namespace_guards.py`, et les suites par domaine). Fixtures anonymisées :
chaînes liquides/illiquides, zero bid, spread large, smile incohérent, split,
earnings, quotes rassises, divergences de sources, portefeuille concentré,
positions simulées.

## 8. Vérification navigateur réel

Chromium (Playwright) sur `/`, `/strategy-os`, `/anomalies`, `/journal`,
`/options-lab`, `/equipe` : **0 erreur JavaScript**, `/api/client-log` = 0.
Seule requête échouée : Google Fonts (proxy sandbox — repli police système).
App démarrée en mode dégradé (`NO_IBKR=1 DEMO=1`) : toutes les routes
répondent, le badge démo est affiché par le serveur uniquement.

## 9. Limitations restantes (honnêteté)

- Le scan quotidien historique (prix/scores) reste alimenté par le
  téléchargement différé (yfinance/Stooq) avec bascule IBKR pour les
  options/quotes — le routage valeur-par-valeur `data_sources` est en place
  mais le monolithe n'est pas encore entièrement re-câblé dessus.
- Les anciennes vues (comité, scorecard, options_lab) existent toujours comme
  ENTRÉES ; leurs pages historiques affichent encore leurs vocabulaires — la
  décision canonique est celle de `/api/strategy/decision/<sym>`.
- `/api/anomalies/<sym>` travaille sur la série close-only du scan (gaps et
  volumes non couverts sur cette route tant que les barres OHLCV complètes ne
  transitent pas par le scan).
- Univers = constituants actuels (biais du survivant documenté dans
  `vertex/research/dataset.py`).
- IV history par titre non encore persistée (IV Rank refusé honnêtement tant
  que < 20 observations).

## 10. Variables d'environnement

`VERTEX_CODE` (verrou), `VERTEX_SECRET`, `ANTHROPIC_API_KEY` (optionnel),
`VERTEX_AI_MODEL` (défaut claude-sonnet-5), `TRADINGVIEW_SECRET` (webhook,
503 si absent), `NO_IBKR=1`, `DEMO=1`, `IBKR_HOST/PORT/CLIENT_ID`,
`VERTEX_LAN=1`.

## 11. Lancement / diagnostic / restauration

- Lancement : `python terminal.py` (port 5002) ; Windows `Lancer_VERTEX.bat`.
- Santé : `GET /healthz` · `GET /api/live/status` · `GET /api/system/diagnostics`
  · `GET /api/data-quality` · `GET /api/client-log` (doit rester 0).
- Hub : `GET /strategy-os` (alias `/vertex-intelligence`).
- Tests : `python -m pytest tests/ -q` (100 % requis avant tout commit).
- Restauration desk : backups quotidiens `desk_backup_*.json` +
  `/api/desk/restore`. Constitution : versions conservées dans
  `vertex/strategy/profiles/` (recharger une version antérieure).
