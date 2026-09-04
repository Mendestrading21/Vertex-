"""tests/test_legende_treemap.py — LOT 19 : légende de treemap mensongère.

Mesuré au navigateur (desk 1 position, marques indisponibles) : le pavé
NVDA est ROUGE (repli concentration 100 % > 25 %) pendant que la légende
affirme « couleur = P&L latent (vert gagnant / rouge perdant / gris sans
marque) ». La couleur affirmait une perte non mesurée. Le repli est sain ;
la légende doit dire LES DEUX encodages. Né ROUGE.
"""
from vertex.ui.pages import portfolio_page


def test_la_legende_declare_le_repli_concentration():
    html = portfolio_page.render()
    assert 'sinon concentration' in html, (
        'quand aucune marque n\'existe, la couleur encode la concentration — '
        'la légende doit le dire, pas affirmer un P&L')
    assert 'gris sans marque' not in html, 'ancienne légende fausse (le repli ne rend pas gris)'
