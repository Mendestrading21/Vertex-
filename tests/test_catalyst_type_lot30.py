"""tests/test_catalyst_type_lot30.py — SKYLER LOT 30 : type de catalyseur figé.

Le moteur émet `catalyst_kind` — le `kind` EXPLICITE (earnings/macro/news…)
du même événement daté le plus proche qui produit déjà `catalyst`. Le kind
est un FAIT du moteur events (jamais deviné en re-parsant le label, jamais
rétroactif : ancien record sans kind → None honnête, bucket `inconnu`).
La calibration par contexte gagne la découpe `by_catalyst_type` —
OBSERVATION UNIQUEMENT, jamais consommée par la sélection du facteur.
Moteur 0.8.0 → 0.9.0 (nouveau champ émis + figé). Aucun changement de shell.
"""
import inspect

import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import skyler_core as SK


# ─── Moteur : émission du kind (source unique = même événement que catalyst) ────

def _detail():
    return {'price': 100.0, 'score': 72, 'verdict': 'ACHETER', 'trend': 80,
            'rsi': 55, 'regime': 'TREND', 'setup_quality': 70, 'atr_pct': 2.0,
            'confidence': 62,
            'plan': {'entry': 100.0, 'stop': 94.0, 'tp1': 106.0, 'tp2': 112.0,
                     'tp3': 118.0, 'rr': 3.0, 'rr_res': 3.0,
                     'resistance': 115.0, 'atr': 2.0}}


def _events_two_kinds():
    return {'events': [
        {'kind': 'earnings', 'label': 'Résultats TST', 'dte': 12,
         'category': 'fact', 'source': 'calendar.earnings'},
        {'kind': 'macro', 'label': 'CPI', 'dte': 5,
         'category': 'fact', 'source': 'calendar.macro'},
        {'kind': 'news', 'label': 'Article', 'dte': None,
         'category': 'fact', 'source': 'news_plus'},
    ], 'n': 3, 'revisions': {'available': False}}


def test_engine_version_bumped_prospective():
    parts = tuple(int(x) for x in SK.ENGINE_VERSION.split('.'))
    assert parts >= (0, 9, 0)


def test_decide_emits_kind_of_nearest_dated_event():
    d = SK.decide('TST', _detail(), events=_events_two_kinds(), as_of='10:00:00')
    assert d['catalyst'] == 'CPI (J-5)'          # le plus proche (dte 5 < 12)
    assert d['catalyst_kind'] == 'macro'         # kind du MÊME événement


def test_decide_kind_none_without_dated_events():
    ev = {'events': [{'kind': 'news', 'label': 'Article', 'dte': None,
                      'category': 'fact', 'source': 'news_plus'}],
          'n': 1, 'revisions': {'available': False}}
    d = SK.decide('TST', _detail(), events=ev, as_of='10:00:00')
    assert d['catalyst'] is None and d['catalyst_kind'] is None


# ─── Ledger : figé au freeze, jamais deviné rétroactivement ─────────────────────

def test_freeze_stores_explicit_kind():
    d = {'symbol': 'KT', 'as_of': 't', 'decision': 'ACHETER',
         'score': {'total': 30, 'level': 'A', 'insufficient_blocks': []},
         'level': 'A', 'contradictions': [], 'unknowns': [],
         'catalyst': 'Résultats KT (J-12)', 'catalyst_kind': 'earnings'}
    r = DM.freeze(decision=d, packet={'schema_version': 1, 'engine_version': 'vT'},
                  price=100.0, closes=None, portfolio_ctx=None, now=0)
    assert r['catalyst_kind'] == 'earnings'


def test_freeze_never_guesses_kind_from_label():
    """Décision d'un moteur antérieur : catalyst présent mais kind absent —
    le record dit None, JAMAIS un kind re-parsé depuis « CPI (J-3) »."""
    d = {'symbol': 'KT', 'as_of': 't', 'decision': 'ACHETER',
         'score': {'total': 30, 'level': 'A', 'insufficient_blocks': []},
         'level': 'A', 'contradictions': [], 'unknowns': [],
         'catalyst': 'CPI (J-3)'}
    r = DM.freeze(decision=d, packet={'schema_version': 1, 'engine_version': 'vT'},
                  price=100.0, closes=None, portfolio_ctx=None, now=0)
    assert r.get('catalyst_kind') is None


