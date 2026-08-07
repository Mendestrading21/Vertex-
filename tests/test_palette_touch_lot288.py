"""SKYLER LOT 288 — gardien du chemin TACTILE vers la palette de commandes.

Contrat : sur iPhone il n'y a pas de ⌘K — l'affordance réelle est le tap
sur le champ de recherche du topbar (clic ET focus câblés sur openPalette
dans vx-shell.js). En mobile (≤640px), la pastille « ⌘K » est masquée :
c'est une affordance clavier mensongère au tactile, et elle mangeait
~30px d'un champ mesuré à 93px sur 390px.
"""
import re

SHELL_JS = 'vertex/static/vertex/js/vx-shell.js'
RESPONSIVE_CSS = 'vertex/static/vertex/css/responsive.css'


def _read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def test_search_field_opens_palette_on_tap():
    js = _read(SHELL_JS)
    assert "$('vx-global-search')?.addEventListener('click', openPalette)" in js
    # Le focus (clavier/lecteur d'écran) mène au même endroit.
    assert "addEventListener('focus'" in js.split("vx-global-search", 2)[1]


def test_kbd_hint_hidden_on_mobile():
    css = _read(RESPONSIVE_CSS)
    mobile = css.split('@media (max-width:640px)', 1)[1]
    assert re.search(r'\.vx-topbar-search \.vx-kbd\{display:none\}', mobile), (
        'la pastille ⌘K doit être masquée en mobile — affordance clavier '
        'mensongère au tactile')
