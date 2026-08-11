# VERTEX — Matrice Page × Données × Graphiques (Phase 2)

> Branche `agent/vertex-total-rebuild` @ `362c7d4`. Une ligne par espace principal.
> Croise `ROUTE_ENDPOINT_MAP.md` (routes/endpoints/moteurs) et
> `CHART_INVENTORY.md` (graphiques). Priorité de refonte : P0 (haute) → P3 (basse).

## Légende
- **Débordement** : mesure Phase 0 §5 (mobile 390 / desktop 1440).
- **Doublons** : graphiques répétés ailleurs (voir C-09).

---

### 1. Briefing `/` — `briefing.py`
- **Mission** : « que s'est-il passé, quel risque/opportunité, quelle action du jour ».
- **Question principale** : quel est le régime et la première action analytique ?
- **Endpoints** : `/scan`, `/api/briefing/editorial`, `/api/command`,
  `/api/market/summary`, `/api/market/regime`, `/api/alerts/status`, `/api/pos-quotes`.
- **Moteurs** : `briefing.build_editorial`, `market_lens`, `committee`, `decision_stack`.
- **Graphiques (11)** : 4 jauges (régime×2, vix, breadth — **redondantes**),
  market SPY area, breadth 1-barre, R:R bars, posture donut, rotation secteurs,
  calendrier timeline. **Beaucoup de doublons** avec Marchés.
