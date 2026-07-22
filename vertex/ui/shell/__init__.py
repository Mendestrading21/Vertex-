"""vertex.ui.shell — app shell unique du Vertex Master Redesign (§9-13).

Rend le squelette commun (sidebar 8 espaces, topbar, drawers, palette,
toasts, mobile action bar) autour du contenu d'une page. Migration strangler :
les nouvelles pages utilisent ce shell, le monolithe historique reste intact
le temps de la bascule des routes.
"""
from __future__ import annotations

SHELL_VERSION = 'vx-shell-1'

# Navigation principale (§10). Marchés est FUSIONNÉ dans le Dashboard (/#markets) —
# plus d'entrée dédiée : le Dashboard porte indices, taux, secteurs, breadth, VIX.
PRIMARY_NAV = (
    {'id': 'briefing', 'label': 'Dashboard', 'href': '/', 'icon': 'home'},
    {'id': 'opportunities', 'label': 'Opportunités', 'href': '/opportunities', 'icon': 'radar'},
    {'id': 'portfolio', 'label': 'Portefeuille', 'href': '/portfolio', 'icon': 'briefcase'},
    {'id': 'analysis', 'label': 'Analyse', 'href': '/analysis', 'icon': 'chart'},
    {'id': 'options', 'label': 'Options', 'href': '/options', 'icon': 'bolt'},
    {'id': 'performance', 'label': 'Performance', 'href': '/performance', 'icon': 'trend'},
    {'id': 'intelligence', 'label': 'Intelligence', 'href': '/intelligence', 'icon': 'brain'},
    {'id': 'system', 'label': 'Système', 'href': '/system', 'icon': 'settings'},
)

# Icônes : SVG inline sobres (pas d'emojis comme langage principal).
_ICONS = {
    'home': '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3z"/>',
    'radar': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><path d="M12 12 18 6"/>',
    'briefcase': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
    'chart': '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16v-5m4 5V8m4 8v-3"/>',
    'trend': '<path d="M3 17 9 11l4 4 8-8"/><path d="M21 12V7h-5"/>',
    'brain': '<path d="M9 4a3 3 0 0 0-3 3v1a3 3 0 0 0-1 5.8V15a3 3 0 0 0 4 2.8"/><path d="M15 4a3 3 0 0 1 3 3v1a3 3 0 0 1 1 5.8V15a3 3 0 0 1-4 2.8"/><path d="M12 3v18"/>',
    'settings': '<circle cx="12" cy="12" r="3"/><path d="M19 12a7 7 0 0 0-.1-1.2l2-1.6-2-3.4-2.4 1a7 7 0 0 0-2-1.2L14 3h-4l-.4 2.6a7 7 0 0 0-2 1.2l-2.4-1-2 3.4 2 1.6A7 7 0 0 0 5 12c0 .4 0 .8.1 1.2l-2 1.6 2 3.4 2.4-1a7 7 0 0 0 2 1.2L10 21h4l.4-2.6a7 7 0 0 0 2-1.2l2.4 1 2-3.4-2-1.6c.1-.4.1-.8.1-1.2z"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    'bell': '<path d="M18 8a6 6 0 1 0-12 0c0 7-3 8-3 8h18s-3-1-3-8"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
    'plug': '<path d="M9 7V3m6 4V3M7 7h10v4a5 5 0 0 1-10 0V7z"/><path d="M12 16v5"/>',
    'refresh': '<path d="M21 12a9 9 0 1 1-2.6-6.4"/><path d="M21 3v6h-6"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'chevrons': '<path d="m11 17-5-5 5-5m7 10-5-5 5-5"/>',
    'back': '<path d="m15 18-6-6 6-6"/>',
    'star': '<path d="m12 3 2.7 5.6 6.1.8-4.5 4.2 1.1 6-5.4-3-5.4 3 1.1-6L3.2 9.4l6.1-.8L12 3z"/>',
    'bolt': '<path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z"/>',
}


def icon(name: str, size: int = 18) -> str:
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
            f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{_ICONS.get(name, "")}</svg>')


