"""Tests §6 — contrat canonique d'interprétation + verdicts options."""
from vertex.visualization import schemas as sc
from vertex.visualization.schemas import (
    interpretation, unknown, is_valid_interpretation,
    ST_FAVORABLE, ST_DEFAVORABLE, ST_INCONNU,
)
from vertex.options import interpretation as oi
from vertex.options import overview as ov


# ---------------------------------------------------------------- contrat
def test_interpretation_has_all_required_keys():
    d = interpretation('x.chart', 'Question ?', 'Lecture dominante.',
                       ST_FAVORABLE, confidence=0.8,
                       positive_evidence=['a'], negative_evidence=[],
                       uncertainties=[], strategy_impact='fait X',
                       source='IBKR', as_of='2026-07-12T00:00:00')
    assert is_valid_interpretation(d)
    for k in ('chart_id', 'question', 'dominant_reading', 'status',
              'positive_evidence', 'negative_evidence', 'uncertainties',
              'strategy_impact', 'source', 'as_of', 'limitations'):
        assert k in d


def test_confidence_clamped_and_lists_normalized():
    d = interpretation('c', 'q', 'r', ST_FAVORABLE, confidence=5.0,
                       positive_evidence='seul', negative_evidence=None)
    assert d['confidence'] == 1.0
    assert d['positive_evidence'] == ['seul']
    assert d['negative_evidence'] == []


def test_empty_reading_forces_unknown():
    d = interpretation('c', 'q', '', ST_FAVORABLE)
    assert d['status'] == ST_INCONNU


def test_invalid_status_becomes_unknown():
    d = interpretation('c', 'q', 'r', 'HAUSSIER_FORT')
    assert d['status'] == ST_INCONNU


def test_unknown_helper_is_valid_and_honest():
    d = unknown('c', 'q', reason='pas de données')
    assert is_valid_interpretation(d)
    assert d['status'] == ST_INCONNU
    assert d['dominant_reading'] == ''
    assert 'pas de données' in d['uncertainties']


def test_is_valid_rejects_garbage():
    assert not is_valid_interpretation(None)
    assert not is_valid_interpretation({'chart_id': 'x'})
    bad = interpretation('c', 'q', 'r', ST_FAVORABLE)
    bad['positive_evidence'] = 'not a list'
    assert not is_valid_interpretation(bad)


# ---------------------------------------------------------------- verdicts options
def test_volatility_high_is_unfavorable_for_buyer():
    d = oi.interpret_volatility('AAPL', current_iv=0.60, iv_low=0.20,
                                iv_high=0.65, closes=[100 + i for i in range(30)])
    assert is_valid_interpretation(d)
    assert d['status'] == ST_DEFAVORABLE


def test_volatility_low_is_favorable_for_buyer():
    d = oi.interpret_volatility('AAPL', current_iv=0.22, iv_low=0.20,
                                iv_high=0.65)
    assert d['status'] == ST_FAVORABLE


def test_volatility_unknown_without_corridor():
    d = oi.interpret_volatility('AAPL', current_iv=None, iv_low=None,
                                iv_high=None)
    assert d['status'] == ST_INCONNU


def test_event_risk_imminent_earnings_unfavorable():
    d = oi.interpret_event_risk('AAPL', earnings_in_days=2,
                                ex_dividend_days=None, right='CALL', dte=30)
    assert d['status'] == ST_DEFAVORABLE


def test_event_risk_unknown_dates():
    d = oi.interpret_event_risk('AAPL', earnings_in_days=None,
                                ex_dividend_days=None, right='CALL', dte=30)
    assert d['status'] == ST_INCONNU


# ---------------------------------------------------------------- overview
def _board():
    return [
        {'sym': 'AAPL', 'type': 'CALL', 'bucket': 'moyen', 'strike': 210,
         'dte': 45, 'iv': 32.0, 'quality': 70, 'pop': 55, 'spread_pct': 2.0,
         'oi': 12000, 'why': 'x'},
        {'sym': 'MSFT', 'type': 'CALL', 'bucket': 'court', 'strike': 420,
         'dte': 20, 'iv': 28.0, 'quality': 60, 'pop': 48, 'spread_pct': 1.5,
         'oi': 9000, 'why': 'y'},
        {'sym': 'XYZ', 'type': 'PUT', 'bucket': 'moyen', 'strike': 40,
         'dte': 60, 'iv': 55.0, 'quality': 35, 'pop': 40, 'spread_pct': 6.0,
         'oi': 800, 'why': 'z'},
    ]


def test_overview_counts_calls_puts_and_symbols():
    s = ov.summarize(_board(), as_of='2026-07-12T00:00:00')
    c = s['counters']
    assert c['calls'] == 2 and c['puts'] == 1
    assert c['symbols'] == 3
    assert c['total'] == 3
    assert is_valid_interpretation(s['interpretation'])


def test_overview_empty_board_is_unknown():
    s = ov.summarize([], as_of=None)
    assert s['empty'] is True
    assert s['interpretation']['status'] == ST_INCONNU


def test_overview_radar_sorted_by_quality():
    s = ov.summarize(_board())
    quals = [r['quality'] for r in s['radar']]
    assert quals == sorted(quals, reverse=True)
