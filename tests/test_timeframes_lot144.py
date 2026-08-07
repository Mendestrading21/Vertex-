"""
LOT 144 — Caractérisation du moteur de confluence multi-horizons
(`vertex/engines/timeframes.py`).

Ce moteur contribue au score Vertex (`adj` borné ±5) et alimente le
drapeau `mtf` du scan — il n'avait AUCUN test direct. Ces tests figent
le comportement observé (états, gardes, contrat de sortie) : tout
changement futur de sémantique doit faire échouer cette suite et être
assumé explicitement.

Séries synthétiques déterministes (np.linspace) — aucune donnée
inventée présentée comme réelle : on caractérise des formes de marché
(hausse, baisse, repli, plat), pas des titres.
"""

import numpy as np
import pandas as pd
import pytest

from vertex.engines import timeframes

IDX = pd.date_range('2024-01-01', periods=400, freq='D')

EXPECTED_KEYS = {'weekly_rsi', 'weekly_roc', 'weekly_above30', 'weekly_rising',
                 'weekly_stacked', 'state', 'state_col', 'adj', 'note'}

STATES = {'ALIGNÉ HAUSSIER', 'REPLI DANS TENDANCE', 'REBOND CONTRE-TENDANCE',
          'ALIGNÉ BAISSIER', 'NEUTRE'}


def _up():
    return pd.Series(np.linspace(100, 200, 400), index=IDX)


def _down():
    return pd.Series(np.linspace(200, 100, 400), index=IDX)


def _pullback_in_uptrend():
    # Longue hausse puis repli récent LÉGER : le prix reste AU-DESSUS de
    # l'EMA30 hebdo mais l'EMA10 hebdo se retourne → branche NEUTRE.
    vals = np.concatenate([np.linspace(100, 200, 360), np.linspace(200, 192, 40)])
    return pd.Series(vals, index=IDX)


# ── Les 5 états et leurs contributions au score (figés) ──────────────────────

def test_aligne_haussier_hebdo_et_journalier_en_phase():
    r = timeframes.analyze(_up(), daily_above50=True)
    assert r['state'] == 'ALIGNÉ HAUSSIER'
    assert r['adj'] == 5
    assert r['weekly_above30'] and r['weekly_rising'] and r['weekly_stacked']


def test_repli_dans_tendance_hebdo_saine_journalier_faible():
    r = timeframes.analyze(_up(), daily_above50=False)
    assert r['state'] == 'REPLI DANS TENDANCE'
    assert r['adj'] == 3
    assert r['weekly_above30'] and r['weekly_rising']


def test_rebond_contre_tendance_hebdo_baissiere_journalier_haussier():
    r = timeframes.analyze(_down(), daily_above50=True)
    assert r['state'] == 'REBOND CONTRE-TENDANCE'
    assert r['adj'] == -4
    assert not r['weekly_above30']


def test_aligne_baissier_les_deux_horizons_contre():
    r = timeframes.analyze(_down(), daily_above50=False)
    assert r['state'] == 'ALIGNÉ BAISSIER'
    assert r['adj'] == -5
    assert not r['weekly_above30'] and not r['weekly_rising']


def test_neutre_au_dessus_ema30_mais_ema10_qui_se_retourne():
    # La branche la moins évidente : prix > EMA30 hebdo (fond intact) mais
    # EMA10 hebdo en baisse (élan cassé) → signal ambigu, contribution nulle.
    r = timeframes.analyze(_pullback_in_uptrend(), daily_above50=True)
    assert r['state'] == 'NEUTRE'
    assert r['adj'] == 0
    assert r['weekly_above30'] and not r['weekly_rising']


# ── Gardes d'entrée : jamais de verdict sans historique suffisant ────────────

def test_moins_de_32_semaines_renvoie_none():
    short = pd.Series(np.linspace(100, 110, 100),
                      index=pd.date_range('2024-01-01', periods=100, freq='D'))
    assert timeframes.analyze(short) is None


def test_entree_non_reechantillonnable_renvoie_none():
    # Une liste brute (pas de Série pandas datée) ne doit jamais lever :
    # le moteur répond None (pas d'invention de verdict).
    assert timeframes.analyze([1, 2, 3]) is None


# ── Contrat de sortie (consommé par le scan et l'UI) ─────────────────────────

@pytest.mark.parametrize('serie,bull', [
    (_up(), True), (_up(), False), (_down(), True), (_down(), False),
    (_pullback_in_uptrend(), True),
])
def test_contrat_de_sortie_complet_et_type(serie, bull):
    r = timeframes.analyze(serie, daily_above50=bull)
    assert set(r.keys()) == EXPECTED_KEYS
    assert r['state'] in STATES
    assert isinstance(r['adj'], int) and -5 <= r['adj'] <= 5
    assert isinstance(r['weekly_rsi'], int) and 0 <= r['weekly_rsi'] <= 100
    assert isinstance(r['weekly_roc'], float)
    for k in ('weekly_above30', 'weekly_rising', 'weekly_stacked'):
        assert isinstance(r[k], bool)
    assert r['note'].strip()
    assert r['state_col'].startswith('#') and len(r['state_col']) == 7
    # Cohérence interne : « empilé » (prix > EMA10 > EMA30) implique
    # nécessairement « au-dessus de l'EMA30 ».
    if r['weekly_stacked']:
        assert r['weekly_above30']


# ── Comportement limite documenté (pas un souhait — l'existant) ──────────────

def test_serie_parfaitement_plate_comportement_limite_documente():
    # Série strictement constante (pathologique — n'existe pas en réel) :
    # prix == EMA30 exactement, donc « au-dessus » est False → le moteur
    # classe ALIGNÉ BAISSIER (adj -5) et le RSI vaut 100 (aucune baisse →
    # dn=0 → convention fillna(100) du moteur). Ce test DOCUMENTE ce
    # comportement limite tel quel ; le changer = décision explicite.
    flat = pd.Series(np.full(400, 150.0), index=IDX)
    r = timeframes.analyze(flat)
    assert r['state'] == 'ALIGNÉ BAISSIER'
    assert r['adj'] == -5
    assert r['weekly_rsi'] == 100