def _sidebar(active: str) -> str:
    items = []
    for it in PRIMARY_NAV:
        current = ' aria-current="page"' if it['id'] == active else ''
        items.append(
            f'<a class="vx-nav-item" href="{it["href"]}" data-nav-id="{it["id"]}"{current}>'
            f'{icon(it["icon"])}<span class="vx-nav-label">{it["label"]}</span></a>')
    nav = ''.join(items[:-1])
    system_item = items[-1]
    return f'''<aside class="vx-sidebar" aria-label="Navigation principale">
  <div class="vx-sidebar-logo"><span class="vx-logo-mark">V</span>
    <span class="vx-logo-name">Vertex</span></div>
  <nav class="vx-sidebar-nav">{nav}</nav>
  <div class="vx-sidebar-foot">
    <div class="vx-sidebar-status" id="vx-global-status">
      <span class="vx-dot" style="width:7px;height:7px;border-radius:99px;background:var(--vx-text-faint)"></span>
      <span class="vx-status-label">État…</span></div>
    {system_item}
    <button class="vx-nav-item vx-collapse-btn" id="vx-collapse-btn"
      aria-label="Réduire la navigation">{icon('chevrons')}<span class="vx-nav-label">Réduire</span></button>
  </div>
</aside>'''


def _topbar(space_label: str, sub_label: str = '') -> str:
    crumb = f'<span class="vx-crumb-root">Vertex</span><span aria-hidden="true">/</span><b>{space_label}</b>'
    if sub_label:
        crumb += f'<span aria-hidden="true">/</span><span>{sub_label}</span>'
    return f'''<header class="vx-topbar">
  <button class="vx-btn vx-btn-icon vx-btn-ghost vx-hide-mobile" id="vx-mobile-nav-btn"
    aria-label="Ouvrir la navigation" style="display:none">{icon('chevrons')}</button>
  <button class="vx-back-btn" id="vx-back-btn" data-visible="0">{icon('back')}<span>Retour</span></button>
  <nav class="vx-breadcrumb" aria-label="Fil d’Ariane">{crumb}</nav>
  <div class="vx-topbar-search">{icon('search', 16)}
    <input id="vx-global-search" type="search" placeholder="Rechercher une action, une option ou une page"
      autocomplete="off" aria-label="Recherche globale" />
    <span class="vx-kbd">⌘K</span></div>
  <div class="vx-topbar-right">
    <button class="vx-btn vx-btn-sm vx-btn-primary" id="vx-add-btn">{icon('plus', 14)}<span class="vx-hide-mobile">Ajouter</span></button>
    <div class="vx-session vx-hide-mobile" id="vx-session">—<br><span class="vx-muted">New York —:—</span></div>
    <button class="vx-btn vx-btn-icon vx-btn-ghost" id="vx-connections-btn"
      aria-label="Connexions" title="Connexions (IBKR, TradingView, Claude, sync)">{icon('plug')}</button>
    <button class="vx-btn vx-btn-icon vx-btn-ghost" id="vx-notifs-btn" style="position:relative"
      aria-label="Notifications">{icon('bell')}<span class="vx-notif-badge" id="vx-notif-badge" hidden>0</span></button>
    <button class="vx-btn vx-btn-icon vx-btn-ghost" id="vx-refresh-btn" data-state="ready"
      aria-label="Actualiser les données">{icon('refresh')}</button>
  </div>
</header>'''


def _mobile_bar(active: str) -> str:
    order = ('briefing', 'opportunities', 'portfolio', 'analysis', 'performance')
    links = []
    for it in PRIMARY_NAV:
        if it['id'] not in order:
            continue
        current = ' aria-current="page"' if it['id'] == active else ''
        links.append(f'<a href="{it["href"]}"{current}>{icon(it["icon"], 20)}'
                     f'<span>{it["label"]}</span></a>')
    return (f'<div class="vx-mobile-bar"><nav aria-label="Navigation mobile">{"".join(links)}'
            f'<button id="vx-mobile-more" aria-label="Plus">{icon("chevrons", 20)}<span>Plus</span></button>'
            f'</nav></div>')


