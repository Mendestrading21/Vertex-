"""tests/test_visual_hyper.py — garanties de la refonte HYPER VISUAL (§42).

Fige en non-régression les invariants visuels introduits sur la branche
feature/vertex-hyper-visual-intelligence : sémantique des couleurs (marque ≠
positif), token macro teal, échelle typo, système de graphiques (plein écran +
vue tableau), inspecteur global, portefeuille cockpit, vues enregistrées.

Tests statiques sur les sources CSS/JS/pages — aucun réseau, aucune donnée.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(ROOT, 'vertex', 'static', 'vertex', 'css')
JS = os.path.join(ROOT, 'vertex', 'static', 'vertex', 'js')
PAGES = os.path.join(ROOT, 'vertex', 'ui', 'pages')


def _read(*parts):
    return open(os.path.join(*parts), encoding='utf-8').read()


# ── Couleurs : marque ≠ positif, tokens sémantiques riches ────────────────
def test_brand_color_is_not_positive_color():
    """La marque (signal olive) ne doit JAMAIS être la couleur de gain positif."""
    tok = _read(CSS, 'tokens.css')
    assert '--vx-signal-500:#84aa31' in tok
    assert '--vx-positive:#36c889' in tok
    # brand pointe sur signal, pas sur positive
    assert '--vx-brand:var(--vx-signal-500)' in tok
    assert '--vx-brand:var(--vx-positive)' not in tok


def test_macro_teal_token_exists():
    """Le macro/cross-asset a un token teal DISTINCT de la marque (§4)."""
    tok = _read(CSS, 'tokens.css')
    assert '--vx-teal:#53b9ad' in tok
    assert '--vx-teal-soft' in tok
    # séries neutres riches
    for needle in ('--vx-stone', '--vx-plum', '--vx-steel:'):
        assert needle in tok, needle


def test_typography_scale_extended():
    """Échelle typo étendue présente (hero, KPI large, table) — §5."""
    tok = _read(CSS, 'tokens.css')
    for needle in ('--vx-fs-hero', '--vx-fs-kpi-lg', '--vx-fs-table', '--vx-fw-black'):
        assert needle in tok, needle


def test_no_excessive_small_text_in_tokens():
    """Aucune taille de police de token sous 10px (lisibilité §5, problème C)."""
    tok = _read(CSS, 'tokens.css')
    for m in re.finditer(r'--vx-fs-[\w-]+:(\d+(?:\.\d+)?)px', tok):
        assert float(m.group(1)) >= 10, 'taille de police trop petite: ' + m.group(0)


# ── Grille 12 colonnes explicite (§11) ────────────────────────────────────
def test_grid_span_and_preset_classes():
    lay = _read(CSS, 'layout.css')
    for needle in ('.vx-span-4', '.vx-span-8', '.vx-grid-4', '.vx-grid-3', '.vx-grid-auto'):
        assert needle in lay, needle


# ── Système de graphiques : plein écran + vue tableau (§8, §35) ────────────
def test_chart_card_has_fullscreen_and_table_view():
    core = _read(JS, 'charts', 'chart-core.js')
    assert 'C.toggleFullscreen' in core
    assert 'C.showDataTable' in core
    assert 'vx-chart-fs' in core and 'vx-chart-tbl' in core
    css = _read(CSS, 'charts.css')
    assert '.vx-chart-fs' in css and 'vx-chart-fs-backdrop' in css


def test_chart_macro_series_palette():
    """Palette macro dédiée (teal en tête) exposée dans VXCharts.colors."""
    core = _read(JS, 'charts', 'chart-core.js')
    assert 'macroSeries' in core
    assert "teal: '#53b9ad'" in core or 'teal:' in core


# ── Inspecteur latéral global (§29) ───────────────────────────────────────
def test_inspector_drawer_component_exists():
    path = os.path.join(JS, 'ui', 'inspector-drawer.js')
    assert os.path.isfile(path), 'inspector-drawer.js manquant'
    src = _read(JS, 'ui', 'inspector-drawer.js')
    assert 'VX.inspect' in src
    assert 'data-inspect' in src
    assert '/api/ticker/' in src


def test_inspector_loaded_in_shell():
    shell = _read(ROOT, 'vertex', 'ui', 'shell', '__init__.py')
    assert 'ui/inspector-drawer.js' in shell


def test_inspector_does_not_navigate_over_peek():
    """Le handler data-open-analysis ignore les clics [data-inspect] (pas de
    navigation par-dessus l'aperçu)."""
    ent = _read(JS, 'vx-entities.js')
    assert "closest('[data-inspect]')" in ent


def test_opportunities_wires_inspector():
    src = _read(PAGES, 'opportunities_page.py')
    assert 'data-inspect' in src


# ── Portefeuille cockpit (§23) ────────────────────────────────────────────
def test_portfolio_command_strip_and_cards():
    src = _read(PAGES, 'portfolio_page.py')
    assert 'pfCommandStrip' in src
    assert 'vx-cmd-strip' in src
    assert 'vx-poscard' in src        # positions en cartes, pas en lignes
    # KPI de risque réels (aucun chiffre inventé)
    assert 'diversification' in src


# ── Vues enregistrées (§31) ───────────────────────────────────────────────
def test_saved_views_in_screener():
    src = _read(PAGES, 'opportunities_page.py')
    for needle in ('vxScreenViews', 'op-save-view', 'op-views', 'op-del-view'):
        assert needle in src, needle


# ── Honnêteté : aucune donnée inventée introduite ─────────────────────────
def test_inspector_has_honest_empty():
    src = _read(JS, 'ui', 'inspector-drawer.js')
    # « — » honnête plutôt qu'un zéro inventé
    assert "'—'" in src or '"—"' in src
