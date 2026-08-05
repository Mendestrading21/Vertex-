"""tests/test_red_team_producer_lot14.py — SKYLER LOT 14 : producteur red-team.

Le comité exige (ADVERSARIAL_COMMITTEE §8) que toute note S/S+ subisse une
red-team répondant à 10 questions minimum. Ce lot construit le PRODUCTEUR
déterministe : chaque question reçoit soit une réponse FONDÉE sur les données
réelles du packet (avec niveau de preuve), soit un statut UNANSWERED honnête —
jamais une réponse inventée. `complete=True` UNIQUEMENT si les 10 questions
ont une réponse fondée. Le moteur passe en 0.4.0 (la red-team produite entre
dans la décision).
"""
import pytest

from vertex.engines import red_team as RT
from vertex.engines import skyler_core as SK


def _packet(technical=True, market='TREND_UP', catalysts=True, options=True,
            portfolio=True, anomaly=True, stop=True):
    plan = {'entry': 100.0, 'stop': (94.0 if stop else None), 'tp2': 112.0,
            'rr_res': 3.0}
    if not stop:
        plan.pop('stop')
    ctx = {
        'technical': ({'available': True, 'score': 70, 'verdict': 'ATTENDRE',
                       'rsi': 62.0, 'plan': plan}
                      if technical else {'available': False, 'reason': 'x'}),
        'market': ({'regime': {'label': market, 'confidence': 0.8,
                               'adjustments': {'new_risk_allowed': market != 'RISK_OFF'}}}
                   if market else {'available': False, 'reason': 'x'}),
        'catalysts': ({'available': True,
                       'events': [{'label': 'Résultats', 'dte': 21}]}
                      if catalysts else {'available': False, 'reason': 'x'}),
        'anomalies': ({'available': True, 'events': [], 'extreme': 'high'}
                      if anomaly else {'available': False, 'reason': 'x'}),
        'fundamentals': {'available': False, 'reason': 'non branché'},
        'options': ({'available': True, 'universe': 'LEAPS',
                     'best': {'iv': 0.45, 'quality': 80}}
                    if options else {'available': False, 'reason': 'x'}),
        'portfolio': ({'available': True, 'n_positions': 3, 'hhi': 0.35,
                       'top_symbol': 'AAA', 'top_weight_pct': 40.0}
                      if portfolio else {'available': False, 'reason': 'x'}),
    }
    return {'schema_version': 1, 'engine_version': SK.ENGINE_VERSION,
            'symbol': 'RTP', 'demo': False, 'contexts': ctx,
            'contradictions': [], 'unknowns': [], 'audit_trail': []}


def _score(blocks=None, insufficient=None):
    return {'total': 30, 'max': 40,
            'blocks': blocks if blocks is not None else
            {'technical_timing': {'points': 4, 'max': 6},
             'asymmetry_scenarios': {'points': 4, 'max': 6},
             'data_quality': {'points': 3, 'max': 4}},
            'level': 'A', 'insufficient_blocks': insufficient or []}


# ─── Contrat des 10 questions ───────────────────────────────────────────────────

def test_review_covers_the_ten_committee_questions():
    r = RT.review(_packet(), _score())
    assert r['version'] == RT.RED_TEAM_VERSION
    assert len(r['questions']) == 10
    ids = [q['id'] for q in r['questions']]
    assert ids == ['Q%02d' % i for i in range(1, 11)]
    for q in r['questions']:
        assert q['question']
        assert q['status'] in ('ANSWERED', 'UNANSWERED')
        if q['status'] == 'ANSWERED':
            assert q['answer'] and q['evidence_level'] in ('F1', 'F2', 'F3', 'F4')
        else:
            assert q['reason']                    # pourquoi sans réponse — dit


def test_complete_only_when_all_ten_answered():
    full = RT.review(_packet(), _score())
    assert full['answered'] == 10
    assert full['complete'] is True
    partial = RT.review(_packet(options=False), _score())
    assert partial['complete'] is False
    assert partial['answered'] < 10


