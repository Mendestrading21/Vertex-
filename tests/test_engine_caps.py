"""ENG-01 — gardien des PLAFONDS des moteurs (dans le CODE SERVI, pas la doc).

Deux bornes protègent l'utilisateur d'un excès de confiance et doivent tenir même sous
entrées extrêmes :
- Kelly ≤ 12 % (demi-Kelly capé — JAMAIS un sizing automatique).
- p_win ≤ 0,85 (humilité statistique, règle §6 : ne jamais promettre une quasi-certitude).

Régression (cap retiré/relâché) = test rouge.
"""
import inspect

import pytest

from vertex.engines.quant_engine import kelly_cap
from vertex.quant import ml_calibration
from vertex.quant.ml_calibration import predict


@pytest.mark.parametrize('edge,conf,rr', [
    (100, 100, 100), (95, 90, 50), (80, 80, 10), (100, 50, 3), (60, 70, 5),
])
def test_kelly_plafonne_a_12pct(edge, conf, rr):
    k = kelly_cap(edge, conf, rr)
    assert k is not None
    assert 0 <= k <= 12, f'Kelly non plafonné à 12 % : {k}'


def test_kelly_cap_reste_dans_le_code_servi():
    src = inspect.getsource(kelly_cap)
    assert '12' in src, 'le plafond Kelly 12 % doit vivre dans kelly_cap()'


@pytest.mark.parametrize('v', [
    {'trend_quality': 100, 'entry_quality': 100, 'rr': 100, 'expected_move': 100, 'institutionality': 100},
    {'trend_quality': 95, 'entry_quality': 90, 'rr': 80, 'expected_move': 90, 'institutionality': 85},
    {'trend_quality': 88, 'entry_quality': 92, 'rr': 70},
])
def test_p_win_plafonne_a_85pct(v):
    out = predict(v)
    assert 0.05 <= out['p_win'] <= 0.85, "p_win hors bornes : %s" % out['p_win']


def test_p_win_cap_reste_dans_le_code_servi():
    src = inspect.getsource(ml_calibration.predict)
    assert '0.85' in src, 'le plafond p_win 0,85 doit vivre dans predict()'
