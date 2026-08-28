"""tests/test_diff_session_lot15.py — LOT 15 : carte « Ce qui a changé » morte.

Mesuré au navigateur (vérification phase D) : la carte #vx-diff de la page
Aujourd'hui portait un squelette PERPÉTUEL — aucun code ne la remplissait,
alors que le producteur réel existe (`market_context.changes_since_prev`,
« jamais inventé », déjà transporté par /scan). Nés ROUGES.
"""
from vertex.ui.pages import briefing


def _page():
    return briefing.render()


def test_vx_diff_a_un_remplisseur():
    html = _page()
    assert 'loadDiff' in html, (
        'la carte #vx-diff doit être remplie par la page — squelette '
        'perpétuel mesuré au navigateur sinon')
    assert 'changes_since_prev' in html, 'le producteur réel est le contexte marché'


def test_vx_diff_est_dans_l_orchestration():
    html = _page()
    #  l'appel doit être branché au boot (après le chargement du scan)
    assert 'loadDiff(scan)' in html


def test_le_noeud_mort_vx_mkt_diff_est_retire():
    """#vx-mkt-diff n'était rempli par personne non plus — retiré (test de
    retrait du blueprint : un widget sans producteur ne reste pas)."""
    assert 'vx-mkt-diff' not in _page()
