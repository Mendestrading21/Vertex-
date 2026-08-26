"""Tests d’intégration du déclencheur de rescan global, sans identité client.

#779/G1 — la porte anti-rafale a quitté `terminal.py` pour
`vertex/app/rescan_gate.py` : elle n'avait aucune dépendance au monolithe.
Ce fichier vise donc le module qui la tient, plutôt que des variables privées
du monolithe qui n'existent plus.

Ce qui est protégé n'a pas changé, et c'est le point : la fenêtre est
**globale**, et aucune réponse ne trahit qui a demandé.
"""
import terminal
from vertex.app import rescan_gate


def _reset_rescan(monkeypatch, now=1_000.0):
    monkeypatch.setattr(rescan_gate, 'COOLDOWN_S', 30)
    monkeypatch.setattr(rescan_gate.time, 'monotonic', lambda: now)
    rescan_gate.reinitialiser()


def test_rescan_first_request_is_queued_and_preserves_market_state(monkeypatch):
    _reset_rescan(monkeypatch)
    sentinel = {'source': 'cached', 'rows': [{'symbol': 'AAA'}], 'scan_status': 'IDLE'}
    saved = dict(terminal.scan_state)
    terminal.scan_state.clear()
    terminal.scan_state.update(sentinel)
    try:
        response = terminal.app.test_client().post('/api/rescan')
        payload = response.get_json()
        assert response.status_code == 200
        assert payload['ok'] is True
        assert payload['status'] == 'rescan_queued'
        assert payload['universe'] == len(terminal.UNIVERSE)
        assert rescan_gate.EVENEMENT.is_set()
        assert terminal.scan_state == sentinel
    finally:
        terminal.scan_state.clear()
        terminal.scan_state.update(saved)


def test_rescan_rapid_second_request_is_rate_limited_without_identity(monkeypatch):
    _reset_rescan(monkeypatch)
    client = terminal.app.test_client()
    assert client.get('/api/rescan').status_code == 200

    response = client.post('/api/rescan')
    payload = response.get_json()

    assert response.status_code == 429
    assert payload == {'ok': False, 'error': 'rescan_rate_limited', 'retry_after': 30}
    assert response.headers['Retry-After'] == '30'
    flat_payload = str(payload).lower()
    for forbidden in ('ip', 'address', 'client', 'requester', 'identity', 'token'):
        assert forbidden not in flat_payload


def test_scan_endpoint_exposes_only_global_rescan_cooldown(monkeypatch):
    _reset_rescan(monkeypatch)
    client = terminal.app.test_client()
    assert client.post('/api/rescan').status_code == 200

    scan_payload = client.get('/scan').get_json()
    assert scan_payload['rescan_cooldown_remaining'] == 30
    assert 'ip' not in scan_payload
    assert 'requester' not in scan_payload


def test_l_evenement_reste_celui_qu_attend_la_boucle():
    """LE PIÈGE SILENCIEUX DE CETTE EXTRACTION.

    `_live.configure(rescan_event=…)` transmet l'objet à la boucle de scan, qui
    attend **celui-là**. Le réassigner — au lieu de le muter par `set()` —
    laisserait la boucle attendre un objet que plus personne ne réveille : le
    re-scan cesserait de fonctionner sans qu'aucune erreur ne soit levée."""
    assert terminal._rescan_evt is rescan_gate.EVENEMENT, (
        'le monolithe a recree son propre evenement')
    #  ON VISE LE CABLAGE, PAS L'ETAT COURANT. Une premiere version affirmait
    #  `live_engine._CFG['rescan_event'] is rescan_gate.EVENEMENT` : elle
    #  passait seule et echouait dans la suite complete, parce que
    #  `tests/test_live_engine.py` reconfigure legitimement le moteur avec ses
    #  propres etats. Un test dependant de l'ordre des autres ne prouve rien.
    import pathlib
    src = pathlib.Path(terminal.__file__).read_text(encoding='utf-8')
    assert 'rescan_event=_rescan_evt' in src, (
        'le monolithe ne transmet plus l\'evenement a la boucle de scan : '
        'le re-scan ne repartirait jamais, en silence')


def test_la_fenetre_ne_peut_pas_etre_ouverte_par_l_environnement():
    """`VERTEX_RESCAN_COOLDOWN_SEC=0` ouvrirait la porte en grand. La borne
    basse est à 1 s, et ce n'est pas un détail : c'est ce qui empêche huit
    onglets de relancer un scan d'univers complet en boucle.

    Testé par la FONCTION, jamais par un `importlib.reload` : recharger le
    module recréerait `EVENEMENT`, et la boucle de scan attendrait alors un
    objet que plus personne ne réveille — le test aurait cassé le produit pour
    se prouver juste."""
    f = rescan_gate.fenetre_depuis_env
    assert f('0') == 1 and f('-5') == 1, 'la porte peut etre desactivee'
    assert f(None) == 30 and f('pas un nombre') == 30, (
        'une variable illisible ne retombe plus sur le defaut')
    assert f('120') == 120
