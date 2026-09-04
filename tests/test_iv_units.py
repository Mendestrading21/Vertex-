"""tests/test_iv_units.py — SKYLER LOT 114 : frontière d'unités IV figée.

Trou réel de couverture : vertex/options/iv_units.py — la FRONTIÈRE de
normalisation née du grand défaut « IV % vs décimal » (contrat
OPTIONS_CORRECTNESS : plus jamais d'heuristique silencieuse dans le
cœur). Seules 4 assertions existaient (test_options_correctness) :
la porte legacy from_legacy_board — détection ÉTIQUETÉE, jamais muette —
et les rejets NaN/inf n'étaient figés nulle part.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
import pytest

from vertex.options import iv_units as U


def test_unknown_unit_raises_a_guessed_unit_is_a_bug():
    for bad in ('BANANES', None, 'percent', ''):
        with pytest.raises(ValueError):
            U.normalize_iv(0.4, bad)


def test_normalize_rejects_nan_inf_and_nonpositive():
    for garbage in (float('nan'), float('inf'), float('-inf'), 0, -0.3,
                    None, 'texte'):
        assert U.normalize_iv(garbage, U.DECIMAL) is None, garbage
        assert U.normalize_iv(garbage, U.PERCENT) is None, garbage


def test_normalize_exact_conversions():
    assert U.normalize_iv(40.4, U.PERCENT) == pytest.approx(0.404)
    assert U.normalize_iv(0.404, U.DECIMAL) == pytest.approx(0.404)
    assert U.normalize_iv('40.4', U.PERCENT) == pytest.approx(0.404), (
        'valeur textuelle numérique acceptée — le float fait foi')


def test_legacy_board_percent_detected_and_labelled():
    iv, unit, warning = U.from_legacy_board(40.4)
    assert iv == pytest.approx(0.404) and unit == U.PERCENT
    assert 'POURCENTAGE' in warning and 'from_legacy_board' in warning, (
        'la détection se DIT — jamais une conversion muette')


def test_legacy_board_decimal_passes_through_without_warning():
    iv, unit, warning = U.from_legacy_board(0.404)
    assert iv == pytest.approx(0.404) and unit == U.DECIMAL
    assert warning is None


def test_legacy_threshold_boundary_is_exact():
    at, unit_at, warn_at = U.from_legacy_board(1.5)
    assert at == 1.5 and unit_at == U.DECIMAL and warn_at is None, (
        '1.5 pile = décimal (150 % de vol, rare mais réel)')
    above, unit_above, warn_above = U.from_legacy_board(1.51)
    assert above == pytest.approx(0.0151) and unit_above == U.PERCENT
    assert warn_above is not None


def test_legacy_board_garbage_is_triple_none():
    for garbage in (None, 'texte', float('nan'), float('inf'), 0, -2):
        assert U.from_legacy_board(garbage) == (None, None, None), garbage


def test_units_are_the_only_two_and_exported():
    assert U.PERCENT == 'PERCENT' and U.DECIMAL == 'DECIMAL'
    assert set(U.__all__) == {'PERCENT', 'DECIMAL', 'normalize_iv',
                              'from_legacy_board'}, (
        'la frontière n\'exporte que ses deux portes — pas d\'heuristique cachée')
