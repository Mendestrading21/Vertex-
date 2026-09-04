"""SKYLER LOT 294 — gardien de la cible tactile des contrôles segmentés.

Contrat : les boutons `.vx-segmented button` (réglages Système :
densité, navigation, animations) mesuraient 26px de haut à 390px —
hors de la règle tactile mobile car sans classe vx-btn. En ≤640px ils
reçoivent min-height:40px, aligné sur `.vx-btn,.vx-tab,.vx-chip`.
"""

RESPONSIVE_CSS = 'vertex/static/vertex/css/responsive.css'


def test_segmented_buttons_touch_target_on_mobile():
    with open(RESPONSIVE_CSS, encoding='utf-8') as f:
        mobile = f.read().split('@media (max-width:640px)', 1)[1]
    assert '.vx-segmented button{min-height:40px}' in mobile


def test_general_touch_rule_still_present():
    with open(RESPONSIVE_CSS, encoding='utf-8') as f:
        mobile = f.read().split('@media (max-width:640px)', 1)[1]
    assert '.vx-btn,.vx-tab,.vx-chip{min-height:40px}' in mobile
