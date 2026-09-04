"""
LOT 156 — Caractérisation de la structure de marché par pivots
(`vertex/quant/pivots.py`, ratio 0.65 — `structure()` est appelée par
analysis.py : c'est elle qui fournit le stop STRUCTUREL et la logique
d'entrée du plan de trade).

Ces tests figent les 5 signaux, les gardes, le repli d'ATR et le
contrat — les changer devient une décision explicite. Zigzags
synthétiques déterministes (aucun aléa).
"""

import numpy as np
import pandas as pd

from vertex.quant import pivots


def _df(close):
    close = np.asarray(close, float)
    idx = pd.date_range('2024-01-01', periods=len(close), freq='D')
    c = pd.Series(close, index=idx)
    return pd.DataFrame({'High': c + 1.0, 'Low': c - 1.0, 'Close': c}, index=idx)


def _zig(base, amp, slope, n_legs=8, leg=10):
    # Zigzag : jambes alternées ±amp autour d'une pente — sommets/creux nets.
    out, lvl = [], base
    for i in range(n_legs):
        d = 1 if i % 2 == 0 else -1
        for _ in range(leg):
            lvl += d * amp / leg + slope / leg
            out.append(lvl)
    return out


UP = _zig(100, 6, 4)        # sommets ET creux montants → UP
DOWN = _zig(200, 6, -4)     # descendants → DOWN
FLAT = _zig(150, 6, 0)      # ni l'un ni l'autre → RANGE


# ── Les 5 signaux ────────────────────────────────────────────────────────────

def test_tendance_up_milieu_de_mouvement_pas_d_entree():
    d = pivots.structure(_df(UP), atr=2.0)
    assert d['trend'] == 'UP' and d['signal'] == 'EN_TENDANCE'
    assert d['confirmed'] is False and d['entry'] is None
    assert 'attendre' in d['logic']          # pas d'entrée optimale → patienter


def test_tendance_down_refus_jamais_d_achat():
    d = pivots.structure(_df(DOWN), atr=2.0)
    assert d['trend'] == 'DOWN' and d['signal'] == 'REFUS_DOWNTREND'
    assert d['confirmed'] is False
    assert d['entry'] is None and d['stop'] is None and d['target'] is None
    assert 'piège' in d['logic']             # un rebond en downtrend = piège


def test_range_achat_seulement_sur_cassure():
    d = pivots.structure(_df(FLAT), atr=2.0)
    assert d['trend'] == 'RANGE' and d['signal'] == 'RANGE'
    assert 'cassure confirmée' in d['logic']


def test_breakout_recent_entree_stop_structurel_cible_extension():
    # Clôture qui franchit le dernier sommet RÉCEMMENT (≤ 1.2 ATR au-dessus,
    # sous le sommet il y a < 7 séances) → vraie cassure, sans chasser.
    base = pivots.structure(_df(UP), atr=2.0)
    seq = np.linspace(UP[-1], base['last_high'] + 0.5, 5).tolist()
    d = pivots.structure(_df(UP + seq), atr=2.0)
    assert d['signal'] == 'BREAKOUT' and d['confirmed'] is True
    assert d['entry'] is not None
    assert d['stop'] < d['last_low']                      # stop SOUS le dernier creux
    # cible = extension (measured move) : sommet + (sommet − creux)
    assert d['target'] == round(d['last_high'] + (d['last_high'] - d['last_low']), 2)
    assert d['rr'] == round((d['target'] - d['entry']) / (d['entry'] - d['stop']), 1)


def test_repli_repris_support_puis_reprise():
    # Repli vers le dernier creux (≤ 1.8 ATR) PUIS clôture en reprise
    # (last > prev) → entrée à moindre risque, cible le dernier sommet.
    seq = np.linspace(UP[-1], 125.0, 7).tolist() + [125.6]
    d = pivots.structure(_df(UP + seq), atr=2.0)
    assert d['signal'] == 'REPLI_REPRIS' and d['confirmed'] is True
    assert 0 <= d['dist_to_low_atr'] <= 1.8
    assert d['target'] == d['last_high']                  # cible = le sommet
    assert d['stop'] < d['last_low']
    assert d['rr'] is not None and d['rr'] > 0
    assert 'PUIS reprise' in d['logic']


# ── Gardes et replis ─────────────────────────────────────────────────────────

def test_gardes_serie_courte_et_entree_invalide():
    assert pivots.structure(_df([1, 2, 3, 4, 5]), atr=1.0) is None  # < 2k+5 barres
    assert pivots.structure('pas-un-df', atr=1.0) is None            # pas de colonnes


def test_atr_absent_repli_1_pct_du_dernier_cours():
    # atr None/0 → repli à 1 % du dernier cours : les distances restent
    # calculables, jamais de division par zéro.
    d = pivots.structure(_df(UP), atr=None)
    assert d is not None and d['signal'] == 'EN_TENDANCE'
    assert d['dist_to_low_atr'] > 0


# ── Contrat de sortie ────────────────────────────────────────────────────────

def test_contrat_et_fenetres_swing():
    d = pivots.structure(_df(UP), atr=2.0)
    assert set(d) == {'trend', 'signal', 'confirmed', 'last_high', 'last_low',
                      'n_highs', 'n_lows', 'dist_to_high_atr', 'dist_to_low_atr',
                      'entry', 'stop', 'target', 'rr', 'logic',
                      'swing_highs', 'swing_lows'}
    assert len(d['swing_highs']) <= 4 and len(d['swing_lows']) <= 4  # fenêtres bornées
    assert d['swing_highs'] == sorted(d['swing_highs'])   # zigzag UP → sommets montants
    assert d['last_high'] == d['swing_highs'][-1]
    assert d['last_low'] == d['swing_lows'][-1]
