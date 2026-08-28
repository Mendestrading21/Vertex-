"""tests/test_badge_sante_lot20.py — LOT 20 : le badge de santé sur-affirmait.

Mesuré au navigateur : l'en-tête Système affichait « Opérationnel ·
8 moteurs » (vert) pendant que la jauge de la même page disait « 0/8
moteurs opérationnels » et le héros « Système partiellement dégradé ».
Cause : /healthz est une sonde de VIE (status='ok' = le process répond,
par conception — épinglé par test_healthz_and_readyz_are_distinct) et le
badge la traduisait en état opérationnel global + un compte de moteurs
DÉCLARÉS lu comme des moteurs SAINS. Nés ROUGES.
"""
from vertex.ui.pages import system_page


def _page():
    return system_page.render()


def test_le_badge_lit_readyz_pas_la_sonde_de_vie():
    html = _page()
    assert "VX.fetch('/readyz'" in html, (
        'l\'état global doit venir des vérifications réelles (/readyz), '
        'pas de la sonde de vie')


def test_le_badge_ne_compte_plus_les_moteurs_declares():
    html = _page()
    #  le mensonge mesuré : « Opérationnel · N moteurs » depuis hz.engines
    #  (une liste de noms DÉCLARÉS, pas un état).
    assert "hz.engines" not in html.replace(' ', '') or \
           "moteur'+(n>1?'s':'')" not in html, (
        'le compte de moteurs déclarés ne peut plus se lire comme un état sain')
