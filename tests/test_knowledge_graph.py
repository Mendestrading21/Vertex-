"""tests/test_knowledge_graph.py — SKYLER LOT 11 : Knowledge Graph institutionnel.

Le graphe relie sociétés, secteurs et catalyseurs UNIQUEMENT depuis des sources
réelles tracées (watchlist statique du code, séries canoniques, calendrier,
positions desk). Chaque relation porte sa provenance et son niveau de preuve.
Les relations sans source (fournisseurs, clients, concurrents) ne sont JAMAIS
inventées — elles deviennent des questions de recherche. La propagation
d'impact est explicable arête par arête. Déterministe, lecture seule.
"""
import pytest

from vertex.engines import knowledge_graph as KG


def _closes(base, n=60, drift=0.001, wob=0.01, phase=0):
    out, x = [], float(base)
    for i in range(n):
        x = x * (1 + drift + (wob if (i + phase) % 2 else -wob))
        out.append(round(x, 4))
    return out


def _inputs():
    closes = {'NVDA': _closes(100), 'AMD': _closes(50),          # co-mouvement parfait
              'XOM': _closes(80, drift=-0.001, phase=1)}         # anti-corrélé
    sector_map = {'NVDA': 'Semiconducteurs', 'AMD': 'Semiconducteurs', 'XOM': 'Energie'}
    events_by_sym = {'NVDA': [{'kind': 'earnings', 'label': 'Résultats NVDA',
                               'dte': 12, 'source': 'calendar.earnings'}],
                     'AMD': [{'kind': 'earnings', 'label': 'Résultats AMD',
                              'dte': 14, 'source': 'calendar.earnings'}]}
    positions = [{'symbol': 'NVDA', 'quantity': 10}, {'symbol': 'AMD', 'quantity': 20}]
    return dict(symbols=['NVDA', 'AMD', 'XOM'], sector_map=sector_map,
                closes_by_sym=closes, events_by_sym=events_by_sym,
                positions=positions, as_of='10:00:00', demo=True)


# ─── Construction : provenance obligatoire, versions, déterminisme ──────────────

def test_build_versions_and_shape():
    g = KG.build(**_inputs())
    assert g['schema_version'] == KG.SCHEMA_VERSION
    assert g['engine_version'] == KG.GRAPH_ENGINE_VERSION
    assert g['generator'] == 'deterministic'
    assert g['as_of'] == '10:00:00' and g['demo'] is True
    assert g['nodes'] and g['edges']


def test_every_edge_has_provenance_and_evidence_level():
    g = KG.build(**_inputs())
    for e in g['edges']:
        assert e['source'], 'arête sans source : %r' % e
        assert e['evidence_level'] in ('F1', 'F2', 'F3', 'F4')
        assert e['relation'] in KG.RELATIONS
        assert e['basis']


def test_sector_membership_from_curated_watchlist():
    g = KG.build(**_inputs())
    memb = [e for e in g['edges'] if e['relation'] == 'MEMBER_OF_SECTOR']
    assert {(e['src'], e['dst']) for e in memb} == {
        ('company:NVDA', 'sector:Semiconducteurs'),
        ('company:AMD', 'sector:Semiconducteurs'),
        ('company:XOM', 'sector:Energie')}
    assert all('sectors.py' in e['source'] for e in memb)
    assert all(e['evidence_level'] == 'F1' for e in memb)


def test_comovement_from_canonical_series_is_f2_with_window():
    g = KG.build(**_inputs())
    co = [e for e in g['edges'] if e['relation'] == 'CO_MOVES_WITH']
    pair = {tuple(sorted((e['src'], e['dst']))) for e in co}
    assert ('company:AMD', 'company:NVDA') in pair
    e = co[0]
    assert e['evidence_level'] == 'F2'
    assert e['value'] >= KG.CORR_STRONG
    assert e['window'] >= KG.MIN_POINTS
    assert 'corrélation' in e['basis']


def test_comovement_requires_min_points_honest_limit():
    ins = _inputs()
    ins['closes_by_sym'] = {'NVDA': _closes(100, n=10), 'AMD': _closes(50, n=10)}
    g = KG.build(**ins)
    assert not [e for e in g['edges'] if e['relation'] == 'CO_MOVES_WITH']
    assert any('série' in l or 'points' in l for l in g['limits'])


def test_catalyst_exposure_only_dated_events():
    g = KG.build(**_inputs())
    cat = [e for e in g['edges'] if e['relation'] == 'EXPOSED_TO_CATALYST']
    assert {e['src'] for e in cat} == {'company:NVDA', 'company:AMD'}
    assert all(e['evidence_level'] == 'F1' for e in cat)      # calendrier déclaré
    # XOM sans événement daté : aucune arête inventée
    assert not [e for e in cat if e['src'] == 'company:XOM']


def test_held_positions_edges_from_desk():
    g = KG.build(**_inputs())
    held = [e for e in g['edges'] if e['relation'] == 'HELD_IN_PORTFOLIO']
    assert {e['src'] for e in held} == {'company:NVDA', 'company:AMD'}


