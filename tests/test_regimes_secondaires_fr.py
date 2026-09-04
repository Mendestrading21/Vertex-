"""tests/test_regimes_secondaires_fr.py — LOT 29 : jeton anglais brut.

Mesuré au navigateur (mode démo peuplé) : la carte Régime de Marchés
affichait « aussi YIELD_CURVE_INVERTED » — le jeton interne du moteur de
régimes rendu tel quel. Les 5 signaux secondaires du moteur ont un
libellé français ; un jeton inconnu futur retombe sur le libellé du
régime principal s'il en est un, sinon reste affiché tel quel (honnête,
jamais masqué). Né ROUGE.
"""
from vertex.ui.pages import markets_page


def test_les_signaux_secondaires_ont_un_libelle_francais():
    html = markets_page.render()
    assert 'SECONDARY_LABEL' in html
    for jeton, fr in (('YIELD_CURVE_INVERTED', 'Courbe des taux inversée'),
                      ('YIELD_CURVE_STEEP', 'Courbe des taux pentue'),
                      ('BREADTH_DIVERGENCE', 'Divergence de participation'),
                      ('DOLLAR_STRENGTHENING', 'Dollar en renforcement'),
                      ('DOLLAR_WEAKENING', 'Dollar en affaiblissement')):
        assert jeton in html and fr in html, jeton
