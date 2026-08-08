"""
LOT 368 — Les SEGMENTS DE CHEMIN, jumeaux du `?view=` du lot 367.

Un segment (`/analysis/<sym>`, `/memory/<decision_id>`) est du texte libre :
plus exposé qu'un paramètre de requête. Deux surfaces étaient sans gardien.

**1. Le symbole.** Sondé avec 6 charges hostiles sur 7 gabarits de route :
aucune fuite. `/analysis/<sym>` rend bien la page (200, ~75 Ko — la charge
atteint donc réellement le moteur de rendu) et la neutralise deux fois :

    /analysis/"><img src=x onerror=alert(1)>  →  const SYM="IMGS"

les caractères non alphanumériques sont **retirés** avant l'injection JS, et
le texte affiché est **échappé** (`&lt;`, `&quot;`, `&gt;`). Les redirections
`/titre/` et `/company/` restent **relatives** (`/analysis/…`) — pas de
redirection ouverte — et une charge CRLF est refusée par Werkzeug.

**2. La mémoire décisionnelle.** `/memory/<decision_id>` sert bien une page
HTML (200, 19 Ko, 1 bloc inline qui parse, 35 `id` sans doublon) que le
lot 359 avait signalée comme non couverte. Sa docstring promet que « TOUT
contenu de la mémoire est ÉCHAPPÉ (XSS) » — **rien ne le vérifiait**. Ici on
injecte un record hostile dans une mémoire temporaire et on exige l'échappement.

Note de méthode : la première sonde envoyait des charges contenant `/`.
Werkzeug refuse `%2F` dans un segment et rend son 404 par défaut (701 octets) —
la charge n'atteignait jamais le rendu, et la sonde ne prouvait rien. Toutes
les charges ci-dessous sont **sans barre oblique**.
"""
import json
import re

import pytest

import terminal
from vertex.services import persist

# Sans barre oblique : la charge doit atteindre le moteur de rendu.
CHARGES = [
    ('attribut HTML', '"><img src=x onerror=alert(1)>', 'onerror=alert'),
    ('balise svg', '<svg onload=alert(1)>', 'onload=alert'),
    ('sortie de chaîne JS', "';alert(1);'", ';alert(1);'),
    ('concaténation JS', "'-alert(1)-'", '-alert(1)-'),
    ('attribut sans balise', '" onmouseover="alert(1)', 'onmouseover='),
]

