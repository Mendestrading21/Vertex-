"""Lot 45 — les rows PUBLIÉS ne sont jamais mutés en place (dette du lot 42).

Le lot 42 a rendu les publications de scan atomiques et générationnées, et a
NOMMÉ la dette restante : les objets publiés restaient partagés — la boucle
options (`_publish_board`) mutait `scan_state['rows']` en place pour
rafraîchir le verdict véhicule, et le chemin démo remutait `rows` APRÈS la
publication partielle. Un lecteur (route Flask, autre thread) pouvait voir un
même objet changer sous ses yeux entre deux générations.

Contrat de ce lot : une mise à jour du board REPUBLIE une copie — l'objet
déjà publié reste figé, la publication passe par `_publier` (bloc atomique,
même cycle : génération et phase conservées).
"""
import terminal
from vertex.app.state import scan_state


def test_le_board_ne_mute_pas_les_rows_deja_publies():
    anciens = [{'symbol': 'NVDA', 'score': 80}, {'symbol': 'MSFT', 'score': 70}]
    sauv = {k: scan_state.get(k) for k in ('rows', 'detail', 'scan_gen', 'scan_phase')}
    try:
        scan_state.update({'rows': anciens, 'detail': {}, 'scan_gen': 7,
                           'scan_phase': 'complet'})
        focus = [{'sym': 'NVDA', 'exp': '2027-01-15', 'strike': 190.0,
                  'type': 'CALL', 'quality': 71, 'cost': 3000}]
        terminal._publish_board(focus)
        #  1. l'objet publié AVANT reste figé — aucun verdict injecté dedans
        assert all('vehicle' not in r for r in anciens), (
            'la liste déjà publiée a été mutée en place — un lecteur du '
            'cycle précédent voit son snapshot changer')
        #  2. la republication est une COPIE porteuse du verdict
        assert scan_state['rows'] is not anciens
        assert any(r.get('vehicle') for r in scan_state['rows'])
        #  3. même cycle : génération et phase conservées
        assert scan_state['scan_gen'] == 7
        assert scan_state['scan_phase'] == 'complet'
    finally:
        scan_state.update(sauv)


def test_le_board_est_publie_atomiquement():
    """Plus d'écritures à l'unité dans _publish_board : board, horodatage,
    snapshot de suivi et rows partent dans UN bloc `_publier`."""
    src = open('terminal.py', encoding='utf-8').read()
    seg = src.split('def _publish_board', 1)[1].split('\ndef ', 1)[0]
    for interdit in ("scan_state['options_board'] =",
                     "scan_state['options_as_of'] =",
                     "scan_state['option_tracking_snapshot'] ="):
        assert interdit not in seg, (
            'écriture à l\'unité dans _publish_board : %s — un lecteur peut '
            'voir un board sans horodatage' % interdit)
    assert '_publier(' in seg


def test_le_chemin_demo_ne_remute_pas_apres_publication():
    """Le bloc démo de _scan_once copie rows avant d'attacher le verdict, et
    republie la copie dans son bloc."""
    src = open('terminal.py', encoding='utf-8').read()
    i = src.index('VITRINE : board d’options synthétique') if 'VITRINE : board d’options synthétique' in src else src.index('VITRINE')
    seg = src[i:i + 900]
    assert 'dict(r) for r in rows' in seg, (
        'le chemin démo doit copier rows avant _attach_vehicle — la liste '
        'publiée en amont ne doit plus être mutée')
    assert "'rows': rows" in seg, (
        'la copie porteuse du verdict doit être REPUBLIÉE dans le bloc démo')
