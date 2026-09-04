"""tests/test_rescan_honnete.py — LOT 32 : le rescan annonçait 517 titres en démo.

Mesuré en direct : `POST /api/rescan` en mode démo répond « recalcul des
517 titres » alors que la boucle démo n'en scanne que 20
(terminal.py : `UNIVERSE[:20] if DEMO_MODE`). Un compte annoncé doit être
le compte RÉEL. Né ROUGE.
"""
import terminal


def test_le_rescan_annonce_le_compte_reellement_scanne(monkeypatch):
    from vertex.app.routes import scan_api
    from vertex.app import rescan_gate
    monkeypatch.setattr(rescan_gate, 'restant', lambda: 0)
    monkeypatch.setattr(scan_api, 'DEMO_MODE', True, raising=False)
    c = terminal.app.test_client()
    d = c.post('/api/rescan').get_json()
    if d.get('status') == 'rescan_queued':
        from vertex.data.constants import DEMO_UNIVERSE_N
        assert d['universe'] == DEMO_UNIVERSE_N, (
            'en démo, la boucle scanne UNIVERSE[:20] — le message doit le dire')
        assert 'des 20 titres' in d['msg']
