"""tests/test_mediane_sectorielle.py — LOT 17 : [object Object] à l'écran.

Mesuré au navigateur (dossier /analysis/NVDA, fondamentaux absents) :
« Médiane sectorielle P/E : [object Object] ». Cause :
`t.sector_median.median_pe ?? t.sector_median` — quand la médiane est un
dict VIDE ({}), le repli rend l'objet lui-même. Né ROUGE.
"""
from vertex.ui.pages import analysis_page


def test_la_mediane_sectorielle_ne_rend_jamais_l_objet():
    html = analysis_page.render(sym='NVDA')
    assert '??t.sector_median)' not in html.replace(' ', ''), (
        'le repli sur l\'objet entier rend « [object Object] » à l\'écran')
    #  la valeur ne se rend que numérique, sinon absente (kv → n/d)
    assert 'sector_median.median_pe!=null' in html.replace(' ', '')
