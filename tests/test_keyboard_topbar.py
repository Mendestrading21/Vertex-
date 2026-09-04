"""SKYLER LOT 302 — gardien du parcours clavier du topbar.

Contrat : le focus clavier sur le champ de recherche n'ouvre PLUS la
palette (mesuré : la palette s'ouvrait de force au Tab, capturait le
focus, et les 4 boutons du topbar — Ajouter, Connexions, Notifications,
Actualiser — étaient inatteignables au clavier). Les ouvertures : clic/
tap (tactile, lot 288) ou frappe dans le champ (le caractère saisi
amorce la recherche).
"""

SHELL_JS = 'vertex/static/vertex/js/vx-shell.js'


def _js():
    with open(SHELL_JS, encoding='utf-8') as f:
        return f.read()


def test_focus_does_not_open_palette():
    js = _js()
    assert "e.target.blur(); openPalette();" not in js
    # Aucun listener focus sur le champ de recherche.
    seg = js.split("$('vx-global-search')")
    assert all("addEventListener('focus'" not in s.split('\n')[0] for s in seg[1:])


def test_typing_opens_palette_with_seed():
    js = _js()
    assert "$('vx-global-search')?.addEventListener('keydown'" in js
    assert "if (e.key === 'Tab' || e.ctrlKey || e.metaKey || e.altKey) return;" in js
    assert "pInput.value = e.key; renderPalette(e.key);" in js
