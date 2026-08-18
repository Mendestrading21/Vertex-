"""tests/test_events_timeline.py — SKYLER LOT 4 : série canonique, dédup news,
timeline d'événements normalisée (fait vs interprétation, impact par mots-clés
transparents, révisions honnêtement absentes). Aucun OHLCV artificiel.
"""
from vertex.data import series as SR
from vertex.engines import events as EV
from vertex.services import news_plus


# ─── Série de clôtures CANONIQUE ────────────────────────────────────────────────

def test_canonical_closes_from_scan_series():
    cl, src = SR.closes({'series': {'close': [101.0, 102.5]}})
    assert cl == [101.0, 102.5]
    assert src == 'scan.series.close'


def test_no_alternative_shapes_admitted():
    """Une seule source canonique — les formes legacy 'closes'/'history' ne
    nourrissent plus les chemins décisionnels (jamais de série ambiguë)."""
    cl, src = SR.closes({'closes': [1, 2, 3], 'history': [4, 5]})
    assert cl == [] and src is None


def test_closes_filters_invalid_points_without_inventing():
    cl, src = SR.closes({'series': {'close': [100.0, None, 'x', -5, 101.0]}})
    assert cl == [100.0, 101.0]
    assert src == 'scan.series.close'


def test_closes_empty_detail_honest():
    assert SR.closes(None) == ([], None)
    assert SR.closes({}) == ([], None)


# ─── Déduplication des news ─────────────────────────────────────────────────────

def test_dedupe_news_by_normalized_title_and_link():
    items = [
        {'title': 'Apple beats estimates', 'link': 'a', 'publisher': 'X'},
        {'title': 'Apple  beats   estimates', 'link': 'b', 'publisher': 'Y'},   # même titre normalisé
        {'title': 'Apple beats estimates', 'link': 'a', 'publisher': 'Z'},      # même lien
        {'title': 'Autre nouvelle', 'link': 'c', 'publisher': 'X'},
    ]
    out = news_plus.dedupe_news(items)
    assert len(out) == 2
    assert out[0]['title'] == 'Apple beats estimates'   # premier conservé, jamais réécrit
    assert out[1]['title'] == 'Autre nouvelle'


def test_dedupe_never_rewrites_and_handles_empty():
    out = news_plus.dedupe_news([{'title': 'A - B (test)', 'link': 'x'}])
    assert out == [{'title': 'A - B (test)', 'link': 'x'}]
    assert news_plus.dedupe_news([]) == []
    assert news_plus.dedupe_news(None) == []


# ─── Timeline d'événements normalisée ───────────────────────────────────────────

def _sample():
    return EV.build(
        'TST',
        news=[{'title': 'TST beats earnings estimates', 'link': 'l1', 'publisher': 'P', 'time': 'Mon'},
              {'title': 'Une manchette quelconque', 'link': 'l2', 'publisher': 'P', 'time': 'Mon'}],
        earnings=[{'sym': 'TST', 'date': '2026-08-07', 'dte': 3}],
        macro=[{'label': 'Emploi US (NFP)', 'date': '2026-08-07', 'dte': 3,
                'importance': 'haute', 'kind': 'NFP'}],
        anomaly={'events': [{'kind': 'spike', 'i': 30, 'ret_pct': 8.0, 'z': 2.5,
                             'label': 'Mouvement anormal +8.0 % (z=2.5)'}]},
        as_of='10:00:00')


def test_timeline_normalized_shape():
    ev = _sample()
    assert ev['symbol'] == 'TST' and ev['as_of'] == '10:00:00'
    assert ev['generator'] == 'deterministic'
    kinds = {e['kind'] for e in ev['events']}
    assert {'news', 'earnings', 'macro', 'anomaly'} <= kinds
    for e in ev['events']:
        assert e['category'] in ('fact', 'interpretation')
        assert e['label'] and e['source']
        assert 'dte' in e and 'impact_hint' in e
    coverage = ev['coverage']
    assert all(coverage['input_channels'].values())
    assert coverage['all_events_have_source'] is True
    assert coverage['dated_events'] == 4
    assert coverage['undated_events'] == ev['n'] - 4


