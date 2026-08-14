"""SIGNAL OS — LOT SHELL : la couche visuelle arrivait APRÈS le premier rendu.

Signal OS était chargé par `loadSignalOS()`, à la fin de `live-updates.js` : un
`<link>` et un `<script>` **créés en JavaScript** puis injectés dans le `<head>`
à l'exécution.

Trois conséquences, toutes réelles :

1. **Le document se peignait une fois sans la feuille.** Sur une navigation
   complète, le navigateur a le HTML et les 17 feuilles historiques bien avant
   que `live-updates.js` (chargé en `defer`) ne s'exécute. L'ancien thème est
   donc peint, puis remplacé.
2. **Le service worker ne la voyait pas.** Il met en cache le HTML de shell ; ce
   HTML ne mentionnait pas `signal-os.css`. Le repli hors-ligne servait un shell
   dont la couche visuelle n'était pas dans la même copie.
3. **L'ordre de cascade dépendait du temps.** Un `<link>` ajouté par script se
   place là où le script tourne. La position de Signal OS dans la cascade était
   donc une conséquence de l'ordonnancement, pas une décision.

## Ce que ces gardiens mesurent

Sur les **octets servis** par les huit routes, pas sur la source : la question
« la feuille atteint-elle la page ? » ne se répond pas en lisant un fichier
Python (leçon du lot 381 — `vx_kit.py` portait bien `DESK_KEYS` et n'atteignait
aucune des huit pages).

| | mesuré |
| --- | --- |
| routes servant `signal-os.css` | **8 / 8** |
| feuille déclarée APRÈS `neon-glass.css` | **8 / 8** |
| `loadSignalOS` encore dans un octet servi | **0** |
"""

import re

import pytest

import terminal

_ROUTES = ('/', '/markets', '/opportunities', '/analysis', '/portfolio',
           '/options', '/journal', '/system')


@pytest.fixture(scope='module')
def client():
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


@pytest.mark.parametrize('route', _ROUTES)
def test_signal_os_atteint_chaque_espace_servi(client, route):
    """La feuille est-elle DANS la page que le navigateur reçoit ?"""
    html = client.get(route).get_data(as_text=True)
    assert '/static/vertex/css/signal-os.css' in html, (
        '%s ne déclare pas Signal OS : cet espace garde l\'identité '
        'historique.' % route)


@pytest.mark.parametrize('route', _ROUTES)
def test_signal_os_est_declaree_apres_la_couche_historique(client, route):
    """Dernier arrivé, dernier appliqué. Si `neon-glass.css` passait après,
    la couche historique reprendrait la main sur la nouvelle identité — sans
    qu'aucun test de contenu ne bouge."""
    html = client.get(route).get_data(as_text=True)
    assert html.index('neon-glass.css') < html.index('signal-os.css'), (
        '%s déclare Signal OS AVANT neon-glass.css : la cascade s\'inverse.'
        % route)


def test_la_couche_n_est_plus_injectee_a_l_execution(client):
    """Le mécanisme d'avant ne doit pas revenir par une autre porte."""
    live = client.get('/static/vertex/js/live-updates.js').get_data(as_text=True)
    # On garde le MÉCANISME, pas le nom de la fonction : le commentaire qui
    # explique le retrait cite `loadSignalOS`, et un gardien qui interdit un mot
    # interdit aussi qu'on explique pourquoi on l'a retiré.
    for mecanisme in ("appendChild(css)", "appendChild(js)", "createElement('link')"):
        assert mecanisme not in live, (
            'l\'injection à l\'exécution est de retour (%s) : flash de l\'ancien '
            'thème, et la feuille sort du contrat de cache du shell.' % mecanisme)


def test_la_micro_copy_du_shell_vient_du_serveur(client):
    """Réécrire un libellé dans le DOM laisse DEUX vérités : celle que le
    serveur envoie et celle que l'utilisateur lit. Tout gardien qui lit les
    octets servis garde alors l'ancienne, et la nouvelle n'est gardée par rien.

    Le placeholder de recherche et le bouton principal étaient dans ce cas.
    """
    html = client.get('/').get_data(as_text=True)
    assert 'placeholder="Ticker, option ou page"' in html
    assert '>Analyser</span>' in html
    js = client.get('/static/vertex/js/signal-os.js').get_data(as_text=True)
    assert "search.placeholder" not in js, (
        'la couche JS réécrit de nouveau le placeholder : le serveur et l\'écran '
        'ne disent plus la même chose.')


def test_le_service_worker_a_ete_purge_pour_cette_couche(client):
    """Le HTML de shell a changé ET une feuille servie s'y ajoute : sans bump,
    un visiteur hors-ligne garde un shell qui ignore Signal OS."""
    sw = client.get('/sw.js').get_data(as_text=True)
    m = re.search(r"const CACHE='td-shell-v(\d+)'", sw)
    assert m, 'version du cache introuvable'
    assert int(m.group(1)) >= 207, (
        'version servie v%s — le shell de ce lot exige au moins v207'
        % m.group(1))
