"""tests/test_contract_filter_lot95.py — SKYLER LOT 95 : filtres durs figés.

`vertex/options/contract_filter.py` (les filtres DURS : un contrat écarté
ici n'est JAMAIS scoré ni proposé) n'était couvert qu'indirectement via
call_selector. Caractérisations DIRECTES nées vertes (dites) — moteur
INTACT. (Constat honnête : call_selector, que je croyais non couvert,
l'est par test_options_engine — import combiné, dit.)
"""
from vertex.options import contract_filter as cf
from vertex.options.models import CALL_CATEGORIES
from vertex.strategy import constitution as C

PROFILE = C.load_profile()


def _call(strike, dte, delta, mid, oi=4000, vol=600, spread=0.6):
    bid = round(mid - spread / 2, 2)
    ask = round(mid + spread / 2, 2)
    return {'symbol': 'NVDA', 'underlying': 'NVDA', 'expiry': '2026-10-16',
            'dte': dte, 'strike': float(strike), 'right': 'C', 'bid': bid,
            'ask': ask, 'mid': mid, 'delta': delta, 'iv': 0.40,
            'open_interest': oi, 'volume': vol}


def test_dte_bounds_are_inclusive_and_none_rejected():
    d = PROFILE.dte
    assert cf.dte_within_constitution(d.absolute_minimum, PROFILE) is True
    assert cf.dte_within_constitution(d.absolute_maximum, PROFILE) is True
    assert cf.dte_within_constitution(d.absolute_minimum - 1, PROFILE) is False
    assert cf.dte_within_constitution(d.absolute_maximum + 1, PROFILE) is False
    assert cf.dte_within_constitution(None, PROFILE) is False, (
        'DTE inconnu → jamais accepté par défaut')


def test_delta_band_exists_for_every_call_category():
    for cat in CALL_CATEGORIES:
        band = cf.delta_band(cat, PROFILE)
        assert band is not None and band[0] < band[1], cat
    assert cf.delta_band('CATEGORIE_INCONNUE', PROFILE) is None


def test_in_delta_band_requires_known_delta():
    cat = CALL_CATEGORIES[0]
    lo, hi = cf.delta_band(cat, PROFILE)
    mid = (lo + hi) / 2
    assert cf.in_delta_band({'delta': mid}, cat, PROFILE) is True
    assert cf.in_delta_band({'delta': hi + 0.2}, cat, PROFILE) is False
    assert cf.in_delta_band({'delta': None}, cat, PROFILE) is False, (
        'delta inconnu → jamais classé (absent ≠ conforme)')


def test_hard_filter_rejects_with_documented_reasons():
    d = PROFILE.dte
    good_dte = (d.absolute_minimum + d.absolute_maximum) // 2
    contracts = [
        _call(520, good_dte, 0.45, 24.0),                       # sain
        _call(520, d.absolute_maximum + 60, 0.45, 24.0),        # DTE hors bornes
        _call(520, good_dte, 0.45, 24.0, oi=1, vol=0, spread=9.0),  # illiquide
        dict(_call(520, good_dte, -0.45, 24.0), right='P'),     # PUT ignoré
    ]
    res = cf.hard_filter(contracts, PROFILE, spot=500.0, right='C')
    assert len(res['kept']) == 1
    reasons = [r for rej in res['rejected'] for r in rej['reasons']]
    assert any('hors bornes constitution' in r for r in reasons)
    assert any('liquidité intraitable' in r for r in reasons)
    # le PUT n'est ni gardé ni rejeté : hors périmètre du moteur CALL
    assert len(res['rejected']) == 2


def test_kept_contracts_carry_liquidity_and_anomaly_annotations():
    d = PROFILE.dte
    res = cf.hard_filter([_call(520, (d.absolute_minimum + d.absolute_maximum) // 2,
                                 0.45, 24.0)], PROFILE, spot=500.0)
    kept = res['kept'][0]
    assert '_liquidity' in kept and kept['_liquidity']['tradeable'] is True
    assert '_anomalies' in kept


def test_bucket_by_category_uses_delta_bands():
    d = PROFILE.dte
    good_dte = (d.absolute_minimum + d.absolute_maximum) // 2
    bands = {cat: cf.delta_band(cat, PROFILE) for cat in CALL_CATEGORIES}
    contracts = [ _call(500, good_dte, (b[0] + b[1]) / 2, 20.0)
                  for b in bands.values() ]
    buckets = cf.bucket_by_category(contracts, PROFILE)
    for cat, band in bands.items():
        assert any(band[0] <= abs(c['delta']) <= band[1]
                   for c in buckets[cat]), cat
