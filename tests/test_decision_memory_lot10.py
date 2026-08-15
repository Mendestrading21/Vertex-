"""tests/test_decision_memory_lot10.py — SKYLER LOT 10 : mémoire décisionnelle.

La mémoire institutionnelle fige chaque décision canonique (version du moteur,
données au moment de la décision, thèse, scénarios, portefeuille), mesure les
résultats UNIQUEMENT aux horizons déclarés (5/20/60 séances, catalyseur, thèse,
échéance option), classe les erreurs par une taxonomie déterministe et détecte
les biais récurrents — sans jamais réécrire une décision historique, sans
donnée future en entrée, sans recalcul silencieux entre versions de moteur et
sans modification automatique des poids ou de la Constitution.
"""
import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import skyler_core as SK


def _decision(sym='TST', decision='ACHETER', as_of='10:00:00', total=30,
              level='A', capped=None, scen=True, insufficient=None):
    scenarios = ({'available': True,
                  'bear': {'name': 'pessimiste', 'target': 94.0, 'return_pct': -6.0,
                           'trigger': 'cassure du stop technique', 'invalidation': 94.0,
                           'probability': None},
                  'base': {'name': 'probable', 'target': 112.0, 'return_pct': 12.0,
                           'trigger': 'poursuite vers TP2', 'invalidation': 94.0,
                           'probability': None},
                  'bull': {'name': 'exceptionnel', 'target': 118.0, 'return_pct': 18.0,
                           'trigger': 'extension', 'invalidation': 94.0,
                           'probability': None},
                  'model': {'type': 'plan_levels_deterministic', 'calibrated': False}}
                 if scen else
                 {'available': False, 'reason': 'plan moteur incomplet'})
    return {'symbol': sym, 'generator': 'deterministic', 'as_of': as_of,
            'decision': decision, 'capped_by_gate': capped, 'sizing': None,
            'score': {'total': total, 'max': 40, 'blocks': {}, 'level': level,
                      'insufficient_blocks': insufficient or []},
            'level': level, 'gates': [], 'scenarios': scenarios,
            'invalidation': 94.0, 'max_risk_pct': 6.0,
            'catalyst': 'Résultats (J-21)', 'main_reason': 'Score Skyler %d/40' % total,
            'strongest_objection': 'Probabilités non calibrées.',
            'unknowns': ['fundamentals'], 'contradictions': [],
            'audit_trail': []}


def _packet(sym='TST', as_of='10:00:00'):
    return {'schema_version': SK.SCHEMA_VERSION, 'engine_version': SK.ENGINE_VERSION,
            'profile_version': 2, 'symbol': sym, 'generated_as_of': as_of,
            'demo': True, 'contexts': {}, 'contradictions': [], 'unknowns': [],
            'audit_trail': []}


def _freeze(**kw):
    args = dict(decision=_decision(), packet=_packet(), price=100.0,
                closes=[95.0, 96.0, 97.0, 98.0, 99.0, 99.5, 99.8, 100.0],
                portfolio_ctx=None, now=1000)
    args.update(kw)
    return DM.freeze(**args)


# ─── Gel : tous les champs du ledger, versions explicites ───────────────────────

def test_freeze_records_all_mandated_fields():
    r = _freeze()
    # identité et versions (séparation par version de moteur)
    assert r['decision_id']
    assert r['engine_version'] == SK.ENGINE_VERSION
    assert r['packet_schema_version'] == SK.SCHEMA_VERSION
    # données et fraîcheur au moment de la décision
    assert r['as_of'] == '10:00:00' and r['recorded_at'] == 1000
    assert r['price_at_decision'] == 100.0
    assert r['demo'] is True
    # score, niveau, décision, état opérationnel
    assert r['score_total'] == 30 and r['level'] == 'A'
    assert r['decision'] == 'ACHETER'
    assert 'operational_state' in r
    # thèse, catalyseur, déclencheur, invalidation
    assert r['thesis'] and r['catalyst'] == 'Résultats (J-21)'
    assert r['trigger'] == 'poursuite vers TP2'
    assert r['invalidation'] == 94.0
    # scénarios avec probabilités honnêtes (None) et EV honnête (None)
    assert r['scenarios']['available'] is True
    assert r['scenarios']['bear']['probability'] is None
    assert r['expected_value'] is None and 'aucune probabilit' in r['ev_note']
    # confiance honnête, objection, opinion minoritaire, inconnues, portefeuille
    assert r['confidence'] is None and r['confidence_factors'] is None
    assert r['strongest_objection']
    assert 'minority_opinion' in r
    assert r['unknowns'] == ['fundamentals']
    assert r['portfolio']['available'] is False


