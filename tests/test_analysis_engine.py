"""
LOT 146 — Caractérisation étendue du cœur analytique
(`vertex/engines/analysis.py`, 333 lignes).

Le golden existant (`tests/test_analysis.py`) fige UN scénario ; il ne
couvrait aucune des branches de détection : robustesse aux flux sans
volume, historique court, profils, radar d'anomalies, régime CHOP,
cassure confirmée, invariants du plan, transparence du score. Ces
tests figent le comportement observé — tout changement futur doit
faire échouer cette suite et être assumé explicitement.

DataFrames synthétiques déterministes — on caractérise des formes de
marché, pas des titres réels.
"""

import json

import numpy as np
import pandas as pd
import pytest

from vertex.engines import analysis

IDX = pd.date_range('2024-01-01', periods=260, freq='D')


def _df(close, vol=None, open_=None):
    return pd.DataFrame({
        'Open': open_ if open_ is not None else close.shift(1).fillna(close.iloc[0]),
        'High': close + 1.5, 'Low': close - 1.5, 'Close': close,
        **({'Volume': vol} if vol is not None else {}),
    }, index=close.index)


def _base():
    # Hausse régulière + oscillation : la fixture du golden.
    return pd.Series(np.linspace(80, 130, 260) + 6 * np.sin(np.linspace(0, 20, 260)), index=IDX)


def _flatvol():
    return pd.Series(np.full(260, 1e6), index=IDX)


# ── Robustesse d'entrée : jamais de KeyError, jamais de NaN servi ────────────

def test_flux_sans_colonne_volume_indices_etf_stooq():
    # Certains flux (indices/ETF) n'ont pas de Volume : repli volx=1.0,
    # série volume None — jamais de KeyError.
    r = analysis.analyse(_df(_base()), 0.05)
    assert r['volx'] == 1.0
    assert r['series']['volume'] is None
    assert r['score'] is not None


def test_historique_court_repli_ewm_jamais_nan():
    # 60 barres < fenêtres SMA 50/200 partielles : repli sur l'EWM — la
    # fiche sort complète et JSON-sûre (les titres récemment cotés ne
    # cassent pas /scan).
    r = analysis.analyse(_df(_base().tail(60), _flatvol().tail(60)), 0.05)
    assert isinstance(r['ma200'], float) and r['ma200'] == r['ma200']  # pas NaN
    s = json.dumps({k: v for k, v in r.items()
                    if k not in ('physics', 'vertex', 'mtf', 'structure')}, default=str)
    assert 'NaN' not in s


# ── Profils : la NATURE du titre (le golden fige déjà OFFENSIF) ──────────────

def test_profil_defensif_titre_calme_beta_faible_dividende():
    calm = pd.Series(np.linspace(100, 104, 260), index=IDX)
    r = analysis.analyse(_df(calm, _flatvol()), 0.0,
                         fund={'beta': 0.5, 'div': 0.03, 'sector': 'Utilities'})
    assert r['profile'] == 'DÉFENSIF'
    assert 'LEAPS' in r['profile_hint'] or 'actions' in r['profile_hint']


def test_profil_equilibre_sans_fondamentaux():
    r = analysis.analyse(_df(_base(), _flatvol()), 0.05)
    assert r['profile'] == 'ÉQUILIBRÉ'


# ── Radar d'anomalies : l'inhabituel statistique est signalé ─────────────────

def test_anomalie_gap_haussier_detectee():
    close = _base()
    op = close.shift(1).fillna(close.iloc[0]).copy()
    op.iloc[-1] = close.iloc[-2] * 1.06  # ouverture +6 % vs clôture précédente
    r = analysis.analyse(_df(close, _flatvol(), open_=op), 0.05)
    keys = [a['k'] for a in r['anomalies']]
    assert 'gap' in keys
    assert r['gap_pct'] == 6.0
    gap = next(a for a in r['anomalies'] if a['k'] == 'gap')
    assert 'haussier' in gap['lbl'] and 1 <= gap['sev'] <= 3


def test_anomalie_pic_de_volume_detectee():
    vol = _flatvol().copy()
    vol.iloc[-1] = 6e6  # 6x la moyenne — z-score >> 2.5
    r = analysis.analyse(_df(_base(), vol), 0.05)
    assert 'volspike' in [a['k'] for a in r['anomalies']]
    assert r['volx'] > 4


