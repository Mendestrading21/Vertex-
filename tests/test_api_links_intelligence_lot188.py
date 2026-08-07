"""
LOT 188 — Gardien des ENDPOINTS API référencés par les pages vivantes
(complète les lots 182/186 : syntaxe inline → fichiers src= →
désormais les LIENS D'API des fetch) + invariants d'intelligence_page
(662 l, la page vivante la moins gardée). Un fetch vers une route
inexistante serait un lien mort invisible (l'UI afficherait une
erreur réseau à chaque visite). Constat : les 54 endpoints référencés
existent TOUS — le gardien empêche la régression.
"""
import fnmatch
import functools
import re

import pytest

import terminal
from vertex.ui.pages.intelligence_page import VIEWS, _DEFAULT_VIEW

_PAGES = ('/', '/markets', '/opportunities', '/portfolio', '/journal',
          '/options', '/system', '/tracking', '/intelligence',
          '/titre/AAPL', '/analysis/AAPL')


@functools.lru_cache(maxsize=1)
def _fetched():
    """{url: pages} — toutes les URLs fetchées par les pages servies."""
    c = terminal.app.test_client()
    urls = {}
    for pg in _PAGES:
        html = c.get(pg, follow_redirects=True).get_data(as_text=True)
        for u in re.findall(r"""(?:VX\.fetch|fetch)\(\s*['"`](/[^'"`\?\$]+)""", html):
            urls.setdefault(u.rstrip('/') or '/', set()).add(pg)
    return urls


def _known(url, rules):
    for r in rules:
        if url == r or fnmatch.fnmatch(url, re.sub(r'<[^>]+>', '*', r)):
            return True
    # URL concaténée en JS ('/api/x/'+sym) → tronquée : un préfixe de route
    # paramétrée compte comme connue.
    return any(r.startswith(url) for r in rules)


# ── Aucun lien d'API mort dans les pages vivantes ────────────────────────────

def test_chaque_endpoint_fetche_existe_dans_l_app():
    rules = [str(r) for r in terminal.app.url_map.iter_rules()]
    assert len(_fetched()) >= 40                    # anti-vide : le gardien contrôle
    morts = {u: sorted(p) for u, p in _fetched().items() if not _known(u, rules)}
    assert morts == {}


# ── intelligence_page : les invariants jamais gardés ─────────────────────────

def test_les_6_vues_rendent_200_avec_le_bon_onglet_actif():
    c = terminal.app.test_client()
    assert [v for v, _ in VIEWS] == ['analyst', 'committee', 'strategy',
                                     'impacts', 'research', 'memory']
    for vid, label in VIEWS:
        html = c.get('/intelligence?view=%s' % vid).get_data(as_text=True)
        actif = re.findall(r'aria-selected="true"[^>]*>([^<]+)', html)
        assert actif == [label], vid                # un seul onglet actif, le bon


def test_vue_inconnue_retombe_sur_la_vue_par_defaut():
    c = terminal.app.test_client()
    html = c.get('/intelligence?view=zzz').get_data(as_text=True)
    actif = re.findall(r'aria-selected="true"[^>]*>([^<]+)', html)
    assert actif == [dict(VIEWS)[_DEFAULT_VIEW]]    # jamais une page cassée


def test_aucun_id_duplique_dans_aucune_vue():
    c = terminal.app.test_client()
    for vid, _ in VIEWS:
        html = c.get('/intelligence?view=%s' % vid).get_data(as_text=True)
        ids = re.findall(r'id="([^"]+)"', html)
        assert [i for i in set(ids) if ids.count(i) > 1] == [], vid


def test_etats_honnetes_omnipresents_et_page_saine():
    c = terminal.app.test_client()
    html = c.get('/intelligence').get_data(as_text=True)
    assert html.count('VX.states') >= 12            # vide/erreur/chargement partout
    assert '#8f8a83' not in html.lower()
    for verb in ('placeorder', 'submit_order', 'transmit('):
        assert verb not in html.lower()
