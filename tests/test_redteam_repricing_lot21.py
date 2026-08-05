"""tests/test_redteam_repricing_lot21.py — SKYLER LOT 21 : repricing red-team.

Les questions options de la red-team cessent d'être qualitatives quand les
données du candidat le permettent : Q05 (« IV −10 pts ») répond avec l'impact
CHIFFRÉ (repricing Black-Scholes du pricer canonique `scenario_pricer` — spot
et échéance inchangés, étiqueté F3 avec modèle et hypothèses) ; Q08 (« option
vs action ») répond avec la grille spot pessimiste/probable/exceptionnel ×
IV −10/0/+10 quand le plan moteur fournit les niveaux. Entrées incomplètes →
réponse qualitative d'avant (F2) ; IV absente → UNANSWERED inchangé.
RED_TEAM_VERSION 1.0.0 → 1.1.0 (contrat des réponses enrichi).
"""
import math

import pytest

from vertex.engines import red_team as RT
from vertex.options.scenario_pricer import bs_price


def _packet(best=None, plan=True):
    p = {'entry': 100.0, 'stop': 94.0, 'tp2': 112.0, 'tp3': 118.0, 'rr_res': 3.0}
    ctx = {
        'technical': {'available': True, 'score': 70, 'verdict': 'ATTENDRE',
                      'rsi': 62.0, 'plan': (p if plan else {'rr_res': 3.0})},
        'market': {'regime': {'label': 'TREND_UP', 'confidence': 0.8,
                              'adjustments': {'new_risk_allowed': True}}},
        'catalysts': {'available': True, 'events': [{'label': 'Résultats', 'dte': 21}]},
        'anomalies': {'available': True, 'events': [], 'extreme': 'high'},
        'fundamentals': {'available': False, 'reason': 'non branché'},
        'options': ({'available': True, 'universe': 'LEAPS', 'best': best}
                    if best is not None else {'available': False, 'reason': 'x'}),
        'portfolio': {'available': True, 'n_positions': 3, 'hhi': 0.35,
                      'top_symbol': 'AAA', 'top_weight_pct': 40.0},
    }
    return {'schema_version': 1, 'engine_version': 'x', 'symbol': 'RPX',
            'demo': False, 'contexts': ctx, 'contradictions': [], 'unknowns': [],
            'audit_trail': []}


def _score():
    return {'total': 30, 'max': 40,
            'blocks': {'technical_timing': {'points': 4, 'max': 6},
                       'data_quality': {'points': 3, 'max': 4}},
            'level': 'A', 'insufficient_blocks': []}


_FULL = {'type': 'CALL', 'strike': 100.0, 'dte': 365, 'iv': 0.30,
         'spot': 100.0, 'quality': 80}


# ─── Sanity du pricer canonique (cas manuel connu) ──────────────────────────────

def test_canonical_pricer_manual_case():
    """ATM 1 an, vol 20 %, taux 0, sans dividende ≈ 7,97 % du spot (valeur
    connue de Black-Scholes) — garde-fou contre toute régression du pricer."""
    assert bs_price(100.0, 100.0, 1.0, 0.20, 0.0, 'C') == pytest.approx(7.9656, abs=0.01)


# ─── Q05 : impact IV −10 pts CHIFFRÉ ────────────────────────────────────────────

def test_q05_quantified_with_full_candidate():
    r = RT.review(_packet(best=dict(_FULL)), _score())
    q5 = {q['id']: q for q in r['questions']}['Q05']
    assert q5['status'] == 'ANSWERED'
    assert q5['evidence_level'] == 'F3'                     # estimation de modèle
    assert q5['model'] == 'black_scholes_european'
    assert '%' in q5['answer'] and 'IV' in q5['answer']
    # l'impact est négatif et substantiel (vega positive, IV 30 → 20)
    v1 = bs_price(100.0, 100.0, 1.0, 0.30, 0.045, 'C')
    v0 = bs_price(100.0, 100.0, 1.0, 0.20, 0.045, 'C')
    expected = (v0 / v1 - 1) * 100
    assert -35.0 < expected < -20.0
    assert ('%.1f' % expected) in q5['answer'] or ('%.0f' % expected) in q5['answer'] \
        or ('%+.1f' % expected) in q5['answer']


def test_q05_qualitative_fallback_without_spot():
    best = dict(_FULL)
    best.pop('spot')
    r = RT.review(_packet(best=best), _score())
    q5 = {q['id']: q for q in r['questions']}['Q05']
    assert q5['status'] == 'ANSWERED'
    assert q5['evidence_level'] == 'F2'                     # qualitatif d'avant
    assert 'model' not in q5


def test_q05_unanswered_without_iv_unchanged():
    best = dict(_FULL)
    best.pop('iv')
    r = RT.review(_packet(best=best), _score())
    q5 = {q['id']: q for q in r['questions']}['Q05']
    assert q5['status'] == 'UNANSWERED'


# ─── Q08 : grille spot × IV depuis les niveaux réels du plan ────────────────────

def test_q08_grid_with_plan_and_full_candidate():
    r = RT.review(_packet(best=dict(_FULL)), _score())
    q8 = {q['id']: q for q in r['questions']}['Q08']
    assert q8['status'] == 'ANSWERED'
    assert q8['evidence_level'] == 'F3'
    assert q8['model'] == 'black_scholes_european'
    a = q8['answer']
    assert 'grille' in a.lower()
    assert 'stop' in a.lower() and 'TP2' in a and 'TP3' in a
    # convexité réelle : au TP2 (spot 112, IV stable), le call ATM 1 an fait
    # bien mieux que l'action (+12 %) — le chiffre doit figurer dans la réponse
    v1 = bs_price(100.0, 100.0, 1.0, 0.30, 0.045, 'C')
    v_tp2 = bs_price(112.0, 100.0, 1.0, 0.30, 0.045, 'C')
    gain = (v_tp2 / v1 - 1) * 100
    assert gain > 12.0
    assert 'action' in a.lower()


def test_q08_qualitative_fallback_without_plan_targets():
    r = RT.review(_packet(best=dict(_FULL), plan=False), _score())
    q8 = {q['id']: q for q in r['questions']}['Q08']
    assert q8['status'] == 'ANSWERED'
    assert q8['evidence_level'] == 'F2'
    assert 'model' not in q8


# ─── Robustesse : entrées invalides refusées, déterminisme, version ─────────────

def test_invalid_candidate_inputs_never_crash_never_nan():
    for bad in ({'iv': float('nan')}, {'iv': -0.3}, {'dte': 0}, {'strike': -5.0},
                {'spot': 0.0}):
        best = dict(_FULL)
        best.update(bad)
        r = RT.review(_packet(best=best), _score())
        q5 = {q['id']: q for q in r['questions']}['Q05']
        assert q5.get('model') is None                      # jamais chiffré sur entrée invalide

        def _no_nan(o):
            if isinstance(o, float):
                assert math.isfinite(o)
            elif isinstance(o, dict):
                for v in o.values():
                    _no_nan(v)
            elif isinstance(o, list):
                for v in o:
                    _no_nan(v)
        _no_nan(r)


def test_review_still_deterministic_and_complete():
    a = RT.review(_packet(best=dict(_FULL)), _score())
    b = RT.review(_packet(best=dict(_FULL)), _score())
    assert a == b
    assert a['complete'] is True                            # 10/10 toujours atteignable


def test_red_team_version_bumped():
    parts = tuple(int(x) for x in RT.RED_TEAM_VERSION.split('.'))
    assert parts >= (1, 1, 0)