def test_freeze_decision_id_deterministic_and_version_scoped():
    a = _freeze()
    b = _freeze()
    assert a['decision_id'] == b['decision_id']       # même entrée → même id
    # une autre version de moteur produit un AUTRE id : jamais de recalcul
    # silencieux d'une décision historique sous une nouvelle version
    p2 = _packet()
    p2['engine_version'] = '9.9.9'
    c = _freeze(packet=p2)
    assert c['decision_id'] != a['decision_id']
    assert c['engine_version'] == '9.9.9'


def test_freeze_never_invents_missing_data():
    d = _decision(scen=False)
    d['catalyst'] = None
    r = _freeze(decision=d, price=None, closes=None)
    assert r['price_at_decision'] is None             # absent ≠ inventé
    assert r['scenarios']['available'] is False
    assert r['trigger'] is None
    assert r['catalyst'] is None
    assert r['tail_at_decision'] is None


def test_freeze_portfolio_snapshot_frozen_at_decision():
    pctx = {'available': True, 'n_positions': 3, 'total_value': 30000.0,
            'hhi': 0.34, 'top_symbol': 'AAA', 'top_weight_pct': 40.0}
    r = _freeze(portfolio_ctx=pctx)
    assert r['portfolio']['n_positions'] == 3
    assert r['portfolio']['top_weight_pct'] == 40.0


# ─── Mémoire : append-only, immuable, séparée par version ───────────────────────

def test_append_decision_is_append_only_and_deduped():
    mem = DM.empty_memory()
    r = _freeze()
    mem2 = DM.append_decision(mem, r)
    assert len(mem2['decisions']) == 1
    assert mem['decisions'] == []                     # pure : l'entrée n'est pas mutée
    mem3 = DM.append_decision(mem2, r)                # même id → pas de doublon
    assert len(mem3['decisions']) == 1


def test_append_decision_never_rewrites_history():
    """Un record portant un decision_id existant mais un contenu différent est
    REFUSÉ : la décision historique originale reste intacte."""
    mem = DM.append_decision(DM.empty_memory(), _freeze())
    tampered = dict(_freeze())
    tampered['decision'] = 'REFUSER'                  # falsification, même id
    mem2 = DM.append_decision(mem, tampered)
    assert len(mem2['decisions']) == 1
    assert mem2['decisions'][0]['decision'] == 'ACHETER'


def test_append_decision_keeps_both_engine_versions():
    mem = DM.append_decision(DM.empty_memory(), _freeze())
    p2 = _packet()
    p2['engine_version'] = '9.9.9'
    mem = DM.append_decision(mem, _freeze(packet=p2))
    versions = {r['engine_version'] for r in mem['decisions']}
    assert versions == {SK.ENGINE_VERSION, '9.9.9'}


def test_memory_bounded():
    mem = DM.empty_memory()
    for i in range(DM.MAX_DECISIONS + 20):
        d = _decision(sym='S%d' % i, as_of=str(i))
        mem = DM.append_decision(mem, DM.freeze(decision=d, packet=_packet(),
                                                price=100.0, closes=None,
                                                portfolio_ctx=None, now=i))
    assert len(mem['decisions']) == DM.MAX_DECISIONS


# ─── Anti-look-ahead : seules les séances POSTÉRIEURES comptent ─────────────────

def test_sessions_after_excludes_pre_decision_bars():
    closes_at = [95.0, 96.0, 97.0, 98.0]              # série au moment de la décision
    tail = closes_at[-3:]
    grown = closes_at + [101.0, 102.0]                # deux séances nouvelles
    after = DM.sessions_after(grown, tail)
    assert after == [101.0, 102.0]                    # aucune barre pré-décision


def test_sessions_after_unalignable_series_is_honest_none():
    # la fenêtre a roulé au-delà de l'empreinte : mesure impossible, jamais devinée
    assert DM.sessions_after([1.0, 2.0, 3.0], [50.0, 51.0, 52.0]) is None
    assert DM.sessions_after([], [50.0]) is None
    assert DM.sessions_after([50.0], None) is None