_OVERLAYS = '''
<div class="vx-overlay" id="vx-overlay" data-open="0"></div>
<aside class="vx-drawer" id="vx-drawer" data-open="0" role="dialog" aria-modal="true" aria-label="Panneau contextuel">
  <div class="vx-drawer-header"><h2 id="vx-drawer-title">—</h2>
    <button class="vx-btn vx-btn-icon vx-btn-ghost vx-right" data-close-drawer aria-label="Fermer">✕</button></div>
  <div class="vx-drawer-body" id="vx-drawer-body"></div>
</aside>
<div class="vx-modal" id="vx-modal" data-open="0" role="dialog" aria-modal="true">
  <div class="vx-modal-box">
    <div class="vx-modal-header"><h2 id="vx-modal-title">—</h2>
      <button class="vx-btn vx-btn-icon vx-btn-ghost vx-right" data-close-modal aria-label="Fermer">✕</button></div>
    <div class="vx-modal-body" id="vx-modal-body"></div>
    <div class="vx-modal-footer" id="vx-modal-footer"></div>
  </div>
</div>
<div class="vx-palette" id="vx-palette" data-open="0" role="dialog" aria-modal="true" aria-label="Palette de commandes">
  <div class="vx-palette-box">
    <input id="vx-palette-input" placeholder="Ticker, page ou action… (↑↓ pour naviguer, Entrée pour ouvrir)"
      autocomplete="off" aria-label="Palette de commandes" />
    <div class="vx-palette-list" id="vx-palette-list" role="listbox"></div>
  </div>
</div>
<div class="vx-context-menu" id="vx-context-menu" data-open="0" role="menu"></div>
<div class="vx-toasts" role="status" aria-live="polite"></div>
'''


def render_shell(*, title: str, active: str, space_label: str, sub_label: str = '',
                 content: str, page_js: str = '', page_label: str = '',
                 mobile_actions: str = '') -> str:
    """Assemble la page complète autour du contenu fourni."""
    mobile_bar = mobile_actions or _mobile_bar(active)
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#080808">
<title>{title} · Vertex</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/static/icon-180.png">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="preload" as="font" type="font/woff2" crossorigin href="/static/vertex/fonts/GeneralSans-Regular.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin href="/static/vertex/fonts/GeneralSans-Medium.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin href="/static/vertex/fonts/JetBrainsMono-Regular.woff2">
<link rel="stylesheet" href="/static/vertex/css/fonts.css">
<link rel="stylesheet" href="/static/vertex/css/tokens.css">
<link rel="stylesheet" href="/static/vertex/css/base.css">
<link rel="stylesheet" href="/static/vertex/css/layout.css">
<link rel="stylesheet" href="/static/vertex/css/components.css">
<link rel="stylesheet" href="/static/vertex/css/buttons.css">
<link rel="stylesheet" href="/static/vertex/css/states.css">
<link rel="stylesheet" href="/static/vertex/css/animations.css">
<link rel="stylesheet" href="/static/vertex/css/forms.css">
<link rel="stylesheet" href="/static/vertex/css/tables.css">
<link rel="stylesheet" href="/static/vertex/css/charts.css">
<link rel="stylesheet" href="/static/vertex/css/utilities.css">
<link rel="stylesheet" href="/static/vertex/css/responsive.css">
<link rel="stylesheet" href="/static/vertex/css/polish.css">
<link rel="stylesheet" href="/static/vertex/css/control-surface.css">
<link rel="stylesheet" href="/static/vertex/css/cockpit.css">
<link rel="stylesheet" href="/static/vertex/css/premium.css">
<link rel="stylesheet" href="/static/vertex/css/glass.css">
<link rel="stylesheet" href="/static/vertex/css/tokens-v4-bridge.css">
<link rel="stylesheet" href="/static/vertex/css/shell.css">
<link rel="stylesheet" href="/static/vertex/css/components-v4.css">
</head>
<body data-shell="{SHELL_VERSION}">
<a class="vx-skip-link" href="#vx-content">Aller au contenu principal</a>
<div class="vx-app" id="vx-app" data-sidebar="expanded">
{_sidebar(active)}
<div class="vx-main">
{_topbar(space_label, sub_label)}
<main class="vx-content" id="vx-content" data-page-label="{page_label or space_label}">
{content}
</main>
</div>
</div>
{mobile_bar}
{_OVERLAYS}
<script src="/static/chart.umd.min.js" defer></script>
<script src="/static/vertex/js/vx-core.js"></script>
<script src="/static/vertex/js/vx-entities.js"></script>
<script src="/static/vertex/js/vx-shell.js"></script>
<script src="/static/vertex/js/ui/inspector-drawer.js" defer></script>
<script src="/static/vertex/js/live-updates.js" defer></script>
<script src="/static/vertex/js/charts/chart-theme-obsidian-copper.js" defer></script>
<script src="/static/vertex/js/charts/chart-core.js" defer></script>
<script src="/static/vertex/js/charts/radar-chart.js" defer></script>
{page_js}
</body></html>'''
