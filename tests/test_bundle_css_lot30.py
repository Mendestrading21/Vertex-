"""tests/test_bundle_css_lot30.py — LOT 30 : la chaîne des 19 feuilles CSS.

Lighthouse (lot 28) : perf 68-71, LCP 6-7 s simulés — dominés par 18
requêtes de feuilles en chaîne critique. Cible : UNE feuille agrégée,
assemblée EN MÉMOIRE au premier appel dans l'ordre EXACT de la cascade
(l'ordre est un contrat — le déplacer change le rendu), servie immutable ;
les fichiers individuels restent servis (développement, bancs, rollback).
Nés ROUGES.
"""
import re

import pytest


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _links(html):
    return re.findall(r'<link rel="stylesheet" href="([^"]+)"', html)


def test_la_coque_charge_une_seule_feuille(client):
    links = _links(client.get('/').get_data(as_text=True))
    assert len(links) == 1, links
    assert '/asset/css/bundle' in links[0]


def test_le_bundle_est_la_cascade_exacte(client):
    from vertex.ui.shell import CSS_ORDER
    r = client.get('/asset/css/bundle.css')
    assert r.status_code == 200
    corps = r.get_data(as_text=True)
    #  chaque feuille est présente, marquée, et DANS L'ORDRE du contrat
    pos = -1
    for nom in CSS_ORDER:
        marque = '/* ═ bundle: %s ═ */' % nom
        i = corps.find(marque)
        assert i >= 0, 'feuille absente du bundle : %s' % nom
        assert i > pos, 'ordre de cascade rompu à %s' % nom
        pos = i
    assert 'immutable' in (r.headers.get('Cache-Control') or '')


def test_les_feuilles_individuelles_restent_servies(client):
    assert client.get('/static/vertex/css/vertex-2-0.css').status_code == 200


def test_le_bundle_ne_vit_pas_sur_le_disque():
    import os
    assert not os.path.exists('vertex/static/vertex/css/bundle.css'), (
        'assemblé en mémoire — jamais un artefact généré dans l\'arbre suivi')