- **Débordement** : **mobile OVERFLOW 430/390** · desktop ok.
- **Priorité** : **P0** (page d'accueil, doublons + overflow + densité).

### 2. Marchés `/markets` — `markets_page.py`
- **Mission** : état macro/indices/secteurs/breadth/volatilité.
- **Question** : quel régime, où va le capital, participation saine ?
- **Sous-vues** : `overview·macro·sectors·breadth·volatility`.
- **Endpoints** : `/scan`, `/api/market/summary`, `/api/market/regime`.
- **Moteurs** : `regime_engine`, `market_lens`, internals du scan.
- **Graphiques (~19)** : **4 vues des mêmes secteurs** (bar/heatmap/RRG/treemap),
  **3 jauges régime + 3 jauges breadth**, indices multi-lignes, SPY, courbe des
  taux, calendrier, funnel (**doublon** Opportunités), rings, waterfall santé,
  distribution HTML (hors VXCharts).
- **Débordement** : **mobile OVERFLOW 469/390** · desktop ok.
- **Priorité** : **P0** (surcharge graphique majeure + overflow).

### 3. Opportunités `/opportunities` — `opportunities_page.py`
- **Mission** : entonnoir d'idées (signaux → univers → contrats → anomalies → catalyseurs).
- **Question** : quelles idées méritent l'attention et pourquoi ?
- **Sous-vues** : `radar·stocks·options·anomalies·calendar`.
- **Endpoints** : `/scan`, `/api/opportunities/funnel`, `/api/data-quality`,
  `/api/options/simulate`.
- **Moteurs** : `tracking.repository`, `options` (scenario_pricer), scoring du scan.
- **Graphiques (8)** : `op-radar` (**scatter mal nommé**), funnel (**doublon**),
  scoreBar HTML, payoff, scenarioMatrix, theta, iv-sensitivity, timeline.
- **Débordement** : **mobile OVERFLOW 456/390** · desktop ok. (Captures mobiles
  très lourdes ≈1,5 Mo → contenu très dense.)
- **Priorité** : **P1**.

### 4. Portefeuille `/portfolio` — `portfolio_page.py`
- **Mission** : positions réelles IBKR, risque, allocation, options détenues, watchlist.
- **Question** : où est le risque, l'équipe est-elle équilibrée ?
- **Sous-vues** : `team·positions·options·risk·watchlist`.
- **Endpoints** : `/scan`, `/api/positions/state`, `/api/ibkr/positions`,
  `/api/pos-quotes`, `/api/position-decision/<sym>`, `/api/portfolio/team`,
  `/api/options/analyze`.
- **Moteurs** : `positions/*`, `portfolio/risk_engine`, `multileg_lab`.
- **Graphiques (8)** : P&L bars, allocation treemap (**recouvre** contrib+roles),
  roles donut, options treemap (**couleur PUT/CALL sans sens**), payoff combiné,
  payoff drawer, HHI gauge, secteur donut.
- **Débordement** : **mobile OVERFLOW 403/390** · desktop ok. Repli **honnête**
  sans marque quand aucune position.
- **Priorité** : **P1** (dépend d'IBKR ; états vides bien gérés).

### 5. Analyse `/analysis` (+`/analysis/<sym>`) — `analysis_page.py`
- **Mission** : fiche titre canonique unique (verdict, score/40, scénarios, technique, options, décision).
- **Question** : dois-je m'intéresser à ce titre, à quel prix, avec quelle invalidation ?
- **Endpoints** : `/api/ticker/<sym>`, `/api/analyst/<sym>`, `/api/names`,
  `/api/anomalies/<sym>`, `/api/strategy/decision/<sym>`, `/api/options-for/<sym>`,
  `/api/planning/ticket`, `/api/tradingview/signals`.
- **Moteurs** : `decision_stack`, `quant_engine`, `evidence`, `options_lab`, `executive_engine`.
- **Graphiques (2)** : scorecard radar (**doublon** Intelligence), `an-chart`
  (**pièce maîtresse** : lwCandlestick + MM + plan + événements).
- **Débordement** : **mobile ok 390** · desktop ok. **Meilleure page responsive.**
- **⚠️ Honnêteté** : décision « confiante » possible sur ticker inexistant (C-08).
- **Priorité** : **P1** (référence de qualité ; corriger C-08 + 2 chandeliers C-05).

### 6. Options `/options` — `options_intel_page.py`
- **Mission** : Options Intelligence (environnement long-option, vol, radar, scénarios, événements).
- **Question** : l'environnement est-il porteur pour acheter de la convexité ?
- **Sous-vues** : `overview·volatility·radar·scenarios·events`.
- **Endpoints** : `/api/options/overview`, `/environment`, `/volatility/<sym>`,
  `/scenarios/<sym>`, `/vol-charts/<sym>`, `/event-risk/<sym>`.
- **Moteurs** : `options/*` (environment, scenario_pricer, event_risk, vol_charts).
- **Graphiques** : gauge environnement, payoffs par stratégie. Suite options
  **à garder** (chacune une question distincte).
- **Débordement** : **mobile ok 390** · desktop ok.
- **⚠️ Double rattachement** : espace nav **et** décrit comme sous-page
  d'Opportunités (`redesign.py:87/122`).
- **Priorité** : **P2** (clarifier le rattachement).

### 7. Performance `/performance` — `performance_page.py`
- **Mission** : journal, track record auto-mesuré, enseignements.
- **Question** : ma méthode est-elle rentable et disciplinée ?
- **Sous-vues** : `overview·journal·track-record·learnings`.
- **Endpoints** : `/api/track-record` + journal desk (localStorage).
- **Moteurs** : `track_record`, `performance_ledger`.
- **Graphiques (5)** : equity, drawdown, monthly heatmap, distribution, track-bar.
  **À garder** (conclusions explicites). Données locales → mode delayed honnête.
- **Débordement** : **mobile OVERFLOW 417/390** · desktop ok.
- **Priorité** : **P2**.

### 8. Intelligence `/intelligence` — `intelligence_page.py`
- **Mission** : cerveau (analyste, comité, stratégie, impacts, recherche, mémoire).
- **Question** : diffuse — **hub multi-vues** (mission la moins nette).
- **Sous-vues** : `analyst·committee·strategy·impacts·research·memory`.
- **Endpoints** : `/api/decision/<sym>`, `/api/committee-review`,
  `/api/strategy/profile`, `/api/strategy/decision/<sym>`, `/api/validator`, `/api/desk`.
- **Moteurs** : `committee`, `constitution`, `executive_engine`, `quant_engine`, `strategy/memory`.
- **Graphiques (4)** : analyst radar (**doublon** Analyse), committee gauge,
  research Sharpe walk-forward, impact flow.
- **Débordement** : **mobile OVERFLOW 405/390** · desktop ok.
- **Priorité** : **P2** (mission à resserrer ; candidat à fusion/redécoupage IA).

### 9. Système `/system` — `system_page.py`
- **Mission** : connexions, qualité données, automatisations, réglages, archive.
- **Question** : mes données/connexions sont-elles fiables ?
- **Sous-vues** : `connections·data·automations·settings·archive`.
- **Endpoints** : `/api/system/*`, `/api/data-quality`, `/api/ai/*`,
  `/api/live/status|refresh`, `/api/desk*`, `/api/client-log`.
- **Moteurs** : `connections`, `status_service`, `startup`, `config_validation`.
- **Graphiques (3)** : brain-movers bars, moteurs OK gauge, data-quality donut.
- **États honnêtes** : IBKR OFFLINE / TV CONFIGURATION_MISSING / IA MISSING bien
  étiquetés ✅. Mais **data-quality tout MISSING en démo** (C-07).
- **Débordement** : **mobile OVERFLOW 547/390 (le pire)** · desktop ok.
- **Priorité** : **P0** (overflow le plus sévère + C-07).

---

## Pages secondaires (hors `PRIMARY_NAV`)
| route | module | mission | débordement mobile | priorité |
|---|---|---|---|---|
| `/tracking` | `tracking_page.py` | suivis hypothétiques (approfondit Portefeuille) | **OVERFLOW 448/390** | P2 |
| `/design-system` | `design_system_page.py` | design system vivant | ok 390 | P3 |
| `/system/design-system` | `design_system_demo.py` | vitrine composants (données factices) | — | P3 (retrait post-refonte à décider) |

## Synthèse priorités
- **P0 (overflow + doublons majeurs)** : Système, Marchés, Briefing.
- **P1** : Opportunités, Portefeuille, Analyse (corriger C-05/C-08).
- **P2** : Performance, Intelligence, Options, Tracking.
- **P3** : Design system.
