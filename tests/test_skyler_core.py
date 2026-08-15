"""tests/test_skyler_core.py — SKYLER LOT 5 : Skyler Core.

Exigences (SKILL §10 lot 5 + SKYLER_ARCHITECTURE.md) : SkylerPacket typé, score
/40 depuis les blocs du profil V2, hard gates prioritaires sur le score,
scénarios SANS probabilité arbitraire (modèle non calibré → None assumé),
détecteur de contradictions, audit trail, réponse déterministe sans Claude,
non-invention (contexte absent = INSUFFISANT, jamais rempli).
"""
import json

import pytest

from vertex.engines import skyler_core as SK


def _detail(score=72, verdict='ACHETER', rr_res=3.0, with_plan=True):
    d = {
        'price': 100.0, 'score': score, 'verdict': verdict, 'trend': 80,
        'rsi': 55, 'regime': 'TREND', 'setup_quality': 70, 'atr_pct': 2.0,
        'confidence': 62,
    }
    if with_plan:
        d['plan'] = {'entry': 100.0, 'stop': 94.0, 'tp1': 106.0, 'tp2': 112.0,
                     'tp3': 118.0, 'rr': 3.0, 'rr_res': rr_res,
                     'resistance': 115.0, 'atr': 2.0}
    return d


def _market(label='TREND_UP', new_risk=True):
    return {'regime': {'label': label, 'confidence': 0.7,
                       'adjustments': {'new_risk_allowed': new_risk},
                       'transition': {'from': None, 'to': label, 'changed': None}},
            'conflicts': [], 'as_of': '10:00:00',
            'dimensions': {'vix': {'value': 15.0, 'status': 'LIVE'}}}


def _events():
    return {'events': [{'kind': 'earnings', 'label': 'Résultats TST', 'dte': 12,
                        'category': 'fact', 'impact_hint': 'EARNINGS',
                        'confidence': 'DECLARED', 'date': '2026-08-16',
                        'source': 'calendar.earnings', 'impact_derivation': 'calendar',
                        'importance': None}],
            'n': 1, 'revisions': {'available': False}}


# ─── Packet : contrats typés, non-invention, audit trail ────────────────────────

def test_packet_shape_and_versions():
    p = SK.build_packet('TST', _detail(), market=_market(), events=_events(),
                        as_of='10:00:00')
    assert p['schema_version'] == 1 and p['engine_version']
    assert p['profile_version'] == 3                  # constitution V3 active
    assert p['symbol'] == 'TST'
    assert p['freshness_floor'] == '10:00:00'
    assert isinstance(p['audit_trail'], list) and p['audit_trail']
    for step in p['audit_trail']:
        assert step['step'] and 'result' in step


def test_unwired_contexts_are_insufficient_never_invented():
    p = SK.build_packet('TST', _detail(), as_of='10:00:00')
    for name in ('fundamentals', 'options', 'portfolio'):
        ctx = p['contexts'][name]
        assert ctx['available'] is False
        assert 'reason' in ctx
    assert 'market' in p['unknowns'] or p['contexts']['market']['available'] is False


def test_empty_detail_honest():
    p = SK.build_packet('TST', {}, as_of=None)
    assert p['contexts']['technical']['available'] is False


# ─── Score /40 depuis le profil V2 ──────────────────────────────────────────────

def test_score_blocks_match_profile_and_bound():
    p = SK.build_packet('TST', _detail(), market=_market(), events=_events(),
                        as_of='10:00:00')
    sc = SK.score40(p)
    from vertex.strategy.constitution import load_profile
    blocks_cfg = load_profile().raw['skyler_score']['blocks']
    assert set(sc['blocks']) == set(blocks_cfg)
    for name, b in sc['blocks'].items():
        assert 0 <= b['points'] <= blocks_cfg[name]     # jamais au-dessus du max du bloc
        assert b['max'] == blocks_cfg[name]
        assert b['basis']                                # chaque point est justifié
    assert sc['total'] == sum(b['points'] for b in sc['blocks'].values())
    assert 0 <= sc['total'] <= 40


def test_unwired_blocks_score_zero_and_flagged():
    p = SK.build_packet('TST', _detail(), market=_market(), events=_events(),
                        as_of='10:00:00')
    sc = SK.score40(p)
    assert sc['blocks']['fundamentals_quality']['points'] == 0
    assert sc['blocks']['fundamentals_quality']['status'] == 'INSUFFICIENT'
    assert sc['blocks']['options_quality']['status'] == 'INSUFFICIENT'
    assert 'fundamentals_quality' in sc['insufficient_blocks']


def test_level_from_v2_conviction_levels():
    p = SK.build_packet('TST', _detail(), market=_market(), events=_events(),
                        as_of='10:00:00')
    sc = SK.score40(p)
    assert sc['level'] in ('S_PLUS', 'S', 'A', 'B', 'REFUS_WATCH')


# ─── Hard gates : prioritaires, jamais contournés par le score ─────────────────

def test_rr_below_2_gate_triggers():
    p = SK.build_packet('TST', _detail(rr_res=1.2), market=_market(),
                        events=_events(), as_of='10:00:00')
    gates = SK.hard_gates(p, SK.score40(p))
    g = next(g for g in gates if g['id'] == 'RR_BELOW_2')
    assert g['triggered'] is True and g['reason']


