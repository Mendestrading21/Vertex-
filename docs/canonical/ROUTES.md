# Vertex — matrice des routes

> **Status: ACTIVE**
> Last verified: 2026-07-22
> Owner: Vertex architecture

La baseline possède huit espaces visibles. La V4 rendra Marchés explicite sans
supprimer les redirections ni modifier les contrats de données existants.

Gardiens automatiques : `test_all_routes_respond` (aucune page ne rend
d'erreur), `test_all_legacy_routes_redirect` (301 + query préservée),
`test_no_route_removed_without_redirect`.

## 1. Pages (blueprint `redesign` — 9 routes)

| Route | Module | Sous-vues (`?view=`) |
|---|---|---|
| `/` | `briefing.render` | (unique, personnalisable) |
| `/markets` | redirection 302 → `/#ancre` du Dashboard (fusion : sectors→`/#sectors`, macro→`/#markets`, breadth/volatility→`/#pulse`) | — |
| `/opportunities` | `opportunities_page.render` | radar, stocks, options, anomalies, calendar |
| `/portfolio` | `portfolio_page.render` | team, positions, risk, watchlist |
| `/analysis` | `analysis_page.render_index` | recherche (`view=compare` accepté, non exploité — limitation n° 11) |
| `/analysis/<sym>` | `analysis_page.render` | fiche canonique (13 sections) |
| `/performance` | `performance_page.render` | overview, journal, track-record, learnings |
| `/intelligence` | `intelligence_page.render` | analyst, committee, strategy, research, memory |
| `/system` | `system_page.render` | connections, data, settings, archive |

Assets : `/static/vertex/<path:filename>` (cache 3600 s) ; racine `/static/`
servie par Flask (Chart.js, icônes).

## 2. Redirections legacy (301, query string conservée)

40 entrées `LEGACY_REDIRECTS` + 2 routes paramétrées :

`/daily→/` · `/analyse→/analysis` · `/news→/` ·
`/calendar→/opportunities?view=calendar` · `/semaine→/` · `/brief→/` ·
`/stocks→/analysis` · `/compare→/analysis?view=compare` ·
`/comparateur→/analysis?view=compare` · `/entreprises→/analysis` ·
`/analyse-entreprise→/analysis` · `/strategie→/portfolio` ·
`/strategy→/portfolio` · `/ma-page→/portfolio?view=watchlist` ·
`/moi→/portfolio?view=watchlist` · `/watchlist→/portfolio?view=watchlist` ·
`/suivi→/portfolio?view=watchlist` · `/suivis→/portfolio?view=watchlist` ·
`/options→/opportunities?view=options` ·
`/options-lab→/opportunities?view=options` ·
`/options-desk→/opportunities?view=options` ·
`/sectors→/#sectors` · `/heatmap→/#sectors` ·
`/catalysts→/opportunities?view=calendar` ·
`/catalyseurs→/opportunities?view=calendar` ·
`/anomalies→/opportunities?view=anomalies` ·
`/journal→/performance?view=journal` ·
`/decisions→/performance?view=journal` ·
`/review→/intelligence?view=committee` ·
`/research→/intelligence?view=research` ·
`/equipe→/intelligence?view=strategy` ·
`/equipe-du-mois→/intelligence?view=strategy` · `/bordel→/intelligence` ·
`/strategy-os→/intelligence?view=strategy` ·
`/vertex-intelligence→/intelligence?view=analyst` ·
`/health→/system?view=data` · `/settings→/system?view=settings` ·
`/parametres→/system?view=settings` · `/vault→/system?view=archive` ·
`/archive→/system?view=archive`

Paramétrées : `/titre/<sym>→/analysis/<SYM>` · `/company/<sym>→/analysis/<SYM>`.

Doublons de cible = synonymes FR/EN volontaires ({strategie, strategy},
{ma-page, moi, watchlist, suivi, suivis}, {options, options-lab,
options-desk}, {vault, archive}…). Aucun conflit.

## 3. Routes API actives

### terminal.py (13 routes non migrées)

| Route | Méthode | Rôle | UI redesign ? |
|---|---|---|---|
| `/scan` | GET | dump complet `scan_state` | ✅ (8 pages) |
| `/api/rescan` | GET/POST | réveille la boucle de scan | API seule |
| `/api/ticker/<sym>` | GET | pack options + profil + pairs | ✅ |
| `/api/company/<sym>` | GET | profil entreprise (cache hebdo) | API seule |
| `/api/names` | GET | `{ticker: nom}` (palette) | ✅ |
| `/api/correlations/<sym>` | GET | corrélations réelles 6 mois | API seule |
| `/desc/<sym>` | GET | description titre | API seule |
| `/options/<sym>` | GET | `options_pack` brut | API seule |
| `/quotes` | GET | cotations live (cache 75 s) | API seule |
| `/ibkr` | GET | snapshot IBKR | API seule |
| `/weekly-regen` | GET/POST | régénère la sélection hebdo | API seule |
| `/api/alerts/status` | GET | alertes serveur déclenchées | ✅ (briefing) |
| `/api/track-record` | GET | fiabilité mesurée des verdicts | ✅ (performance) |

### Blueprints `vertex/app/routes/*`

| Route | Méthode | Blueprint | UI redesign ? |
|---|---|---|---|
| `/login`, `/logout` | GET/POST | auth | ✅ (verrou d'accès) |
| `/api/market/summary` | GET | feeds | ✅ |
| `/api/cockpit`, `/api/watchlist`, `/api/options`, `/api/search`, `/api/weekly`, `/api/strategie`, `/api/comite` | GET | feeds | API seules |
| `/news-feed` | GET | content | API seule ⚠ (news assainies, non affichées — à trancher) |
| `/cal-feed` | GET | content | ✅ |
| `/weekly-feed` | GET | content | API seule |
| `/api/desk` | GET/POST | desk | ✅ (sync 17 clés) |
| `/api/desk/backups`, `/api/desk/restore` | GET/POST | desk | API seules (restauration manuelle) |
| `/api/watchlist-tv` | GET | desk | API seule (copier dans TradingView) |
| `/api/ibkr/positions` | GET | desk | ✅ (200 + ok:false hors ligne) |
| `/api/pos-quotes` | POST | desk | ✅ (contrat composite, corrigé) |
| `/api/vertex/<sym>`, `/api/risk` | GET | analysis_api | API seules |
| `/api/validator` | GET | analysis_api | ✅ (intelligence) |
| `/api/command` | GET | command | ✅ (briefing) |
| `/api/portefeuille` | GET | command | API seule |
| `/api/options-lab` | GET | options_lab_api | API seule ⚠ (research center sans UI — à trancher) |
| `/api/live/status`, `/api/live/refresh` | GET/POST | live_api | ✅ |
| `/api/live/report` | GET | live_api | API seule |
| `/healthz`, `/api/healthz` | GET | system | ✅ |
| `/api/client-log` | GET/POST | system | ✅ (télémétrie branchée dans vx-core.js) |
| `/api/system-status` | GET | system | ✅ |
| `/favicon.ico`, `/favicon.svg`, `/manifest.webmanifest`, `/sw.js` | GET | system | ✅ (SW `td-shell-v7`) |
| `/api/strategy/profile` | GET | strategy_os | ✅ |
| `/api/strategy/decision/<sym>` | GET | strategy_os | ✅ (200 + available:false si inconnu) |
| `/api/market/regime` | GET | strategy_os | ✅ |
| `/api/anomalies/<sym>` | GET | strategy_os | ✅ |
| `/api/portfolio/team` | GET/POST | strategy_os | ✅ |
| `/api/alerts/active` | GET | strategy_os | ✅ (notifications shell) |
| `/api/system/diagnostics`, `/api/data-quality` | GET | strategy_os | ✅ |
| `/api/decision/<sym>` | GET | decision_api | ✅ (intelligence) |
| `/api/position-decision/<sym>` | GET | decision_api | API seule |
| `/api/options-for/<sym>` | GET | decision_api | ✅ (analyse) |
| `/api/brief` | GET | decision_api | API seule (UI = `/api/briefing/editorial`) |
| `/api/committee-review` | GET | decision_api | ✅ |
| `/api/tradingview/webhook` | POST | tv_webhooks | entrant externe (secret + anti-replay) |
| `/api/tradingview/signals` | GET | tv_webhooks | ✅ (analyse) |
| `/api/briefing/editorial` | GET | redesign | ✅ |
| `/api/options/simulate` | GET | redesign | ✅ (normalisations tracées, 422 honnête) |

## 4. Routes « API seules » (orphelines post-refonte) — décision

30 routes restent des endpoints HTTP valides sans consommateur dans la
nouvelle UI : `/api/rescan`, `/api/company/<sym>`, `/api/correlations/<sym>`,
`/desc/<sym>`, `/options/<sym>`, `/quotes`, `/ibkr`, `/weekly-regen`,
`/api/cockpit`, `/api/watchlist`, `/api/options`, `/api/search`,
`/api/weekly`, `/api/strategie`, `/api/comite`, `/news-feed`,
`/weekly-feed`, `/api/desk/backups`, `/api/desk/restore`,
`/api/watchlist-tv`, `/api/vertex/<sym>`, `/api/risk`, `/api/portefeuille`,
`/api/options-lab`, `/api/live/report`, `/api/position-decision/<sym>`,
`/api/brief`, `/api/client-log` (GET).

**Décision : conservées** (tests, scripts, raccourcis iPhone, restauration
manuelle des backups) — règle « aucune suppression de route sans
redirection ». Deux cas produit signalés à l'utilisateur : brancher ou
retirer le fil de news (`/news-feed`) et le research center options
(`/api/options-lab`).

## 5. Alias et quasi-doublons

- `/api/alerts/status` (alertes **déclenchées**, terminal.py) vs
  `/api/alerts/active` (alertes **actives**, strategy_os) — sémantiques
  distinctes, tous deux consommés ; noms proches assumés.
- `/healthz` + `/api/healthz`, `/favicon.ico` + `/favicon.svg` : alias
  volontaires.
