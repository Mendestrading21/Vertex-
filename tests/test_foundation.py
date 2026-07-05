"""
tests/test_foundation.py — Fondations extraites (univers, constantes, config, statut).

Vérifie que la refonte institutionnelle n'a rien cassé : les modules extraits
sont cohérents et le moteur d'analyse produit des scores bornés, sans NaN.
"""

import os

os.environ.setdefault('DEMO', '1')


def test_universe_integrity():
    from vertex.data import universe as u
    assert len(u.UNIVERSE) > 500
    assert u.UNIVERSE == list(dict.fromkeys(u.UNIVERSE)), 'univers non dédupliqué'
    assert len(u.LIVE_SYMBOLS) <= len(u.UNIVERSE)
    assert all(isinstance(s, str) and s for s in u.WATCHLIST)
    # cartographies secteur/industrie cohérentes
    assert len(u._GICS_SECTOR) > 100
    assert len(u._INDUSTRY_MAP) > 100


def test_constants_bounds():
    from vertex.data import constants as c
    assert c.BENCH == 'SPY'
    assert 0 < c.R < 0.2
    assert c.REFRESH_SEC > 0
    assert c.BUILD


def test_config_resolves():
    from vertex.app import config
    assert isinstance(config.DEMO_MODE, bool)
    assert isinstance(config.IBKR_ENABLED, bool)
    assert isinstance(config.AUTH_ON, bool)
    assert config.SECRET_KEY  # jamais vide


def test_system_status_shape():
    from vertex.services.status_service import build_system_status, engine_status
    st = build_system_status(
        {'rows': [1, 2], 'detail': {}, 'updated': '10:00:00', 'scan_ts': None},
        build='TEST', readonly=True, ibkr_enabled=False, demo_mode=True,
        engines=[engine_status('scoring', ok=True)])
    assert st['readonly'] is True
    assert st['analysis_only'] is True
    assert st['order_execution'] == 'disabled-by-design'
    assert 'freshness' in st and 'engines' in st
    assert st['scan']['symbols'] == 2


def test_analyse_scores_bounded_no_nan():
    """Le moteur d'analyse : score dans [0,100], aucun NaN dans la sortie."""
    import math
    import terminal as t
    data = t._demo_universe(['AAPL', t.BENCH])
    bc = data[t.BENCH]['Close'].dropna()
    bench_ret = float(bc.iloc[-1]) / float(bc.iloc[-63]) - 1
    d = t.analyse(data['AAPL'].dropna(), bench_ret, fund={'sector': 'Technology'})
    assert d is not None
    assert 0 <= d['score'] <= 100, d['score']

    def _no_nan(o):
        if isinstance(o, float):
            assert not (math.isnan(o) or math.isinf(o)), 'NaN/Inf dans la sortie analyse'
        elif isinstance(o, dict):
            for v in o.values():
                _no_nan(v)
        elif isinstance(o, (list, tuple)):
            for v in o:
                _no_nan(v)
    _no_nan(d)
