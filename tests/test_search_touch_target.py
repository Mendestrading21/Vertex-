"""SKYLER LOT 289 — gardien de la cible tactile du champ de recherche.

Contrat : le champ de recherche du topbar est LE chemin tactile vers la
palette de commandes (lot 288). En mobile (≤640px) il doit respecter la
même règle de cible tactile ≥40px que les boutons (mesuré avant : 33px
de haut à 390px), et l'icône loupe — calée en absolu pour un champ de
33px — doit se recentrer.
"""

RESPONSIVE_CSS = 'vertex/static/vertex/css/responsive.css'


def _mobile_block():
    with open(RESPONSIVE_CSS, encoding='utf-8') as f:
        return f.read().split('@media (max-width:640px)', 1)[1]


def test_search_input_meets_touch_target_on_mobile():
    mobile = _mobile_block()
    assert '.vx-topbar-search input{min-height:40px}' in mobile


def test_search_icon_recentered_on_mobile():
    mobile = _mobile_block()
    assert '.vx-topbar-search svg{top:50%;transform:translateY(-50%)}' in mobile
