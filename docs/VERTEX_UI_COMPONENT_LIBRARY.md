# Vertex — Bibliothèque de composants UI (V3)

Composants uniques, consommés par les 8 pages — aucune copie locale.
CSS : `vertex/static/vertex/css/` · JS : `vertex/static/vertex/js/`.

## Structure (shell)

| Composant | Implémentation |
|---|---|
| AppShell | `vertex/ui/shell/__init__.py` (`render_shell`) |
| Sidebar (240/72 px, actif orange, état système, Système en bas, Réduire) | shell + `layout.css` + `vx-shell.js` (`vxSidebarState`) |
| Topbar (retour contextuel, breadcrumb, recherche ⌘K, état marché + horloge NY à point de vie, connexions, notifications, refresh, bouton Ajouter brand) | shell + `vx-shell.js` |
| Breadcrumb / BackButton | `.vx-breadcrumb`, `#vx-back-btn` (VXContext) |
| PageHeader / SectionHeader | `.vx-page-header`, `.vx-section-header` |
| MobileActionBar | `.vx-mobile-bar` (5 espaces + Plus) |

## Cartes (3 niveaux — §9)

`.vx-card--hero` (halo ambré, contenu principal) · `.vx-card` (analytical,
hover élévation) · `.vx-card--compact` (KPI/statut). Variantes : `vx-elevated`,
`vx-accent`, `vx-active` (contour orange). Sous-éléments : header/title/
question/conclusion/footer. Spécialisations par usage : KpiCard (`.vx-kpi` +
sparkline), ChartCard (contrat `VXCharts.card`), InsightCard (`.vx-insight`
tones ai/risk), AlertCard/PositionCard/OpportunityCard/EventCard = cartes +
badges dédiés.

## Badges & indicateurs

`vx-badge` (base) · `vx-badge-decision[data-decision]` · `vx-badge-risk` ·
`vx-badge-status[data-status]` · `vx-badge-entity[data-kind]` ·
`vx-badge-demo` · UpdateIndicator (`VX.updateIndicator` → « À l'instant »,
« Il y a 8 min », source, mode live/delayed/fallback/error) ·
`vx-live-dot[data-live]` (5 états §29).

## Boutons (`buttons.css`)

Primary (dégradé brand) · Secondary · Ghost · Soft · Danger · Success ·
Icon · Split · Dropdown · Link — états hover/focus/active/disabled +
`data-state="loading|success|error"`. Jamais `alert()/confirm()/prompt()`
(gardien `test_no_blocking_dialogs`).

## Navigation interne & filtres

Tabs (`.vx-tab`, indicateur orange, `?view=` = état dans l'URL) ·
SegmentedControl (`.vx-segmented`) · FilterBar (`.vx-filterbar` + `.vx-chip`
aria-pressed + `.vx-filter-count`) · Selects/inputs (`forms.css`, focus
brand) · formulaire progressif (`.vx-steps`).

## Surfaces flottantes (`vx-shell.js`)

Drawer (focus trap, Échap, overlay) · Modal (footer d'actions) ·
CommandPalette (⌘K, groupes, navigation clavier complète) · ContextMenu
(menu ⋯ entité, 12 actions, clavier) · Toasts (4 tons) ·
NotificationCenter (drawer alertes + badge).

## Données

DataTable (`tables.css` : tri aria-sort, sticky header, hover actions,
`.vx-table-cards` = transformation cartes en mobile) · Timeline
(`timeline-chart.js`) · KV rows (`.vx-kv`).

## États (`states.css` — §28)

Skeletons dimensionnés (`vx-skeleton(-kpi/-line/-chart)`) · EmptyState
(icône+message+action, max 240 px) · StaleBanner · ErrorBanner ·
OfflineBanner · DemoBanner + badge · états live (§29).

## Actions universelles sur un titre (§31)

`vx-entities.js` : un seul module pour favoris/watchlist/suivis/positions/
alertes/notes — délégation globale `[data-open-analysis]` /
`[data-entity-menu]`, badges de statut partout, bus d'événements
(`vx:*-changed`) → toute modification se reflète sur toutes les pages.
Sync : 17 clés canoniques, last-writer-wins, flush sendBeacon.
