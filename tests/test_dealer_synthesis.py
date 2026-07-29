"""tests/test_dealer_synthesis.py — synthèse positionnement dealer : thèse honnête."""
from vertex.options import gex, flow, dealer_synthesis as ds


def _profile(bullish=True):
    if bullish:
        chain = [
            {'type': 'CALL', 'strike': 460, 'gamma': 0.05, 'oi': 5000, 'spot': 440},
            {'type': 'CALL', 'strike': 450, 'gamma': 0.03, 'oi': 3000, 'spot': 440},
            {'type': 'PUT', 'strike': 420, 'gamma': 0.02, 'oi': 1000, 'spot': 440},
        ]
    else:
        chain = [
            {'type': 'PUT', 'strike': 420, 'gamma': 0.06, 'oi': 6000, 'spot': 440},
            {'type': 'CALL', 'strike': 460, 'gamma': 0.01, 'oi': 500, 'spot': 440},
        ]
    return gex.compute(chain, symbol='MSFT')


def test_bullish_positioning_thesis():
    g = _profile(bullish=True)
    fl = flow.analyze([{'type': 'CALL', 'strike': 460, 'vol': 500, 'cost': 2000, 'oi': 100, 'dte': 21}],
                      symbol='MSFT')
    t = ds.build(g, fl, earnings_in_days=1, symbol='MSFT')
    assert t['empty'] is False
    assert t['bias'] == 'haussier'
    assert t['regime'] == 'stabilisant'
    assert t['magnet'] == 460                    # mur call = aimant haussier
    assert t['earnings_risk'] and 'imminent' in t['earnings_risk']
    assert t['horizon_dte'] == 21
    assert 'aimant' in t['narrative'].lower()
    # honnêteté : jamais présenté comme prévision de prix
    assert 'PAS une prévision' in t['narrative'] or 'pas une prévision' in t['narrative'].lower()
    assert 'aucune recommandation d\'ordre' in t['narrative']


def test_bearish_short_gamma_thesis():
    g = _profile(bullish=False)
    t = ds.build(g, flow.analyze([], symbol='MSFT'), symbol='MSFT')
    assert t['bias'] == 'baissier'
    assert t['regime'] == 'accelerateur'         # net négatif → amplification
    assert t['support'] == 420


def test_empty_profile_is_honest():
    t = ds.build(gex.compute([]), flow.analyze([]))
    assert t['empty'] is True
    assert t['narrative'] is None
    assert t['reason']


def test_earnings_none_when_absent():
    g = _profile(bullish=True)
    t = ds.build(g, flow.analyze([]), earnings_in_days=None, symbol='MSFT')
    assert t['earnings_risk'] is None
