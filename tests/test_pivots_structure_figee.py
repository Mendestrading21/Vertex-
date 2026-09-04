"""tests/test_pivots_structure_figee.py — SKYLER LOT 93 : pivots/structure figé.

`vertex/quant/pivots.py` (la structure de marché par pivots fractals —
elle nourrit committee.py et la zone d'achat du lot 92) n'avait AUCUN
test dédié. Caractérisations nées vertes (dites) sur séries synthétiques
déterministes — moteur INTACT.
"""
import pandas as pd

from vertex.quant import pivots


def _df(closes):
    return pd.DataFrame({'Close': closes,
                         'High': [c + 0.5 for c in closes],
                         'Low': [c - 0.5 for c in closes]})


# Zigzag haussier : sommets 10→12→14 montants, creux 6→8→10 montants (k=3).
UP = [5, 6, 7, 8, 10, 9, 8, 7, 6, 7, 8, 9, 12, 11, 10, 9, 8, 9, 10, 11,
      14, 13, 12, 11, 10, 11, 12, 13]


def test_invalid_inputs_return_none():
    assert pivots.structure(None, 1) is None
    assert pivots.structure(pd.DataFrame({'Close': [1, 2, 3]}), 1) is None
    assert pivots.structure(_df([1] * 8), 1) is None, 'série trop courte → None'


def test_uptrend_detected_mid_move_waits():
    st = pivots.structure(_df(UP), atr=1.0)
    assert st['trend'] == 'UP'
    assert st['signal'] == 'EN_TENDANCE' and st['confirmed'] is False
    assert 'attendre la cassure' in st['logic']


def test_downtrend_rebound_is_refused():
    down = [c * -1 + 30 for c in UP]      # miroir : sommets/creux descendants
    st = pivots.structure(_df(down), atr=1.0)
    assert st['trend'] == 'DOWN'
    assert st['signal'] == 'REFUS_DOWNTREND' and st['confirmed'] is False
    assert 'piège' in st['logic']


def test_fresh_breakout_confirmed_with_measured_move():
    st = pivots.structure(_df(UP + [14, 14.9, 15.2]), atr=1.0)
    assert st['signal'] == 'BREAKOUT' and st['confirmed'] is True
    assert st['entry'] == 15.2
    assert st['stop'] < st['last_low'], 'stop SOUS le dernier creux'
    assert st['target'] == round(st['last_high'] + (st['last_high'] - st['last_low']), 2)
    assert st['rr'] == round((st['target'] - st['entry']) / (st['entry'] - st['stop']), 1)


def test_extended_breakout_is_not_chased():
    st = pivots.structure(_df(UP + [14, 15.5, 16.5]), atr=1.0)
    assert st['signal'] != 'BREAKOUT', '> 1,2 ATR au-dessus du sommet → on ne court pas'
    assert st['confirmed'] is False


def test_pullback_resumed_confirms_entry():
    st = pivots.structure(_df(UP[:-2] + [10.4, 10.8]), atr=1.0)
    assert st['trend'] == 'UP'
    assert st['signal'] == 'REPLI_REPRIS' and st['confirmed'] is True
    assert st['target'] == st['last_high'], 'cible = dernier sommet'


def test_range_requires_confirmed_break():
    flat = [5, 6, 7, 8, 10, 9, 8, 7, 6, 7, 8, 9, 10, 9, 8, 7, 6, 7, 8, 9,
            10, 9, 8, 7, 6, 7, 8, 9]     # mêmes sommets (10) et creux (6)
    st = pivots.structure(_df(flat), atr=1.0)
    assert st['trend'] == 'RANGE' and st['signal'] == 'RANGE'
    assert st['confirmed'] is False
    assert 'cassure confirmée' in st['logic']


def test_missing_atr_falls_back_never_crashes():
    st = pivots.structure(_df(UP), atr=None)
    assert st is not None and st['trend'] == 'UP'
    st0 = pivots.structure(_df(UP), atr=0)
    assert st0 is not None, 'ATR 0 → repli 1 % du prix, jamais de division par zéro'
