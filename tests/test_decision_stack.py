"""
tests/test_decision_stack.py — La DecisionStack est la vérité : ses règles sont testées.

Chaque règle institutionnelle de dégradation a un test dédié. Toute sortie doit
appartenir à l'énumération autorisée et rester explicable.
"""

from vertex.engines import decision_stack as ds


def _stock(**over):
    base = {
        'symbol': 'TEST', 'price': 100, 'score': 82, 'grade': 'A', 'verdict': 'BUY',
        'rs': 75, 'rsi': 55, 'ext_atr': 1.0, 'pos52': 70, 'confidence': 70,
        'profile': 'OFFENSIF', 'signals': {'stacked': True},
        'plan': {'entry': 100, 'stop': 92, 'tp1': 108, 'tp2': 116, 'tp3': 130, 'rr_res': 2.5},
        'mtf': {'state': 'ALIGNÉ HAUSSIER'},
    }
    base.update(over)
    return base


def test_decision_in_allowed_set():
    r = ds.evaluate(_stock())
    assert r['final_decision'] in ds.DECISIONS
    assert r['decision_label'] and r['explanation']


def test_strong_setup_buys():
    r = ds.evaluate(_stock(), market={'roro': 'RISK-ON', 'spy_regime': 'TREND'})
    assert r['final_decision'] in {'STRONG_BUY', 'BUY'}
    assert r['market_permission'] is True


def test_missing_data_blocks():
    r = ds.evaluate({'symbol': 'X'})  # pas de price/score/plan
    assert r['final_decision'] == 'DATA_INSUFFICIENT'
    assert r['data_quality']['blocks_decision'] is True


def test_unknown_symbol_is_honestly_insufficient(monkeypatch):
    """Garde-fou C-08 : un symbole hors univers / sans donnée ne doit JAMAIS
    produire un verdict confiant. La décision reste 'Données insuffisantes' et
    la confiance de haut niveau est nulle (le comité interne peut refléter le
    seul vent de marché, mais il ne pilote pas la décision)."""
    r = ds.evaluate({'symbol': 'ZZZZZ'}, market={'roro': 'RISK-OFF', 'spy_regime': 'TREND'},
                    scan_age_s=10, demo=True)
    assert r['final_decision'] == 'DATA_INSUFFICIENT'
    assert r['decision_label'] == 'Données insuffisantes'
    assert r['confidence'] == 0            # confiance de décision nulle
    assert r['conviction'] == 0
    assert r['reasoning'] is None          # aucun scénario fabriqué
    assert r['score_breakdown'] is None    # aucune décomposition inventée
    assert 'price' in r['data_quality']['missing_fields']


def test_risk_off_no_strong_buy():
    r = ds.evaluate(_stock(score=90), market={'roro': 'RISK-OFF', 'spy_regime': 'TREND'})
    assert r['final_decision'] != 'STRONG_BUY'


def test_extension_downgrades():
    # sur-étendu + qualité forte → achat sur repli
    r = ds.evaluate(_stock(rsi=82, ext_atr=5, score=80))
    assert r['final_decision'] == 'BUY_PULLBACK'
    # sur-étendu + qualité moyenne → trop tard
    r2 = ds.evaluate(_stock(rsi=82, ext_atr=5, score=60, verdict='WATCH'))
    assert r2['final_decision'] in {'TOO_LATE', 'WATCH_BREAKOUT', 'WAIT'}


def test_low_rr_no_buy():
    r = ds.evaluate(_stock(plan={'entry': 100, 'stop': 96, 'tp1': 103, 'tp2': 105,
                                  'tp3': 108, 'rr_res': 1.0}))
    assert r['final_decision'] not in {'STRONG_BUY', 'BUY'}


def test_high_correlation_no_new_risk():
    r = ds.evaluate(_stock(), portfolio={'max_correlation': 0.9})
    assert r['final_decision'] == 'NO_NEW_RISK'


def test_illiquid_option_forces_action():
    r = ds.evaluate(_stock(), option={'quality': 80, 'spread': 20, 'oi': 50, 'iv': 40})
    assert r['vehicle'] == 'ACTION'


def test_liquid_option_offensive_allows_option():
    r = ds.evaluate(_stock(), option={'quality': 75, 'spread': 3, 'oi': 5000,
                                      'iv': 45, 'iv_rank': 40})
    assert r['vehicle'] == 'OPTION'


