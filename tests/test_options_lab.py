"""
tests/test_options_lab.py — Options Research Center (moteur + API).

Le moteur construit les 12 chapitres depuis un état de scan synthétique :
bornes des scores, décision dans l'énumération, lecture au sens du trade
(PUT), dégradation propre quand le board est vide. Analyse only.
"""

import copy

from vertex.data import demo
from vertex.engines import options_lab


def _state():
    rows = [{'symbol': s, 'score': sc, 'price': px}
            for s, sc, px in (('AAPL', 85, 230), ('MSFT', 72, 420), ('NVDA', 66, 190),
                              ('KO', 38, 60), ('T', 25, 18))]
    detail = {r['symbol']: {'rs': 40 + i * 10, 'score': r['score'], 'sector': 'Tech',
                            'rsi': 55, 'adx': 25, 'mom': 3.0, 'vol_z': 1.5, 'pos52': 80,
                            'price': r['price'], 'verdict': 'BUY', 'trend': 'UP',
                            'confidence': 70, 'perf_m': 4.0, 'perf_q': 9.0}
              for i, r in enumerate(rows)}
    board = demo.demo_options_board(rows, detail)
    return {
        'options_board': board, 'detail': detail, 'rows': rows,
        'market_ctx': {'roro': 'RISK-ON', 'spy_regime': 'TREND', 'vix': 15,
                       'vix_band': 'calme', 'breadth': {'above50': 62}},
        'sectors': [{'sector': 'Tech', 'avg_rs': 60, 'avg_change': 1.2}],
        'strategy': {'picks': []}, 'scan_ts_h': '10:00',
    }


def test_build_has_all_twelve_chapters():
    d = options_lab.build(_state(), demo=True)
    for k in ('overview', 'research', 'analysis', 'plan', 'viz', 'strategies',
              'tops', 'comparator', 'committee', 'risks', 'timeline'):
        assert d.get(k), k
    assert d['demo'] is True and d['empty'] is False


def test_overview_counts_are_consistent():
    st = _state()
    d = options_lab.build(st, demo=True)
    o = d['overview']
    assert o['contracts'] == len(st['options_board'])
    assert o['calls'] + o['puts'] == o['contracts']
    assert o['pcr'] is not None and 0 < o['pcr'] < 3
    assert o['oi_total'] > 0 and o['iv_avg'] > 0
    assert o['ai']


def test_research_decision_is_in_enum_and_thesis_answers_why():
    d = options_lab.build(_state(), demo=True)
    r = d['research']
    assert r['decision']['verdict'] in ('ACHETER', 'ATTENDRE', 'ÉVITER')
    assert len(r['thesis']) >= 3
    assert any('Pourquoi cette option' in t for t in r['thesis'])
    assert r['score'] is not None and 0 <= r['score'] <= 100


def test_analysis_scores_are_bounded_and_scored_rows_have_reco():
    d = options_lab.build(_state(), demo=True)
    rows = d['analysis']
    assert len(rows) == 10
    for a in rows:
        assert a['score'] is None or 0 <= a['score'] <= 100
        assert a['text'] and a['reco'] and a['impact'] and a['importance']


def test_put_star_reads_scores_in_trade_direction():
    st = _state()
    # force un board 100 % PUT sur un titre FORT : la force doit jouer CONTRE la thèse
    st['options_board'] = [c for c in st['options_board'] if c['type'] == 'PUT'
                           and c['sym'] == 'AAPL']
    assert st['options_board'], 'la démo doit produire un PUT de couverture AAPL'
    d = options_lab.build(st, demo=True)
    comp = next(a for a in d['analysis'] if a['key'] == 'company')
    # AAPL score 85 → au sens PUT : 15/100, impact négatif
    assert comp['score'] is not None and comp['score'] <= 40
    assert comp['impact'] == 'négatif'


def test_risk_off_blocks_buy_decision():
    st = _state()
    st['market_ctx']['roro'] = 'RISK-OFF'
    d = options_lab.build(st, demo=True)
    assert d['research']['decision']['verdict'] == 'ÉVITER'


def test_viz_payload_is_drawable():
    v = options_lab.build(_state(), demo=True)['viz']
    assert len(v['payoff']['points']) > 30
    assert len(v['cone']) > 10 and all(r['p5'] <= r['p50'] <= r['p95'] for r in v['cone'])
    assert v['dist']['p_be'] is None or 0 <= v['dist']['p_be'] <= 100
    assert v['theta'][0]['v'] >= v['theta'][-1]['v']          # le temps ne crée pas de valeur
    assert set(v['radar']) == {'Delta', 'Gamma', 'Theta', 'Vega', 'IV'}
    assert v['kelly']['pct'] is not None and 0 <= v['kelly']['pct'] <= 15
    assert v['heat'] and all('sym' in h for h in v['heat'])


def test_strategies_sixteen_scored_in_context():
    st = options_lab.build(_state(), demo=True)['strategies']
    assert len(st['items']) == 16
    for s in st['items']:
        assert 0 <= s['score'] <= 100 and s['when'] and s['avoid'] and s['context']
    # risk-on + tendance : le directionnel haussier doit battre les stratégies de range
    sc = {s['name']: s['score'] for s in st['items']}
    assert sc['Bull Call Spread'] > sc['Iron Condor']


def test_tops_lists_have_rows_and_notes():
    tops = options_lab.build(_state(), demo=True)['tops']
    assert len(tops) >= 8
    for t in tops:
        assert t['rows'] and all(r['note'] for r in t['rows'])


def test_comparator_has_eight_vehicles_and_verdict():
    c = options_lab.build(_state(), demo=True)['comparator']
    assert len(c['rows']) == 8 and c['verdict']
    action = c['rows'][0]
    assert action['name'].startswith('Action')


def test_committee_and_risks_and_timeline():
    d = options_lab.build(_state(), demo=True)
    assert len(d['committee']) >= 15
    assert len(d['risks']) == 10
    for r in d['risks']:
        assert r['level'] in ('FAIBLE', 'MOYEN', 'ÉLEVÉ') and r['fix']
    assert len(d['timeline']) >= 5


def test_empty_board_degrades_cleanly():
    d = options_lab.build({'options_board': [], 'detail': {}}, demo=True)
    assert d['empty'] is True and d['research'] is None


def test_terminal_serves_the_new_page_and_api():
    import terminal
    rules = {r.rule for r in terminal.app.url_map.iter_rules()}
    assert '/api/options-lab' in rules
    assert 'olabRoot' in terminal.PAGE_OPTIONS_LAB          # nouvelle page montée
