"""
LOT 176 — Clôture de la tournée « honnêteté des routes » : les trois
lacunes minces restantes en un lot — l'entonnoir d'opportunités
(`opportunities_api.py`, chemin d'erreur fail-honest), le copilote
(`ai_api.py` /api/copilot/ask POST, jamais un crash), et le Live Engine
(`live_api.py`, report vide honnête + parsing des domaines). Sondé
empiriquement ; comportements documentés tels quels.
"""
import os

import pytest

import terminal


@pytest.fixture()
def client():
    return terminal.app.test_client()


# ── /api/opportunities/funnel : fail-honest ──────────────────────────────────

def test_funnel_nominal_7_etages_exacts(client):
    d = client.get('/api/opportunities/funnel').get_json()
    assert [s.get('key') for s in d['stages']] == [
        'universe', 'eligible', 'radar', 'priority',
        'actionable', 'followed', 'positions']
    assert 'roles' in d


def test_funnel_moteur_en_panne_500_structure_vide_honnete(client, monkeypatch):
    # Le moteur qui lève → 500 avec structure VIDE + erreur nommée — le client
    # affiche un état d'erreur, jamais un entonnoir à moitié inventé.
    from vertex.app.routes import opportunities_api as OA
    monkeypatch.setattr(OA._funnel, 'build_funnel',
                        lambda *a, **k: (_ for _ in ()).throw(ValueError('boom')))
    r = client.get('/api/opportunities/funnel')
    assert r.status_code == 500
    assert r.get_json() == {'stages': [], 'roles': [], 'error': 'ValueError: boom'}


# ── /api/copilot/ask : jamais un crash, repli étiqueté ───────────────────────

def test_ask_body_vide_et_corrompu_meme_refus_honnete(client):
    # Body JSON vide OU illisible : la route avale (silent=True) et le copilote
    # répond ok False « question vide » — HTTP 200, jamais une 500.
    attendu = {'answer': None, 'error': 'question vide', 'ok': False, 'source': None}
    r1 = client.post('/api/copilot/ask', json={})
    assert r1.status_code == 200 and r1.get_json() == attendu
    r2 = client.post('/api/copilot/ask', data='{corrompu',
                     content_type='application/json')
    assert r2.status_code == 200 and r2.get_json() == attendu


def test_ask_sans_cle_repli_deterministe_etiquete(client):
    if os.environ.get('ANTHROPIC_API_KEY'):
        pytest.skip('clé configurée — le repli sans clé ne peut être observé')
    r = client.post('/api/copilot/ask',
                    json={'question': 'Que penser de TSTQ ?', 'symbol': 'TSTQ'})
    d = r.get_json()
    assert d['label'] == 'Moteurs déterministes (Claude non configuré ou indisponible)'
    # Le repli est TOUJOURS étiqueté dans la réponse elle-même (le contenu
    # varie selon les données du scan, l'étiquette jamais).
    assert ('Réponse assemblée par les moteurs déterministes — configure '
            'ANTHROPIC_API_KEY') in d['answer']


# ── /api/live/report + /api/live/refresh : parsing et vide honnête ───────────

def test_report_a_froid_vide_honnete(client):
    # Aucune synchronisation encore menée dans ce contexte → structure vide
    # datée null, jamais un rapport fabriqué. (Si un refresh a déjà tourné
    # dans la même exécution de suite, le rapport le reflète honnêtement.)
    d = client.get('/api/live/report').get_json()
    assert set(d.keys()) >= {'lines', 'requested', 'ts'}
    assert isinstance(d['lines'], list)


def test_refresh_domaine_inconnu_rien_relance(client):
    d = client.get('/api/live/refresh?domains=inconnu').get_json()
    assert d['ok'] is True
    assert d['kicked'] is False                     # rien à relancer
    assert d['requested'] == ['inconnu']            # la demande est tracée
    assert d['report']['lines'] == []               # aucun domaine réel touché


def test_refresh_parsing_des_domaines_multiples(client):
    # Le parsing purge espaces et segments vides en gardant l'ordre. (`kicked`
    # dépend de l'état du moteur — occupé → pas de relance — donc non figé ici.)
    d = client.get('/api/live/refresh?domains=prices, news ,').get_json()
    assert d['ok'] is True
    assert d['requested'] == ['prices', 'news']


# ── Invariant produit : les 3 modules sont bien LECTURE SEULE ────────────────

def test_modules_sans_verbe_d_ordre():
    import inspect
    from vertex.app.routes import opportunities_api, ai_api, live_api
    for mod in (opportunities_api, ai_api, live_api):
        src = inspect.getsource(mod).lower()
        for verb in ('placeorder', 'place_order', 'submit_order', 'transmit'):
            assert verb not in src
