"""tests/test_real_calibration.py — SKYLER LOT 19 : calibration réelle.

Le dernier facteur figé de la confiance (calibration 0,50) se branche sur les
résultats MESURÉS de la mémoire décisionnelle — pour LA version de moteur
courante uniquement : scenario hit rate (part des décisions mesurées classées
DECISION_CORRECTE ou VARIANCE_NORMALE au plus long horizon mesuré) → facteur
borné [0,50, 0,90]. Échantillon < MIN_CALIBRATION_SAMPLE → 0,50 avec raison
« échantillon insuffisant » — jamais un facteur inventé sur 3 mesures.
ENGINE_VERSION 0.5.0 → 0.6.0 ; historique séparé par version, comme toujours.
"""
import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import skyler_core as SK


def _record(i, version='vX', ret=None, total=30, insufficient=None):
    """Décision figée + (optionnel) résultat mesuré à H20 avec rendement ret."""
    d = {'symbol': 'C%02d' % i, 'as_of': str(i), 'decision': 'ACHETER',
         'score': {'total': total, 'level': 'A',
                   'insufficient_blocks': insufficient or []},
         'level': 'A', 'contradictions': [], 'unknowns': [],
         'scenarios': {'available': True,
                       'bear': {'return_pct': -6.0}, 'base': {'return_pct': 12.0},
                       'bull': {'return_pct': 18.0}}}
    r = DM.freeze(decision=d, packet={'schema_version': 1, 'engine_version': version},
                  price=100.0, closes=None, portfolio_ctx=None, now=i)
    o = None
    if ret is not None:
        o = {'decision_id': r['decision_id'], 'engine_version': version,
             'symbol': r['symbol'], 'sessions_observed': 20,
             'horizons': {'H20': {'status': 'MESURE', 'sessions': 20,
                                  'return_pct': ret, 'basis': 't'}},
             'mfe_pct': None, 'mae_pct': None}
    return r, o


def _memory(n_correct, n_wrong, version='vX'):
    mem = DM.empty_memory()
    i = 0
    for _ in range(n_correct):
        r, o = _record(i, version=version, ret=5.0)
        mem = DM.append_outcome(DM.append_decision(mem, r), o)
        i += 1
    for _ in range(n_wrong):
        r, o = _record(i, version=version, ret=-15.0)     # sous le pessimiste
        mem = DM.append_outcome(DM.append_decision(mem, r), o)
        i += 1
    return mem


# ─── Facteur de calibration : honnête sous échantillon, borné au-dessus ─────────

def test_min_sample_constant_reasonable():
    assert DM.MIN_CALIBRATION_SAMPLE >= 20


def test_empty_memory_capped_with_reason():
    c = DM.calibration_factor(DM.empty_memory(), 'vX')
    assert c['value'] == 0.5
    assert c['hit_rate'] is None
    assert 'insuffisant' in c['basis']


def test_small_sample_never_invents_factor():
    mem = _memory(3, 0)                                   # 3 mesures parfaites
    c = DM.calibration_factor(mem, 'vX')
    assert c['value'] == 0.5                              # jamais gonflé sur 3 cas
    assert c['n_measured'] == 3
    assert 'insuffisant' in c['basis']


def test_sufficient_sample_hit_rate_documented():
    mem = _memory(15, 5)                                  # 20 mesures, 75 % de hits
    c = DM.calibration_factor(mem, 'vX')
    assert c['n_measured'] == 20
    assert c['hit_rate'] == pytest.approx(0.75)
    assert c['value'] == pytest.approx(0.5 + 0.4 * 0.75)  # 0.80
    assert 'hit rate' in c['basis'] and 'vX' in c['basis']


def test_factor_bounded_never_beyond_090():
    mem = _memory(25, 0)                                  # 100 % de hits
    c = DM.calibration_factor(mem, 'vX')
    assert c['value'] == pytest.approx(0.9)               # jamais 1,0
    mem2 = _memory(0, 25)                                 # 0 % de hits
    c2 = DM.calibration_factor(mem2, 'vX')
    assert c2['value'] == pytest.approx(0.5)              # plancher


def test_versions_never_mixed():
    mem = _memory(25, 0, version='old')                   # historique d'une autre version
    c = DM.calibration_factor(mem, 'vX')
    assert c['n_measured'] == 0                           # rien pour vX
    assert c['value'] == 0.5 and 'insuffisant' in c['basis']


def test_variance_normale_counts_as_hit():
    """Une perte DANS la fourchette pessimiste est une décision correcte du
    point de vue calibration des scénarios (le scénario l'avait contenue)."""
    mem = DM.empty_memory()
    for i in range(20):
        r, o = _record(i, ret=-4.0)                       # perte > pessimiste (−6)
        mem = DM.append_outcome(DM.append_decision(mem, r), o)
    c = DM.calibration_factor(mem, 'vX')
    assert c['hit_rate'] == pytest.approx(1.0)
    assert c['value'] == pytest.approx(0.9)


def test_calibration_factor_deterministic():
    mem = _memory(15, 5)
    assert DM.calibration_factor(mem, 'vX') == DM.calibration_factor(mem, 'vX')


# ─── Le moteur consomme le facteur réel ─────────────────────────────────────────

def test_engine_version_bumped_for_real_calibration():
    parts = tuple(int(x) for x in SK.ENGINE_VERSION.split('.'))
    assert parts >= (0, 6, 0)


def _detail():
    return {'score': 70, 'verdict': 'ATTENDRE',
            'plan': {'entry': 100, 'stop': 94, 'tp2': 112, 'rr_res': 3.0}}


def test_confidence_consumes_real_calibration():
    d = SK.decide('CLX', _detail(), as_of='t',
                  calibration={'value': 0.8, 'basis': 'hit rate 15/20 = 75 %'})
    cal = d['confidence']['factors']['calibration']
    assert cal['value'] == 0.8
    assert 'hit rate' in cal['basis']


def test_confidence_default_still_capped_without_history():
    d = SK.decide('CLX', _detail(), as_of='t')
    cal = d['confidence']['factors']['calibration']
    assert cal['value'] == 0.5
    assert 'historique' in cal['basis'] or 'insuffisant' in cal['basis']


def test_route_passes_memory_calibration(tmp_path, monkeypatch):
    """La route calcule le facteur depuis la mémoire persistée (fail-safe) —
    mémoire vide → facteur 0,50 avec raison « insuffisant » dans la décision."""
    import terminal
    from vertex.services import persist
    from vertex.app.state import scan_state
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    scan_state.setdefault('detail', {})['CLRX'] = {
        'price': 100.0, 'score': 70, 'verdict': 'ATTENDRE',
        'plan': {'entry': 100, 'stop': 94, 'tp2': 112, 'rr_res': 3.0}}
    try:
        d = terminal.app.test_client().get('/api/skyler/CLRX').get_json()
        cal = d['decision']['confidence']['factors']['calibration']
        assert cal['value'] == 0.5
        assert 'insuffisant' in cal['basis']
    finally:
        scan_state['detail'].pop('CLRX', None)
