"""tests/test_market_context.py — SKYLER LOT 3 : MarketContext canonique.

Exigences (SKYLER_ARCHITECTURE.md) : chaque dimension porte valeur/unité/source/
as_of/statut ; absent ≠ 0 (MISSING honnête) ; stale détecté ; conflit de sources
visible ; transition de régime ; « ce qui a changé depuis la dernière session » ;
déterministe et JSON-sérialisable. Aucune dimension inventée.
"""
import json

from vertex.engines import market_context as MC


def _state(vix=18.0, vix_mc=None, breadth=62.0, regime='TREND', risk='Risk-On',
           ts=1000000.0):
    return {
        'scan_ts': ts, 'scan_ts_h': '10:00:00', 'updated': '10:00:00',
        'market': {'regime': regime, 'breadth': breadth, 'vix': vix, 'risk': risk},
        'market_ctx': {'spy_regime': 'UP', 'vix': (vix_mc if vix_mc is not None else vix),
                       'vix_band': 'CALME' if vix < 20 else 'TENDU', 'breadth': breadth,
                       'roro': 1.2},
        'rows': [{'symbol': 'AAA'}],
    }


def test_live_dimensions_carry_full_provenance():
    ctx = MC.build(_state(), now=1000010.0)
    assert ctx['schema_version'] == 1
    assert ctx['generator'] == 'deterministic'
    v = ctx['dimensions']['vix']
    assert v['value'] == 18.0 and v['unit'] == 'index'
    assert v['source'] and v['as_of'] == '10:00:00' and v['status'] == 'LIVE'
    b = ctx['dimensions']['breadth_ma200_pct']
    assert b['value'] == 62.0 and b['unit'] == '%' and b['status'] == 'LIVE'
    assert ctx['freshness_floor'] == '10:00:00'   # jamais plus frais que la donnée


def test_missing_dimensions_are_missing_not_zero():
    ctx = MC.build(_state(), now=1000010.0)
    for name in ('rates_curve', 'dollar', 'credit_spreads', 'vol_term_structure',
                 'dispersion', 'liquidity', 'cross_asset'):
        d = ctx['dimensions'][name]
        assert d['status'] == 'MISSING' and d['value'] is None, name
        assert name in ctx['missing']


def test_stale_scan_marks_stale_not_live():
    ctx = MC.build(_state(ts=1000000.0), now=1000000.0 + 3000)   # > 2100 s
    assert ctx['dimensions']['vix']['status'] == 'STALE'
    assert ctx['dimensions']['breadth_ma200_pct']['status'] == 'STALE'


def test_demo_mode_labeled():
    ctx = MC.build(_state(), now=1000010.0, demo=True)
    assert ctx['dimensions']['vix']['status'] == 'DEMO'


def test_empty_state_is_honest():
    ctx = MC.build({}, now=0)
    assert ctx['dimensions']['vix']['status'] == 'MISSING'
    assert ctx['regime']['label'] == 'UNKNOWN'
    assert ctx['as_of'] is None


def test_conflicting_vix_sources_flagged():
    ctx = MC.build(_state(vix=18.0, vix_mc=24.5), now=1000010.0)
    assert ctx['dimensions']['vix']['status'] == 'CONFLICTED'
    assert any(c['dimension'] == 'vix' for c in ctx['conflicts'])
    c = next(c for c in ctx['conflicts'] if c['dimension'] == 'vix')
    assert {round(v, 1) for v in c['values']} == {18.0, 24.5}


def test_regime_classified_with_confidence():
    ctx = MC.build(_state(vix=15.0, breadth=75.0, regime='TREND'), now=1000010.0)
    assert ctx['regime']['label'] in ('TREND_UP', 'RISK_ON')
    assert 0.0 <= ctx['regime']['confidence'] <= 1.0
    assert ctx['regime']['dimensions_used']


def test_regime_transition_since_prev():
    prev = MC.build(_state(vix=40.0, breadth=25.0, regime='CHOP', risk='Risk-Off'),
                    now=1000010.0)
    cur = MC.build(_state(vix=15.0, breadth=75.0), now=1000020.0, prev=prev)
    tr = cur['regime']['transition']
    assert tr['changed'] is True
    assert tr['from'] == prev['regime']['label'] and tr['to'] == cur['regime']['label']
    # sans prev : transition inconnue, pas inventée
    solo = MC.build(_state(), now=1000010.0)
    assert solo['regime']['transition']['from'] is None
    assert solo['regime']['transition']['changed'] is None


def test_changes_since_prev_listed():
    prev = MC.build(_state(vix=28.0, breadth=40.0, risk='Risk-Off'), now=1000010.0)
    cur = MC.build(_state(vix=15.0, breadth=75.0, risk='Risk-On'), now=1000020.0, prev=prev)
    joined = ' '.join(cur['changes_since_prev'])
    assert 'VIX' in joined
    assert any('breadth' in c.lower() for c in cur['changes_since_prev'])
    # aucun changement → liste vide (pas de bruit inventé)
    same = MC.build(_state(), now=1000030.0, prev=MC.build(_state(), now=1000010.0))
    assert same['changes_since_prev'] == []


def test_context_is_json_serializable_and_deterministic():
    a = MC.build(_state(), now=1000010.0)
    b = MC.build(_state(), now=1000010.0)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_route_serves_context(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    from vertex.app.state import scan_state
    saved = {k: scan_state.get(k) for k in ('market', 'market_ctx')}
    scan_state.update(_state())
    try:
        d = terminal.app.test_client().get('/api/market/context').get_json()
        assert d['schema_version'] == 1
        assert 'vix' in d['dimensions'] and 'regime' in d
    finally:
        for k, v in saved.items():
            if v is None:
                scan_state.pop(k, None)
            else:
                scan_state[k] = v
