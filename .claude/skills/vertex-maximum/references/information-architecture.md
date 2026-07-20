# Architecture d'information — routes réelles → pages cibles

Vertex = monolithe **strangler** : les pages HTML sont servies par le blueprint `redesign`
(`vertex/app/routes/redesign.py`) via un shell unique (`vertex/ui/shell/__init__.py`, `PRIMARY_NAV` = 8 espaces)
et les modules `vertex/ui/pages/*.py`. `terminal.py` (~11k lignes) ne sert plus (presque) que du JSON/API + PWA.
Inventaire complet : `docs/vertex-audit/01-repository-map.md` + `02-current-information-architecture.md`.

## Les 8 espaces (nav = source de vérité `shell/__init__.py:14`)
| # | Espace | Route | Sous-vues (onglets `?view=`) | Renderer |
|---|---|---|---|---|
| 1 | **Dashboard** | `/` | blocs ancrés (essentiel, opportunités, portefeuille, alertes, brief, régime, calendrier, news, **marchés/breadth/VIX fusionnés**, pulse, top/flop, secteurs) | `ui/pages/briefing.py` |
| 2 | **Opportunités** | `/opportunities?view=` | screener · options · portfolio · anomalies · calendar | `opportunities_page.py` |
| 3 | **Portefeuille** | `/portfolio?view=` | team(Équipe) · positions · options · risk · watchlist | `portfolio_page.py` (+ `/tracking`) |
| 4 | **Analyse** | `/analysis` + `/analysis/<sym>` | index (lanceur) + fiche canonique par titre | `analysis_page.py` |
| 5 | **Options** | `/options?view=` + `/options/<sym>` | overview · volatility · radar · scenarios · events + dossier titre | `options_intel_page.py` · `options_symbol_page.py` |
| 6 | **Performance** | `/performance?view=` | overview · journal · track-record · learnings | `performance_page.py` |
| 7 | **Intelligence** | `/intelligence?view=` | analyst · committee · strategy · impacts · research · memory | `intelligence_page.py` |
| 8 | **Système** | `/system?view=` | connections · data · automations · settings · archive (+ design-system) | `system_page.py` |

## Correspondance mission → réalité (la cible existe déjà en grande partie)
- Mission « Dashboard cockpit » → `/` (briefing) : consolider (Markets fusionnés ici via `/markets`→ancre).
- Mission « Desk/Exécution » → **PAS de page dédiée aujourd'hui** ; reformulée **prep/sim** : à bâtir depuis
  `desk.py` + `planning_api.py` (`/api/planning/ticket`) + `risk_engine`, **sans transmission** (lecture seule).
- Mission « Journal » / « Events » / « Watchlist » / « Settings » → existent (Performance→journal, Dashboard→
  calendrier + `content.py`/`cal-feed`, Portefeuille→watchlist, Système→settings).

## Navigation (shell)
Sidebar `PRIMARY_NAV` + `aria-current` (gardien `test_redesign_ui.py::test_active_nav_item_marked`) · breadcrumbs
`Vertex / espace / sous-vue` + bouton retour (`vxNavigationContext`) · recherche globale `#vx-global-search` +
**command palette** `#vx-palette` (backend `/api/command`) · topbar : Ajouter, horloge de séance, Connexions,
Notifications, Refresh · **pas de sélecteur de compte** (mono-utilisateur). Vestige à nettoyer : double nav
(`ui/nav.py` 10 items, legacy) vs `PRIMARY_NAV` 8 items.

## Onglets
Les onglets sont de **pures URL** (`?view=`, `<a class="vx-tab">`), pas d'état JS — cohérent, cache-friendly,
partageable. À conserver.
