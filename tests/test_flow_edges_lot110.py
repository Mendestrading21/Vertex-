"""tests/test_flow_edges_lot110.py — SKYLER LOT 110 : cas limites du flux figés.

Trou réel de couverture : vertex/options/flow.py a 6 tests nominaux
(classement, fraîcheur, skew, vide honnête, bool rejeté) mais les cas
limites — repli mid×100, clé volume alternative, NaN/inf, OI absent
jamais « frais », frontières EXACTES du skew 60/40, cap top, type
inconnu — n'étaient figés nulle part.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
from vertex.options import flow


def _c(t, k, vol, cost, oi=None):
    return {'type': t, 'strike': k, 'vol': vol, 'cost': cost, 'oi': oi}


def test_mid_fallback_and_cost_priority():
    d = flow.analyze([{'type': 'CALL', 'strike': 100, 'vol': 10, 'mid': 2.5}])
    assert d['contracts'][0]['premium'] == 2500          # 10 × (2.5 × 100)
    both = flow.analyze([{'type': 'CALL', 'strike': 100, 'vol': 10,
                          'cost': 400, 'mid': 2.5}])
    assert both['contracts'][0]['premium'] == 4000, (
        'cost (déjà ×100) prime sur mid quand les deux existent')


def test_volume_key_fallback_when_vol_absent():
    d = flow.analyze([{'type': 'PUT', 'strike': 90, 'volume': 20, 'cost': 100}])
    assert d['empty'] is False and d['contracts'][0]['vol'] == 20


def test_nan_and_infinity_are_rejected():
    d = flow.analyze([
        {'type': 'CALL', 'strike': 100, 'vol': float('nan'), 'cost': 200},
        {'type': 'CALL', 'strike': 100, 'vol': 10, 'cost': float('inf')}])
    assert d['empty'] is True, 'NaN/inf ne deviennent jamais un premium affiché'


def test_no_oi_means_never_fresh():
    for oi in (None, 0):
        d = flow.analyze([_c('CALL', 100, vol=500, cost=100, oi=oi)])
        row = d['contracts'][0]
        assert row['vol_oi'] is None and row['fresh'] is False, (
            'sans OI prouvé, jamais un badge « positionnement frais »')


def test_skew_boundaries_60_40_exact():
    calls60 = flow.analyze([_c('CALL', 100, 60, 100), _c('PUT', 90, 40, 100)])
    assert calls60['call_pct'] == 60 and calls60['skew'] == 'calls'
    puts40 = flow.analyze([_c('CALL', 100, 40, 100), _c('PUT', 90, 60, 100)])
    assert puts40['call_pct'] == 40 and puts40['skew'] == 'puts'
    even = flow.analyze([_c('CALL', 100, 50, 100), _c('PUT', 90, 50, 100)])
    assert even['skew'] == 'équilibré'


def test_top_caps_display_but_not_the_count():
    board = [_c('CALL', 100 + i, vol=10 + i, cost=100) for i in range(12)]
    d = flow.analyze(board, top=3)
    assert len(d['contracts']) == 3 and d['notable_count'] == 12, (
        'top borne l\'affichage, jamais le décompte honnête')
    floor = flow.analyze(board, top=0)
    assert len(floor['contracts']) == 1                  # plancher 1, jamais 0


def test_unknown_type_is_classified_call():
    d = flow.analyze([{'type': 'BIZARRE', 'strike': 100, 'vol': 10, 'cost': 100}])
    assert d['contracts'][0]['type'] == 'CALL', (
        'réalité figée : tout ce qui n\'est pas PUT est classé CALL')


def test_non_dicts_and_missing_strike_are_filtered():
    d = flow.analyze([None, 'texte', 42,
                      {'type': 'CALL', 'vol': 10, 'cost': 100}])   # sans strike
    assert d['empty'] is True and 'exploitables' in d['reason']
