"""tests/test_skyler_sweep_x1.py — SKYLER X1 : balayage de l'univers.

Le moteur canonique `decide` appliqué à TOUS les titres scannés → classement
par score /40 avec décision, niveau, gate plafonnante, catalyseur. Contexte
marché calculé UNE fois (partagé), déterministe, vide honnête, jamais de
journalisation (seules les consultations individuelles journalisent).
"""
import json

from vertex.engines import skyler_sweep as SW


def _detail(score, rr=3.0, verdict='ACHETER'):
    cl = [100.0]
    for i in range(30):
        cl.append(round(cl[-1] * (1 + (0.001 if i % 2 == 0 else -0.001)), 6))
    return {'price': 100.0, 'score': score, 'verdict': verdict, 'trend': 70,
            'rsi': 55, 'confidence': 60, 'series': {'close': cl},
            'plan': {'entry': 100.0, 'stop': 94.0, 'tp1': 106.0, 'tp2': 112.0,
                     'tp3': 118.0, 'rr_res': rr, 'resistance': 115.0}}


def _state():
    return {
        'scan_ts': 1000000.0, 'scan_ts_h': '10:00:00', 'updated': '10:00:00',
        'market': {'regime': 'TREND', 'vix': 15.0, 'risk': 'Risk-On',
                   'breadth': {'above200': 70}},
        'market_ctx': {'spy_regime': 'UP', 'vix': 15.0, 'vix_band': 'calme',
                       'roro': 'RISK-ON', 'breadth': 70},
        'rows': [{'symbol': 'AAA'}],
        'detail': {'AAA': _detail(85), 'BBB': _detail(45), 'CCC': _detail(70, rr=1.0)},
        'options_board': [],
    }


def test_sweep_ranks_by_score_desc():
    res = SW.sweep(_state())
    assert res['n'] == 3
    scores = [r['score_total'] for r in res['rows']]
    assert scores == sorted(scores, reverse=True)
    assert res['rows'][0]['symbol'] == 'AAA'          # meilleur score technique


def test_sweep_rows_carry_decision_fields():
    res = SW.sweep(_state())
    for r in res['rows']:
        assert r['decision'] in ('ACHETER', 'RENFORCER', 'ATTENDRE', 'REDUIRE', 'REFUSER')
        assert 0 <= r['score_total'] <= 40
        assert r['level']
        assert 'capped_by_gate' in r and 'invalidation' in r and 'catalyst' in r


def test_sweep_gate_visible_in_ranking():
    res = SW.sweep(_state())
    ccc = next(r for r in res['rows'] if r['symbol'] == 'CCC')
    assert ccc['capped_by_gate'] == 'RR_BELOW_2'       # R:R 1.0 → porte visible
    assert ccc['decision'] in ('ATTENDRE', 'REFUSER')


def test_sweep_shares_market_context_once():
    res = SW.sweep(_state())
    assert res['market_regime'] and res['market_regime'] != ''
    assert res['as_of'] == '10:00:00'
    assert res['generator'] == 'deterministic'


def test_sweep_empty_state_honest():
    res = SW.sweep({})
    assert res['n'] == 0 and res['rows'] == []
    assert 'reason' in res


def test_sweep_deterministic():
    a, b = SW.sweep(_state()), SW.sweep(_state())
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_sweep_limit():
    res = SW.sweep(_state(), limit=2)
    assert len(res['rows']) == 2 and res['n'] == 3     # total honnête, coupe dite


def test_sweep_route_and_no_journaling(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    from vertex.app.state import scan_state
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    saved = {k: scan_state.get(k) for k in ('detail', 'market', 'market_ctx')}
    scan_state.update(_state())
    try:
        d = terminal.app.test_client().get('/api/skyler/sweep').get_json()
        assert d['n'] == 3 and d['rows'][0]['symbol'] == 'AAA'
        # le balayage ne journalise JAMAIS (pas 20 entrées par affichage)
        assert persist.load_json('skyler_decisions.json', []) == []
    finally:
        for k, v in saved.items():
            if v is None:
                scan_state.pop(k, None)
            else:
                scan_state[k] = v


def test_opportunities_radar_has_skyler_ranking_card():
    """Gardien X1 : le Radar des Opportunités expose le classement Skyler."""
    import terminal
    body = terminal.app.test_client().get('/opportunities').get_data(as_text=True)
    assert 'vx-skyler-rank' in body
    assert 'loadSkylerRank' in body
