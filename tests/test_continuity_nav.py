"""CONTINUITY LOT 4 — gardiens de la navigation instantanée.

Préchargement (survol / focus / idle), navigation ticker fluide (SPA), transitions
respectant reduced-motion. Contrats statiques ; latence & consommation du préchargement
validées au navigateur (le rapport de continuite 04 (archive, retiree du depot)).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / 'vertex' / 'static' / 'vertex' / 'js'
ROUTER = (JS / 'vx-router.js').read_text(encoding='utf-8')
CORE = (JS / 'vx-core.js').read_text(encoding='utf-8')


def test_prefetch_machinery_present():
    for needle in ('function prefetch', 'takeFragment', 'PF_CONC', 'PF_TTL', 'PF_MAX'):
        assert needle in ROUTER, needle


def test_prefetch_triggers_hover_focus_idle():
    assert "addEventListener('mouseover'" in ROUTER
    assert "addEventListener('focusin'" in ROUTER
    assert 'idlePrefetch' in ROUTER
    assert 'requestIdleCallback' in ROUTER


def test_prefetch_bounded_concurrency_and_dedup():
    assert 'pfQueue' in ROUTER and 'pfActive' in ROUTER      # file d'attente + compteur
    assert 'pfInflight' in ROUTER                            # dédup


def test_navigate_consumes_prefetch():
    """navigate() sert le fragment préchargé si présent (clic instantané)."""
    assert 'takeFragment(href)' in ROUTER
    assert 'déjà préchargé' in ROUTER or 'prechargé' in ROUTER or 'Promise.resolve({ t: pf.text' in ROUTER


def test_ticker_navigation_uses_router():
    """VX.openAnalysis passe par le routeur SPA (repli dur si absent)."""
    assert 'VX.router && VX.router.go' in CORE
    assert "VX.router.go(href)" in CORE


def test_transition_respects_reduced_motion():
    assert 'prefers-reduced-motion' in ROUTER


def test_idle_prefetch_map_covers_key_spaces():
    for space in ('briefing', 'opportunities', 'portfolio', 'analysis', 'markets'):
        assert space + ':' in ROUTER, space