def test_score_anomalies_formule_et_niveaux():
    # score = min(100, somme des sévérités × 16) ; niveaux CALME <25,
    # ACTIF <55, ALERTE ≥55 — cohérence vérifiée sur tout résultat.
    for r in (analysis.analyse(_df(_base(), _flatvol()), 0.05),
              analysis.analyse(_df(_base()), 0.05)):
        expected = min(100, sum(a['sev'] for a in r['anomalies']) * 16)
        assert r['anomaly_score'] == expected
        lvl = ('CALME' if r['anomaly_score'] < 25 else
               'ACTIF' if r['anomaly_score'] < 55 else 'ALERTE')
        assert r['anomaly_lvl'] == lvl


# ── Détections : cassure confirmée, régime CHOP ──────────────────────────────

def test_cassure_confirmee_nouveau_plus_haut_avec_volume():
    close = _base().copy()
    close.iloc[-1] = close.iloc[-21:-1].max() + 3   # nouveau plus-haut 20 j
    vol = _flatvol().copy()
    vol.iloc[-1] = 6e6                              # porté par le volume
    assert analysis.analyse(_df(close, vol), 0.05)['breakout'] is True


def test_pas_de_cassure_sans_volume_de_confirmation():
    assert analysis.analyse(_df(_base(), _flatvol()), 0.05)['breakout'] is False


def test_regime_chop_oscillation_plate():
    chop = pd.Series(100 + 3 * np.sin(np.linspace(0, 60, 260)), index=IDX)
    r = analysis.analyse(_df(chop, _flatvol()), 0.0)
    assert r['regime'] == 'CHOP'
    assert r['chop'] >= 60


# ── Plan : stop structurel, échelle de TP, qualité bornée ────────────────────

@pytest.mark.parametrize('mkdf', [
    lambda: _df(_base(), _flatvol()),
    lambda: _df(_base().tail(60), _flatvol().tail(60)),
    lambda: _df(pd.Series(100 + 3 * np.sin(np.linspace(0, 60, 260)), index=IDX), _flatvol()),
])
def test_plan_invariants(mkdf):
    p = analysis.analyse(mkdf(), 0.05)['plan']
    risk = p['entry'] - p['stop']
    assert risk > 0                                    # stop toujours SOUS l'entrée
    assert abs(p['tp1'] - (p['entry'] + risk)) < 0.02  # échelle 1R/2R/3R exacte
    assert abs(p['tp2'] - (p['entry'] + 2 * risk)) < 0.02
    assert abs(p['tp3'] - (p['entry'] + 3 * risk)) < 0.02
    assert p['rr'] == 3.0
    assert p['stop_dist_atr'] > 0
    assert 0 <= p['setup_quality'] <= 100
    assert p['stop_type'] in ('structure', 'ATR (plafond risque)',
                              'ATR (structure trop proche)')


# ── Transparence du score : une seule arithmétique, bornée ───────────────────

@pytest.mark.parametrize('mkdf', [
    lambda: _df(_base(), _flatvol()),
    lambda: _df(_base().tail(60), _flatvol().tail(60)),
    lambda: _df(pd.Series(100 + 3 * np.sin(np.linspace(0, 60, 260)), index=IDX), _flatvol()),
])
def test_score_egale_base_plus_ajustement_structurel_borne(mkdf):
    r = analysis.analyse(mkdf(), 0.05)
    # L'ajustement (physique + multi-horizons) est borné [-12, +10] et le
    # score affiché est EXACTEMENT base + ajustement, clampé 0-100 —
    # transparence totale, pas de deuxième vérité.
    assert -12 <= r['struct_adj'] <= 10
    assert r['score'] == max(0, min(100, r['base_score'] + r['struct_adj']))


def test_checklist_signaux_contrat_et_compte():
    r = analysis.analyse(_df(_base(), _flatvol()), 0.05)
    sig = r['signals']
    assert set(sig) == {'above20', 'above50', 'above200', 'stacked', 'golden',
                        'goldenNow', 'momCross', 'rsiBull', 'volUp'}
    expected = sum(1 for k in ('above20', 'above50', 'above200', 'stacked',
                               'golden', 'momCross', 'volUp') if sig[k])
    assert r['sigcount'] == expected
