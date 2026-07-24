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


def test_markets_volatility_single_reading():
    """PR n°3 : Vue Volatilité = UNE seule lecture principale (jauge VIX + rail
    stress + positionnement régime en texte). Les jauges régime/participation
    DUPLIQUÉES ont été retirées (une donnée = un domicile)."""
    src = open(os.path.join(ROOT, 'vertex', 'ui', 'pages', 'markets_page.py'), encoding='utf-8').read()
    for needle in ('vx-mk-vix-gauge', 'vx-rail--stress', 'vx-mk-vol-rail', "/api/market/summary"):
        assert needle in src, needle
    # jauges dupliquées retirées
    assert 'vx-mk-vol-regime' not in src and 'vx-mk-vol-breadth' not in src
    assert 'VIX non fourni' in src  # état vide honnête


def test_chart_core_new_types():
    """chart-core.js expose les nouveaux types : anneaux, entonnoir, barres-étincelles."""
    js = open(os.path.join(ROOT, 'vertex', 'static', 'vertex', 'js', 'charts', 'chart-core.js'),
              encoding='utf-8').read()
    for needle in ('C.rings = function', 'C.funnel = function', 'C.sparkbars = function'):
        assert needle in js, needle


def test_design_system_charts_catalog():
    """La page démo /system/design-system inclut un catalogue de graphiques."""
    src = open(os.path.join(ROOT, 'vertex', 'ui', 'pages', 'design_system_demo.py'), encoding='utf-8').read()
    for needle in ('Catalogue de graphiques', 'dsc-rings', 'dsc-funnel', 'C.rings', 'C.funnel'):
        assert needle in src, needle


def test_breadth_selection_funnel_real_data():
    """Vue Breadth : entonnoir de sélection alimenté par les données réelles du scan.
    PR n°3 : les anneaux (rings) redondants et la barre unique (breadthCard) ont
    été retirés ; on conserve la jauge + la tendance + l'entonnoir."""
    src = open(os.path.join(ROOT, 'vertex', 'ui', 'pages', 'markets_page.py'), encoding='utf-8').read()
    for needle in ('vx-mk-funnel', 'VXCharts.funnel', 'Univers scanné', 'vx-mk-breadth-trend'):
        assert needle in src, needle
    # doublons retirés : anneaux + barre unique
    assert 'vx-mk-participation-rings' not in src and 'VXCharts.rings' not in src
    assert 'vx-mk-breadth-chart' not in src


def test_markets_breadth_participation_gauge():
    """Vue Breadth : jauge de participation + détail (>MM50/MM200, adv/déc, NH/NL)
    sourcés depuis summary.breadth (objet), état vide honnête sinon."""
    src = open(os.path.join(ROOT, 'vertex', 'ui', 'pages', 'markets_page.py'), encoding='utf-8').read()
    for needle in ('vx-mk-breadth-gauge', 'vx-mk-breadth-detail',
                   'Titres > MM50', 'above200', 'async function loadBreadth'):
        assert needle in src, needle
    assert 'Participation non calculée' in src


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
    """Anti-contresens : la tuile VIX du Hero n'est JAMAIS colorée directionnellement
    (un VIX en hausse n'est pas « bon » en émeraude). PR n°3."""
    src = open(os.path.join(ROOT, 'vertex', 'ui', 'pages', 'briefing.py'), encoding='utf-8').read()
    # la tuile VIX est construite sans classe de couleur (3e argument vide)
    assert "kpiTile('VIX',vixHtml,''" in src


def test_briefing_is_summary_not_markets_copy():
    """PR n°3 : Aujourd'hui RÉSUME (Hero éditorial + 4 KPI cliquables + diff), il ne
    recopie plus Marchés. Les jauges Pouls, le graphe SPY et le breadthCard
    (domiciliés dans Marchés) ont été retirés — une donnée = un domicile."""
    src = open(os.path.join(ROOT, 'vertex', 'ui', 'pages', 'briefing.py'), encoding='utf-8').read()
    for needle in ('vx-hero', 'async function loadSummary', 'vx-diff',
                   'Aucun historique de comparaison disponible', 'kpiTile'):
        assert needle in src, needle
    # duplications de Marchés retirées
    for banned in ('loadPulse', 'vx-gauge-vix', 'vx-gauge-trend', 'vx-market-chart',
                   'VXCharts.breadthCard', 'loadRotation'):
        assert banned not in src, 'duplication Marchés résiduelle : ' + banned
