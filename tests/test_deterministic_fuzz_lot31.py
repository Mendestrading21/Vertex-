"""tests/test_deterministic_fuzz_lot31.py — SKYLER LOT 31 : fuzz déterministe.

Batterie adversariale à LISTE FIXE (zéro aléatoire — même esprit que le lot
12) sur les chemins livrés récemment : `propagate` (lot 28),
`calibration_factor_for` / `calibration_by_context` (lots 26/28/30),
`freeze` + `catalyst_kind` (lot 30), export souverain (lot 29). Un magasin
runtime est un fichier disque : il peut être corrompu — aucun moteur ne doit
lever sur une entrée dégénérée ; il refuse HONNÊTEMENT (liste vide, cellule
absente, bucket `inconnu`, facteur 0,50), et reste déterministe.
"""
import json

import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import knowledge_graph as KG


def _graph():
    return {'nodes': [{'id': 'AAA'}, {'id': 'BBB'}, {'id': 'CCC'}],
            'edges': [{'src': 'AAA', 'dst': 'BBB', 'relation': 'MEMBER_OF_SECTOR',
                       'basis': 'b', 'evidence_level': 'F1'},
                      {'src': 'BBB', 'dst': 'CCC', 'relation': 'CO_MOVES_WITH',
                       'basis': 'b', 'evidence_level': 'F2'}]}


# ─── propagate : entrées dégénérées → refus honnête, jamais d'exception ─────────

DEGENERATE_NODES = (None, '', 123, 12.5, True, ['AAA'], {'id': 'AAA'}, ('AAA',))


def test_propagate_degenerate_node_ids_refused_honestly():
    g = _graph()
    for node in DEGENERATE_NODES:
        assert KG.propagate(g, node) == []


def test_propagate_degenerate_graphs_refused_honestly():
    for g in (None, {}, {'nodes': None, 'edges': None},
              {'nodes': [], 'edges': []}):
        assert KG.propagate(g, 'AAA') == []


DEGENERATE_HOPS = (None, 'abc', '', -1, 0, 0.0, {}, [])


def test_propagate_degenerate_max_hops_yield_no_paths():
    """max_hops invalide ou < 1 = AUCUNE propagation (0 saut ne produit pas
    de chemin) — jamais d'exception, jamais un défaut silencieusement deviné."""
    g = _graph()
    for mh in DEGENERATE_HOPS:
        assert KG.propagate(g, 'AAA', max_hops=mh) == []


def test_propagate_huge_max_hops_terminates_and_is_bounded():
    g = _graph()
    huge = KG.propagate(g, 'AAA', max_hops=99)
    assert huge == KG.propagate(g, 'AAA', max_hops=3)   # chemins simples bornés
    assert len(huge) <= KG.MAX_PATHS


DEGENERATE_MAX_PATHS = ('abc', '', {}, [], None, -5, 0)


def test_propagate_degenerate_max_paths_keep_guard():
    """max_paths inexploitable → garde par défaut MAX_PATHS ; ≤ 0 → garde
    minimale 1. Jamais d'exception, garde JAMAIS désactivée."""
    g = _graph()
    for mp in DEGENERATE_MAX_PATHS:
        out = KG.propagate(g, 'AAA', max_paths=mp)
        assert isinstance(out, list) and 1 <= len(out) <= KG.MAX_PATHS


def test_propagate_deterministic_under_fuzz():
    g = _graph()
    assert KG.propagate(g, 'AAA', max_hops=2) == KG.propagate(g, 'AAA', max_hops=2)


# ─── Calibration : magasin corrompu → 0,50 honnête, jamais d'exception ──────────

CORRUPTED_MEMORIES = (
    None,
    {},
    {'decisions': 'corrompu', 'outcomes': []},
    {'decisions': [42, 'x', None, []], 'outcomes': 'corrompu'},
    {'decisions': [{'engine_version': 'vF'}], 'outcomes': [{'decision_id': 'z'}]},
)


def test_calibration_factor_survives_corrupted_stores():
    for mem in CORRUPTED_MEMORIES:
        f = DM.calibration_factor(mem, 'vF')
        assert f['value'] == 0.5 and f['n_measured'] == 0


DEGENERATE_CONTEXT_VALUES = ({'x': 1}, ['A'], 123, 0.5, True, '')


