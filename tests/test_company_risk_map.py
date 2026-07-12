"""Tests §24 — carte des risques d'entreprise (données réelles, jamais fabriqué)."""
from vertex.company import risk_map as RM


def _comp(**fu):
    base = {'symbol': 'TST', 'moat': 'solide', 'fundamentals': {
        'pe': 25, 'debt_to_ebitda': 1.5, 'rev_growth': 15, 'margin': 20,
        'eps_growth': 18}}
    base['fundamentals'].update(fu)
    return base


_MED = {'median_pe': 20}


def test_risk_map_categories_present():
    r = RM.build(_comp(), sector_median=_MED)
    cats = {x['category'] for x in r['risks']}
    assert 'Valorisation' in cats and 'Financier / dette' in cats
    assert 'Croissance' in cats and 'Événementiel (earnings)' in cats


def test_high_valuation_flagged():
    r = RM.build(_comp(pe=40), sector_median={'median_pe': 20})  # ×2
    val = next(x for x in r['risks'] if x['category'] == 'Valorisation')
    assert val['level'] == RM.HIGH


def test_missing_data_is_unknown_not_fabricated():
    r = RM.build({'symbol': 'X', 'fundamentals': {}}, sector_median={})
    val = next(x for x in r['risks'] if x['category'] == 'Valorisation')
    assert val['level'] == RM.UNKNOWN and val['probability'] is None


def test_high_debt_flagged():
    r = RM.build(_comp(debt_to_ebitda=4.0), sector_median=_MED)
    fin = next(x for x in r['risks'] if x['category'] == 'Financier / dette')
    assert fin['level'] == RM.HIGH


def test_negative_growth_is_high_risk():
    r = RM.build(_comp(rev_growth=-3), sector_median=_MED)
    g = next(x for x in r['risks'] if x['category'] == 'Croissance')
    assert g['level'] == RM.HIGH


def test_imminent_earnings_high_event_risk():
    r = RM.build(_comp(), sector_median=_MED, earnings_in_days=3)
    ev = next(x for x in r['risks'] if 'Événementiel' in x['category'])
    assert ev['level'] == RM.HIGH


def test_highest_level_and_high_risks_list():
    r = RM.build(_comp(pe=50, debt_to_ebitda=5), sector_median={'median_pe': 20})
    assert r['highest_level'] == RM.HIGH
    assert 'Valorisation' in r['high_risks']


def test_known_count_excludes_unknown():
    r = RM.build({'symbol': 'X', 'fundamentals': {'pe': 25}},
                 sector_median={'median_pe': 20})
    assert r['known_count'] <= r['total_count']
    assert r['known_count'] >= 1
