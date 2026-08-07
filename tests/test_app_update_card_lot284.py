"""SKYLER LOT 284 — gardien de la carte « Application » (Système → Réglages).

Contrat : la version du shell affichée est LUE des caches réels du
navigateur (jamais un numéro codé en dur dans la page) ; la mise à jour
forcée vide SW + caches puis recharge, et ne touche JAMAIS localStorage
(les données desk survivent).
"""
import re

from vertex.ui.pages import system_page


def _settings_html():
    return system_page.render('settings')


def _js():
    return system_page._JS


def test_app_card_present_only_in_settings():
    html = _settings_html()
    assert 'id="vx-app-update"' in html and 'aria-label="Application"' in html
    assert 'Aucune donn&eacute;e desk n&#8217;est touch&eacute;e' in html
    # Domicile unique : la CARTE ne vit que dans Réglages (le JS de page,
    # lui, est partagé entre les vues — on teste le HTML, pas le script).
    assert 'aria-label="Application"' not in system_page._VIEW_CONTENT['connections']


def test_shell_version_is_read_from_caches_not_hardcoded():
    js = _js()
    assert 'caches.keys()' in js and 'td-shell-v(\\d+)' in js
    # Aucun numéro de version en dur dans la page (la vérité vit dans le SW).
    assert not re.search(r'td-shell-v\d', js)


def test_force_update_clears_sw_and_caches_without_touching_desk():
    js = _js()
    body = js.split('async function forceAppUpdate()', 1)[1].split('\nfunction ', 1)[0]
    assert 'unregister()' in body and 'caches.delete' in body
    assert 'location.reload()' in body
    assert 'localStorage' not in body  # les données desk restent intactes
