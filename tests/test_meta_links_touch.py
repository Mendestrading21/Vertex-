"""SKYLER LOT 293 — gardien de la cible tactile des liens d'approfondissement.

Contrat : les liens dans les lignes `vx-meta` (« Calendrier complet → »,
« Risque complet → », « Journal complet → »…) mesuraient 15px de haut à
390px — quasi intappables au pouce. En mobile (≤640px) ils reçoivent un
padding vertical qui porte la cible à ≥40px (15 + 2×13 = 41).
"""

RESPONSIVE_CSS = 'vertex/static/vertex/css/responsive.css'


def test_meta_links_touch_target_on_mobile():
    with open(RESPONSIVE_CSS, encoding='utf-8') as f:
        mobile = f.read().split('@media (max-width:640px)', 1)[1]
    assert '.vx-meta a{display:inline-block;padding:13px 0}' in mobile


def test_deep_links_still_exist():
    # Les 3 liens d'approfondissement de la fiche Analyse restent en place.
    with open('vertex/ui/pages/analysis_page.py', encoding='utf-8') as f:
        src = f.read()
    assert 'Calendrier complet' in src
    assert 'Risque complet' in src
    assert 'Journal complet' in src
