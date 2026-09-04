"""tests/test_reco_facade.py — SKYLER LOT 87 : façade recommendation figée.

`vertex/engines/recommendation.py` (façade UNIQUE : vocabulaire __VXVOCAB,
normalize, gestion de position détenue, options sur position) n'avait
AUCUN test dédié — le module testé ailleurs est `vertex.options.
recommendation`, un homonyme. Tests de CARACTÉRISATION nés verts (dits) :
ils figent le comportement actuel sans toucher au moteur.
"""
import json

from vertex.engines import recommendation as reco
from vertex.engines.decision_stack import DECISIONS


def test_vocab_covers_every_stack_decision_and_held_verdict():
    vocab = json.loads(reco.vocab_js())
    for key, (label, tone) in DECISIONS.items():
        assert key in vocab, f'décision {key} sans libellé client (__VXVOCAB)'
        assert vocab[key]['label'] == label and vocab[key]['tone'] == tone
        assert vocab[key]['cls'] in ('p-good', 'p-info', 'p-warn', 'p-bad', 'p-mut')
    for key in reco.HELD:
        assert key in vocab, f'verdict de gestion {key} sans libellé client'


def test_normalize_empty_and_unknown_are_honest():
    for raw in (None, ''):
        n = reco.normalize(raw)
        assert n == {'label': '—', 'tone': 'gray', 'cls': 'p-mut'}
    n = reco.normalize('VERDICT_JAMAIS_VU')
    assert n['tone'] == 'gray' and n['cls'] == 'p-mut'
    assert n['label'] == 'VERDICT_JAMAIS_VU'   # passthrough, jamais inventé


def test_normalize_historic_aliases_case_insensitive():
    assert reco.normalize('acheter fort')['tone'] == 'strong-green'
    assert reco.normalize(' REFUSÉ ')['tone'] == 'red'
    assert reco.normalize('renforcer')['tone'] == 'green'


def test_empty_position_defaults_to_hold():
    r = reco.position_decision({})
    assert r['verdict'] == 'HOLD'
    assert r['verdict'] in reco.HELD and r['label'] and r['cls']


def test_stop_hit_forces_exit():
    r = reco.position_decision({'stop': 95, 'current': 94})
    assert r['verdict'] == 'EXIT' and r['confidence'] == 78


def test_discipline_drawdown_stock_20_option_25():
    # action : -20 % coupe ; option : -20 % ne coupe PAS (limite -25 %)
    assert reco.position_decision({'type': 'STK', 'pl_pct': -20})['verdict'] == 'EXIT'
    assert reco.position_decision({'type': 'CALL', 'pl_pct': -20})['verdict'] != 'EXIT'
    assert reco.position_decision({'type': 'CALL', 'pl_pct': -25})['verdict'] == 'EXIT'


def test_option_near_expiry_theta_rules():
    gain = reco.position_decision({'type': 'CALL', 'dte': 10, 'pl_pct': 15})
    flat = reco.position_decision({'type': 'CALL', 'dte': 10})
    assert gain['verdict'] == 'TAKE_PROFIT'
    assert flat['verdict'] == 'EXIT'


def test_near_target_secures_and_big_gains_protect():
    assert reco.position_decision({'tp': 102, 'current': 100})['verdict'] == 'TAKE_PROFIT'
    assert reco.position_decision({'pl_pct': 120})['verdict'] == 'TRIM'
    assert reco.position_decision({'pl_pct': 45})['verdict'] == 'RAISE_STOP'


def test_underlying_signal_drives_add_or_trim():
    trim = reco.position_decision({}, underlying={'final_decision': 'AVOID'})
    add = reco.position_decision({'pl_pct': 5},
                                 underlying={'final_decision': 'STRONG_BUY'})
    assert trim['verdict'] == 'TRIM'
    assert add['verdict'] == 'ADD'


def test_options_for_position_empty_board_is_honest():
    r = reco.options_for_position('ACN', [])
    assert r['suggestions'] == []
    assert r['note'] and 'Aucun contrat' in r['note']


def test_options_for_position_excludes_missing_dte_from_horizon_roles():
    rows = [
        {'sym': 'TST', 'type': 'CALL', 'quality': 99, 'dte': None, 'delta': 0.30},
        {'sym': 'TST', 'type': 'PUT', 'quality': 99, 'dte': 'inconnu', 'delta': -0.30},
        {'sym': 'TST', 'type': 'CALL', 'quality': 80, 'dte': 365, 'delta': 0.70},
        {'sym': 'TST', 'type': 'CALL', 'quality': 70, 'dte': 45, 'delta': 0.30},
        {'sym': 'TST', 'type': 'PUT', 'quality': 70, 'dte': 60, 'delta': -0.30},
    ]
    roles = {item['role']: item for item in reco.options_for_position('TST', rows, 'STK')['suggestions']}
    assert roles['LEAPS']['dte'] == 365
    assert roles['COVERED_CALL']['dte'] == 45
    assert roles['PROTECTIVE_PUT']['dte'] == 60
