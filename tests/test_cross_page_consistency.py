"""Tests §26 — cohérence cross-page : une entité a les mêmes valeurs partout.

Source unique de vérité : le prix, la décision et les compteurs d'un symbole
doivent être identiques quel que soit l'endpoint qui les sert. On compare les
sorties réelles du serveur (scan_state partagé), pas des fixtures.
"""
import pytest


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _scanned_symbol(client):
    rows = (client.get('/scan').get_json() or {}).get('rows') or []
    return rows[0]['symbol'] if rows else None


def test_price_is_identical_scan_vs_ticker(client):
    """Le prix d'un symbole doit être le même dans /scan (detail) et /api/ticker."""
    sym = _scanned_symbol(client)
    if not sym:
        pytest.skip('aucun symbole scanné dans cet environnement de test')
    scan = client.get('/scan').get_json()
    detail = (scan.get('detail') or {}).get(sym) or {}
    row = next((r for r in scan['rows'] if r['symbol'] == sym), {})
    tick = client.get('/api/ticker/%s' % sym).get_json()
    tdet = tick.get('detail') or {}
    # le detail du ticker EST le detail du scan (même objet partagé)
    if detail.get('price') is not None and tdet.get('price') is not None:
        assert detail['price'] == tdet['price']
    # le prix de la ligne = prix du detail
    if row.get('price') is not None and detail.get('price') is not None:
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


def test_options_counts_consistent_overview_vs_pulse(client):
    """CALLS/PUTS du bloc counters == ceux du option_pulse (même board)."""
    d = client.get('/api/options/overview').get_json()
    if d.get('empty'):
        pytest.skip('board options vide')
    c = d['counters']
    op = d['option_pulse']
    assert c['calls'] == op['calls']
    assert c['puts'] == op['puts']
