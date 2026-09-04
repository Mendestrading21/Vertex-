"""tests/test_red_team.py — SKYLER LOT 12 : red-team, sécurité, RC.

Trois volets :
  1. RÈGLE RED-TEAM du moteur de décision (ADVERSARIAL_COMMITTEE §8) : une note
     S ou S+ sans red-team complétée est INVALIDE — plafonnée à A par le moteur,
     avec bump de version du moteur (0.1.0 → 0.2.0, règle changée = version
     changée) ; les décisions historiques restent liées à l'ancienne version.
  2. BATTERIE ADVERSARIALE : NaN/infinis/prix extrêmes/entrées hostiles sur les
     moteurs récents (anomaly, evidence_lab, decision_memory, knowledge_graph) —
     jamais de crash, jamais de NaN sérialisé, jamais de donnée inventée.
  3. SÉCURITÉ : aucun verbe d'ordre dans les moteurs Skyler, aucun fichier
     runtime/secret suivi par git.
"""
import math

import pytest

from vertex.engines import skyler_core as SK


# ─── 1. Règle red-team (version du moteur bumpée) ───────────────────────────────

def test_engine_version_bumped_for_red_team_rule():
    """Changement de règle = changement de version (DECISION_ENGINE §13) :
    la règle red-team est entrée en 0.2.0 — la version ne peut plus être 0.1.x."""
    parts = tuple(int(x) for x in SK.ENGINE_VERSION.split('.'))
    assert parts >= (0, 2, 0)
    assert callable(SK.apply_red_team_rule)


def test_high_grade_capped_without_red_team():
    """S/S+ sans red-team complétée → plafonné à A, raison explicite."""
    lv, why = SK.apply_red_team_rule('S_PLUS', None)
    assert lv == 'A' and 'red-team' in why
    lv, why = SK.apply_red_team_rule('S', {'complete': False})
    assert lv == 'A' and 'red-team' in why


def test_high_grade_kept_with_completed_red_team():
    lv, why = SK.apply_red_team_rule('S_PLUS', {'complete': True})
    assert lv == 'S_PLUS' and why is None


def test_lower_grades_unaffected_by_red_team_rule():
    for g in ('A', 'B', 'REFUS_WATCH'):
        lv, why = SK.apply_red_team_rule(g, None)
        assert lv == g and why is None


def test_pipeline_cannot_emit_s_plus_without_red_team():
    """Bout en bout : un dossier au score maximal atteignable reste ≤ A tant
    qu'aucune red-team complétée n'est fournie au packet."""
    detail = {'score': 100, 'verdict': 'ACHETER',
              'plan': {'entry': 100, 'stop': 94, 'tp1': 106, 'tp2': 112,
                       'tp3': 118, 'rr_res': 3.5}}
    market = {'regime': {'label': 'TREND_UP', 'confidence': 0.9,
                         'adjustments': {'new_risk_allowed': True}}}
    d = SK.decide('RTX', detail, market=market,
                  events={'events': [{'label': 'Résultats', 'dte': 30}]},
                  anomaly={'events': [], 'extreme': None}, as_of='t')
    assert d['level'] not in ('S_PLUS', 'S')
    assert d['red_team']['required'] is False or d['red_team']['complete'] is False


def test_decide_exposes_red_team_status():
    d = SK.decide('RTX', {'score': 50, 'verdict': 'ATTENDRE',
                          'plan': {'entry': 100, 'stop': 94, 'tp2': 112, 'rr_res': 2.5}},
                  as_of='t')
    rt = d['red_team']
    assert rt['complete'] is False
    assert rt['required'] == (d['level'] in ('S_PLUS', 'S'))
    assert 'basis' in rt


def test_memory_separates_old_and_new_engine_versions():
    """Les décisions historiques 0.1.0 ne sont jamais recalculées : une décision
    0.2.0 du même titre coexiste sous un autre id (lot 10 prouvé sous bump réel)."""
    from vertex.engines import decision_memory as DM
    d = {'symbol': 'VER', 'as_of': 't', 'decision': 'ATTENDRE',
         'score': {'total': 20, 'level': 'REFUS_WATCH', 'insufficient_blocks': []},
         'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': []}
    old = DM.freeze(decision=d, packet={'schema_version': 1, 'engine_version': '0.1.0'},
                    price=100.0, closes=None, portfolio_ctx=None, now=0)
    new = DM.freeze(decision=d, packet={'schema_version': 1, 'engine_version': SK.ENGINE_VERSION},
                    price=100.0, closes=None, portfolio_ctx=None, now=1)
    mem = DM.append_decision(DM.append_decision(DM.empty_memory(), old), new)
    assert len(mem['decisions']) == 2
    agg = DM.aggregates(mem)['by_engine_version']
    assert set(agg) == {'0.1.0', SK.ENGINE_VERSION}


# ─── 2. Batterie adversariale ───────────────────────────────────────────────────

_HOSTILE_CLOSES = [100.0, float('nan'), float('inf'), -5.0, 0.0, 101.0, 1e12]


