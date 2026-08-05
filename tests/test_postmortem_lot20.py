"""tests/test_postmortem_lot20.py — SKYLER LOT 20 : drill-down + post-mortem.

Chaque décision figée devient inspectable : GET /api/skyler/memory/<decision_id>
renvoie le record complet, son résultat mesuré et une revue POST-MORTEM
déterministe (mode Post-Mortem du comité) — décision vs résultat, scénario
ayant CONTENU le résultat, classification par horizon mesuré — uniquement
depuis les données figées, honnête quand rien n'est mesuré. Id inconnu → 404
structuré. La carte Mémoire (Performance) liste les dernières décisions avec
lien post-mortem → shell modifié → SW v96 → v97.
"""
import pytest

from vertex.engines import decision_memory as DM


def _frozen(ret_bear=-6.0, ret_base=12.0, ret_bull=18.0, scen=True,
            decision='ACHETER', sym='PMX'):
    d = {'symbol': sym, 'as_of': 't', 'decision': decision,
         'score': {'total': 30, 'level': 'A', 'insufficient_blocks': []},
         'level': 'A', 'contradictions': [], 'unknowns': [],
         'scenarios': ({'available': True,
                        'bear': {'return_pct': ret_bear},
                        'base': {'return_pct': ret_base},
                        'bull': {'return_pct': ret_bull}}
                       if scen else {'available': False, 'reason': 'plan incomplet'})}
    return DM.freeze(decision=d, packet={'schema_version': 1, 'engine_version': 'vP'},
                     price=100.0, closes=None, portfolio_ctx=None, now=0)


def _outcome(r, ret, horizon='H20'):
    return {'decision_id': r['decision_id'], 'engine_version': 'vP',
            'symbol': r['symbol'], 'sessions_observed': 20,
            'horizons': {horizon: {'status': 'MESURE', 'sessions': 20,
                                   'return_pct': ret, 'basis': 't'}},
            'mfe_pct': ret + 2.0, 'mae_pct': -1.0}


# ─── Post-mortem déterministe ───────────────────────────────────────────────────

def test_postmortem_unmeasured_is_honest():
    pm = DM.post_mortem(_frozen(), None)
    assert pm['available'] is False
    assert 'mesur' in pm['reason']


def test_postmortem_scenario_containment_probable():
    r = _frozen()
    pm = DM.post_mortem(r, _outcome(r, 14.0))
    assert pm['available'] is True
    assert pm['scenario_containing'] == 'PROBABLE'         # 12 ≤ 14 < 18
    assert pm['longest_horizon'] == 'H20'
    assert pm['return_pct'] == pytest.approx(14.0)
    h20 = [h for h in pm['horizons'] if h['horizon'] == 'H20'][0]
    assert h20['classification']['class'] == 'DECISION_CORRECTE'


def test_postmortem_pessimistic_contained_loss():
    r = _frozen()
    pm = DM.post_mortem(r, _outcome(r, -4.0))              # −6 ≤ −4 < 12
    assert pm['scenario_containing'] == 'PESSIMISTE'
    h = pm['horizons'][0]
    assert h['classification']['class'] == 'VARIANCE_NORMALE'


def test_postmortem_out_of_range_low():
    r = _frozen()
    pm = DM.post_mortem(r, _outcome(r, -15.0))
    assert pm['scenario_containing'] == 'HORS_FOURCHETTE_BASSE'
    assert pm['horizons'][0]['classification']['class'].startswith('ERREUR')


def test_postmortem_exceptional_reached():
    r = _frozen()
    pm = DM.post_mortem(r, _outcome(r, 22.0))              # ≥ 18
    assert pm['scenario_containing'] == 'EXCEPTIONNEL_ATTEINT'


def test_postmortem_without_scenarios_honest():
    r = _frozen(scen=False)
    pm = DM.post_mortem(r, _outcome(r, 5.0))
    assert pm['available'] is True
    assert pm['scenario_containing'] is None
    assert 'scénario' in pm['scenario_note'] or 'scenario' in pm['scenario_note']


def test_postmortem_discipline_honestly_unevaluable():
    r = _frozen()
    pm = DM.post_mortem(r, _outcome(r, 14.0))
    assert 'discipline' in pm['discipline_note'].lower()
    assert 'trade' in pm['discipline_note'].lower()        # inobservable sans trades réels


def test_postmortem_includes_mfe_mae_and_summary():
    r = _frozen()
    pm = DM.post_mortem(r, _outcome(r, 14.0))
    assert pm['mfe_pct'] == pytest.approx(16.0)
    assert pm['mae_pct'] == pytest.approx(-1.0)
    assert 'ACHETER' in pm['summary'] and '14' in pm['summary']


def test_postmortem_deterministic():
    r = _frozen()
    assert DM.post_mortem(r, _outcome(r, 14.0)) == DM.post_mortem(r, _outcome(r, 14.0))


# ─── Route drill-down ───────────────────────────────────────────────────────────

def test_memory_detail_route(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    r = _frozen()
    mem = DM.append_outcome(DM.append_decision(DM.empty_memory(), r), _outcome(r, 14.0))
    persist.save_json(DM.MEMORY_FILE, mem)
    c = terminal.app.test_client()
    d = c.get('/api/skyler/memory/%s' % r['decision_id']).get_json()
    assert d['record']['decision_id'] == r['decision_id']
    assert d['outcome']['sessions_observed'] == 20
    assert d['post_mortem']['scenario_containing'] == 'PROBABLE'
    assert d['generator'] == 'deterministic'


def test_memory_detail_unknown_id_404(tmp_path, monkeypatch):
    import terminal
    from vertex.services import persist
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    resp = terminal.app.test_client().get('/api/skyler/memory/zzzzzzzzzzzzzzzz')
    assert resp.status_code == 404
    d = resp.get_json()
    assert d['ok'] is False and d['error'] == 'decision_inconnue'


# ─── Surfaçage : liens post-mortem dans la carte Mémoire, SW v97 ────────────────

def test_memory_card_has_postmortem_links():
    import terminal
    body = terminal.app.test_client().get('/journal', follow_redirects=True).get_data(as_text=True)
    assert '/memory/' in body                          # vue lisible (lot 23)
    assert 'Dernières décisions figées' in body or 'Derni&egrave;res d&eacute;cisions' in body


def test_service_worker_bumped_to_at_least_v97():
    import re
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 97
    assert 'td-shell-v96' not in body
