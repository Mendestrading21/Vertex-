"""tests/test_event_engine_lot116.py — SKYLER LOT 116 : catalyseurs non-earnings figés.

Trou réel de couverture : vertex/catalysts/event_engine.py (§21/§23 —
classement des catalyseurs event-driven) n'avait AUCUN test. Sa règle
de sûreté — un événement NON CONFIRMÉ ne justifie jamais un mode
earnings ni un hold-through — n'était figée nulle part.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
from vertex.catalysts import event_engine as ev


def _e(etype='EARNINGS', days=10, confirmed=True, **kw):
    d = {'type': etype, 'days_until': days, 'confirmed': confirmed,
         'date': '2026-08-16'}
    d.update(kw)
    return d


def test_unconfirmed_never_reaches_the_horizon():
    cls = ev.classify_events([_e(days=5, confirmed=False)])
    assert len(cls['unconfirmed']) == 1 and cls['confirmed'] == []
    assert cls['within_30d'] == [] and cls['has_near_catalyst'] is False, (
        'non confirmé = jamais un catalyseur actionnable, même à 5 jours')


def test_unknown_type_reclassified_other_and_reported():
    cls = ev.classify_events([_e(etype='RUMEUR_TWITTER')])
    assert cls['confirmed'][0]['type'] == 'OTHER'
    assert cls['unknown_types'] == ['RUMEUR_TWITTER'], (
        'le type inconnu est reclassé ET dénoncé — jamais avalé en silence')
    absent = ev.classify_events([_e(etype=None)])
    assert absent['confirmed'][0]['type'] == 'OTHER'
    assert absent['unknown_types'] == []            # absent ≠ inconnu


def test_horizon_bounds_0_and_30_inclusive_sorted_by_proximity():
    cls = ev.classify_events([_e(days=30), _e(days=0), _e(days=31),
                              _e(days=-1), _e(days=None), _e(days=15)])
    assert [e['days_until'] for e in cls['within_30d']] == [0, 15, 30], (
        'bornes incluses, passé/31 j/date inconnue exclus, trié par proximité')
    assert cls['has_near_catalyst'] is True


def test_empty_or_none_events_are_honestly_empty():
    for empty in ([], None):
        cls = ev.classify_events(empty)
        assert cls == {'confirmed': [], 'unconfirmed': [], 'within_30d': [],
                       'unknown_types': [], 'has_near_catalyst': False}


def test_summary_earnings_window_45_days_inclusive():
    assert ev.catalyst_summary([], earnings_in_days=45)['has_catalyst'] is True
    assert ev.catalyst_summary([], earnings_in_days=46)['has_catalyst'] is False
    assert ev.catalyst_summary([], earnings_in_days=0)['has_catalyst'] is True
    assert ev.catalyst_summary([], earnings_in_days=-2)['has_catalyst'] is False, (
        'earnings passés : plus un catalyseur')
    assert ev.catalyst_summary([], earnings_in_days=None)['has_catalyst'] is False


def test_summary_caps_next_events_at_3():
    events = [_e(days=d) for d in (1, 2, 3, 4, 5)]
    s = ev.catalyst_summary(events)
    assert [e['days_until'] for e in s['next_events']] == [1, 2, 3]


def test_unconfirmed_events_produce_a_named_warning():
    s = ev.catalyst_summary([_e(confirmed=False), _e(confirmed=False),
                             _e(days=8)])
    assert len(s['warnings']) == 1
    assert '2 événement(s) non confirmé(s)' in s['warnings'][0]
    assert 'jamais utilisés pour tenir' in s['warnings'][0]


def test_all_confirmed_means_no_warning():
    s = ev.catalyst_summary([_e(days=8), _e(days=12)])
    assert s['warnings'] == [] and s['has_catalyst'] is True
