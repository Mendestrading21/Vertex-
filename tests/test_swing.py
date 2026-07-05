"""
tests/test_swing.py — Projection swing d'options (rendement estimé ~1σ / 3 sem).

Non-régression golden + garde-fous : entrées invalides → (None, False),
la fenêtre lointaine + gain suffisant → swing_ok, jamais d'ordre.
"""

from vertex.engines import swing


def test_golden_projections():
    assert swing.project(100, 45, 0.55, 500, 0.9, 120) == (200, True)
    assert swing.project(50, 62, 0.4, 300, 0.35, 180) == (180, True)
    assert swing.project(200, 30, 0.6, 1200, 0.16, 400) == (117, True)


def test_invalid_inputs_are_safe():
    assert swing.project(0, 0, 0, 0, 0, 0) == (None, False)
    assert swing.project(None, None, None, None, None, None) == (None, False)


def test_short_dated_is_not_ok_even_if_profitable():
    # < 90j → swing_ok False même si le rendement est élevé (règle de sécurité)
    ret, ok = swing.project(100, 45, 0.5, 500, 0.9, 60)
    assert ret is not None and ok is False


def test_annotate_adds_fields():
    board = [{'sym': 'X', 'spot': 100, 'iv': 45, 'delta': 0.55, 'cost': 500, 'theta_burn': 0.9, 'dte': 120},
             {'sym': 'Y', 'iv': 30, 'delta': 0.6, 'cost': 1200, 'theta_burn': 0.16, 'dte': 400}]
    out = swing.annotate(board, {'Y': {'price': 200}})
    assert out[0]['swing_ret'] == 200 and out[0]['swing_ok'] is True
    assert 'swing_ret' in out[1] and 'swing_ok' in out[1]      # spot pris depuis le detail


def test_terminal_bindings_are_the_module():
    import terminal
    assert terminal._swing_project is swing.project
    assert terminal._annotate_swing is swing.annotate
