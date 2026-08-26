# 02 — Architecture d'information actuelle (routes réelles → cible)

Source nav = `PRIMARY_NAV` (`vertex/ui/shell/__init__.py:14`, 8 items). Pages servies par le blueprint `redesign`
via `ui/pages/*`. Onglets = pures URL `?view=` (pas d'état JS) — cohérent, cache-friendly, partageable : **à conserver**.

## Les 8 espaces
| # | Espace | Route | Sous-vues `?view=` | Renderer |
|---|---|---|---|---|
| 1 | Dashboard | `/` | essentiel · opportunités · portefeuille · alertes · brief · régime · calendrier · news · marchés/breadth/VIX · pulse · top/flop · secteurs | `ui/pages/briefing.py` |
| 2 | Opportunités | `/opportunities` | screener · options · portfolio · anomalies · calendar | `opportunities_page.py` |
| 3 | Portefeuille | `/portfolio` (+ `/tracking`) | team · positions · options · risk · watchlist | `portfolio_page.py` |
| 4 | Analyse | `/analysis` + `/analysis/<sym>` | index + fiche canonique par titre | `analysis_page.py` |
| 5 | Options | `/options` + `/options/<sym>` | overview · volatility · radar · scenarios · events + dossier titre | `options_intel_page.py` · `options_symbol_page.py` |
| 6 | Performance | `/performance` | overview · journal · track-record · learnings | `performance_page.py` |
| 7 | Intelligence | `/intelligence` | analyst · committee · strategy · impacts · research · memory | `intelligence_page.py` |
| 8 | Système | `/system` | connections · data · automations · settings · archive (+ design-system) | `system_page.py` |

## Findings
- **RT-01 (P1) — ✅ RÉSOLU (Phase 2).** Collision `/options/<sym>` : JSON `opt_ep` (`terminal.py`) **et** page HTML
  `options_symbol_route` (`redesign.py:137`). Vérifié empiriquement : la page (blueprint) masquait le JSON → les 2
  consommateurs `fetch('/options/'+sym).json()` (`terminal.py:3880`, `4043`) recevaient du HTML (panneau « option
  recommandée » silencieusement cassé). **Fix** : JSON déplacé sous `/api/options/pack/<sym>` ; `/options/<sym>`
  réservé à la page ; les 2 consommateurs mis à jour. Vérif DEMO : `/api/options/pack/AAPL`→JSON,
  `/options/AAPL`→HTML, `/api/client-log`=0, 919 tests verts. Les liens `href="/options/<sym>"` (navigations) inchangés.
- **RT-02 (P2) — Routes legacy résiduelles** dans `terminal.py` (`/scan`, `/api/*`) mêlées aux blueprints :
  cartographier et migrer progressivement vers `app/routes/` (pas de big-bang).
- **IA-02 (P2) — Correspondance mission → réalité.** La cible mission existe déjà en grande partie. « Desk /
  Exécution » = **PAS de page dédiée** aujourd'hui → à bâtir en **prep/sim** depuis `app/routes/desk.py` +
  `planning_api.py` (`/api/planning/ticket`) + `risk`/`portfolio`, **sans transmission**. Journal/Events/Watchlist/
  Settings existent déjà (Performance→journal, Dashboard→calendrier, Portefeuille→watchlist, Système→settings).

## Cible
Conserver les 8 espaces + onglets-URL. Résoudre RT-01, absorber la nav legacy (voir `04`), matérialiser un
sous-espace **Préparation** (prep/sim) sans jamais introduire de chemin d'ordre. Détail cible : `13-target-architecture.md`.
