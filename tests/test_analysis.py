"""
tests/test_analysis.py — Cœur analytique (OHLCV → fiche technique).

Test de non-régression « golden » : sur un DataFrame déterministe, analyse()
doit produire exactement les mêmes valeurs qu'avant son extraction du monolithe.
Toute dérive de la logique quant fera échouer ce test.
"""

import numpy as np
import pandas as pd
from vertex.engines import analysis


def _fixture_df():
    idx = pd.date_range('2024-01-01', periods=260, freq='D')
    base = np.linspace(80, 130, 260) + 6 * np.sin(np.linspace(0, 20, 260))
    close = pd.Series(base, index=idx)
    return pd.DataFrame({
        'Open': close.shift(1).fillna(close.iloc[0]),
        'High': close + 1.5, 'Low': close - 1.5, 'Close': close,
        'Volume': pd.Series(np.linspace(1e6, 2e6, 260) + 5e5 * np.sin(np.linspace(0, 30, 260)), index=idx),
    }, index=idx)


_FUND = {'beta': 1.3, 'div': 0.01, 'sector': 'Technology', 'pe': 25, 'margin': 0.2, 'growth': 0.15}


def test_golden_scalar_values():
    r = analysis.analyse(_fixture_df(), 0.05, fund=_FUND)
    assert r['score'] == 82
    assert r['grade'] == 'S'
    assert r['verdict'] == 'BUY'
    assert r['regime'] == 'NEUTRAL'
    assert r['trend'] == 100
    assert r['rs'] == 64
    assert r['profile'] == 'OFFENSIF'
    assert r['anomaly_lvl'] == 'CALME'
    assert r['base_score'] == 72
    assert r['struct_adj'] == 10
    assert r['setup_quality'] == 46


def test_golden_plan():
    plan = analysis.analyse(_fixture_df(), 0.05, fund=_FUND)['plan']
    assert plan['entry'] == 135.48
    assert plan['stop'] == 127.98
    assert plan['tp2'] == 150.48
    assert plan['resistance'] == 136.98
    assert plan['stop_type'] == 'ATR (plafond risque)'


def test_output_is_json_safe():
    # Aucun NaN : le JSON de /scan ne doit jamais casser.
    import json
    r = analysis.analyse(_fixture_df(), 0.05, fund=_FUND)
    s = json.dumps({k: v for k, v in r.items() if k not in ('physics', 'vertex', 'mtf', 'structure')},
                   default=str)
    assert 'NaN' not in s


def test_terminal_binding_is_the_module():
    import terminal
    assert terminal.analyse is analysis.analyse
