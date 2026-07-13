"""Tests — Tactile Command Surface (addendum contrôles).

Vérifie la couche CSS de contrôle, la page de démonstration READONLY et l'absence
de tout chemin d'ordre dans les nouveaux fichiers.
"""
import os
import re

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(ROOT, 'vertex', 'static', 'vertex', 'css', 'control-surface.css')
DEMO = os.path.join(ROOT, 'vertex', 'ui', 'pages', 'design_system_demo.py')


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def test_control_surface_css_exists():
    assert os.path.isfile(CSS)
    src = open(CSS, encoding='utf-8').read()
    # tokens de contrôle + matériaux tactiles présents
    for needle in ('--vx-shadow-raised', '--vx-shadow-pressed', '--vx-shadow-copper',
                   'vx-btn-primary', 'aria-pressed="true"', ':focus-visible',
                   'prefers-reduced-motion'):
        assert needle in src, needle


def test_control_surface_loaded_in_shell():
    shell = open(os.path.join(ROOT, 'vertex', 'ui', 'shell', '__init__.py'), encoding='utf-8').read()
    assert 'control-surface.css' in shell


def test_primary_button_relief_limited():
    """Le relief copper vise .vx-btn-primary ; ghost/link restent plats."""
    src = open(CSS, encoding='utf-8').read()
    assert '.vx-btn-ghost,.vx-btn-link{box-shadow:none}' in src.replace(' ', '')


def test_design_system_route_renders(client):
    r = client.get('/system/design-system')
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert 'Command Surface' in html
    assert 'vx-btn-primary' in html and 'vx-chip' in html and 'vx-segmented' in html


def test_disabled_button_explains_reason(client):
    html = client.get('/system/design-system').get_data(as_text=True)
    # bouton désactivé avec explication en tooltip
    assert re.search(r'disabled[^>]*title="[^"]+"', html) or re.search(r'title="[^"]+"[^>]*disabled', html)


def test_reduced_motion_respected():
    src = open(CSS, encoding='utf-8').read()
    assert 'prefers-reduced-motion:no-preference' in src.replace(' ', '')


def test_no_order_path_in_demo():
    src = open(DEMO, encoding='utf-8').read()
    for w in ('place_order', 'submit_order', 'transmit_order', 'cancel_order',
              'exercise_option', 'auto_execute'):
        assert w not in src
