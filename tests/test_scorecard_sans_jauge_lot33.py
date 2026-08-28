"""tests/test_scorecard_sans_jauge_lot33.py — LOT 33 : la scorecard boiteuse.

Mesuré au navigateur (portefeuille peuplé SANS marques — IBKR hors
ligne) : les 4 tuiles KPI s'empilent dans une colonne de ~190 px et la
moitié droite de la carte reste vide. Cause : la grille est figée à
`auto minmax(0,1fr)` — sans jauge (pas de marques), les tuiles tombent
dans la colonne `auto`. La grille doit suivre la présence de la jauge.
Né ROUGE.
"""
from vertex.ui.pages import portfolio_page


def test_la_grille_suit_la_presence_de_la_jauge():
    html = portfolio_page.render()
    assert "grid-template-columns:auto minmax(0,1fr)\"" not in html.replace("'", '"'), (
        'grille figée : sans jauge, les tuiles tombent dans la colonne auto '
        '(~190 px mesurés) et la moitié de la carte reste vide')
    assert "gauge?'auto minmax(0,1fr)':'minmax(0,1fr)'" in html.replace('"', "'"), (
        'la grille se déclare selon la présence réelle de la jauge')