def test_never_invents_options_answers():
    r = RT.review(_packet(options=False), _score())
    by = {q['id']: q for q in r['questions']}
    assert by['Q05']['status'] == 'UNANSWERED'    # IV −10 pts : IV inconnue
    assert by['Q08']['status'] == 'UNANSWERED'    # option vs action : aucun candidat


def test_unknown_regime_leaves_riskoff_question_open():
    r = RT.review(_packet(market=None), _score())
    by = {q['id']: q for q in r['questions']}
    assert by['Q06']['status'] == 'UNANSWERED'
    assert r['complete'] is False


def test_missing_invalidation_leaves_loss_path_open():
    r = RT.review(_packet(stop=False), _score())
    by = {q['id']: q for q in r['questions']}
    assert by['Q09']['status'] == 'UNANSWERED'
    assert by['Q10']['status'] == 'UNANSWERED'


def test_missing_portfolio_leaves_hidden_exposure_open():
    r = RT.review(_packet(portfolio=False), _score())
    by = {q['id']: q for q in r['questions']}
    assert by['Q07']['status'] == 'UNANSWERED'


def test_answers_cite_real_data():
    r = RT.review(_packet(), _score())
    by = {q['id']: q for q in r['questions']}
    assert 'RSI' in by['Q01']['answer'] or 'fenêtre' in by['Q01']['answer']
    assert 'J-21' in by['Q04']['answer'] or '21' in by['Q04']['answer']
    assert '40' in by['Q07']['answer']            # top weight réel cité
    assert '94' in by['Q09']['answer'] or '6' in by['Q09']['answer']


def test_dominant_hypothesis_detected_from_blocks():
    blocks = {'technical_timing': {'points': 6, 'max': 6},
              'catalysts': {'points': 0, 'max': 5},
              'data_quality': {'points': 1, 'max': 4}}
    r = RT.review(_packet(), _score(blocks=blocks))
    by = {q['id']: q for q in r['questions']}
    assert by['Q03']['status'] == 'ANSWERED'
    assert 'technical_timing' in by['Q03']['answer']


def test_review_deterministic():
    assert RT.review(_packet(), _score()) == RT.review(_packet(), _score())


# ─── Intégration moteur 0.4.0 ───────────────────────────────────────────────────

def test_engine_version_bumped_for_produced_red_team():
    assert SK.ENGINE_VERSION == '0.4.0'


def test_decide_carries_completed_red_team():
    detail = {'score': 70, 'verdict': 'ATTENDRE',
              'plan': {'entry': 100, 'stop': 94, 'tp2': 112, 'rr_res': 3.0}}
    d = SK.decide('RTP', detail, as_of='t',
                  red_team={'complete': True, 'basis': 'revue 10/10'})
    assert d['red_team']['complete'] is True
    d2 = SK.decide('RTP', detail, as_of='t')
    assert d2['red_team']['complete'] is False


def test_route_serves_red_team_review(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    from vertex.app.state import scan_state
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    scan_state.setdefault('detail', {})['RTRX'] = {
        'price': 100.0, 'score': 70, 'verdict': 'ATTENDRE', 'rsi': 55.0,
        'closes': [95.0, 96.0, 97.0, 100.0],
        'plan': {'entry': 100, 'stop': 94, 'tp1': 106, 'tp2': 112, 'tp3': 118, 'rr_res': 3.0}}
    try:
        d = terminal.app.test_client().get('/api/skyler/RTRX').get_json()
        rt = d['red_team_review']
        assert rt['version'] == RT.RED_TEAM_VERSION
        assert len(rt['questions']) == 10
        assert rt['complete'] in (True, False)
        # la décision reflète le même statut que la revue servie
        assert d['decision']['red_team']['complete'] == rt['complete']
    finally:
        scan_state['detail'].pop('RTRX', None)
