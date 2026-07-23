"""tests/test_design_system_v1.py — PR Design n°1 (gardiens de la couche design).

Vérifie la typographie officielle (VERTEX OBSIDIAN / OBSIDIAN COPPER : Inter +
JetBrains Mono), le contrat du Chart Shell canonique, et l'existence des
composants canoniques premium. Gardiens au niveau source (comme le thème JS).
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as fh:
        return fh.read()


# ─────────────────────────────────────────────── Typographie officielle
def test_official_typography_tokens():
    css = _read('vertex/static/vertex/css/tokens.css')
    assert '--vx-font:Inter' in css, 'police UI officielle = Inter'
    assert '"JetBrains Mono"' in css, 'police mono officielle = JetBrains Mono'
    assert 'IBM Plex Mono' not in css, 'IBM Plex Mono ne doit plus être la mono officielle'


def test_shell_loads_official_fonts():
    shell = _read('vertex/ui/shell/__init__.py')
    assert 'JetBrains+Mono' in shell, 'le shell doit charger JetBrains Mono'
    assert 'IBM+Plex+Mono' not in shell, 'le shell ne doit plus charger IBM Plex Mono'
    assert 'family=Inter' in shell


# ─────────────────────────────────────────────── Chart Shell canonique
def test_chart_shell_contract_complete():
    """Le Chart Shell (C.card) porte tout le contrat : titre/question/conclusion/
    période/unité/source/fraîcheur/légende/aide/résumé accessible + états."""
    js = _read('vertex/static/vertex/js/charts/chart-core.js')
    for token in ('vx-chart-title', 'vx-chart-question', 'vx-chart-conclusion',
                  'timeframe', 'opts.unit', 'freshnessBadge', 'opts.summary',
                  'vx-sr-only', 'updateIndicator', 'Comprendre ce graphique'):
        assert token in js, 'contrat Chart Shell incomplet : %s manquant' % token


def test_chart_shell_has_all_states():
    js = _read('vertex/static/vertex/js/charts/chart-core.js')
    assert '_stateBody' in js and 'cardState' in js
    for state in ("'loading'", "'stale'", "'error'", "'empty'"):
        assert state in js, 'état %s absent du Chart Shell' % state


def test_freshness_badge_covers_all_states():
    js = _read('vertex/static/vertex/js/charts/chart-core.js')
    for f in ('live', 'delayed', 'stale', 'demo', 'offline', 'missing'):
        assert f in js, 'fraîcheur %s absente du badge canonique' % f


# ─────────────────────────────────────────────── Composants canoniques
def test_canonical_components_exist():
    css = _read('vertex/static/vertex/css/components.css')
    for cls in ('.vx-verdict-card', '.vx-scenario', '.vx-scenario-grid',
                '.vx-freshness', '.vx-insufficient', '.vx-badge-unit'):
        assert cls in css, 'composant canonique manquant : %s' % cls


def test_canonical_components_use_tokens_not_hardcoded_neutral():
    """Les composants canoniques n'introduisent pas la couleur neutre périmée."""
    css = _read('vertex/static/vertex/css/components.css')
    assert '#8f8a83' not in css, 'couleur neutre périmée réintroduite dans components.css'


def test_no_stale_neutral_fallback_in_pages():
    """Les fallbacks inline #8f8a83 (neutre périmé) ont été purgés des pages."""
    for rel in ('vertex/ui/pages/briefing.py', 'vertex/ui/pages/analysis_page.py',
                'vertex/ui/pages/portfolio_page.py', 'vertex/ui/pages/performance_page.py',
                'vertex/static/vertex/js/pages/tracking.js'):
        assert '#8f8a83' not in _read(rel), '%s contient encore #8f8a83 périmé' % rel


# ─────────────────────────────────────────────── DATA_INSUFFICIENT honnête
def test_intelligence_gates_data_insufficient():
    src = _read('vertex/ui/pages/intelligence_page.py')
    assert "final_decision==='DATA_INSUFFICIENT'" in src
    assert 'vx-insufficient' in src, 'état honnête DATA_INSUFFICIENT non rendu'