def test_measure_refuses_lookahead_by_construction():
    """measure() ne reçoit que les séances postérieures via sessions_after —
    une série identique à celle de la décision produit 0 séance observée."""
    r = _freeze()
    same = [95.0, 96.0, 97.0, 98.0, 99.0, 99.5, 99.8, 100.0]
    after = DM.sessions_after(same, r['tail_at_decision'])
    assert after == []
    out = DM.measure(r, after)
    assert out['sessions_observed'] == 0
    assert out['horizons']['H5']['status'] == 'EN_ATTENTE'


# ─── Résultats par horizon déclaré ──────────────────────────────────────────────

def test_measure_horizons_5_20_60_sessions():
    r = _freeze()
    after = [100.0 + i for i in range(1, 26)]         # 25 séances postérieures
    out = DM.measure(r, after)
    assert out['decision_id'] == r['decision_id']
    assert out['engine_version'] == r['engine_version']
    h5 = out['horizons']['H5']
    assert h5['status'] == 'MESURE' and h5['sessions'] == 5
    assert h5['return_pct'] == pytest.approx(5.0)     # 105/100 − 1
    h20 = out['horizons']['H20']
    assert h20['status'] == 'MESURE'
    assert h20['return_pct'] == pytest.approx(20.0)
    assert out['horizons']['H60']['status'] == 'EN_ATTENTE'   # pas 60 séances
    assert out['horizons']['H60']['return_pct'] is None       # jamais inventé
    # MFE/MAE réels sur la fenêtre observée
    assert out['mfe_pct'] == pytest.approx(25.0)
    assert out['mae_pct'] == pytest.approx(1.0)


def test_measure_catalyst_horizon_labelled_estimate():
    r = _freeze()                                     # catalyseur J-21 → ~15 séances
    out = DM.measure(r, [100.0 + i for i in range(1, 26)])
    hc = out['horizons']['CATALYSEUR']
    assert hc['status'] == 'MESURE'
    assert hc['estimated'] is True                    # conversion jours→séances étiquetée
    assert hc['sessions'] == 15
    assert hc['return_pct'] == pytest.approx(15.0)


def test_measure_thesis_and_option_horizons_honest_na():
    r = _freeze()
    out = DM.measure(r, [101.0] * 10)
    # le moteur 0.1.0 ne déclare ni horizon de thèse ni instrument option :
    # champ présent, statut honnête NON_APPLICABLE avec raison — jamais inventé
    assert out['horizons']['THESE']['status'] == 'NON_APPLICABLE'
    assert out['horizons']['OPTION']['status'] == 'NON_APPLICABLE'


def test_measure_without_price_is_unmeasurable():
    r = _freeze(price=None)
    out = DM.measure(r, [101.0] * 70)
    for h in ('H5', 'H20', 'H60'):
        assert out['horizons'][h]['status'] == 'NON_MESURABLE'
        assert out['horizons'][h]['return_pct'] is None


def test_append_outcome_monotone_never_regresses():
    mem = DM.append_decision(DM.empty_memory(), _freeze())
    r = mem['decisions'][0]
    o5 = DM.measure(r, [101.0] * 6)
    o20 = DM.measure(r, [101.0] * 21)
    mem = DM.append_outcome(mem, o20)
    mem = DM.append_outcome(mem, o5)                  # moins de séances → refusé
    assert len(mem['outcomes']) == 1
    assert mem['outcomes'][0]['sessions_observed'] == 21


# ─── Classification des erreurs (déterministe, base explicite) ──────────────────

def test_classify_correct_decision():
    c = DM.classify_error(_freeze(), 12.0, 'H20')
    assert c['class'] == 'DECISION_CORRECTE' and c['basis']


def test_classify_variance_normale_within_pessimistic():
    c = DM.classify_error(_freeze(), -4.0, 'H20')     # perte dans la fourchette (−6 %)
    assert c['class'] == 'VARIANCE_NORMALE'


def test_classify_scenario_error_beyond_pessimistic_with_gaps():
    r = _freeze(decision=_decision(insufficient=['fundamentals_quality']))
    c = DM.classify_error(r, -15.0, 'H20')
    assert c['class'] == 'ERREUR_DE_DONNEES'          # blocs insuffisants d'abord


def test_classify_model_error_full_data_beyond_pessimistic():
    r = _freeze(decision=_decision(total=30, insufficient=[]))
    c = DM.classify_error(r, -15.0, 'H20')
    assert c['class'] == 'ERREUR_DE_MODELE'           # dossier complet, hors fourchette


