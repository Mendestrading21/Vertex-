"""tests/test_catalyst_hops.py — SKYLER LOT 28 : by_catalyst + 3 sauts gardés.

(a) La calibration par contexte gagne la découpe `by_catalyst`
    (avec_catalyseur / sans_catalyseur — dérivée du champ `catalyst` déjà figé,
    mêmes règles d'échantillon). DÉCOUPE D'OBSERVATION UNIQUEMENT : la
    sélection du facteur (`calibration_factor_for`) ne la consomme PAS — aucun
    bump de moteur.
(b) La propagation du knowledge graph accepte max_hops=3 avec une GARDE DE
    VOLUME dure (MAX_PATHS) — troncature déterministe et TOUJOURS DITE par la
    route, jamais silencieuse.
"""
import inspect

import pytest

from vertex.engines import decision_memory as DM
from vertex.engines import knowledge_graph as KG


def _mk(i, catalyst='Résultats (J-21)', level='A', ret=5.0, version='vK'):
    d = {'symbol': 'K%03d' % i, 'as_of': str(i), 'decision': 'ACHETER',
         'score': {'total': 30, 'level': level, 'insufficient_blocks': []},
         'level': level, 'contradictions': [], 'unknowns': [],
         'catalyst': catalyst,
         'scenarios': {'available': True, 'bear': {'return_pct': -6.0},
                       'base': {'return_pct': 12.0}, 'bull': {'return_pct': 18.0}}}
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


# ─── (a) Découpe by_catalyst — observation seulement ────────────────────────────

def test_by_catalyst_cells_with_sample_rules():
    rows = [_mk(i, catalyst='Résultats (J-21)', ret=(5.0 if i < 20 else -15.0))
            for i in range(25)]
    rows += [_mk(100 + i, catalyst=None, ret=3.0) for i in range(3)]
    ctx = DM.calibration_by_context(_mem(rows), 'vK')
    avec = ctx['by_catalyst']['avec_catalyseur']
    assert avec['status'] == 'MESURE' and avec['n_measured'] == 25
    assert avec['hit_rate'] == pytest.approx(0.8)
    sans = ctx['by_catalyst']['sans_catalyseur']
    assert sans['status'] == 'INSUFFISANT' and sans['value'] is None


def test_by_catalyst_never_consumed_by_selection():
    """25 mesures AVEC catalyseur mais réparties sur 5 niveaux (5 chacun,
    tous insuffisants) : la sélection tombe sur le GLOBAL — jamais sur la
    cellule catalyseur (découpe d'observation, pas de règle moteur)."""
    levels = ['S_PLUS', 'S', 'A', 'B', 'REFUS_WATCH']
    rows = [_mk(i, level=levels[i % 5]) for i in range(25)]
    mem = _mem(rows)
    f = DM.calibration_factor_for(mem, 'vK', level='A', regime='CHOP')
    assert f['scope'] == 'global'
    # et la signature ne connaît pas de paramètre catalyseur
    assert 'catalyst' not in inspect.signature(DM.calibration_factor_for).parameters


def test_by_catalyst_deterministic():
    rows = [_mk(i) for i in range(25)]
    m = _mem(rows)
    assert DM.calibration_by_context(m, 'vK') == DM.calibration_by_context(m, 'vK')


# ─── (b) Propagation 3 sauts avec garde de volume ───────────────────────────────

def _closes(base, n=60, phase=0):
    out, x = [], float(base)
    for i in range(n):
        x = x * (1 + 0.001 + (0.01 if (i + phase) % 2 else -0.01))
        out.append(round(x, 6))
    return out


def _chain_graph():
    """A—B—C—D en chaîne par co-mouvement pur (secteurs distincts) :
    atteindre D depuis A exige 3 sauts."""
    closes = {'CHA': _closes(100), 'CHB': _closes(50), 'CHC': _closes(80),
              'CHD': _closes(60)}
    # co-mouvement complet entre tous (même profil) — mais on teste la
    # PROFONDEUR : le chemin A→B→C→D n'existe qu'à 3 sauts.
    return KG.build(['CHA', 'CHB', 'CHC', 'CHD'], sector_map={},
                    closes_by_sym=closes, events_by_sym={}, as_of='t')


def test_three_hops_reaches_deeper_paths():
    g = _chain_graph()
    p2 = KG.propagate(g, 'company:CHA', max_hops=2)
    p3 = KG.propagate(g, 'company:CHA', max_hops=3)
    assert len(p3) > len(p2)
    assert any(len(p['path']) == 4 for p in p3)        # chemin à 3 sauts présent
    assert not any(len(p['path']) > 4 for p in p3)     # jamais au-delà de max_hops


def test_volume_guard_hard_limit_and_deterministic():
    """Étoile dense (25 sociétés × 3 catalyseurs partagés) : les chemins à
    3 sauts explosent — la garde tronque à max_paths, ordre déterministe."""
    syms = ['ST%02d' % i for i in range(25)]
    ev = {s: [{'label': 'CAT%d' % k, 'dte': 10, 'source': 's'} for k in range(3)]
          for s in syms}
    g = KG.build(syms, sector_map={s: 'Tech' for s in syms},
                 closes_by_sym={}, events_by_sym=ev, as_of='t')
    full = KG.propagate(g, 'company:ST00', max_hops=3, max_paths=10)
    assert len(full) == 10                             # limite dure respectée
    capped = KG.propagate(g, 'company:ST00', max_hops=3)
    assert len(capped) == KG.MAX_PATHS                 # garde par défaut atteinte
    assert capped == KG.propagate(g, 'company:ST00', max_hops=3)   # déterministe


def test_default_two_hops_unchanged():
    g = _chain_graph()
    default = KG.propagate(g, 'company:CHA')
    explicit = KG.propagate(g, 'company:CHA', max_hops=2)
    assert default == explicit                         # compatibilité lot 11


# ─── Route : hops optionnel, clampé, troncature DITE ────────────────────────────

def test_graph_sym_route_hops_param():
    import terminal
    c = terminal.app.test_client()
    d2 = c.get('/api/skyler/graph/ACN').get_json()
    assert d2['hops'] == 2                             # défaut inchangé
    d3 = c.get('/api/skyler/graph/ACN?hops=3').get_json()
    assert d3['hops'] == 3
    d9 = c.get('/api/skyler/graph/ACN?hops=9').get_json()
    assert d9['hops'] == 3                             # clampé [1, 3]
    dbad = c.get('/api/skyler/graph/ACN?hops=abc').get_json()
    assert dbad['hops'] == 2                           # invalide → défaut
    for d in (d2, d3):
        assert 'truncated' in d                        # troncature toujours dite
        assert isinstance(d['truncated'], bool)