def test_no_invented_relation_types():
    """Fournisseurs/clients/concurrents : AUCUNE source réelle branchée —
    ces relations n'existent nulle part dans le graphe, jamais inventées."""
    g = KG.build(**_inputs())
    kinds = {e['relation'] for e in g['edges']}
    for forbidden in ('SUPPLIER_OF', 'CUSTOMER_OF', 'COMPETITOR_OF'):
        assert forbidden not in kinds
        assert forbidden not in KG.RELATIONS


def test_deterministic_same_input_same_graph():
    a, b = KG.build(**_inputs()), KG.build(**_inputs())
    assert a == b


def test_empty_inputs_honest_empty_graph():
    g = KG.build(symbols=[], sector_map={}, closes_by_sym={}, events_by_sym={},
                 positions=None, as_of=None, demo=False)
    assert g['nodes'] == [] and g['edges'] == []
    assert g['hidden_dependencies'] == []
    assert g['research_questions'] == []
    assert g['limits']                                        # limites dites


# ─── Propagation d'impact explicable ────────────────────────────────────────────

def test_propagate_explains_each_hop():
    g = KG.build(**_inputs())
    paths = KG.propagate(g, 'company:NVDA', max_hops=2)
    assert paths
    for p in paths:
        assert p['path'][0] == 'company:NVDA'
        assert len(p['hops']) == len(p['path']) - 1
        for h in p['hops']:
            assert h['relation'] in KG.RELATIONS and h['basis']
    # NVDA → secteur → AMD : chemin sectoriel explicable en 2 sauts
    assert any(p['path'] == ['company:NVDA', 'sector:Semiconducteurs', 'company:AMD']
               for p in paths)


def test_propagate_unknown_node_is_honest_empty():
    g = KG.build(**_inputs())
    assert KG.propagate(g, 'company:ZZZ') == []


# ─── Dépendances cachées : ≥ 2 liens indépendants ───────────────────────────────

def test_hidden_dependency_needs_two_independent_links():
    g = KG.build(**_inputs())
    deps = g['hidden_dependencies']
    assert deps
    d = deps[0]
    assert set(d['symbols']) == {'AMD', 'NVDA'}
    assert len(d['links']) >= 2                               # secteur + co-mouvement
    assert {l['relation'] for l in d['links']} >= {'MEMBER_OF_SECTOR', 'CO_MOVES_WITH'}
    assert d['basis']


def test_no_hidden_dependency_on_single_link():
    ins = _inputs()
    ins['closes_by_sym'] = {}                                 # plus de co-mouvement
    g = KG.build(**ins)
    assert not [d for d in g['hidden_dependencies']
                if set(d['symbols']) == {'AMD', 'NVDA'}]


# ─── Questions de recherche : jamais une relation inventée ──────────────────────

def test_research_questions_for_missing_relations():
    g = KG.build(**_inputs())
    qs = g['research_questions']
    kinds = {q['kind'] for q in qs}
    assert 'value_chain' in kinds                             # fournisseurs/clients/concurrents
    assert all(q['question'] and q['symbol'] for q in qs)
    assert all(q['status'] == 'NON_DOCUMENTE' for q in qs)
    # XOM n'a aucun catalyseur daté : question de recherche, pas d'arête
    assert any(q['symbol'] == 'XOM' and q['kind'] == 'catalyst' for q in qs)


def test_unmapped_symbol_becomes_research_question_not_node_guess():
    ins = _inputs()
    ins['symbols'] = ins['symbols'] + ['ZZZ']                 # hors watchlist
    g = KG.build(**ins)
    assert not [e for e in g['edges']
                if e['src'] == 'company:ZZZ' and e['relation'] == 'MEMBER_OF_SECTOR']
    assert any(q['symbol'] == 'ZZZ' and q['kind'] == 'sector'
               for q in g['research_questions'])


# ─── Routes ─────────────────────────────────────────────────────────────────────

def test_graph_route_serves_real_scan_universe():
    import terminal
    from vertex.app.state import scan_state
    scan_state.setdefault('detail', {})['KGX'] = {
        'price': 100.0, 'series': {'close': _closes(100)}}
    try:
        c = terminal.app.test_client()
        d = c.get('/api/skyler/graph').get_json()
        assert d['generator'] == 'deterministic'
        assert d['engine_version'] == KG.GRAPH_ENGINE_VERSION
        assert 'nodes' in d and 'edges' in d
        assert 'hidden_dependencies' in d and 'research_questions' in d
    finally:
        scan_state['detail'].pop('KGX', None)


def test_graph_symbol_route_propagation():
    import terminal
    from vertex.app.state import scan_state
    scan_state.setdefault('detail', {})['NVDA'] = {
        'price': 100.0, 'series': {'close': _closes(100)}}
    try:
        c = terminal.app.test_client()
        d = c.get('/api/skyler/graph/NVDA').get_json()
        assert d['symbol'] == 'NVDA'
        assert 'paths' in d
        for p in d['paths']:
            for h in p['hops']:
                assert h['basis']                             # explicable arête par arête
    finally:
        scan_state['detail'].pop('NVDA', None)
