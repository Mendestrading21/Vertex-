"""tests/test_alerts_live_lot85.py — SKYLER LOT 85 : alertes + flux live.

Audit navigateur (publié) : cycle alerte 4/4 — création via l'API client
officielle (VXEntities.addAlert), persistance localStorage + sync desk
(le serveur porte l'alerte), UI branchée, suppression propre (serveur
nettoyé). Flux SSE /api/live/events : retry immédiat + replay des
événements NOMMÉS (event: system, JSON) + battement 25 s — mes deux
premières sondes étaient des FAUX POSITIFS (buffering du pipe curl ;
onmessage n'écoute pas les événements nommés), vérifiés au socket brut
puis en navigateur avec addEventListener — dits.

Gardiens PROSPECTIFS (nés verts, dits) : l'architecture du flux live ne
doit pas se défaire.
"""


def test_sse_route_keeps_retry_replay_heartbeat():
    src = open('vertex/app/routes/live_events.py', encoding='utf-8').read()
    assert 'retry: 4000' in src, 'directive de reconnexion immédiate'
    assert 'replay_since' in src, 'rattrapage Last-Event-ID'
    assert 'heartbeat' in src, 'battement anti-coupure (25 s)'
    assert "mimetype='text/event-stream'" in src


def test_live_updates_consumer_subscribes_named_channels():
    js = open('vertex/static/vertex/js/live-updates.js', encoding='utf-8').read()
    assert 'EventSource' in js and 'addEventListener(ch' in js, (
        'les événements sont NOMMÉS — addEventListener par canal obligatoire')
    assert 'lastEventId' in js, 'reprise sans perte après coupure'
    assert 'pagehide' in js, 'fermeture propre du flux en quittant'


def test_client_alerts_api_complete():
    js = open('vertex/static/vertex/js/vx-entities.js', encoding='utf-8').read()
    for needle in ('addAlert', 'removeAlert', 'hasAlert', "get('vxAlerts'"):
        assert needle in js, needle