def test_classify_scenario_error_when_low_score():
    r = _freeze(decision=_decision(total=25, insufficient=[]))
    c = DM.classify_error(r, -15.0, 'H20')
    assert c['class'] == 'ERREUR_DE_SCENARIO'


def test_classify_timing_error_on_missed_probable_move():
    r = _freeze(decision=_decision(decision='ATTENDRE'))
    c = DM.classify_error(r, 14.0, 'H20')             # ≥ scénario probable (+12 %)
    assert c['class'] == 'ERREUR_DE_TIMING'
    c2 = DM.classify_error(r, 3.0, 'H20')
    assert c2['class'] == 'DECISION_CORRECTE'


def test_classify_unmeasured_is_unclassifiable():
    c = DM.classify_error(_freeze(), None, 'H20')
    assert c['class'] == 'NON_CLASSIFIABLE'


def test_error_taxonomy_complete():
    for k in ('ERREUR_DE_DONNEES', 'ERREUR_DE_MODELE', 'ERREUR_DE_SCENARIO',
              'ERREUR_DE_TIMING', 'ERREUR_INSTRUMENT', 'ERREUR_DE_SIZING',
              'ERREUR_DE_DISCIPLINE', 'VARIANCE_NORMALE'):
        assert k in DM.ERROR_CLASSES


# ─── Biais récurrents : calculable ou honnêtement INSUFFISANT ───────────────────

def test_patterns_cover_ten_behaviors_with_honest_status():
    pats = DM.detect_patterns(DM.empty_memory())
    keys = {p['pattern'] for p in pats}
    assert keys == {'poursuite_du_prix', 'renforcement_perdant', 'sortie_prematuree',
                    'surconfiance', 'frequence_excessive', 'dependance_hypothese_unique',
                    'options_trop_courtes', 'spreads_trop_larges',
                    'catalyseur_mal_evalue', 'risque_portefeuille_ignore'}
    for p in pats:
        assert p['status'] in ('DETECTE', 'ABSENT', 'INSUFFISANT')
        assert p['basis']
    # sans trade réel lié, les biais d'exécution restent honnêtement INSUFFISANT
    by = {p['pattern']: p for p in pats}
    assert by['poursuite_du_prix']['status'] == 'INSUFFISANT'
    assert by['sortie_prematuree']['status'] == 'INSUFFISANT'
    assert by['options_trop_courtes']['status'] == 'INSUFFISANT'
    assert by['spreads_trop_larges']['status'] == 'INSUFFISANT'


def test_pattern_blocked_loser_reinforcement_detected():
    d = _decision(decision='ATTENDRE', capped='LOSER_REINFORCEMENT')
    mem = DM.append_decision(DM.empty_memory(),
                             DM.freeze(decision=d, packet=_packet(), price=100.0,
                                       closes=None, portfolio_ctx=None, now=0))
    by = {p['pattern']: p for p in DM.detect_patterns(mem)}
    assert by['renforcement_perdant']['status'] == 'DETECTE'
    assert 'bloqu' in by['renforcement_perdant']['basis']


def test_pattern_single_hypothesis_dependency():
    d = _decision()
    d['score']['blocks'] = {'technical_timing': {'points': 5, 'max': 6},
                            'catalysts': {'points': 0, 'max': 5},
                            'data_quality': {'points': 0, 'max': 4}}
    mem = DM.append_decision(DM.empty_memory(),
                             DM.freeze(decision=d, packet=_packet(), price=100.0,
                                       closes=None, portfolio_ctx=None, now=0))
    by = {p['pattern']: p for p in DM.detect_patterns(mem)}
    assert by['dependance_hypothese_unique']['status'] == 'DETECTE'


# ─── Agrégats séparés par version ; recommandations jamais auto-appliquées ──────

def test_aggregates_separate_engine_versions():
    mem = DM.append_decision(DM.empty_memory(), _freeze())
    p2 = _packet()
    p2['engine_version'] = '9.9.9'
    mem = DM.append_decision(mem, _freeze(packet=p2))
    agg = DM.aggregates(mem)
    assert set(agg['by_engine_version']) == {SK.ENGINE_VERSION, '9.9.9'}
    for v in agg['by_engine_version'].values():
        assert v['n_decisions'] == 1                  # jamais mélangées


