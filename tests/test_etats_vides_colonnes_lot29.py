"""tests/test_etats_vides_colonnes_lot29.py — LOT 29 : états vides écrasés.

Mesuré au navigateur (mode peuplé, NVDA hors scan) : les cartes
« Croissance × rentabilité » et « Chaîne — meilleurs contrats » du dossier
Analyse s'affichaient sur 95 px — leurs chemins d'état vide REMPLAÇAIENT
`host.className`, effaçant la classe de colonne (`vx-col-*`) de la grille
12 colonnes. Nés ROUGES : les états vides préservent le span.
"""
from vertex.ui.pages import analysis_page


def _html():
    return analysis_page.render(sym='NVDA')


def test_aucun_etat_vide_n_efface_la_classe_de_colonne():
    html = _html()
    assert "host.className=''" not in html, (
        'le quadrant vide effaçait vx-col-7 — carte à 95 px mesurée')
    assert "host.className='vx-card'" not in html, (
        'la chaîne vide effaçait son span de colonne')


def test_le_garde_de_span_est_utilise():
    assert '_gardeSpan' in _html(), (
        'un helper unique préserve vx-col-* sur les trois chemins d\'état vide')
