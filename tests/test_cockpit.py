"""Tests — couche Cockpit premium (cockpit.css).

Vérifie la présence de la couche, son chargement dans le shell, le respect de
reduced-motion, et l'absence de bleu néon (identité Obsidian Copper §30).
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(ROOT, 'vertex', 'static', 'vertex', 'css', 'cockpit.css')


def test_cockpit_css_exists_with_tokens():
    assert os.path.isfile(CSS)
    src = open(CSS, encoding='utf-8').read()
    for needle in ('--vx-glow-pos', '--vx-glow-neg', '--vx-glow-copper-soft',
                   'vx-strip-item', 'vx-rail', 'vx-rail--stress', 'vx-stat-xl',
                   'prefers-reduced-motion:reduce'):
        assert needle in src, needle


def test_markets_volatility_cockpit_gauges():
    """Vue Volatilité = cockpit : jauge VIX + rail stress + jauges régime/participation,
    tous sourcés depuis /api/market/summary (réel), états vides honnêtes sinon."""
    src = open(os.path.join(ROOT, 'vertex', 'ui', 'pages', 'markets_page.py'), encoding='utf-8').read()
    for needle in ('vx-mk-vix-gauge', 'vx-rail--stress', 'vx-mk-vol-regime',
                   'vx-mk-vol-breadth', 'vx-mk-vol-rail', "/api/market/summary"):
        assert needle in src, needle
    assert 'VIX non fourni' in src  # état vide honnête


def test_cockpit_loaded_in_shell_last():
    shell = open(os.path.join(ROOT, 'vertex', 'ui', 'shell', '__init__.py'), encoding='utf-8').read()
    assert 'cockpit.css' in shell
    # chargé après control-surface pour rehausser sans être écrasé
    assert shell.index('control-surface.css') < shell.index('cockpit.css')


def test_cockpit_no_neon_blue():
    """Identité Obsidian Copper : la couche premium n'introduit pas de bleu/cyan néon."""
    src = open(CSS, encoding='utf-8').read().lower()
    for banned in ('#00e', '#0ff', 'cyan', 'aqua', 'dodgerblue', '#3b82f6', '#00bcd4'):
        assert banned not in src, banned


def test_cockpit_directional_value_semantics_in_briefing():
    """Le grand chiffre coloré n'est PAS appliqué au VIX ni au taux (anti-contresens)."""
    src = open(os.path.join(ROOT, 'vertex', 'ui', 'pages', 'briefing.py'), encoding='utf-8').read()
    assert "['vix','tnx'].includes(slug)" in src


def test_briefing_market_pulse_gauges_present():
    """Le bandeau Pouls du marché : 3 jauges radiales + rail de positionnement,
    sourcés depuis /api/market/summary (données réelles) — jamais inventés."""
    src = open(os.path.join(ROOT, 'vertex', 'ui', 'pages', 'briefing.py'), encoding='utf-8').read()
    for needle in ('vx-gauge-vix', 'vx-gauge-breadth', 'vx-gauge-trend',
                   'vx-regime-rail', 'async function loadPulse',
                   "/api/market/summary", 'VXCharts.gauge', "data-block=\"pulse\""):
        assert needle in src, needle
    # état vide honnête si la donnée manque (pas de zéro inventé)
    assert 'VIX non calculé' in src and 'Breadth non calculée' in src
