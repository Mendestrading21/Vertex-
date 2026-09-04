"""tests/test_skyler_calibration.py — SKYLER LOT 9 : calibration.

Infrastructure honnête : journal des décisions (borné, dédupliqué, prix
d'entrée enregistré), Brier prouvé à la main sur données synthétiques mais
`available: false` tant qu'aucune probabilité calibrée n'existe (les scénarios
n'en affichent aucune — cohérent), résultats ex post = rendements RÉELS depuis
le prix enregistré, jamais un chiffre inventé.
"""
import pytest

from vertex.engines import skyler_journal as SJ


def _dec(sym='TST', decision='ATTENDRE', total=18, level='REFUS_WATCH', as_of='10:00:00'):
    return {'symbol': sym, 'decision': decision, 'as_of': as_of,
            'score': {'total': total, 'level': level},
            'capped_by_gate': None, 'level': level}


# ─── Journal : enregistrement borné et dédupliqué ───────────────────────────────

def test_record_appends_with_price_and_dedupes():
    j = []
    j = SJ.record(j, _dec(), price=100.0, now=1000.0)
    assert len(j) == 1
    e = j[0]
    assert e['symbol'] == 'TST' and e['decision'] == 'ATTENDRE'
    assert e['price'] == 100.0 and e['recorded_at'] == 1000.0
    assert e['score_total'] == 18
    # même (symbole, as_of, décision) → pas de doublon (rechargements de page)
    j = SJ.record(j, _dec(), price=100.5, now=1010.0)
    assert len(j) == 1
    # nouveau scan (as_of différent) → nouvelle entrée
    j = SJ.record(j, _dec(as_of='10:30:00'), price=101.0, now=2800.0)
    assert len(j) == 2


def test_record_bounded():
    j = []
    for i in range(SJ.MAX_ENTRIES + 50):
        j = SJ.record(j, _dec(sym='S%d' % i, as_of=str(i)), price=100.0, now=float(i))
    assert len(j) == SJ.MAX_ENTRIES


def test_record_without_price_still_recorded_honest():
    j = SJ.record([], _dec(), price=None, now=1000.0)
    assert j[0]['price'] is None            # absent ≠ inventé


# ─── Brier : machinerie prouvée à la main, indisponibilité honnête ──────────────

def test_brier_hand_computed():
    """probs [1.0, 0.5, 0.0], résultats [1, 0, 0] →
    ((1-1)² + (0.5-0)² + (0-0)²)/3 = 0.25/3 ≈ 0.0833."""
    assert SJ.brier([1.0, 0.5, 0.0], [1, 0, 0]) == pytest.approx(0.25 / 3, abs=1e-9)
    assert SJ.brier([0.5], [1]) == pytest.approx(0.25)


def test_brier_refuses_bad_inputs():
    with pytest.raises(ValueError):
        SJ.brier([0.5, 0.2], [1])              # longueurs différentes
    with pytest.raises(ValueError):
        SJ.brier([1.5], [1])                   # probabilité hors [0,1]
    with pytest.raises(ValueError):
        SJ.brier([], [])                       # vide : rien à mesurer


# ─── Calibration : honnête tant que les données manquent ────────────────────────

def test_calibration_empty_journal_honest():
    c = SJ.calibration([], quotes={})
    assert c['n_decisions'] == 0
    assert c['brier']['available'] is False
    assert c['outcomes']['available'] is False


def test_calibration_counts_and_outcomes_from_real_prices():
    j = []
    j = SJ.record(j, _dec(sym='AAA', decision='ACHETER', as_of='1'), price=100.0, now=0.0)
    j = SJ.record(j, _dec(sym='BBB', decision='REFUSER', as_of='1'), price=50.0, now=0.0)
    j = SJ.record(j, _dec(sym='CCC', decision='ATTENDRE', as_of='1'), price=None, now=0.0)
    c = SJ.calibration(j, quotes={'AAA': 110.0, 'BBB': 45.0})
    assert c['n_decisions'] == 3
    assert c['by_decision']['ACHETER'] == 1 and c['by_decision']['REFUSER'] == 1
    oc = c['outcomes']
    assert oc['available'] is True
    assert oc['measured'] == 2                 # CCC sans prix → non mesuré, dit
    assert oc['unmeasured'] == 1
    by = {o['symbol']: o for o in oc['rows']}
    assert by['AAA']['return_pct'] == pytest.approx(10.0)
    assert by['BBB']['return_pct'] == pytest.approx(-10.0)
    # Brier toujours indisponible : aucune probabilité calibrée n'a été émise
    assert c['brier']['available'] is False
    assert 'probabilit' in c['brier']['reason']


def test_calibration_never_invents_outcome_without_quote():
    j = SJ.record([], _dec(sym='ZZZ', as_of='1'), price=100.0, now=0.0)
    c = SJ.calibration(j, quotes={})
    assert c['outcomes']['measured'] == 0 and c['outcomes']['unmeasured'] == 1


# ─── Routes : enregistrement au passage + endpoint calibration ──────────────────

def test_skyler_route_records_decision(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    from vertex.app.state import scan_state
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    scan_state.setdefault('detail', {})['CALX'] = {
        'price': 100.0, 'score': 70, 'verdict': 'ATTENDRE',
        'plan': {'entry': 100, 'stop': 94, 'tp1': 106, 'tp2': 112, 'tp3': 118, 'rr_res': 3.0}}
    try:
        c = terminal.app.test_client()
        assert c.get('/api/skyler/CALX').status_code == 200
        stored = persist.load_json('skyler_decisions.json', [])
        assert any(e['symbol'] == 'CALX' for e in stored)
        d = c.get('/api/skyler/calibration').get_json()
        assert d['n_decisions'] >= 1
        assert d['brier']['available'] is False   # honnête tant que non calibré
        assert d['generator'] == 'deterministic'
    finally:
        scan_state['detail'].pop('CALX', None)


def test_performance_page_has_calibration_card():
    """Gardien LOT 8e : la vue Performance expose la carte Calibration Skyler."""
    import terminal
    body = terminal.app.test_client().get('/journal', follow_redirects=True).get_data(as_text=True)
    assert 'vx-pf-calibration' in body
    assert 'loadCalibration' in body
    assert 'Calibration Skyler' in body
