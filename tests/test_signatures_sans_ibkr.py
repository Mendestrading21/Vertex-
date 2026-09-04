"""tests/test_signatures_sans_ibkr.py — LOT 25 : dette de signatures.

La frontière IBKR market-data-only est tenue depuis le lot 2 (tous les
appelants passent None), mais les SIGNATURES portaient encore un paramètre
`ibkr_positions` et `repository.load_positions` gardait la branche morte
qui aurait construit des positions depuis un compte courtier. Une dette
pareille est une invitation : le paramètre disparaît. Nés ROUGES.
"""
import inspect


def test_load_positions_ne_prend_plus_de_positions_courtier():
    from vertex.positions.repository import load_positions
    params = list(inspect.signature(load_positions).parameters)
    assert 'ibkr_positions' not in params, (
        'le paramètre ibkr_positions doit disparaître — le portefeuille est '
        'déclaré par l\'utilisateur, jamais lu chez le courtier')
    src = inspect.getsource(load_positions)
    assert 'IBKR:' not in src, 'la branche qui fabriquait des positions IBKR doit mourir'


def test_recalculate_all_sans_ibkr():
    from vertex.positions.recalculator import recalculate_all
    assert 'ibkr_positions' not in inspect.signature(recalculate_all).parameters


def test_detector_sans_ibkr():
    from vertex.positions import detector
    for fn in ('startup_position_report',):
        f = getattr(detector, fn)
        assert 'ibkr_positions' not in inspect.signature(f).parameters, fn
