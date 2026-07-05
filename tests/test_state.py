"""
tests/test_state.py — État partagé du scan (domicile unique).

scan_state vit dans vertex/app/state.py ; terminal.py et les Blueprints
importent LE MÊME objet, muté en place par la boucle de scan.
"""

from vertex.app import state


def test_scan_state_has_expected_keys():
    for k in ('rows', 'detail', 'options_board', 'market_ctx', 'recommendations',
              'committee', 'updated', 'error'):
        assert k in state.scan_state


def test_terminal_shares_the_same_object():
    import terminal
    assert terminal.scan_state is state.scan_state       # même référence, pas une copie


def test_mutation_is_visible_across_importers():
    # Muter en place via un module → visible via l'autre (référence partagée).
    import terminal
    marker = object()
    terminal.scan_state['__probe__'] = marker
    try:
        assert state.scan_state.get('__probe__') is marker
    finally:
        terminal.scan_state.pop('__probe__', None)


def test_blueprint_reads_the_shared_state():
    # La route Blueprint /api/brief lit l'état partagé injecté au démarrage.
    import terminal
    terminal.scan_state.setdefault('rows', [])
    r = terminal.app.test_client().get('/api/brief')
    assert r.status_code == 200 and 'setups' in r.get_json()
