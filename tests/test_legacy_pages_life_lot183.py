"""
LOT 183 — VÉRIFICATION DE VIE des pages legacy de terminal.py.

CONSTAT (documenté, rien supprimé — la suppression est une décision
humaine) : les 25 blobs PAGE_* du monolithe (~2 265 lignes de HTML/JS)
ne sont plus servis par AUCUNE route Flask active — la refonte
(vertex/ui/pages + redesign.py) a tout repris, et les 39 anciennes
URLs redirigent vers les 8 espaces canoniques. Ces tests figent cet
état : ressusciter une page legacy ou en supprimer une devient une
décision EXPLICITE (mettre à jour l'inventaire), et aucun vieux lien
utilisateur ne tombe dans le vide.
"""
import re

import pytest

import terminal
from vertex.app.routes.redesign import LEGACY_REDIRECTS

# Inventaire EXACT des pages mortes au moment du constat (lot 183).
_DEAD_PAGES = {
    'PAGE_ANOMALIES', 'PAGE_BORDEL', 'PAGE_BRIEF', 'PAGE_CATALYSTS',
    'PAGE_COMPARE', 'PAGE_DAILY', 'PAGE_DECISIONS', 'PAGE_ENTREPRISES',
    'PAGE_EQUIPE', 'PAGE_HEALTH', 'PAGE_HEATMAP', 'PAGE_JOURNAL',
    'PAGE_ME', 'PAGE_OPTIONS_DESK', 'PAGE_OPTIONS_LAB', 'PAGE_RESEARCH',
    'PAGE_REVIEW', 'PAGE_SECTORS', 'PAGE_SETTINGS', 'PAGE_STOCKS',
    'PAGE_STRATEGIE', 'PAGE_SUIVI', 'PAGE_TITRE', 'PAGE_VAULT',
    'PAGE_WATCHLIST'}


def _pages_declarees():
    src = open('terminal.py', encoding='utf-8').read()
    return set(re.findall(r'^(PAGE_[A-Z_]+)\s*=', src, re.M))


def _pages_servies():
    """Pages référencées par le code d'une vue Flask ACTIVE."""
    servies = set()
    for rule in terminal.app.url_map.iter_rules():
        fn = terminal.app.view_functions[rule.endpoint]
        code = getattr(fn, '__code__', None)
        if code:
            servies |= {n for n in code.co_names if n.startswith('PAGE_')}
    return servies


# ── L'inventaire de vie/mort ─────────────────────────────────────────────────

def test_les_pages_legacy_sont_toutes_mortes_inventaire_exact():
    # Ressusciter une page (la router à nouveau) ou en supprimer une doit
    # mettre à jour CET inventaire — jamais un changement silencieux.
    assert _pages_declarees() == _DEAD_PAGES
    assert _pages_servies() & _DEAD_PAGES == set()


def test_aucun_module_du_produit_ne_les_importe():
    import glob as _glob
    refs = []
    for path in _glob.glob('vertex/**/*.py', recursive=True):
        src = open(path, encoding='utf-8').read()
        if re.search(r'terminal\.PAGE_[A-Z_]+', src):
            refs.append(path)
    assert refs == []                               # mortes ET orphelines


# ── Aucun vieux lien ne tombe dans le vide ───────────────────────────────────

def test_les_39_urls_legacy_redirigent_vers_leur_cible():
    c = terminal.app.test_client()
    assert len(LEGACY_REDIRECTS) == 39
    for old, new in LEGACY_REDIRECTS.items():
        r = c.get(old)
        assert r.status_code in (301, 302, 308), old
        assert r.headers['Location'].endswith(new), old


def test_les_destinations_des_redirections_repondent_200():
    c = terminal.app.test_client()
    dests = {new.split('?')[0] for new in LEGACY_REDIRECTS.values()}
    # Les 8 espaces canoniques du produit — et rien d'autre.
    assert dests == {'/', '/analysis', '/intelligence', '/journal',
                     '/markets', '/opportunities', '/portfolio', '/system'}
    for d in dests:
        assert c.get(d, follow_redirects=True).status_code == 200, d


def test_les_redirections_ne_pointent_jamais_vers_une_url_legacy():
    # Pas de chaîne de redirections : chaque cible est un espace canonique,
    # jamais une autre vieille URL (sinon boucles/301 en cascade).
    for old, new in LEGACY_REDIRECTS.items():
        assert new.split('?')[0] not in LEGACY_REDIRECTS, old
