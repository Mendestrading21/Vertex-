# VERTEX — Analyse d'intégrations externes (6 dépôts)

> Évaluation **sécurité d'abord** de 6 dépôts pour un terminal d'ANALYSE en
> **lecture seule**. Invariant absolu de Vertex : `READONLY=True` — jamais
> d'ordre passé (règle produit + verrouillée par les tests
> `test_no_order_path_anywhere_in_source`, `test_ai_registry_has_no_order_tool`).

## Verdict par dépôt

| Dépôt | Type | Ordres ? | Verdict READONLY | Recommandation |
|-------|------|:--------:|------------------|----------------|
| **tradingview/lightweight-charts** | Lib graphique | non | ✅ sûr | ✅ **INTÉGRÉ** (Analyse — chandeliers pro) |
| **atilaahmettaner/tradingview-mcp** | MCP (libs read-only) | non | ✅ sûr | 🟢 **Intégrer (backtest/screener)** |
| **omdv/ibkr-mcp-server** | MCP IBKR (Python) | non | ✅ sûr | 🟡 Optionnel (2e passerelle) |
| **ertugrul59/tradingview-chart-mcp** | MCP (captures TV) | non | ✅ sûr | 🟡 Marginal (Selenium/ToS) |
| **code-rabi/interactive-brokers-mcp** | MCP IBKR (Node) | **OUI** | ⛔ chemins d'ordre | 🔴 **Rejeter** |
| **marketcalls/openalgo** | Plateforme algo | **OUI** | ⛔ chemins d'ordre | 🔴 **Rejeter** |

## Détail

### 🟢 lightweight-charts (TradingView, Apache-2.0)
Bibliothèque de graphiques financiers open-source, ~35 Ko gzip, canvas HTML5, **pur frontend, zéro donnée/broker/ordre**. Chandeliers/OHLC/aire pro avec axe temps, crosshair, zoom/pan, multi-panneaux — nettement mieux que le candlestick SVG fait main. **Valeur : qualité des graphiques prix/chandeliers** (§19 du brief). Se branche sur les endpoints OHLCV déjà servis par Vertex. **Contraintes : (1) lien d'attribution TradingView à afficher sur les graphiques (licence) ; (2) c'est un upgrade qualité, pas une capacité nouvelle ; (3) JS à télécharger et auto-héberger (CSP OK, self-contained).**

### 🟢 tradingview-mcp — libs `tradingview-screener` + `tradingview-ta` (MIT)
Le format MCP n'est pas utile (Vertex n'est pas un hôte d'agent), mais les **libs sous-jacentes sont read-only et pip-installables sans compte** :
- **Moteur de backtesting** : 9 stratégies (RSI, Bollinger, MACD, EMA cross, Supertrend, Donchian, Keltner, Triple EMA) avec walk-forward, détection d'overfitting, Sharpe/Calmar/max-DD/win-rate. **Vertex n'a PAS de backtesting** → courbes d'équité directement traçables.
- **Screeners multi-bourses** (NASDAQ/NYSE/Binance…) pour listes de candidats read-only.
- **Consensus TA TradingView** (ACHAT/VENTE/NEUTRE) = 2e source de signal.
- **Réserves** : données Yahoo/TV plus faibles que le flux IBKR temps réel (préférer IBKR pour les cours) ; tout texte news doit passer par `news_plus.sanitize_news()` (XSS). C'est une **fonction nouvelle** (au-delà du strictement visuel).

### 🟡 omdv/ibkr-mcp-server (Python, ib_async, MIT) — pas d'ordres
Vraies données en plus : **TWS Scanner** (top gainers/losers/most active), **filtrage greeks par bande de delta**, **OHLCV historique**. MAIS : lance une **2e passerelle IB** (Docker) en parallèle du worker TWS de Vertex → collisions clientId/entitlements ; son `client.py` est en `readonly=False` (à forcer en True si code réutilisé). Chemin sûr : **relever les méthodes read-only** (scanners/history/market_data) dans la connexion ib_async existante, en routes Flask read-only — pas lancer le serveur entier.

### 🟡 ertugrul59/tradingview-chart-mcp (Python, MIT) — pas d'ordres
Captures d'images de graphiques TradingView (Selenium). Seule chose que le moteur graphique de Vertex ne reproduit pas nativement (images TV pixel-perfect). MAIS : **dépendance Selenium/ChromeDriver lourde**, requiert une **session TV connectée (scraping, contre les CGU de TradingView)**, largement redondant. Peu de valeur nette.

