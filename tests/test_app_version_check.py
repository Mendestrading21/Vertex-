"""SKYLER LOT 286 — gardien du verdict de version (carte Application).

Contrat : la carte compare deux versions RÉELLES — locale (caches de
l'appareil) et publiée (lue de /sw.js servi à l'instant, sans cache) —
et le badge dit « à jour » ou « mise à jour disponible ». Jamais de
numéro de version codé en dur (déjà gardé par le lot 284).
"""
from vertex.ui.pages import system_page


def _render_app_info():
    js = system_page._JS
    return js.split('async function renderAppInfo()', 1)[1].split('\nasync function ', 1)[0]


def test_server_version_read_from_sw_js_without_cache():
    body = _render_app_info()
    assert "fetch('/sw.js',{cache:'no-store'})" in body
    assert 'td-shell-v(\\d+)' in body


def test_verdict_compares_real_versions():
    body = _render_app_info()
    assert 'server>local' in body
    assert 'mise à jour disponible' in body and "'à jour'" in body
    # Absents → n/d honnête, jamais un verdict inventé.
    assert "'n/d'" in body
