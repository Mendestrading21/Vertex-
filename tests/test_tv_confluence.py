"""Tests — confluence signal TradingView × verdict Vertex (§30/§32)."""
from vertex.research import tv_confluence as C


def test_bullish_signal_confirms_buy_verdict():
    r = C.confluence('BREAKOUT_CONFIRMED', 'ACHETER')
    assert r['state'] == C.CONFIRM


def test_bearish_signal_contradicts_buy_verdict():
    r = C.confluence('THESIS_INVALIDATION', 'ACHETER')
    assert r['state'] == C.CONTRADICT


def test_bearish_signal_confirms_avoid_verdict():
    assert C.confluence('FAILED_BREAKOUT', 'AVOID')['state'] == C.CONFIRM


def test_neutral_signal_is_neutral():
    assert C.confluence('VOLATILITY_COMPRESSION', 'ACHETER')['state'] == C.NEUTRAL


def test_empty_verdict_is_neutral():
    assert C.confluence('BREAKOUT_CONFIRMED', '')['state'] == C.NEUTRAL


def test_signal_direction_mapping():
    assert C.signal_direction('MOMENTUM_ACCELERATION') == 'BULLISH'
    assert C.signal_direction('FAILED_BREAKOUT') == 'BEARISH'
    assert C.signal_direction('CORRECTION_DEEP') == 'NEUTRAL'


def test_verdict_stance_handles_french_and_english():
    assert C.verdict_stance('STRONG_BUY') == 'BULLISH'
    assert C.verdict_stance('Alléger') == 'BEARISH'
    assert C.verdict_stance('ATTENDRE') == 'NEUTRAL'


def test_summarize_overall_states():
    buy = 'ACHETER'
    s_conf = [{'signal': 'BREAKOUT_CONFIRMED'}, {'signal': 'TREND_ALIGNMENT'}]
    assert C.summarize(s_conf, buy)['overall'] == C.CONFIRM
    s_mix = [{'signal': 'BREAKOUT_CONFIRMED'}, {'signal': 'THESIS_INVALIDATION'}]
    assert C.summarize(s_mix, buy)['overall'] == 'MIXTE'
    s_contra = [{'signal': 'THESIS_INVALIDATION'}]
    assert C.summarize(s_contra, buy)['overall'] == C.CONTRADICT
    assert C.summarize([], buy)['overall'] == C.NEUTRAL


def test_confluence_never_emits_order_language():
    import inspect
    src = inspect.getsource(C)
    for forbidden in ('place_order', 'BUY_NOW', 'execute', 'transmit'):
        assert forbidden not in src
