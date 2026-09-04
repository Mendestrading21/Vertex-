"""tests/test_entonnoir.py — LOT 12 : pipeline opportunités.

Défauts mesurés sur le SHA courant (bancs nés ROUGES) :
- un candidat au régime INCONNU passe l'entonnoir (le hard gate canonique
  « régime inconnu → pas de nouveau risque » de decide.py n'y est pas) ;
- pas de point-in-time (`as_of`) ni de delta depuis le scan précédent ;
- un symbole dupliqué compte deux fois à chaque étage ;
- budgets de surfaçage implicites (coupe à 5 non déclarée).
"""
import pytest

from vertex.opportunities import funnel as F


@pytest.fixture(autouse=True)
def _memo_propre():
    F.reset_for_test()
    yield
    F.reset_for_test()


def _row(sym='AAA', score=80, rr_ok=True, verdict='BUY', regime='TREND', **kw):
    d = {'symbol': sym, 'score': score, 'rr_ok': rr_ok, 'verdict': verdict,
         'regime': regime}
    d.update(kw)
    return d


# ─────────────────────────────────────── gates canoniques

def test_regime_inconnu_ne_passe_jamais_l_entonnoir():
    """decide.py refuse tout nouveau risque en régime inconnu — l'entonnoir
    ne peut pas être plus permissif que le gate canonique."""
    for regime in (None, '', 'UNKNOWN', 'INCONNU'):
        assert F.is_actionable(_row(regime=regime)) is False, repr(regime)


def test_regime_connu_reste_actionnable():
    assert F.is_actionable(_row(regime='TREND')) is True
    assert F.is_actionable(_row(regime='RANGE')) is True


def test_score_eleve_ne_contourne_pas_le_gate_rr():
    assert F.is_actionable(_row(score=99, rr_ok=False)) is False


# ─────────────────────────────────────── déduplication

def test_symbole_duplique_compte_une_fois_et_est_declare():
    rows = [_row('AAA', score=90), _row('AAA', score=70), _row('BBB', score=60)]
    out = F.build_funnel(rows)
    stages = {s['key']: s['count'] for s in out['stages']}
    assert stages['universe'] == 2, 'AAA ne compte qu\'une fois'
    assert out['duplicates_dropped'] == 1
    #  le meilleur score du doublon est conservé (rows triés score desc)
    assert 'AAA' in out['actionable_symbols']


def test_sans_doublon_le_compte_est_zero():
    assert F.build_funnel([_row('AAA'), _row('BBB')])['duplicates_dropped'] == 0


# ─────────────────────────────────────── budgets déclarés

def test_les_listes_surfacees_declarent_leur_budget():
    rows = [_row('S%02d' % i, score=90) for i in range(12)]
    out = F.build_funnel(rows)
    assert out['budgets']['actionable_symbols'] == 5
    assert len(out['actionable_symbols']) <= 5
    assert out['budgets']['entrants'] == 10
    assert out['budgets']['sortants'] == 10


# ─────────────────────────────────────── point-in-time + delta

def test_premier_scan_delta_honnete_jamais_invente():
    out = F.build_funnel([_row('AAA')], scan_ts=1000.0)
    assert out['as_of'] == 1000.0
    d = out['delta']
    assert d['premier_scan'] is True
    assert d['entrants'] == [] and d['sortants'] == []
    assert d['baseline_ts'] is None


def test_delta_entre_deux_scans():
    F.build_funnel([_row('AAA'), _row('BBB')], scan_ts=1000.0)
    out = F.build_funnel([_row('BBB'), _row('CCC')], scan_ts=2000.0)
    d = out['delta']
    assert d['premier_scan'] is False
    assert d['entrants'] == ['CCC'] and d['sortants'] == ['AAA']
    assert d['baseline_ts'] == 1000.0


def test_meme_scan_delta_stable_pas_de_rotation():
    """Deux GET pendant le MÊME scan rendent le même delta (rotation par
    scan_ts, pas par appel) — un rafraîchissement de page ne vide pas le delta."""
    F.build_funnel([_row('AAA')], scan_ts=1000.0)
    a = F.build_funnel([_row('AAA'), _row('DDD')], scan_ts=2000.0)
    b = F.build_funnel([_row('AAA'), _row('DDD')], scan_ts=2000.0)
    assert a['delta'] == b['delta']
    assert a['delta']['entrants'] == ['DDD']


def test_sans_scan_ts_pas_de_delta_invente():
    out = F.build_funnel([_row('AAA')])
    assert out['as_of'] is None
    assert out['delta']['disponible'] is False


# ─────────────────────────────────────── route

def test_la_route_expose_as_of_et_delta():
    import importlib
    import terminal
    from vertex.app.state import scan_state
    sauve = {k: scan_state.get(k) for k in ('rows', 'scan_ts')}
    try:
        scan_state['rows'] = [_row('AAA')]
        scan_state['scan_ts'] = 1234.5
        c = terminal.app.test_client()
        r = c.get('/api/opportunities/funnel')
        assert r.status_code == 200
        j = r.get_json()
        assert j['as_of'] == 1234.5
        assert 'delta' in j and 'stages' in j
    finally:
        for k, v in sauve.items():
            scan_state[k] = v
