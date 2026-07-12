"""Tests §10 — Brief éditorial narratif (jamais de fait inventé)."""
from vertex.market import editorial as E


def _state(**kw):
    base = {
        'market_ctx': {'spy_regime': 'TREND', 'roro': 'RISK-ON', 'vix': 15.2,
                       'vix_band': 'bas', 'breadth': 62},
        'indices': [{'name': 'S&P 500', 'change': 0.74},
                    {'name': 'Nasdaq', 'change': 1.12}],
        'sectors': [{'sector': 'Technologie', 'avg_score': 78},
                    {'sector': 'Énergie', 'avg_score': 41}],
        'committee': {'counts': {'ACHETER': 2, 'ATTENDRE': 5},
                      'decisions': [{'symbol': 'NVDA', 'verdict': 'ACHETER'}]},
    }
    base.update(kw)
    return base


def test_narrative_is_flowing_text_with_word_count():
    d = E.build_narrative(_state())
    assert isinstance(d['narrative'], str) and d['word_count'] > 40
    # mentionne indices, techno, discipline
    assert 'Nasdaq' in d['narrative']
    assert 'Discipline' in d['narrative']


def test_prices_mainly_reflects_context():
    d = E.build_narrative(_state())
    assert 'RISK-ON' in d['prices_mainly'] or 'croissance' in d['prices_mainly'].lower()


def test_no_news_is_signaled_not_invented():
    d = E.build_narrative(_state(), news_state={'items': []})
    assert d['news_available'] is False
    assert 'aucun récit' in d['narrative'].lower() or 'aucune actualité' in d['narrative'].lower()


def test_real_news_is_used_when_present():
    d = E.build_narrative(_state(), news_state={'items': [{'title': 'La Fed maintient ses taux'}]})
    assert d['news_available'] is True
    assert 'Fed' in d['narrative']


def test_unknown_regime_flags_main_risk_and_blocks():
    st = _state(market_ctx={'spy_regime': 'UNKNOWN'})
    d = E.build_narrative(st)
    assert d['main_risk'] and 'indéterminé' in d['main_risk'].lower()
    assert 'indéterminé' in d['prices_mainly'].lower()


def test_low_vix_favours_calls():
    d = E.build_narrative(_state(market_ctx={'vix': 14, 'spy_regime': 'TREND'}))
    assert d['calls_impact'] and 'call' in d['calls_impact'].lower()


def test_empty_state_does_not_crash_and_stays_honest():
    d = E.build_narrative({})
    assert isinstance(d['narrative'], str)
    assert d['news_available'] is False
    # jamais de chiffre inventé : pas d'indices → pas de phrase d'indices
    assert 'S&P 500' not in d['narrative']


def test_dominant_and_weak_sectors_extracted():
    d = E.build_narrative(_state())
    assert 'Technologie' in d['dominant_sectors']
    assert 'Énergie' in d['weak_sectors']
