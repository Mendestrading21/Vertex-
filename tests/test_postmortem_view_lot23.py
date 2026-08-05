"""tests/test_postmortem_view_lot23.py — SKYLER LOT 23 : vue lisible du post-mortem.

`/memory/<decision_id>` rend le post-mortem d'une décision figée en HTML
lisible (shell produit) au lieu du JSON brut : champs clés du record, horizons
mesurés, scénario contenant, classification, MFE/MAE — états honnêtes (non
mesuré = dit). TOUT contenu de la mémoire est ÉCHAPPÉ côté serveur (XSS).
Le lien « détail → » de la carte Mémoire pointe vers la vue ; l'API JSON
reste. Shell modifié → SW v97 → v98. Un index des lots (SKYLER-INDEX.md)
consolide les rapports 10 → 23.
"""
import os

import pytest

from vertex.engines import decision_memory as DM


def _frozen(sym='VMX'):
    d = {'symbol': sym, 'as_of': 't', 'decision': 'ACHETER',
         'score': {'total': 30, 'level': 'A', 'insufficient_blocks': []},
         'level': 'A', 'contradictions': [], 'unknowns': ['fundamentals'],
         'main_reason': 'Score Skyler 30/40', 'catalyst': 'Résultats (J-21)',
         'invalidation': 94.0,
         'scenarios': {'available': True, 'bear': {'return_pct': -6.0},
                       'base': {'return_pct': 12.0}, 'bull': {'return_pct': 18.0}}}
    return DM.freeze(decision=d, packet={'schema_version': 1, 'engine_version': 'vV'},
                     price=100.0, closes=None, portfolio_ctx=None, now=0,
                     session_date='2026-08-01')


def _outcome(r, ret=14.0):
    return {'decision_id': r['decision_id'], 'engine_version': 'vV',
            'symbol': r['symbol'], 'sessions_observed': 20,
            'horizons': {'H20': {'status': 'MESURE', 'sessions': 20,
                                 'return_pct': ret, 'basis': 't'}},
            'mfe_pct': 16.0, 'mae_pct': -1.0}


def _seed(tmp_path, monkeypatch, with_outcome=True, sym='VMX'):
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    r = _frozen(sym=sym)
    mem = DM.append_decision(DM.empty_memory(), r)
    if with_outcome:
        mem = DM.append_outcome(mem, _outcome(r))
    persist.save_json(DM.MEMORY_FILE, mem)
    return r


# ─── Vue lisible ────────────────────────────────────────────────────────────────

def test_view_renders_measured_postmortem(tmp_path, monkeypatch):
    import terminal
    r = _seed(tmp_path, monkeypatch)
    body = terminal.app.test_client().get('/memory/%s' % r['decision_id']).get_data(as_text=True)
    assert 'VMX' in body and 'ACHETER' in body
    assert 'Post-mortem' in body
    assert 'PROBABLE' in body                          # scénario contenant
    assert 'H20' in body and '14' in body              # horizon mesuré + rendement
    assert 'DECISION_CORRECTE' in body
    assert 'vV' in body                                # version du moteur figée


def test_view_honest_when_unmeasured(tmp_path, monkeypatch):
    import terminal
    r = _seed(tmp_path, monkeypatch, with_outcome=False)
    body = terminal.app.test_client().get('/memory/%s' % r['decision_id']).get_data(as_text=True)
    assert 'aucun horizon mesur' in body               # dit, jamais inventé


def test_view_unknown_id_404_readable(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    resp = terminal.app.test_client().get('/memory/zzzzzzzzzzzzzzzz')
    assert resp.status_code == 404
    assert 'inconnue' in resp.get_data(as_text=True)


def test_view_escapes_memory_content(tmp_path, monkeypatch):
    """XSS : un contenu hostile figé en mémoire ne doit JAMAIS sortir brut."""
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    evil = '<script>alert(1)</script>'
    d = {'symbol': 'EVX', 'as_of': 't', 'decision': 'ATTENDRE',
         'score': {'total': 10, 'level': 'REFUS_WATCH', 'insufficient_blocks': []},
         'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': [],
         'main_reason': evil, 'catalyst': evil}
    r = DM.freeze(decision=d, packet={'engine_version': 'vV'}, price=100.0,
                  closes=None, portfolio_ctx=None, now=0)
    persist.save_json(DM.MEMORY_FILE, DM.append_decision(DM.empty_memory(), r))
    body = terminal.app.test_client().get('/memory/%s' % r['decision_id']).get_data(as_text=True)
    assert '<script>alert(1)</script>' not in body
    assert '&lt;script&gt;' in body


# ─── Lien depuis la carte Mémoire + SW ──────────────────────────────────────────

def test_memory_card_links_to_readable_view():
    import terminal
    body = terminal.app.test_client().get('/journal', follow_redirects=True).get_data(as_text=True)
    assert "'/memory/'" in body or '"/memory/"' in body or '/memory/' in body


def test_service_worker_bumped_to_at_least_v98():
    import re
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 98
    assert 'td-shell-v97' not in body


# ─── Index des lots ─────────────────────────────────────────────────────────────

def test_skyler_index_covers_all_lots():
    path = os.path.join(os.path.dirname(__file__), '..',
                        'docs', 'refactor', 'validation', 'SKYLER-INDEX.md')
    assert os.path.exists(path), 'index des lots manquant'
    idx = open(path, encoding='utf-8').read()
    for n in range(10, 24):
        assert 'SKYLER-LOT-%d' % n in idx, 'lot %d absent de l’index' % n
    assert 'GO' in idx
