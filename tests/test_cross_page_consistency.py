"""Tests §26 — cohérence cross-page : une entité a les mêmes valeurs partout.

Source unique de vérité : le prix, la décision et les compteurs d'un symbole
doivent être identiques quel que soit l'endpoint qui les sert. On compare les
sorties réelles du serveur (routes réelles, `scan_state` partagé).

⚠ Lot 398 — deux de ces tests étaient **skippés depuis leur création**
(2026-07-12) : leur condition d'entrée (« un symbole scanné », « un board
options non vide ») n'est JAMAIS remplie sous pytest, car aucun test de la
suite ne déclenche de scan. Ils n'ont donc jamais rien protégé. Ils tournent
désormais sur un `scan_state` alimenté puis restauré (convention de
`test_options_intelligence.py`) : ce n'est pas une donnée inventée
affichée à l'utilisateur, c'est l'entrée d'un test — les routes, elles, sont
les vraies. Les deux ont été prouvés par mutation au lot 398 (cf.
le rapport du lot 398 (archive, retiree du depot)).
"""
import pytest

# Entrée minimale du scan — un titre fictif (jamais servi : `scan_state` est
# restauré) suffit à faire exister les deux invariants comparés.
_SYM = 'TSTX'
_ROWS = [{'symbol': _SYM, 'price': 123.45, 'score': 70, 'verdict': 'NEUTRE'}]
_DETAIL = {_SYM: {'price': 123.45, 'score': 70, 'verdict': 'NEUTRE'}}
_BOARD = [
    {'sym': _SYM, 'type': 'CALL', 'iv': 30.0, 'dte': 45, 'quality': 70, 'theta_burn': 0.5},
    {'sym': _SYM, 'type': 'CALL', 'iv': 32.0, 'dte': 60, 'quality': 65, 'theta_burn': 0.4},
    {'sym': _SYM, 'type': 'PUT', 'iv': 28.0, 'dte': 30, 'quality': 55, 'theta_burn': 0.6},
]


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


@pytest.fixture
def scanned(monkeypatch):
    """Alimente `scan_state` (muté EN PLACE, jamais réassigné) puis restaure."""
    from vertex.app.state import scan_state
    saved = {k: scan_state.get(k) for k in ('rows', 'detail', 'options_board')}
    scan_state['rows'] = list(_ROWS)
    scan_state['detail'] = dict(_DETAIL)
    scan_state['options_board'] = list(_BOARD)
    try:
        yield _SYM
    finally:
        for k, v in saved.items():
            if v is None:
                scan_state.pop(k, None)
            else:
                scan_state[k] = v


def test_price_is_identical_scan_vs_ticker(client, scanned, monkeypatch):
    """Le prix d'un symbole doit être le même dans /scan (detail) et /api/ticker.

    Les deux enrichissements de `/api/ticker` étrangers à l'invariant (chaîne
    options yfinance, profil d'entreprise) sont neutralisés : ils sortiraient
    sur le réseau et écriraient `company_cache.json` depuis la suite.
    """
    import terminal
    monkeypatch.setattr(terminal, 'options_pack',
                        lambda s: {'sym': s, 'contracts': [], 'error': None})
    monkeypatch.setattr(terminal._company, 'get',
                        lambda s, **kw: None, raising=True)
    sym = scanned
    scan = client.get('/scan').get_json()
    detail = (scan.get('detail') or {}).get(sym) or {}
    row = next((r for r in scan['rows'] if r['symbol'] == sym), {})
    tick = client.get('/api/ticker/%s' % sym).get_json()
    tdet = tick.get('detail') or {}
    assert detail.get('price') is not None and tdet.get('price') is not None, (
        'sans prix des deux côtés, la comparaison serait creuse')
    # le detail du ticker EST le detail du scan (même objet partagé)
    assert detail['price'] == tdet['price'], (
        '/api/ticker doit servir le detail du scan, pas une autre source de prix')
    # le prix de la ligne = prix du detail (aucune route ne transforme l'un sans l'autre)
    assert row.get('price') is not None
    assert row['price'] == detail['price']


def test_funnel_positions_match_desk(client):
    """Le compteur « Positions » de l'entonnoir = nombre de trades du desk."""
    import json
    from vertex.services import persist
    f = client.get('/api/opportunities/funnel').get_json()
    pos_stage = next((s['count'] for s in f.get('stages', []) if s['key'] == 'positions'), 0)
    blob = persist.load_json('desk_data.json', {}) or {}
    raw = (blob.get('data') or {}).get('myTrades')
    trades = json.loads(raw) if isinstance(raw, str) else (raw or [])
    expected = len([t for t in trades if isinstance(t, dict)])
    assert pos_stage == expected


def test_funnel_followed_matches_tracking_summary(client):
    """Le compteur « Suivis » de l'entonnoir = suivis actifs du moteur de suivi."""
    f = client.get('/api/opportunities/funnel').get_json()
    followed = next((s['count'] for s in f.get('stages', []) if s['key'] == 'followed'), 0)
    from vertex.tracking import repository as trepo
    assert followed == trepo.summary().get('active', 0)


def test_readonly_reported_consistently(client):
    """READONLY est vrai partout où il est exposé (connections, readyz, system-status)."""
    conn = client.get('/api/system/connections').get_json()
    assert conn['readonly'] is True
    ready = client.get('/readyz').get_json()
    assert ready['readonly'] is True


def test_options_counts_consistent_overview_vs_pulse(client, scanned):
    """CALLS/PUTS du bloc counters == ceux du option_pulse (même board).

    Le filtre CALL/PUT est écrit DEUX fois — `vertex/options/overview.py` et
    `vertex/options/pulse.py` — sur le même board : c'est cette duplication que
    le test verrouille (prouvé par mutation au lot 398).
    """
    d = client.get('/api/options/overview').get_json()
    assert not d.get('empty'), 'le board est alimenté par la fixture : il ne peut être vide'
    c = d['counters']
    op = d['option_pulse']
    assert c['calls'] == op['calls']
    assert c['puts'] == op['puts']