# ─── Calibration : découpe by_catalyst_type (observation uniquement) ────────────

def _mk(i, catalyst='Résultats (J-21)', kind='earnings', level='A',
        ret=5.0, version='vT'):
    d = {'symbol': 'T%03d' % i, 'as_of': str(i), 'decision': 'ACHETER',
         'score': {'total': 30, 'level': level, 'insufficient_blocks': []},
         'level': level, 'contradictions': [], 'unknowns': [],
         'catalyst': catalyst,
         'scenarios': {'available': True, 'bear': {'return_pct': -6.0},
                       'base': {'return_pct': 12.0}, 'bull': {'return_pct': 18.0}}}
    if kind is not None:
        d['catalyst_kind'] = kind
    r = DM.freeze(decision=d, packet={'schema_version': 1, 'engine_version': version},
                  price=100.0, closes=None, portfolio_ctx=None, now=i)
    o = {'decision_id': r['decision_id'], 'engine_version': version,
         'symbol': r['symbol'], 'sessions_observed': 20,
         'horizons': {'H20': {'status': 'MESURE', 'sessions': 20,
                              'return_pct': ret, 'basis': 't'}},
         'mfe_pct': None, 'mae_pct': None}
    return r, o


def _mem(rows):
    mem = DM.empty_memory()
    for r, o in rows:
        mem = DM.append_outcome(DM.append_decision(mem, r), o)
    return mem


def test_by_catalyst_type_cells_with_sample_rules():
    rows = [_mk(i, kind='earnings', ret=(5.0 if i < 20 else -15.0))
            for i in range(25)]
    rows += [_mk(100 + i, kind='macro', ret=3.0) for i in range(3)]
    rows += [_mk(200 + i, catalyst=None, kind=None, ret=3.0) for i in range(3)]
    ctx = DM.calibration_by_context(_mem(rows), 'vT')
    bt = ctx['by_catalyst_type']
    assert bt['earnings']['status'] == 'MESURE'
    assert bt['earnings']['n_measured'] == 25
    assert bt['earnings']['hit_rate'] == pytest.approx(0.8)
    assert bt['macro']['status'] == 'INSUFFISANT' and bt['macro']['value'] is None
    # sans catalyseur : exclus de la découpe par type (leur domicile est
    # by_catalyst.sans_catalyseur)
    assert sum(c['n_measured'] for c in bt.values()) == 28


def test_by_catalyst_type_unknown_kind_honest_bucket():
    """Records d'un moteur antérieur (catalyst figé, kind absent) → bucket
    `inconnu` — jamais un type deviné rétroactivement."""
    rows = [_mk(i, kind=None) for i in range(5)]
    ctx = DM.calibration_by_context(_mem(rows), 'vT')
    assert ctx['by_catalyst_type']['inconnu']['n_measured'] == 5
    assert 'earnings' not in ctx['by_catalyst_type']


def test_by_catalyst_type_never_consumed_by_selection():
    """25 mesures earnings mais réparties sur 5 niveaux (tous insuffisants) :
    la sélection tombe sur le GLOBAL — la découpe par type n'est jamais une
    règle moteur."""
    levels = ['S_PLUS', 'S', 'A', 'B', 'REFUS_WATCH']
    rows = [_mk(i, level=levels[i % 5]) for i in range(25)]
    f = DM.calibration_factor_for(_mem(rows), 'vT', level='A', regime='CHOP')
    assert f['scope'] == 'global'
    sig = inspect.signature(DM.calibration_factor_for).parameters
    assert 'catalyst_kind' not in sig and 'catalyst_type' not in sig


def test_by_catalyst_type_deterministic_and_note():
    rows = [_mk(i) for i in range(25)]
    m = _mem(rows)
    a, b = DM.calibration_by_context(m, 'vT'), DM.calibration_by_context(m, 'vT')
    assert a == b
    assert 'observation' in a['note']