def test_calibration_factor_for_degenerate_level_regime_fall_back_global():
    for bad in DEGENERATE_CONTEXT_VALUES:
        f = DM.calibration_factor_for(DM.empty_memory(), 'vF',
                                      level=bad, regime=bad)
        assert f['scope'] == 'global' and f['value'] == 0.5


def _measured_record(i, **fields):
    """Record MESURÉ minimal injecté directement (simule un magasin disque
    modifié hors moteur) — champs dégénérés passés par **fields."""
    r = {'decision_id': 'fz%03d' % i, 'symbol': 'FZ%03d' % i,
         'engine_version': 'vF', 'decision': 'ACHETER', 'level': 'A',
         'regime': 'TREND_UP', 'catalyst': 'X (J-3)', 'catalyst_kind': 'macro',
         'scenarios': {'available': True, 'bear': {'return_pct': -6.0},
                       'base': {'return_pct': 12.0}, 'bull': {'return_pct': 18.0}}}
    r.update(fields)
    o = {'decision_id': r['decision_id'], 'engine_version': 'vF',
         'symbol': r['symbol'], 'sessions_observed': 20,
         'horizons': {'H20': {'status': 'MESURE', 'sessions': 20,
                              'return_pct': 5.0, 'basis': 't'}},
         'mfe_pct': None, 'mae_pct': None}
    return r, o


DEGENERATE_KINDS = ({'k': 1}, ['earnings'], 123, 0.5, True, '')


def test_by_catalyst_type_degenerate_kinds_bucket_inconnu():
    """kind non-chaîne (magasin corrompu) → bucket `inconnu` — jamais
    d'exception (un dict non hachable ne doit pas tuer la calibration)."""
    mem = DM.empty_memory()
    for i, kind in enumerate(DEGENERATE_KINDS):
        r, o = _measured_record(i, catalyst_kind=kind)
        mem = DM.append_outcome(DM.append_decision(mem, r), o)
    ctx = DM.calibration_by_context(mem, 'vF')
    assert list(ctx['by_catalyst_type']) == ['inconnu']
    assert ctx['by_catalyst_type']['inconnu']['n_measured'] == len(DEGENERATE_KINDS)


def test_context_cells_degenerate_level_regime_never_cells():
    """niveau/décision/régime non-chaîne (magasin corrompu) → pas de cellule
    (comme un régime inconnu) — jamais d'exception."""
    mem = DM.empty_memory()
    for i, bad in enumerate(DEGENERATE_CONTEXT_VALUES):
        r, o = _measured_record(i, level=bad, decision=bad, regime=bad)
        mem = DM.append_outcome(DM.append_decision(mem, r), o)
    ctx = DM.calibration_by_context(mem, 'vF')
    assert ctx['by_level'] == {} and ctx['by_decision'] == {}
    assert ctx['by_regime'] == {}
    assert ctx['n_measured_total'] == len(DEGENERATE_CONTEXT_VALUES)


# ─── freeze + catalyst_kind : jamais d'exception, aval toujours vivant ──────────

def test_freeze_degenerate_kinds_do_not_crash_downstream():
    for i, kind in enumerate(DEGENERATE_KINDS):
        d = {'symbol': 'FR%d' % i, 'as_of': 't', 'decision': 'ATTENDRE',
             'score': {'total': 20, 'level': 'REFUS_WATCH',
                       'insufficient_blocks': []},
             'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': [],
             'catalyst': 'X (J-3)', 'catalyst_kind': kind}
        r = DM.freeze(decision=d, packet={'schema_version': 1,
                                          'engine_version': 'vF'},
                      price=100.0, closes=None, portfolio_ctx=None, now=i)
        assert r['catalyst_kind'] == kind          # figé tel quel, jamais inventé
        mem = DM.append_decision(DM.empty_memory(), r)
        assert DM.calibration_by_context(mem, 'vF')['n_measured_total'] == 0


# ─── Export souverain : magasins corrompus servis SANS exception ────────────────

CORRUPTED_STORES = (
    ('skyler_memory.json', '"corrompu"'),
    ('skyler_sessions.json', '[1, 2, 3]'),
    ('skyler_journal.json', '{"a": 1}'),
)


def test_export_survives_corrupted_stores(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    for name, raw in CORRUPTED_STORES:
        (tmp_path / name).write_text(raw, encoding='utf-8')
    resp = terminal.app.test_client().get('/api/skyler/memory/export')
    assert resp.status_code == 200
    assert json.loads(resp.get_data(as_text=True))         # JSON toujours valide
