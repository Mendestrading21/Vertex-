"""
LOT 173 — Caractérisation HTTP du moteur de SUIVI (§33)
(`vertex/app/routes/tracking_api.py` — le cycle de vie /api/tracking/<id>
(GET/PATCH), /performance, /stop, /restart, /history était à ZÉRO test ;
seuls la liste et le POST de création étaient couverts). Le repository
est déterministe (identifiants/horodatages fournis par l'appelant) ; la
couche HTTP génère les identifiants et lit les prix RÉELS du scan. Ces
tests figent le cycle de vie complet et son honnêteté par HTTP.
"""
import pytest

import terminal
from vertex.app.state import scan_state
from vertex.services import persist


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    yield terminal.app.test_client()
    scan_state.setdefault('detail', {}).pop('TSTQ', None)


def _create_stock(client, price=100.0):
    scan_state.setdefault('detail', {})['TSTQ'] = {'price': price}
    return client.post('/api/tracking',
                       json={'symbol': 'TSTQ', 'decision': 'BUY', 'score': 80}).get_json()


# ── Refus explicites ─────────────────────────────────────────────────────────

def test_introuvable_404_sur_les_5_sous_routes(client):
    assert client.get('/api/tracking/trk_x').status_code == 404
    assert client.get('/api/tracking/trk_x/performance').status_code == 404
    assert client.post('/api/tracking/trk_x/stop').status_code == 404
    assert client.post('/api/tracking/trk_x/restart').status_code == 404
    assert client.get('/api/tracking/trk_x/history').status_code == 404
    assert client.get('/api/tracking/trk_x').get_json() == {'error': 'suivi introuvable'}


def test_creation_sans_symbole_400(client):
    r = client.post('/api/tracking', json={})
    assert r.status_code == 400
    assert r.get_json() == {'error': 'symbol requis'}


# ── Création : référence honnête, jamais un prix inventé ─────────────────────

def test_action_inconnue_du_scan_data_required(client):
    r = client.post('/api/tracking', json={'symbol': 'zzzq'})
    assert r.status_code == 201                     # le suivi existe quand même
    t = r.get_json()
    assert t['symbol'] == 'ZZZQ'                    # normalisé majuscules
    assert t['status'] == 'DATA_REQUIRED'           # pas de prix → dit
    assert t['reference_price'] is None             # JAMAIS un prix inventé


def test_action_au_prix_reel_du_scan(client):
    t = _create_stock(client)
    assert t['status'] == 'ACTIVE'
    assert t['reference_price'] == 100.0
    assert t['reference_price_type'] == 'LAST'
    assert t['reference_price_source'] == 'scan'    # provenance tracée
    assert t['benchmark'] == 'SPY'
    assert t['is_hypothetical'] is True             # jamais une position réelle


def test_option_reference_mid_depuis_le_body(client):
    # Pour une option, la quote vient du body (le scan ne cote pas les contrats).
    r = client.post('/api/tracking', json={'entity_type': 'OPTION', 'symbol': 'TSTQ',
                                           'bid': 3.0, 'ask': 3.4})
    t = r.get_json()
    assert t['entity_type'] == 'OPTION'
    assert t['reference_price'] == 3.2              # MID = (3.0 + 3.4) / 2
    assert t['reference_price_type'] == 'MID'


# ── Performance : prix réels, étiquette hypothétique ─────────────────────────

def test_performance_action_au_prix_courant_du_scan(client):
    t = _create_stock(client, price=100.0)
    scan_state['detail']['TSTQ'] = {'price': 110.0}
    p = client.get('/api/tracking/%s/performance' % t['tracking_id']).get_json()
    assert p['current_price'] == 110.0
    assert p['return_pct'] == 10.0
    assert p['high_since'] == 110.0 and p['drawdown_from_high_pct'] == 0.0
    assert p['is_hypothetical'] is True
    assert any('HYPOTHÉTIQUE' in l for l in p['limitations'])   # étiquette imposée


def test_performance_option_exige_le_mark_sinon_none(client):
    r = client.post('/api/tracking', json={'entity_type': 'OPTION', 'symbol': 'TSTQ',
                                           'bid': 3.0, 'ask': 3.4})
    tid = r.get_json()['tracking_id']
    avec = client.get('/api/tracking/%s/performance?mark=4.08' % tid).get_json()
    assert avec['current_price'] == 4.08
    assert avec['return_pct'] == 27.5               # (4.08 / 3.2 − 1) × 100
    sans = client.get('/api/tracking/%s/performance' % tid).get_json()
    assert sans['current_price'] is None            # pas de mark → pas de chiffre
    assert sans['return_pct'] is None


# ── Stop : gel du résultat final ─────────────────────────────────────────────

def test_stop_gele_le_resultat_au_prix_du_scan(client):
    t = _create_stock(client, price=100.0)
    scan_state['detail']['TSTQ'] = {'price': 110.0}
    s = client.post('/api/tracking/%s/stop' % t['tracking_id'],
                    json={'reason': 'test'}).get_json()
    assert s['status'] == 'STOPPED' and s['stopped_at']
    f = s['final']
    assert f['final_price'] == 110.0                # prix RÉEL du scan au stop
    assert f['return_pct'] == 10.0
    assert f['mfe_pct'] == 10.0 and f['mae_pct'] == 0.0
    assert f['is_hypothetical'] is True and f['reason'] == 'test'


# ── Restart : nouvel identifiant, l'ancien intact ────────────────────────────

def test_restart_nouvel_id_et_historique_de_l_ancien_conserve(client):
    t = _create_stock(client, price=100.0)
    tid = t['tracking_id']
    scan_state['detail']['TSTQ'] = {'price': 110.0}
    client.post('/api/tracking/%s/stop' % tid, json={})
    r = client.post('/api/tracking/%s/restart' % tid, json={})
    assert r.status_code == 201
    n = r.get_json()
    assert n['tracking_id'] != tid                  # identifiant NEUF
    assert n['status'] == 'ACTIVE'
    assert n['reference_price'] == 110.0            # repart du prix courant
    h = client.get('/api/tracking/%s/history' % tid).get_json()
    assert h['final']['return_pct'] == 10.0         # l'ancien reste gelé
    assert h['stopped_at'] is not None


# ── Invariant produit : la couche HTTP est bien LECTURE SEULE ────────────────

def test_module_tracking_api_sans_verbe_d_ordre():
    import inspect
    from vertex.app.routes import tracking_api
    src = inspect.getsource(tracking_api).lower()
    for verb in ('placeorder', 'place_order', 'submit_order', 'transmit'):
        assert verb not in src
