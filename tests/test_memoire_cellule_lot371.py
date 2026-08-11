"""
LOT 371 — `/memory/cell/<group>/<key>` : la sœur de la route qui a failli au
lot 368, validée avec des cellules RÉELLES.

Le lot 368 a trouvé une faille XSS sur `/memory/<decision_id>` (le `title=`
n'était pas échappé) et n'avait pas couvert sa jumelle
`/memory/cell/<group>/<key>` — même fichier, même auteur, même motif : forte
probabilité du même défaut.

**Verdict : saine.** Deux différences décisives avec la route fautive :
son `title=` est une **constante** (`'Cellule de calibration'`), et chaque
valeur du corps passe par `markupsafe.escape`.

Sondé avec une mémoire temporaire dont les records sont hostiles — **4 cellules
rendues en 200 (19 Ko)**, dont une dont la **clé elle-même est la charge**
(`by_regime/"><img src=x onerror=alert(1)>`, donc la charge traverse à la fois
l'URL et la donnée) : aucune charge brute, aucune balise active, `<title>`
unique et clos.

⚠ **Leçon de méthode payée comptant** : une première sonde écrivait les
résultats sous la forme `{'hit': bool}` — la vraie forme est
`{'horizons': {'H5'|'H20'|'H60': {'status': 'MESURE', 'return_pct': …}}}`
(cf. `_measured_class`). Résultat : **aucune cellule formée**, donc des 404
partout et une sonde qui **ne prouvait rien** — exactement le piège du lot 368.
Les fixtures ci-dessous construisent la forme réelle, et un test dédié échoue
si les cellules ne se forment plus.
"""
import json
import re
import urllib.parse

import pytest

import terminal
from vertex.engines import decision_memory as dm
from vertex.engines import skyler_core as sk
from vertex.services import persist

HOSTILE = '"><img src=x onerror=alert(1)>'


@pytest.fixture()
def memoire_hostile(tmp_path, monkeypatch):
    """Mémoire TEMPORAIRE — la vraie n'est jamais touchée (méthode du lot 362).

    Trois décisions MESURÉES : c'est ce qui forme les cellules. Sans horizons
    au statut MESURE, aucune cellule n'existe et la sonde tourne à vide.
    """
    mem = dm.empty_memory()
    for i in range(3):
        did = 'ffff00000000000%d' % i
        mem.setdefault('decisions', []).append({
            'decision_id': did, 'symbol': HOSTILE, 'decision': 'BUY',
            'level': 'S', 'regime': HOSTILE, 'catalyst': HOSTILE,
            'catalyst_kind': HOSTILE, 'score_total': 30,
            'engine_version': sk.ENGINE_VERSION,
            'session_date': '2026-08-0%d' % (i + 1), 'demo': True,
            'thesis': HOSTILE, 'trigger': HOSTILE, 'invalidation': HOSTILE,
        })
        mem.setdefault('outcomes', []).append({
            'decision_id': did,
            'horizons': {'H5': {'status': 'MESURE',
                                'return_pct': 6.0 if i % 2 == 0 else -6.0}},
            'measured_at': '2026-08-08',
        })
    (tmp_path / dm.MEMORY_FILE).write_text(json.dumps(mem), encoding='utf-8')
    monkeypatch.setattr(persist, 'cache_path', lambda n: str(tmp_path / n))
    return mem


@pytest.fixture()
def client():
    return terminal.app.test_client()


def _cellules(mem):
    ctx = dm.calibration_by_context(mem, sk.ENGINE_VERSION)
    return [(g, k) for g in dm.CONTEXT_GROUPS
            if isinstance(ctx.get(g), dict) for k in ctx[g]]


def test_la_sonde_forme_bien_des_cellules(memoire_hostile):
    """Anti-vide : sans cellule, tous les tests suivants tomberaient sur des
    404 et ne prouveraient rien (le piège du lot 368)."""
    cellules = _cellules(memoire_hostile)
    assert len(cellules) >= 4, (
        'aucune cellule formée — la forme des outcomes a changé, revoir la '
        'fixture (horizons/MESURE) avant de conclure quoi que ce soit')


def test_chaque_cellule_reelle_echappe_le_contenu_de_la_memoire(client,
                                                                memoire_hostile):
    rendues = 0
    for groupe, cle in _cellules(memoire_hostile):
        url = '/memory/cell/%s/%s' % (groupe, urllib.parse.quote(str(cle), safe=''))
        r = client.get(url)
        if r.status_code != 200:
            continue
        rendues += 1
        html = r.get_data(as_text=True)
        assert HOSTILE not in html, '%s sert la mémoire BRUTE' % url
        assert not re.search(r'<img[^>]*onerror', html), '%s : balise active' % url
        assert html.count('<title>') == 1 and html.count('</title>') == 1
    assert rendues >= 4, 'trop peu de cellules rendues : sonde à revoir'


def test_une_cle_hostile_traverse_l_url_ET_la_donnee_sans_fuir(client,
                                                               memoire_hostile):
    """Le cas le plus dur : la charge est À LA FOIS le segment d'URL et la clé
    de cellule (groupe `by_regime`, dont la clé vient du record hostile)."""
    url = '/memory/cell/by_regime/' + urllib.parse.quote(HOSTILE, safe='')
    r = client.get(url)
    assert r.status_code == 200, 'la cellule hostile doit exister (%s)' % r.status_code
    html = r.get_data(as_text=True)
    assert HOSTILE not in html
    assert not re.search(r'<img[^>]*onerror', html)
    assert '&lt;img' in html, 'le contenu doit être échappé, pas supprimé'


def test_un_groupe_ou_une_cle_inconnus_rendent_un_404_sans_reflechir(client):
    for url in ('/memory/cell/by_level/' + urllib.parse.quote(HOSTILE, safe=''),
                '/memory/cell/' + urllib.parse.quote(HOSTILE, safe='') + '/x'):
        r = client.get(url)
        assert r.status_code == 404
        html = r.get_data(as_text=True)
        assert HOSTILE not in html and 'onerror=alert' not in html


def test_le_titre_de_la_cellule_reste_une_constante():
    """La faille du lot 368 venait d'un `title=` nourri par la donnée. Ici il
    est constant — si cela change, il devra être échappé au site d'appel."""
    import os
    chemin = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          'vertex', 'app', 'routes', 'analysis_api.py')
    with open(chemin, encoding='utf-8') as f:
        src = f.read()
    assert "render_shell(title='Cellule de calibration'" in src, (
        'le titre de la cellule n\'est plus une constante : il doit désormais '
        'être échappé (faute du lot 368)')
