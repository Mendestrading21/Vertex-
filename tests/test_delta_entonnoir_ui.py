"""tests/test_delta_entonnoir_ui.py — LOT 16 : delta d'entonnoir affiché.

Le lot 12 a livré `delta {entrants, sortants, premier_scan}` dans
/api/opportunities/funnel et consigné le branchement UI (« changements
depuis le dernier scan », contrat Radar). Nés ROUGES : la carte Entonnoir
ne rendait pas le delta.
"""
from vertex.ui.pages import opportunities_page


def _page():
    return opportunities_page.render()


def test_l_entonnoir_rend_le_delta():
    html = _page()
    assert 'fn.delta' in html, 'le delta du scan précédent doit être consommé'
    assert 'Entrés' in html and 'Sortis' in html


def test_le_premier_scan_est_honnete():
    html = _page()
    assert 'Premier scan' in html, (
        'pas de base de comparaison → le dire, jamais inventer un delta')