def test_no_invalidation_gate_triggers_without_plan():
    p = SK.build_packet('TST', _detail(with_plan=False), market=_market(),
                        as_of='10:00:00')
    gates = SK.hard_gates(p, SK.score40(p))
    assert next(g for g in gates if g['id'] == 'NO_INVALIDATION')['triggered'] is True


def test_unevaluable_gates_are_unknown_not_false():
    p = SK.build_packet('TST', _detail(), market=_market(), as_of='10:00:00')
    gates = SK.hard_gates(p, SK.score40(p))
    conc = next(g for g in gates if g['id'] == 'CONCENTRATION_EXCESSIVE')
    assert conc['triggered'] is None                  # portefeuille non fourni → inconnu honnête
    assert 'non fourni' in conc['reason'] or 'branché' in conc['reason']


# ─── Scénarios : jamais de probabilité sans modèle ──────────────────────────────

def test_scenarios_from_real_plan_no_invented_probability():
    sc = SK.scenarios(_detail())
    assert sc['available'] is True
    for name in ('bear', 'base', 'bull'):
        s = sc[name]
        assert s['target'] is not None and s['return_pct'] is not None
        assert s['probability'] is None               # modèle non calibré → JAMAIS un chiffre
        assert 'calibr' in s['probability_note']
        assert s['invalidation'] is not None
    # arithmétique exacte : bear = stop 94 depuis entry 100 → −6 %
    assert sc['bear']['return_pct'] == pytest.approx(-6.0, abs=0.01)
    assert sc['bull']['return_pct'] == pytest.approx(18.0, abs=0.01)


def test_scenarios_without_plan_unavailable():
    sc = SK.scenarios(_detail(with_plan=False))
    assert sc['available'] is False and 'reason' in sc


# ─── Contradictions ─────────────────────────────────────────────────────────────

def test_contradiction_bullish_verdict_vs_blocking_regime():
    p = SK.build_packet('TST', _detail(verdict='ACHETER'),
                        market=_market(label='RISK_OFF', new_risk=False),
                        as_of='10:00:00')
    assert any('régime' in c['detail'].lower() or 'risque neuf' in c['detail'].lower()
               for c in p['contradictions'])


def test_no_false_contradiction_when_aligned():
    p = SK.build_packet('TST', _detail(verdict='ACHETER'), market=_market(),
                        events=_events(), as_of='10:00:00')
    assert p['contradictions'] == []


# ─── Décision canonique déterministe (sans Claude) ─────────────────────────────

def test_decision_capped_by_hard_gate():
    d = SK.decide('TST', _detail(rr_res=1.0), market=_market(), events=_events(),
                  as_of='10:00:00')
    assert d['decision'] in ('ATTENDRE', 'REFUSER')   # gate R:R → jamais ACHETER
    assert d['capped_by_gate'] == 'RR_BELOW_2'
    assert d['generator'] == 'deterministic'


def test_decision_full_shape():
    d = SK.decide('TST', _detail(), market=_market(), events=_events(),
                  as_of='10:00:00')
    from vertex.strategy.constitution import ALLOWED_FINAL_DECISIONS
    assert d['decision'] in ALLOWED_FINAL_DECISIONS
    assert d['score']['total'] <= 40 and d['level']
    assert d['invalidation'] is not None              # stop réel du plan
    assert d['catalyst'] is not None                  # prochain événement daté
    assert d['max_risk_pct'] == pytest.approx(6.0, abs=0.01)
    assert d['strongest_objection']                   # jamais vide : objection ou limite
    assert d['unknowns']
    assert d['audit_trail']


def test_decision_is_deterministic():
    a = SK.decide('TST', _detail(), market=_market(), events=_events(), as_of='10:00:00')
    b = SK.decide('TST', _detail(), market=_market(), events=_events(), as_of='10:00:00')
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_conservative_when_canonical_verdict_prudent():
    """Skyler ne contredit pas le moteur canonique vers le haut : verdict prudent
    + score élevé → plafonné ATTENDRE + contradiction tracée."""
    d = SK.decide('TST', _detail(verdict='ATTENDRE'), market=_market(),
                  events=_events(), as_of='10:00:00')
    assert d['decision'] != 'ACHETER'


# ─── Route ──────────────────────────────────────────────────────────────────────

def test_skyler_route(tmp_path, monkeypatch):
    """⚠ `/api/skyler/<sym>` journalise une séance dans `skyler_sessions.json`.
    Sans redirection, ce test y semait un point par jour sur le ticker
    SYNTHÉTIQUE SKYX (lot 389). Stockage redirigé vers un dossier temporaire —
    mécanisme `_BASE_DIR`, comme `test_desk_routes.py` et le lot 388."""
    import terminal
    from vertex.app.state import scan_state
    from vertex.services import persist
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    scan_state.setdefault('detail', {})['SKYX'] = _detail()
    try:
        d = terminal.app.test_client().get('/api/skyler/SKYX').get_json()
        assert d['symbol'] == 'SKYX'
        assert d['decision']['generator'] == 'deterministic'
        assert d['packet']['schema_version'] == 1
    finally:
        scan_state['detail'].pop('SKYX', None)


def test_analysis_page_has_skyler_card():
    """Gardien LOT 8a : la fiche Analyse expose la carte Skyler (décision canonique)."""
    import terminal
    body = terminal.app.test_client().get('/analysis/AAPL').get_data(as_text=True)
    assert 'an-skyler' in body
    assert 'Skyler' in body
    assert 'loadSkyler' in body
