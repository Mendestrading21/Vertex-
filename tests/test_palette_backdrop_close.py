"""SKYLER LOT 291 — gardien de la fermeture tactile de la palette.

Contrat : la palette est un fond plein écran (`.vx-palette` =
position:fixed inset:0). Sans ce câblage, ses seules sorties étaient
Échap (inexistant au tactile) ou choisir un item — l'utilisateur iPhone
restait piégé. Le tap sur le fond (hors boîte) doit fermer, comme tout
dialogue.
"""

SHELL_JS = 'vertex/static/vertex/js/vx-shell.js'


def test_palette_backdrop_tap_closes():
    with open(SHELL_JS, encoding='utf-8') as f:
        js = f.read()
    assert ("palette?.addEventListener('click', "
            "(e) => { if (e.target === palette) palette.dataset.open = '0'; })") in js


def test_item_tap_still_closes():
    # La sortie existante (choisir un item) reste câblée.
    with open(SHELL_JS, encoding='utf-8') as f:
        js = f.read()
    assert "pItems[+el.dataset.idx]?.run(); palette.dataset.open = '0';" in js
