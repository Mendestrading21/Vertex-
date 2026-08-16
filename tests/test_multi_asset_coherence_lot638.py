from vertex.market import instrument_profile, sector_coherence


def test_instrument_profile_identifies_declared_sector_etf_without_composition_claim():
    profile = instrument_profile.build('SMH')
    assert profile['asset_class'] == 'ETF'
    assert profile['sector_proxy'] == 'Semiconducteurs'
    assert profile['classification_source'] == 'CURATED_SECTOR_PROXY'
    assert 'composition' in profile['note']


def test_instrument_profile_keeps_unclassified_symbol_honest():
    profile = instrument_profile.build('UNKN')
    assert profile['asset_class'] == 'UNKNOWN'
    assert profile['classification'] == 'UNCLASSIFIED'


def test_sector_coherence_compares_member_score_without_changing_decision():
    profile = instrument_profile.build('NVDA')
    out = sector_coherence.build(profile, {'score': 34}, [{
        'sector': 'Semiconducteurs', 'avg_score': 30, 'pct_buy': 55,
        'risk_band': 'High', 'n': 2, 'leader': {'symbol': 'NVDA'},
        'members': [{'symbol': 'NVDA'}, {'symbol': 'AMD'}],
    }])
    assert out['available'] is True
    assert out['instrument_score_minus_sector_avg'] == 4.0
    assert out['instrument_rank_in_sector'] == 1


def test_sector_coherence_refuses_missing_aggregate():
    out = sector_coherence.build(instrument_profile.build('NVDA'), {'score': 34}, [])
    assert out['available'] is False