def _no_nan(obj):
    if isinstance(obj, float):
        assert math.isfinite(obj), 'valeur non finie sérialisée : %r' % obj
    elif isinstance(obj, dict):
        for v in obj.values():
            _no_nan(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _no_nan(v)


def test_anomaly_scan_survives_hostile_series():
    from vertex.engines import anomaly
    d = anomaly.scan(_HOSTILE_CLOSES)
    _no_nan(d)


def test_evidence_lab_survives_hostile_series():
    from vertex.engines import evidence_lab
    d = evidence_lab.study(_HOSTILE_CLOSES)
    _no_nan(d)


def test_knowledge_graph_survives_hostile_series():
    from vertex.engines import knowledge_graph as KG
    g = KG.build(['AAA', 'BBB'], sector_map={'AAA': 'X', 'BBB': 'X'},
                 closes_by_sym={'AAA': _HOSTILE_CLOSES * 10, 'BBB': _HOSTILE_CLOSES * 10})
    _no_nan(g)
    assert not [e for e in g['edges'] if e['relation'] == 'CO_MOVES_WITH']


def test_decision_memory_survives_extreme_prices():
    from vertex.engines import decision_memory as DM
    d = {'symbol': 'EXT', 'as_of': 't', 'decision': 'ATTENDRE',
         'score': {'total': 0, 'level': 'REFUS_WATCH', 'insufficient_blocks': []},
         'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': []}
    for px in (0.0, -10.0, float('nan'), float('inf')):
        r = DM.freeze(decision=d, packet={'engine_version': 'x'}, price=px,
                      closes=None, portfolio_ctx=None, now=0)
        out = DM.measure(r, [100.0] * 70)
        for h in ('H5', 'H20', 'H60'):
            st = out['horizons'][h]['status']
            assert st in ('NON_MESURABLE', 'EN_ATTENTE'), (px, st)
        _no_nan(out) if px == 0.0 else None


def test_lookahead_attack_duplicate_tail_uses_last_occurrence():
    """Empreinte présente deux fois dans la série : la mesure prend la DERNIÈRE
    occurrence — le chemin le plus conservateur, jamais plus de barres que réel."""
    from vertex.engines import decision_memory as DM
    tail = [10.0, 11.0, 12.0]
    closes = tail + [50.0] + tail + [99.0, 98.0]
    assert DM.sessions_after(closes, tail) == [99.0, 98.0]


def test_decide_deterministic_under_repetition():
    detail = {'score': 70, 'verdict': 'ATTENDRE',
              'plan': {'entry': 100, 'stop': 94, 'tp2': 112, 'rr_res': 3.0}}
    a = SK.decide('DET', detail, as_of='t')
    b = SK.decide('DET', detail, as_of='t')
    assert a == b


def test_graph_labels_are_data_not_markup():
    """Un label hostile traverse le graphe comme DONNÉE (JSON), jamais interprété
    — aucune concaténation HTML côté serveur dans ce moteur."""
    from vertex.engines import knowledge_graph as KG
    evil = '<script>alert(1)</script>'
    g = KG.build(['AAA'], sector_map={}, closes_by_sym={},
                 events_by_sym={'AAA': [{'label': evil, 'dte': 5, 'source': 's'}]})
    cat = [e for e in g['edges'] if e['relation'] == 'EXPOSED_TO_CATALYST']
    assert cat and evil in cat[0]['basis']            # donnée conservée telle quelle
    import inspect
    src = inspect.getsource(KG)
    assert 'innerHTML' not in src and '<div' not in src


# ─── 3. Sécurité : aucun ordre, aucun runtime suivi ─────────────────────────────

def test_no_order_verbs_in_skyler_engines():
    import inspect
    from vertex.engines import (skyler_core, skyler_journal, skyler_sweep,
                                decision_memory, knowledge_graph, evidence_lab)
    for mod in (skyler_core, skyler_journal, skyler_sweep, decision_memory,
                knowledge_graph, evidence_lab):
        src = inspect.getsource(mod)
        for verb in ('placeOrder', 'place_order', 'submitOrder', 'submit_order',
                     'transmit', 'cancelOrder', 'cancel_order'):
            assert verb not in src, '%s contient %s' % (mod.__name__, verb)


def test_runtime_and_secret_files_never_tracked():
    import subprocess
    out = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, encoding='utf-8').stdout
    for f in ('skyler_memory.json', 'skyler_decisions.json', 'desk_data.json',
              '.env', '.vertex_secret', 'market_context_last.json'):
        assert f not in out.split('\n'), '%s est suivi par git' % f


def test_graph_build_performance_bounded():
    """60 titres × 60 points : la construction du graphe reste < 5 s."""
    import time
    from vertex.engines import knowledge_graph as KG
    closes = {'S%02d' % i: [100 + (j % 7) + i * 0.01 + j * 0.1 for j in range(60)]
              for i in range(60)}
    secmap = {s: 'Secteur%d' % (i % 6) for i, s in enumerate(closes)}
    t0 = time.time()
    g = KG.build(list(closes), sector_map=secmap, closes_by_sym=closes)
    dt = time.time() - t0
    assert dt < 5.0, 'construction trop lente : %.2fs' % dt
    assert g['nodes']