### 🔴 code-rabi/interactive-brokers-mcp (Node, MIT) — **REJET**
Expose IBKR AVEC exécution d'ordres (`orders.ts`, `place_order`/`confirm_order`). Les outils lecture sont **redondants** avec l'IBKR read-only de Vertex. Serveur Node (mauvais fit Flask). **Vendoriser son code casserait l'invariant READONLY.**

### 🔴 marketcalls/openalgo (Flask, **AGPL-3.0**) — **REJET**
Plateforme de trading algo dont le **cœur est l'exécution d'ordres** (34 brokers). Deux bloqueurs : (1) importer son code ajouterait des chemins d'ordre → viole READONLY + casse les tests gardiens ; (2) **copyleft AGPL-3.0** imposerait AGPL à Vertex. Seul usage défendable : **s'inspirer** de ses dashboards options read-only (GEX / max-pain / IV-smile) et les **réimplémenter** dans le stack de Vertex.

## Plan de connexion recommandé (sûr)

1. ✅ **lightweight-charts** → chandeliers pro **livrés sur Analyse** (`VXCharts.lwCandlestickCard`, v4.2.3 auto-hébergé, attribution TV affichée). Repli auto sur le candlestick Chart.js si OHLC daté absent. *Options : pas de graphe chandeliers du sous-jacent (page = analytics options : OI/strike, scénarios, thêta, greeks) → non applicable, sauf ajout délibéré d'un contexte prix.*
2. **tradingview-screener/-ta** → moteur de backtesting + screeners + consensus TA, en routes Flask read-only, courbes via les composants existants. *Capacité nouvelle (à valider comme hors-visuel).*
3. Idées à réimplémenter (pas de dépendance) : dashboards options GEX/max-pain/IV-smile (inspiration OpenAlgo), TWS Scanner (idée omdv, via l'ib_async existant).
4. **Jamais** : chemins d'ordre (code-rabi IBKR-MCP, OpenAlgo). Toute réutilisation IBKR force `readonly=True`.

> Toute intégration réelle implique un **téléchargement/dépendance externe** → demande une validation explicite avant exécution. Rien n'est téléchargé/installé sans accord.

## Passe 2 — triage de ~30 dépôts (design, charts, options, MCP/data)

Verdict honnête : sur ~30 ressources, **une poignée seulement est intégrable** dans l'archi
Flask + HTML/JS-en-chaînes-Python + vanilla READONLY de Vertex. Le reste est soit du **React/
build** (non importable sans réécriture front), soit **redondant**, soit à **chemins d'ordre**.

- ✅ **LIVRÉ — Stratégies options multi-jambes** (inspiré d'optionlab/optionvisualizer, mais
  **réimplémenté NATIVEMENT** : aucune dépendance ajoutée, ni GPL-3.0 ni scipy ; réutilise le
  Black-Scholes maison). `vertex/engines/multileg_lab.py` + route `/api/options/strategies/<sym>`
  + UI « Stratégies multi-jambes » (payoff, PoP, gain/perte max, breakevens, greeks). 10 tests
  math. Comble le gap réel : le mono-jambe du scenario_pricer.
- 🟡 **Greeks d'ordre supérieur** (vanna/charm/vomma — formules MIT d'optionvisualizer à lifter
  dans options_lab, numpy suffit) : additif, non encore fait.
- 🟡 **Design — patterns tremor/shadcn** : uniquement en inspiration CSS vanilla (métrique-cards,
  delta-badge, tracker). Le design system maison (tokens.css) est déjà solide ; valeur marginale.
- 🟢 **DATA optionnel** (réserve dépendance/clé/réseau, à valider) : `financial-datasets`
  (états financiers — comble le trou Reuters bloqué IBKR), `unusual-whales` (flux d'options,
  abonnement payant), `tradingview-screener` (screener, ToS fragile).
- 🔴 **Rejeté** : React (shadcn, radix, MUI, tremor, recharts, visx, templates next/astro),
  Tailwind (impose un build), ECharts (bloat redondant), Streamlit-apps (runtime propre),
  TV widgets (iframes tiers = privacy/CSP), Selenium scrapers, et tout MCP à chemins d'ordre
  (interactive-brokers-mcp, openalgo, ibkr-mcp-server générique).
