"""
LOT 153 — Caractérisation du contexte marché
(`vertex/market/context.py` — la « météo » du jour : régime SPY,
bandes VIX, Risk-On/Off, breadth, verdict ; servie par decision_api
et terminal ; AUCUN test direct avant ce lot).

Ces tests figent les bornes exactes des bandes, la robustesse aux
entrées dégradées et le contrat — les changer devient une décision
explicite. Données synthétiques déterministes (graine fixe).
"""

import numpy as np
import pandas as pd
import pytest

from vertex.market import context as ctx

IDX = pd.date_range('2024-01-01', periods=260, freq='D')


def _df(close):
    return pd.DataFrame({'Open': close.shift(1).fillna(close.iloc[0]),
                         'High': close + 1.5, 'Low': close - 1.5,
                         'Close': close}, index=close.index)


ROWS = [{'symbol': 'A', 'change': 1.0, 'verdict': 'BUY'},
        {'symbol': 'B', 'change': -0.5, 'verdict': 'WATCH'}]
DETAIL = {'A': {'signals': {'above50': True, 'above200': True}, 'pos52': 99},
          'B': {'signals': {'above50': False}, 'pos52': 3}}
SECS = [{'sector': 'Software', 'avg_score': 70}, {'sector': 'Sante', 'avg_score': 50}]


# ── Robustesse : tout dégradé, rien ne lève ──────────────────────────────────

def test_entrees_degradees_contrat_complet_et_verdict_honnete():
    d = ctx.context(None, None, None, None, None)
    assert set(d) == {'spy_regime', 'spy_trend_txt', 'spy_adx', 'vix', 'vix_band',
                      'vix_chg', 'roro', 'roro_gap', 'breadth', 'verdict'}
    assert d['spy_regime'] is None and d['vix'] is None and d['roro'] is None
    assert d['breadth'] == {}
    # Le verdict est quand même émis, avec « ?% » honnête (pas un chiffre
    # inventé) — comportement limite DOCUMENTÉ.
    assert d['verdict'] == 'MARCHÉ · participation ?% au-dessus MM50'


# ── Régime SPY ───────────────────────────────────────────────────────────────

def test_spy_tendance_et_texte_mm():
    d = ctx.context(_df(pd.Series(np.linspace(400, 600, 260), index=IDX)),
                    None, None, None, None)
    assert d['spy_regime'] == 'TREND'
    assert d['spy_trend_txt'] == 'au-dessus MM20 & MM50'
    assert d['spy_adx'] == 100          # rampe pure : direction unique


def test_spy_oscillation_chop():
    rng = np.random.default_rng(3)
    chop = pd.Series(500 + 8 * np.sin(np.linspace(0, 50, 260)) + rng.normal(0, 2, 260),
                     index=IDX)
    assert ctx.context(_df(chop), None, None, None, None)['spy_regime'] == 'CHOP'


# ── Bandes VIX : bornes EXACTES 16 / 22 ──────────────────────────────────────

@pytest.mark.parametrize('vix,band', [
    (15.9, 'calme'), (16.0, 'normal'), (21.9, 'normal'), (22.0, 'stress'),
])
def test_bandes_vix_exactes(vix, band):
    d = ctx.context(None, pd.Series([vix, vix]), None, None, None)
    assert d['vix'] == vix and d['vix_band'] == band
    assert d['vix_chg'] == 0.0


def test_vix_un_seul_point_none_honnete():
    # Il faut ≥ 2 points (pour la variation) — sinon aucun VIX affiché.
    assert ctx.context(None, pd.Series([15.0]), None, None, None)['vix'] is None


# ── Breadth : participation réelle sur les leaders ───────────────────────────

def test_breadth_participation_avancees_sommets_creux():
    b = ctx.context(None, None, ROWS, DETAIL, None)['breadth']
    assert b == {'above50': 50, 'above200': 50, 'adv': 1, 'dec': 1,
                 'nh': 1, 'nl': 1, 'buy': 50}   # pos52 99 ≥ 98 → nh ; 3 ≤ 5 → nl


# ── RORO : bornes EXACTES ±8 (cyclique vs défensif) ──────────────────────────

@pytest.mark.parametrize('cyclique,roro', [
    (58, 'RISK-ON'), (57, 'NEUTRE'), (43, 'NEUTRE'), (42, 'RISK-OFF'),
])
def test_roro_bornes_exactes_gap_8(cyclique, roro):
    secs = [{'sector': 'Software', 'avg_score': cyclique},
            {'sector': 'Sante', 'avg_score': 50}]
    d = ctx.context(None, None, None, None, secs)
    assert d['roro'] == roro
    assert d['roro_gap'] == cyclique - 50


def test_roro_sans_secteurs_neutre_defauts_50():
    d = ctx.context(None, None, None, None, [])
    assert d['roro'] == 'NEUTRE' and d['roro_gap'] == 0


# ── Verdict du jour : la phrase qui résume tout ──────────────────────────────

def test_verdict_complet_compose_toutes_les_briques():
    d = ctx.context(_df(pd.Series(np.linspace(400, 600, 260), index=IDX)),
                    pd.Series([15.0, 14.0]), ROWS, DETAIL, SECS)
    assert d['verdict'] == ('MARCHÉ EN TENDANCE · RISK-ON · '
                            'participation 50% au-dessus MM50 · VIX 14.0 (calme)')
