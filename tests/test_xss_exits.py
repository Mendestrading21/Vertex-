"""
LOT 177 — Gardien XSS DE BOUT EN BOUT sur les points de sortie de news
(règle critique n°5 du projet : « tout texte externe passe par
sanitize_news avant d'être servi — rendus en innerHTML côté client »).
Le lot 102 a figé la FONCTION ; ces tests injectent un payload
malveillant dans les états partagés et vérifient que chaque ROUTE qui
sert des news le neutralise réellement : /news-feed (avec et sans
filtre), /api/events/<sym>, /api/skyler/<sym> — plus un gardien
statique sur les sites d'appel en production.
"""
import json

import pytest

import terminal
from vertex.app.state import scan_state, news_state


MAL = {'sym': 'TSTQ', 'title': '<script>alert(1)</script>Résultats "record"',
       'fr': '<img src=x onerror=alert(2)>', 'publisher': '<b>Pub</b>',
       'link': 'javascript:alert(3)', 'time': '10:00'}


@pytest.fixture()
def client():
    saved_items = news_state.get('items')
    yield terminal.app.test_client()
    news_state['items'] = saved_items
    scan_state.setdefault('detail', {}).pop('TSTQ', None)


def _inject_feed():
    news_state['items'] = [dict(MAL),
                           dict(MAL, link='https://exemple.com/a?b="c"<d>')]


# ── /news-feed : le point de sortie principal ────────────────────────────────

def test_feed_titre_sans_balise_et_quotes_echappees(client):
    _inject_feed()
    it = client.get('/news-feed').get_json()['items'][0]
    assert it['title'] == 'alert(1)Résultats &quot;record&quot;'
    assert '<' not in it['title']                   # plus JAMAIS une balise servie
    assert it['fr'] == ''                           # l'img onerror est entièrement vidée
    assert '<' not in it['publisher']


def test_feed_liens_javascript_supprimes_https_encodes(client):
    _inject_feed()
    items = client.get('/news-feed').get_json()['items']
    assert items[0]['link'] is None                 # javascript: → supprimé
    # https conservé mais quotes/chevrons %-encodés (sûr en href ET window.open)
    assert items[1]['link'] == 'https://exemple.com/a?b=%22c%22%3Cd%3E'


def test_feed_filtre_sym_ne_contourne_pas_l_assainissement(client):
    # La recherche serveur filtre AVANT l'assainissement au point de sortie —
    # le chemin filtré sert le même texte neutralisé.
    _inject_feed()
    j = client.get('/news-feed?sym=TSTQ').get_json()
    assert j['filtered'] is True and len(j['items']) == 2
    assert all('<' not in (it['title'] or '') for it in j['items'])


# ── /api/events/<sym> et /api/skyler/<sym> : news du détail du scan ──────────

def _inject_detail():
    scan_state.setdefault('detail', {})['TSTQ'] = {'price': 100.0,
                                                   'news': [dict(MAL)]}


def test_events_ne_sert_jamais_le_payload_brut(client):
    _inject_detail()
    blob = json.dumps(client.get('/api/events/TSTQ').get_json(), ensure_ascii=False)
    assert '<script>' not in blob
    assert 'javascript:alert' not in blob
    assert 'onerror=' not in blob
    assert 'alert(1)Résultats &quot;record&quot;' in blob   # le texte survit, neutralisé


def test_skyler_packet_ne_sert_jamais_le_payload_brut(client, tmp_path, monkeypatch):
    """⚠ `/api/skyler/<sym>` journalise une séance dans `skyler_sessions.json` :
    sans redirection, ce test y semait un point par jour sur le ticker
    SYNTHÉTIQUE TSTQ (lot 389)."""
    from vertex.services import persist
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    _inject_detail()
    blob = json.dumps(client.get('/api/skyler/TSTQ').get_json(), ensure_ascii=False)
    assert '<script>' not in blob
    assert 'javascript:alert' not in blob
    assert 'onerror=' not in blob


# ── Gardien statique : les sites d'appel de production ───────────────────────

def test_tous_les_points_de_sortie_appellent_sanitize_news():
    # Régression interdite : retirer un appel sanitize_news d'un point de
    # sortie ferait échouer ce compte. Sites connus : content.py (news-feed),
    # analysis_api ×2 (/api/skyler, /api/events), skyler_sweep, terminal
    # (chaînes IBKR) et vertex/options/pack.py.
    #
    # #779/G1 — le sixième site était le second de `terminal.py` : il vivait
    # DANS `options_pack`, et il a déménagé AVEC lui. C'est le bon résultat —
    # l'assainissement suit le code qui sert la donnée — mais le périmètre du
    # gardien devait suivre, sans quoi il aurait signalé une perte imaginaire.
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    n = 0
    for rel in ('vertex/app/routes/content.py', 'vertex/app/routes/analysis_api.py',
                'vertex/engines/skyler_sweep.py', 'terminal.py',
                'vertex/options/pack.py'):
        src = open(os.path.join(root, rel), encoding='utf-8').read()
        n += src.count('sanitize_news(')
    assert n >= 6, 'un point de sortie de news a perdu son assainissement'