def test_fact_vs_interpretation_separated():
    ev = _sample()
    earn = next(e for e in ev['events'] if e['kind'] == 'earnings')
    ano = next(e for e in ev['events'] if e['kind'] == 'anomaly')
    news = next(e for e in ev['events'] if e['kind'] == 'news')
    assert earn['category'] == 'fact' and earn['confidence'] == 'DECLARED'
    assert ano['category'] == 'interpretation' and ano['confidence'] == 'EXACT_STATISTICAL'
    assert news['category'] == 'fact'           # la publication est un fait ; l'impact, non


def test_impact_hint_only_from_transparent_keywords():
    ev = _sample()
    tagged = next(e for e in ev['events'] if e['kind'] == 'news' and 'beats' in e['label'])
    plain = next(e for e in ev['events'] if e['kind'] == 'news' and 'quelconque' in e['label'])
    assert tagged['impact_hint'] == 'EARNINGS' and tagged['impact_derivation'] == 'keywords'
    assert plain['impact_hint'] is None         # pas de mot-clé → pas d'impact inventé
    coverage = ev['coverage']['news_impact_coverage']
    assert coverage['keyword_classified_news'] == 1
    assert coverage['unclassified_news'] == 1
    assert coverage['status'] == 'KEYWORD_DERIVATION_ONLY'


def test_dated_events_sorted_by_dte_first():
    ev = _sample()
    dted = [e for e in ev['events'] if e['dte'] is not None]
    assert dted == sorted(dted, key=lambda e: e['dte'])
    assert ev['events'][0]['dte'] is not None   # le daté passe avant le non-daté


def test_revisions_honestly_absent():
    ev = EV.build('TST')
    assert ev['revisions']['available'] is False
    assert 'source' in ev['revisions']['reason']


def test_revisions_from_news_are_mentions_not_consensus():
    ev = EV.build('TST', news=[{'title': 'Broker upgrades TST and raises price target',
                                'publisher': 'P', 'time': 'Mon'}])
    revisions = ev['revisions']
    assert revisions['available'] is True
    assert revisions['status'] == 'NEWS_MENTIONS_ONLY'
    assert revisions['mentions'][0]['derivation'] == 'title_keywords'
    assert 'consensus' in revisions['note']


def test_empty_build_honest():
    ev = EV.build('TST')
    assert ev['events'] == [] and ev['n'] == 0
    assert ev['coverage']['input_channels'] == {
        'news_provided': False, 'earnings_provided': False,
        'macro_provided': False, 'anomaly_provided': False,
    }


def test_news_deduplicated_inside_timeline():
    ev = EV.build('TST', news=[{'title': 'Même titre', 'link': 'a'},
                               {'title': 'Même  titre', 'link': 'b'}])
    assert sum(1 for e in ev['events'] if e['kind'] == 'news') == 1
    freshness = ev['coverage']['news_timestamp_coverage']
    assert freshness['timestamped_news'] == 0
    assert freshness['untimestamped_news'] == 1
    assert freshness['status'] == 'TIMESTAMP_COVERAGE_ONLY'


# ─── Route de bout en bout ──────────────────────────────────────────────────────

def test_events_route_serves_timeline_and_sanitizes():
    import terminal
    from vertex.app.state import scan_state
    cl = [100.0 + i * 0.1 for i in range(30)]
    scan_state.setdefault('detail', {})['EVTX'] = {
        'series': {'close': cl},
        'news': [{'title': 'EVTX <script>alert(1)</script> upgrade', 'link': 'x',
                  'publisher': 'P', 'time': 'Mon'}],
    }
    try:
        d = terminal.app.test_client().get('/api/events/EVTX').get_json()
        assert d['symbol'] == 'EVTX'
        titles = ' '.join(e['label'] for e in d['events'])
        assert '<script>' not in titles          # sanitize_news au point de sortie
        assert any(e['kind'] == 'news' for e in d['events'])
    finally:
        scan_state['detail'].pop('EVTX', None)


def test_events_route_exposes_macro_calendar_unavailability(monkeypatch):
    import terminal
    from vertex.data import macro_calendar

    def _unavailable(*args, **kwargs):
        raise RuntimeError('interne')

    monkeypatch.setattr(macro_calendar, 'events', _unavailable)
    d = terminal.app.test_client().get('/api/events/EVTX').get_json()
    macro = d['coverage']['macro_calendar']
    assert macro == {
        'available': False,
        'status': 'MACRO_CALENDAR_UNAVAILABLE',
        'events_loaded': 0,
        'read_only': True,
        'reason': 'calendrier macro indisponible ; aucune absence d’événement n’est inférée',
    }
    assert d['coverage']['input_channels']['macro_provided'] is False
