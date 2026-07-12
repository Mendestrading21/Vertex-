"""Tests §11-12 — entonnoir d'opportunités & rôles stratégiques."""
from vertex.opportunities import funnel as F


def _row(score, verdict='ACHETER', rr_ok=True, **kw):
    r = {'symbol': kw.get('symbol', 'TST'), 'score': score, 'verdict': verdict,
         'rr_ok': rr_ok}
    r.update(kw)
    return r


def test_funnel_stage_counts_are_monotone_down_to_actionable():
    rows = [_row(80, symbol='A'), _row(70, symbol='B'), _row(60, symbol='C'),
            _row(50, symbol='D'), {'symbol': 'E'}]  # E sans score
    f = F.build_funnel(rows)
    counts = {s['key']: s['count'] for s in f['stages']}
    assert counts['universe'] == 5
    assert counts['eligible'] == 4            # E exclu (pas de score)
    assert counts['radar'] >= counts['priority'] >= counts['actionable']


def test_actionable_requires_rr_score_and_buy():
    assert F.is_actionable(_row(80, 'ACHETER', True))
    assert not F.is_actionable(_row(80, 'ACHETER', False))   # R:R non validé
    assert not F.is_actionable(_row(70, 'ACHETER', True))    # score < 72
    assert not F.is_actionable(_row(80, 'ATTENDRE', True))   # pas un achat


def test_zero_actionable_is_valid_and_noted():
    rows = [_row(60, 'ATTENDRE', False)]
    f = F.build_funnel(rows)
    assert next(s['count'] for s in f['stages'] if s['key'] == 'actionable') == 0
    assert f['zero_actionable_is_valid'] is True
    assert f['note'] and 'valide' in f['note'].lower()


def test_followed_and_positions_counts_passthrough():
    f = F.build_funnel([_row(80)], followed=3, positions=7)
    counts = {s['key']: s['count'] for s in f['stages']}
    assert counts['followed'] == 3 and counts['positions'] == 7


def test_roles_are_valid_vocabulary():
    for row in (_row(80, st_mom=70, vx_asym=60, perf_q=15, rs=70),
                _row(75, st_fund=60, rs=58),
                _row(70, profile='DÉFENSIF'),
                _row(70, vehicle='ETF')):
        assert F.classify_role(row) in F.ROLES


def test_role_attack_for_high_momentum_growth():
    r = _row(85, st_mom=72, vx_asym=62, perf_q=18, rs=70)
    assert F.classify_role(r) == F.ROLE_ATTACK


def test_role_reserve_for_etf():
    assert F.classify_role(_row(70, vehicle='ETF')) == F.ROLE_RESERVE


def test_role_defense_for_defensive_profile():
    assert F.classify_role(_row(68, profile='DÉFENSIF')) == F.ROLE_DEFENSE


def test_role_defense_when_risk_score_is_genuinely_zero():
    # st_risk == 0 (risque très faible RÉEL) doit rester 0 et donner DÉFENSE,
    # pas être coercé vers le défaut neutre 50 (`0 or 50 == 50`).
    r = _row(60, st_mom=20, st_fund=40, rs=40, vx_asym=20, perf_q=2, st_risk=0)
    assert F.classify_role(r) == F.ROLE_DEFENSE


def test_role_missing_risk_uses_neutral_default():
    # st_risk absent → défaut neutre 50 → pas de bascule défensive automatique.
    r = _row(60, st_mom=20, st_fund=40, rs=40, vx_asym=20, perf_q=2)
    assert F.classify_role(r) == F.ROLE_MID


def test_role_distribution_sums_to_priority_count():
    rows = [_row(80, st_mom=70, vx_asym=60, perf_q=15, rs=70, symbol='A'),
            _row(70, st_fund=60, rs=58, symbol='B'),
            _row(68, profile='DÉFENSIF', symbol='C')]
    f = F.build_funnel(rows)
    priority = next(s['count'] for s in f['stages'] if s['key'] == 'priority')
    assert sum(x['count'] for x in f['roles']) == priority
