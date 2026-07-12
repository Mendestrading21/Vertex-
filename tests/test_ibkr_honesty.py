"""Tests — honnêteté de l'état de connexion IBKR (§2/§10).

« Activé » (config) ne doit JAMAIS être présenté comme « connecté » sans preuve
d'une session live. Le statut reflète l'état réel du socket, pas un drapeau de
configuration.
"""
from vertex.services import status_service, connections


def _status(scan_state, *, ibkr_enabled=True):
    return status_service.build_system_status(
        scan_state, build='test', readonly=True, ibkr_enabled=ibkr_enabled,
        demo_mode=False, ai_on=False)


def test_ibkr_enabled_but_no_session_is_idle_not_connected():
    st = _status({})                       # activé, aucune clé de session
    assert st['data_sources']['ibkr'] == 'enabled-idle'


def test_ibkr_connected_delayed_when_session_without_realtime():
    st = _status({'ibkr_connected': True, 'ibkr_live': False})
    assert st['data_sources']['ibkr'] == 'connected-delayed'


def test_ibkr_connected_live_only_with_realtime_proof():
    st = _status({'ibkr_connected': True, 'ibkr_live': True})
    assert st['data_sources']['ibkr'] == 'connected-live'


def test_ibkr_disabled_when_not_enabled():
    st = _status({'ibkr_connected': True, 'ibkr_live': True}, ibkr_enabled=False)
    assert st['data_sources']['ibkr'] == 'disabled'   # config prime : non activé = désactivé


def test_connections_never_declares_ibkr_live_without_proof():
    snap = connections.snapshot(ibkr_enabled=True, scan_state={})
    ib = next(c for c in snap['connections'] if c['name'] == 'IBKR')
    assert ib['status'] == 'OFFLINE'       # activé mais aucune session confirmée
    assert 'sans preuve' in ib['detail'].lower() or 'aucune session' in ib['detail'].lower()


def test_connections_reports_live_only_with_session():
    snap = connections.snapshot(ibkr_enabled=True,
                                scan_state={'ibkr_connected': True, 'ibkr_live': True})
    ib = next(c for c in snap['connections'] if c['name'] == 'IBKR')
    assert ib['status'] == 'LIVE'