def test_expensive_iv_forces_action():
    r = ds.evaluate(_stock(), option={'quality': 75, 'spread': 3, 'oi': 5000,
                                      'iv': 95, 'iv_rank': 85})
    assert r['vehicle'] == 'ACTION'


def test_avoid_stays_avoid():
    r = ds.evaluate(_stock(verdict='AVOID', score=30))
    assert r['final_decision'] == 'AVOID'


def test_conviction_confidence_bounded():
    for over in [{}, {'score': 0}, {'score': 100}, {'confidence': 0}]:
        r = ds.evaluate(_stock(**over))
        assert 0 <= r['conviction'] <= 100
        assert 0 <= r['confidence'] <= 100


# ─── LE COMITÉ (Ch. IX / XVI / XVIII) ─────────────────────────────────────
def test_committee_present_and_bounded():
    # Toute décision porte la vue du comité, jamais un score anonyme.
    r = ds.evaluate(_stock(), market={'roro': 'RISK-ON', 'spy_regime': 'TREND'})
    com = r['committee']
    assert com['view'] and 20 <= com['confidence'] <= 95
    assert isinstance(com['members'], list) and com['members']
    # chaque membre a une posture explicite
    assert all(m['stance'] in {'Favorable', 'Défavorable', 'Neutre'} for m in com['members'])


def test_contradiction_is_exposed_not_hidden():
    # Prix fort (pos52 haut) mais momentum faible : la tension DOIT être affichée.
    r = ds.evaluate(_stock(pos52=90, rs=30, rsi_div='bear'))
    assert r['committee']['has_contradiction'] is True
    assert any('momentum' in f.lower() or 'tension' in f.lower() for f in r['risk_flags'])


def test_contradiction_lowers_confidence():
    calm = ds.evaluate(_stock(pos52=70, rs=75))
    tense = ds.evaluate(_stock(pos52=90, rs=30, rsi_div='bear'))
    assert tense['committee']['confidence'] <= calm['committee']['confidence']


def test_devils_advocate_surfaces_strongest_objection():
    # Marché RISK-OFF : l'avocat du diable doit porter une objection réelle.
    r = ds.evaluate(_stock(), market={'roro': 'RISK-OFF', 'spy_regime': 'CHOP'})
    assert r['committee']['devils_advocate']


def test_unknowns_channel_always_present():
    # « Ce que nous ne savons pas » (Ch. XVI) est toujours un canal exposé.
    r = ds.evaluate(_stock())
    assert 'unknowns' in r and isinstance(r['unknowns'], list)


def test_score_breakdown_is_traceable():
    # Ch. XVIII : la décision expose la décomposition du score (sous-scores + ajustements).
    r = ds.evaluate(_stock(score=90, base_score=82, phys_adj=5, mtf_adj=3,
                           sub={'technical': 80, 'momentum': 85, 'fundamental': 70, 'risk': 60,
                                'fundamental_is_proxy': True}))
    bd = r['score_breakdown']
    assert bd['base_score'] == 82 and bd['final_score'] == 90
    labels = {s['label']: s['value'] for s in bd['subscores']}
    assert labels['Technique'] == 80 and labels['Momentum'] == 85
    assert any(s['label'] == 'Fondamental' and s['is_proxy'] for s in bd['subscores'])
    deltas = {a['label'][:8]: a['delta'] for a in bd['adjustments']}
    assert deltas['Physique'] == 5 and deltas['Multi-ho'] == 3


def test_tipping_points_say_what_would_upgrade():
    # R:R faible → « Surveiller » ; le seuil de bascule doit citer le minimum
    # stratégie canonique R:R ≥ 2.0 (aligné sur le hard gate ExecutiveEngine).
    r = ds.evaluate(_stock(plan={'entry': 100, 'stop': 96, 'tp1': 103, 'tp2': 105,
                                  'tp3': 108, 'rr_res': 1.1}))
    tp = r['tipping_points']
    assert any('2.0' in t for t in tp)
    # RISK-OFF → mentionne le retour en RISK-ON
    r2 = ds.evaluate(_stock(score=90), market={'roro': 'RISK-OFF', 'spy_regime': 'TREND'})
    assert any('RISK-ON' in t for t in r2['tipping_points'])


def test_no_tipping_points_when_already_top():
    r = ds.evaluate(_stock(), market={'roro': 'RISK-ON', 'spy_regime': 'TREND'})
    if r['final_decision'] == 'STRONG_BUY':
        assert r['tipping_points'] == []
