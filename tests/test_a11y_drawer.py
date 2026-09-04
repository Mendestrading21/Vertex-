# -*- coding: utf-8 -*-
"""LOT 209 — gardiens d'accessibilité du drawer/modal du shell.

Observation du lot 206 (tour responsive) : les panneaux hors-canvas
FERMÉS restaient exposés aux lecteurs d'écran et au focus clavier.
Correctif : aria-hidden="true" + inert posés fermé (markup serveur),
retirés/reposés par openDrawer/closeDrawer et openModal/closeModal.
Ces gardiens figent le contrat — côté HTML servi ET côté source JS.
"""
import re
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHELL_JS = (ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'vx-shell.js').read_text(encoding='utf-8')


@pytest.fixture(scope='module')
def home_html():
    import terminal
    app = terminal.app
    with app.test_client() as c:
        r = c.get('/', follow_redirects=True)
        assert r.status_code == 200
        return r.get_data(as_text=True)


def _tag(html, el_id):
    m = re.search(r'<[a-z]+[^>]*id="' + re.escape(el_id) + r'"[^>]*>', html)
    assert m, f'élément #{el_id} absent du HTML servi'
    return m.group(0)


def test_drawer_ferme_est_aria_hidden_et_inert(home_html):
    tag = _tag(home_html, 'vx-drawer')
    assert 'data-open="0"' in tag
    assert 'aria-hidden="true"' in tag, 'le drawer fermé doit être invisible aux lecteurs d’écran'
    assert 'inert' in tag, 'le drawer fermé doit être infocusable (inert)'


def test_modal_ferme_est_aria_hidden_et_inert(home_html):
    tag = _tag(home_html, 'vx-modal')
    assert 'data-open="0"' in tag
    assert 'aria-hidden="true"' in tag
    assert 'inert' in tag


def test_drawer_garde_son_identite_dialogue(home_html):
    tag = _tag(home_html, 'vx-drawer')
    assert 'role="dialog"' in tag
    assert 'aria-modal="true"' in tag
    assert 'aria-label=' in tag


def test_le_js_bascule_aria_hidden_et_inert():
    # ouverture : les deux attributs sont RETIRÉS ; fermeture : reposés.
    assert "removeAttribute('aria-hidden')" in SHELL_JS
    assert "removeAttribute('inert')" in SHELL_JS
    assert "setAttribute('aria-hidden', 'true')" in SHELL_JS
    assert "setAttribute('inert', '')" in SHELL_JS
    # les deux panneaux passent par le même chemin (panelOpen/panelClose)
    assert SHELL_JS.count('panelOpen(') >= 3   # définition + drawer + modal
    assert SHELL_JS.count('panelClose(') >= 3


def test_fermeture_rend_le_focus():
    # le contrat existant (retour de focus) n'a pas été cassé par le lot
    assert 'lastFocus?.focus?.()' in SHELL_JS
