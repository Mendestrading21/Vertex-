"""Lot 39 — le bundle CSS servi est minifié (chaîne critique du LCP).

Lighthouse (re-mesure post-lot 38, accueil, émulation mobile) : perf 63 —
SOUS le budget ≥ 65 du contrôle 131 — avec « unminified-css : 66 KiB »
directement sur la chaîne critique. Le bundle est déjà UNE requête (lot 30) ;
ce lot retire les octets morts (commentaires, indentation) SANS toucher la
sémantique : minifieur conservateur (chaînes préservées, calc() intact,
espaces des sélecteurs `>` `~` `+` conservés).

Les 19 marqueurs `/* ═ bundle: nom ═ */` restent — ce sont le sommaire du
bundle et le contrat du banc lot 30.
"""
import re

import pytest


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _minifier():
    from vertex.app.routes.system import _minifier_css
    return _minifier_css


# ── Le minifieur est CONSERVATEUR (cas pièges unitaires) ─────────────────────

def test_les_chaines_sont_preservees():
    m = _minifier()
    assert m('a::before{content:"/* pas un commentaire */";}') == \
        'a::before{content:"/* pas un commentaire */"}'
    assert m("a::after{content:'a  b';}") == "a::after{content:'a  b'}"


def test_calc_garde_ses_espaces():
    m = _minifier()
    assert m('.x { width: calc(100% - 20px); }') == '.x{width:calc(100% - 20px)}'


def test_les_combinateurs_gardent_leur_sens():
    m = _minifier()
    #  `a > b` et `a b` sont des sélecteurs différents : l'espace unique reste.
    assert m('.a > .b { color: red; }') == '.a > .b{color:red}'
    assert m('.a  .b{color:red}') == '.a .b{color:red}'


def test_les_commentaires_partent():
    m = _minifier()
    assert m('/* zap */ .a{/* zap */color:red}') == '.a{color:red}'


def test_media_query_intacte():
    m = _minifier()
    assert m('@media (max-width: 600px) { .a { color: red; } }') == \
        '@media (max-width: 600px){.a{color:red}}'


# ── Le bundle servi est réellement minifié ───────────────────────────────────

def test_le_bundle_servi_est_minifie(client):
    import os
    from vertex.ui.shell import CSS_ORDER
    corps = client.get('/asset/css/bundle.css').get_data(as_text=True)
    #  les marqueurs restent (sommaire + contrat lot 30)
    for nom in CSS_ORDER:
        assert ('/* ═ bundle: %s ═ */' % nom) in corps
    #  hors marqueurs : plus aucun commentaire
    sans_marques = re.sub(r'/\* ═ bundle: [^*]+ ═ \*/', '', corps)
    assert '/*' not in sans_marques, 'commentaires résiduels dans le bundle servi'
    #  gain réel : au moins 25 % de moins que la concaténation brute
    dossier = 'vertex/static/vertex/css'
    brut = sum(os.path.getsize(os.path.join(dossier, n)) for n in CSS_ORDER)
    assert len(corps.encode('utf-8')) < brut * 0.75, (
        'bundle %d o pour %d o bruts — minification ineffective'
        % (len(corps.encode('utf-8')), brut))