_INLINE = re.compile(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', re.S)


@pytest.fixture(scope='module')
def client():
    return terminal.app.test_client()


# ── 1. Le symbole ne traverse jamais jusqu'aux octets servis ─────────────────

@pytest.mark.parametrize('nom,charge,trace', CHARGES)
def test_un_symbole_hostile_est_filtre_avant_le_rendu(client, nom, charge, trace):
    r = client.get('/analysis/' + charge)
    assert r.status_code == 200, 'la page doit rester servie (%s)' % r.status_code
    html = r.get_data(as_text=True)
    assert charge not in html, 'la charge ressort telle quelle dans la page'
    assert trace not in html, 'charge exécutable dans la page'


def test_la_constante_SYM_servie_reste_alphanumerique(client):
    html = client.get('/analysis/' + '"><img src=x onerror=alert(1)>').get_data(as_text=True)
    trouves = re.findall(r'const SYM\s*=\s*(["\'])([^"\']*)\1', html)
    assert trouves, 'const SYM n\'est plus servie — gardien à revoir'
    for _, valeur in trouves:
        assert re.fullmatch(r'[A-Z0-9.\-]*', valeur), (
            'const SYM servie contient autre chose qu\'un symbole : %r' % valeur)


@pytest.mark.parametrize('route', ('/titre/', '/company/'))
def test_les_redirections_restent_relatives(client, route):
    # Une Location absolue vers un hôte contrôlé serait une redirection ouverte.
    r = client.get(route + 'https:%5C%5Cevil.test')
    assert r.status_code in (301, 302)
    loc = r.headers.get('Location', '')
    assert loc.startswith('/'), 'redirection ouverte possible : Location=%r' % loc
    assert 'evil.test' not in loc.split('/analysis/')[0]


def test_le_gardien_ne_tourne_pas_a_vide(client):
    # Un symbole LÉGITIME doit produire une vraie page : sinon les tests
    # ci-dessus passeraient sur des pages d'erreur sans rien prouver.
    r = client.get('/analysis/AAPL')
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert len(html) > 20000 and 'const SYM="AAPL"' in html


# ── 2. La mémoire décisionnelle échappe son contenu ──────────────────────────

HOSTILE = '<img src=x onerror=alert(1)>'


@pytest.fixture()
def memoire_piegee(tmp_path, monkeypatch):
    """Mémoire TEMPORAIRE contenant un record hostile — la vraie n'est jamais
    touchée (méthode du lot 362)."""
    from vertex.engines import decision_memory as dm
    record = {
        'decision_id': 'deadbeefcafe0001', 'symbol': HOSTILE,
        'decision': HOSTILE, 'level': 'S', 'score_total': 33,
        'engine_version': HOSTILE, 'session_date': '2026-08-08',
        'demo': True, 'thesis': HOSTILE, 'catalyst': HOSTILE,
        'trigger': HOSTILE, 'invalidation': HOSTILE,
    }
    mem = dm.empty_memory()
    mem.setdefault('decisions', []).append(record)
    (tmp_path / dm.MEMORY_FILE).write_text(json.dumps(mem), encoding='utf-8')
    monkeypatch.setattr(persist, 'cache_path', lambda n: str(tmp_path / n))
    return 'deadbeefcafe0001'


def test_le_post_mortem_echappe_tout_le_contenu_de_la_memoire(client, memoire_piegee):
    r = client.get('/memory/' + memoire_piegee)
    assert r.status_code == 200, 'le record injecté doit être trouvé (%s)' % r.status_code
    html = r.get_data(as_text=True)
    assert HOSTILE not in html, (
        'la mémoire ressort BRUTE — la promesse « TOUT contenu de la mémoire '
        'est ÉCHAPPÉ » de la docstring ne tient plus')
    # Seule la forme EXÉCUTABLE compte : `onerror=alert` subsiste légitimement
    # en TEXTE inerte une fois les chevrons échappés.
    assert '<img' not in html, 'balise active issue de la mémoire'
    assert '&lt;img' in html, 'le contenu doit être échappé, pas supprimé'


def test_un_symbole_qui_sort_du_titre_ne_peut_pas_injecter(client, tmp_path,
                                                           monkeypatch):
    """Le cas qui a fait tomber le gardien au lot 368 : `</title>` referme la
    balise et tout ce qui suit devient du HTML ACTIF dans le <head>."""
    from vertex.engines import decision_memory as dm
    charge = '</title><script>alert(1)</script>'
    mem = dm.empty_memory()
    mem.setdefault('decisions', []).append({
        'decision_id': 'deadbeefcafe0002', 'symbol': charge, 'decision': 'BUY',
        'level': 'S', 'score_total': 30, 'engine_version': 'x',
        'session_date': '2026-08-08', 'demo': True, 'thesis': 't',
        'catalyst': 'c', 'trigger': 'tr', 'invalidation': 'inv'})
    (tmp_path / dm.MEMORY_FILE).write_text(json.dumps(mem), encoding='utf-8')
    monkeypatch.setattr(persist, 'cache_path', lambda n: str(tmp_path / n))

    html = client.get('/memory/deadbeefcafe0002').get_data(as_text=True)
    apres_titre = html.split('</title>', 1)[1] if '</title>' in html else ''
    assert '<script>alert(1)</script>' not in apres_titre, (
        'un symbole de la mémoire sort du <title> et injecte du script actif')
    assert '&lt;/title&gt;' in html or '&lt;script&gt;' in html, (
        'la charge doit apparaître échappée dans le titre')


def test_un_identifiant_inconnu_rend_un_404_lisible_sans_le_refleter(client):
    charge = '"><img src=x onerror=alert(1)>'
    r = client.get('/memory/' + charge)
    assert r.status_code == 404
    html = r.get_data(as_text=True)
    assert charge not in html and 'onerror=alert' not in html
    assert 'Décision inconnue' in html, 'le 404 doit rester lisible et honnête'
