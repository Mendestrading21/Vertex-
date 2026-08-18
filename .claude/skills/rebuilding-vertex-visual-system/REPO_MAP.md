# Vertex Repository Map for Visual Rebuild

## Sommaire
- Canonical routes
- Shell
- Pages
- CSS
- JavaScript
- Charts
- Palette
- Strategy boundary
- Service worker
- Tests
- Safe editing rules

## Canonical routes
Eight primary spaces must remain the product navigation contract:
- `/` — Aujourd’hui / briefing
- `/markets` — Marchés
- `/opportunities` — Opportunités
- `/analysis` and `/analysis/<ticker>` — Analyse
- `/portfolio` — Portefeuille
- `/options` — Options
- `/journal` — Journal
- `/system` — Système

Legacy routes may redirect. Do not create new competing canonical pages without an explicit architectural decision.

## Shell
Primary location: `vertex/ui/shell/`.

Responsibilities:
- PRIMARY_NAV;
- global shell markup;
- sidebar/topbar/mobile navigation;
- page wrapper;
- common assets.

Browser shell behavior lives mainly under `vertex/static/vertex/js/vx-shell.js` and `vx-core.js`.

## Page implementations
Primary directory: `vertex/ui/pages/`.

Important page files include patterns such as:
- `briefing.py`
- `markets_page.py`
- `opportunities_page.py`
- analysis-related page(s)
- `portfolio_page.py`
- options-related page(s)
- `performance_page.py` / journal-related views
- `system` related views

Before editing, search the actual route registration and builder; do not infer filenames from labels.

## CSS
Directory: `vertex/static/vertex/css/`.

Important layers:
- `tokens.css` — canonical design tokens.
- `base.css` — base/reset/accessibility.
- component/layout CSS files.
- `responsive.css` — breakpoint behavior.
- `states.css` — data/live/demo states.
- `tables.css` — table behavior.
- `neon-glass.css` — historical visual layer still referenced by guards/pages.
- `signal-os.css` — current migration layer for Vertex Signal OS.

Strategy: use Signal OS to establish the new language, then move durable shared rules into the most canonical layer when safe. Avoid accumulating endless override layers.

## JavaScript UI
Directory: `vertex/static/vertex/js/`.

Key files:
- `vx-core.js` — formatting, states, navigation context, shared helpers.
- `vx-shell.js` — shell interactions, command palette, drawers/modals.
- `vx-entities.js` — synchronized entity actions/state.
- `signal-os.js` — visual/micro-copy migration layer; keep network-free/read-only.
- `live-updates.js` — global asset/bootstrap behavior.

## Charts
Directory: `vertex/static/vertex/js/charts/`.

Canonical core:
- `chart-core.js`
- `chart-theme-obsidian-copper.js`

Reusable modules include price, candlestick, area, bars, donut, heatmap, equity, drawdown, option payoff/scenarios/theta/IV, timeline and annotations.

Do not introduce a second chart engine for a single page unless there is a documented capability gap.

## Palette
Python source of truth: `vertex/visualization/palette.py`.
Browser mirrors must remain coherent with it. Tests intentionally detect drift between Python palette, JS theme and fallback series.

## Strategy / financial boundary
Financial meaning belongs under `vertex/strategy/`, `vertex/options/`, portfolio/engine modules and API/backend logic. UI may format and visualize outputs but must not silently duplicate scoring, probability, sizing or recommendation logic.

## READONLY boundary
Search for and keep forbidden order execution paths absent. Existing safety tests are product requirements, not inconvenience.

## Service worker
Route/source: `vertex/app/routes/system.py`.

The service worker caches static assets for offline fallback. Any change under `/static` requires version/cache contract updates and relevant tests. Read `tests/test_sw_cache_scope_lot361.py` before changing static assets.

## Tests to inspect during visual work
High-value families:
- `tests/test_redesign_ui.py`
- `tests/test_ui_v3.py`
- `tests/test_production_guards_canonical.py`
- `tests/test_visual_intelligence.py`
- `tests/test_signal_os_contract.py`
- `tests/test_sw_cache_scope_lot361.py`
- page-specific reconstruction/design-system tests

Search for the route/class/token being edited to find additional guards.

## Safe editing rules
1. Fetch/read the current file before replacement.
2. Preserve route/data contracts unless the task explicitly changes product behavior.
3. Change shared primitives centrally.
4. Keep CSS token-driven.
5. Keep chart palette synchronized across Python/JS/fallbacks.
6. Update cache contract for static changes.
7. Run targeted tests after each coherent change.
8. Run full suite before release-ready status.
9. Delete legacy code only after proving no route/import/test/runtime reference remains.
10. Never solve a visual problem by inventing backend data.