def test_recommendations_require_human_validation_and_change_nothing():
    d = _decision(decision='ATTENDRE', capped='LOSER_REINFORCEMENT')
    mem = DM.append_decision(DM.empty_memory(),
                             DM.freeze(decision=d, packet=_packet(), price=100.0,
                                       closes=None, portfolio_ctx=None, now=0))
    recs = DM.recommendations(DM.detect_patterns(mem), DM.aggregates(mem))
    assert recs                                        # au moins une proposition
    for r in recs:
        assert r['status'] == 'EN_ATTENTE_VALIDATION_HUMAINE'
        assert r['basis']
    # aucune écriture sur la Constitution : le module ne l'importe même pas
    import inspect
    src = inspect.getsource(DM)
    assert 'propose_new_version' not in src and 'save_profile' not in src


# ─── Routes : enregistrement au passage + endpoint mémoire ──────────────────────

def test_skyler_route_freezes_decision_in_memory(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    from vertex.app.state import scan_state
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    scan_state.setdefault('detail', {})['MEMX'] = {
        'price': 100.0, 'score': 70, 'verdict': 'ATTENDRE',
        'closes': [95.0, 96.0, 97.0, 98.0, 100.0],
        'plan': {'entry': 100, 'stop': 94, 'tp1': 106, 'tp2': 112, 'tp3': 118, 'rr_res': 3.0}}
    try:
        c = terminal.app.test_client()
        assert c.get('/api/skyler/MEMX').status_code == 200
        mem = persist.load_json(DM.MEMORY_FILE, None)
        assert mem and any(r['symbol'] == 'MEMX' for r in mem['decisions'])
        r = [x for x in mem['decisions'] if x['symbol'] == 'MEMX'][0]
        assert r['engine_version'] == SK.ENGINE_VERSION
        assert r['thesis'] and r['decision_id']
        # l'endpoint mémoire répond avec agrégats par version et patterns
        d = c.get('/api/skyler/memory').get_json()
        assert d['generator'] == 'deterministic'
        assert d['n_decisions'] >= 1
        assert SK.ENGINE_VERSION in d['aggregates']['by_engine_version']
        assert {p['pattern'] for p in d['patterns']} >= {'surconfiance'}
        assert d['note']
    finally:
        scan_state['detail'].pop('MEMX', None)


def test_memory_endpoint_empty_is_honest(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    d = terminal.app.test_client().get('/api/skyler/memory').get_json()
    assert d['n_decisions'] == 0
    assert d['aggregates']['by_engine_version'] == {}
    assert all(p['status'] in ('ABSENT', 'INSUFFISANT') for p in d['patterns'])


def test_memory_file_gitignored():
    import os
    gi = open(os.path.join(os.path.dirname(__file__), '..', '.gitignore'),
              encoding='utf-8').read()
    assert 'skyler_memory.json' in gi


def test_freeze_options_context_and_swing_horizons_are_explicit():
    packet = _packet()
    packet['contexts'] = {
        'options': {
            'available': True,
            'universe': 'SWING_3_6M',
            'mandate_status': 'IN_MANDATE',
            'best': {
                'dte': 135, 'delta': 0.45, 'iv': 0.35, 'oi': 1200,
                'volume': 100, 'spread_pct': 3.0, 'quote_age_seconds': 60,
                'mandate': {'bounds': {'holding_plan_sessions': [5, 10, 15]}},
            },
        },
    }
    record = _freeze(packet=packet)
    assert record['option']['available'] is True
    assert record['option']['universe'] == 'SWING_3_6M'
    assert record['option']['dte_bucket'] == '135_164'
    assert record['option']['holding_plan_sessions'] == [5, 10, 15]
    outcome = DM.measure(record, [100.0 + i for i in range(1, 16)])
    assert outcome['horizons']['H10']['return_pct'] == pytest.approx(10.0)
    assert outcome['horizons']['H15']['return_pct'] == pytest.approx(15.0)
    assert outcome['horizons']['OPTION']['status'] == 'NON_APPLICABLE'
    assert 'quote de sortie absente' in outcome['horizons']['OPTION']['basis']


def test_option_dte_bucket_is_stable_and_honest_for_missing_values():
    assert DM.option_dte_bucket(90) == '75_104'
    assert DM.option_dte_bucket(135) == '135_164'
    assert DM.option_dte_bucket(210) == '181_210'
    assert DM.option_dte_bucket(None) is None
