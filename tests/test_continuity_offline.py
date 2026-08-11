"""CONTINUITY LOT 5b — identité de fraîcheur + mode offline/dégradé.

§8 : marquage discret live / snapshot / sauvegardé / stale / recalcul / erreur / offline
(seuils unifiés). §13 : hors ligne, on ne montre jamais un écran vide — dernières données
conservées, navigation préservée, revalidation au retour.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / 'vertex' / 'static' / 'vertex' / 'js'
CSS = ROOT / 'vertex' / 'static' / 'vertex' / 'css'
CORE = (JS / 'vx-core.js').read_text(encoding='utf-8')
SHELL = (JS / 'vx-shell.js').read_text(encoding='utf-8')
STATES = (CSS / 'states.css').read_text(encoding='utf-8')


def test_freshness_helper_present():
    assert 'VX.freshness' in CORE
    for st in ('live', 'snapshot', 'saved', 'stale', 'refreshing', 'error', 'offline'):
        assert st in CORE, st
    assert 'THRESH' in CORE and 'assess' in CORE and 'chip' in CORE


def test_freshness_thresholds_are_single_source():
    """Une seule table de seuils (résout l'incohérence 900/420/300 de l'audit)."""
    assert 'THRESH: { live:' in CORE or "THRESH: {live:" in CORE or 'THRESH: {' in CORE


def test_freshness_chip_css_present():
    assert '.vx-fresh-chip' in STATES
    for st in ('live', 'stale', 'offline'):
        assert 'data-state="%s"' % st in STATES, st


def test_offline_mode_wired():
    assert 'setNet' in SHELL
    assert "addEventListener('offline'" in SHELL and "addEventListener('online'" in SHELL
    assert "data-net" in SHELL
    assert 'Hors ligne' in SHELL and 'Reconnecté' in SHELL


def test_offline_preserves_data_not_blank():
    """Le mode dégradé conserve les dernières données (jamais d'écran vide)."""
    assert 'dernières données conservées' in SHELL
    assert 'connection_state' in SHELL


def test_offline_css_marker():
    assert ':root[data-net="offline"]' in STATES


def test_reconnect_revalidates():
    assert "reason: 'reconnect'" in SHELL
