"""tests/test_rates_lot107.py — SKYLER LOT 107 : courbe de taux figée.

Trou réel de couverture : vertex/data_sources/rates.py — RateCurve sert
de fixture à une dizaine de fichiers de tests, mais la courbe ELLE-MÊME
(interpolation linéaire, clamp aux extrémités, fallback plat documenté
§6.6, rate_sensitivity) n'avait AUCUN test direct.
Caractérisations nées vertes (dites) — moteur INTACT.
"""
import pytest

from vertex.data_sources.rates import FALLBACK_FLAT_RATE, RateCurve, rate_sensitivity
from vertex.data_sources.models import SOURCE_FALLBACK_EOD


def test_empty_curve_returns_documented_fallback_never_a_market_rate():
    q = RateCurve().rate_for_tenor(90)
    assert q.rate == FALLBACK_FLAT_RATE == 0.045
    assert q.fallback_used is True and q.source == SOURCE_FALLBACK_EOD
    assert any('repli' in n and 'documenté' in n for n in q.notes), (
        'le repli se DIT — jamais présenté comme une courbe réelle')
    coverage = q.curve_coverage
    assert coverage['available'] is False and coverage['status'] == 'FALLBACK_FLAT_RATE'
    assert coverage['point_count'] == 0 and coverage['tenors_days'] == []


def test_linear_interpolation_is_exact():
    c = RateCurve({30: 0.04, 90: 0.05}, source='TEST')
    q = c.rate_for_tenor(60)
    assert q.rate == 0.045 and q.fallback_used is False and q.source == 'TEST'
    assert q.curve_coverage['available'] is True
    assert q.curve_coverage['tenors_days'] == [30, 90]
    assert c.rate_for_tenor(45).rate == 0.0425          # quart de chemin


def test_tenor_clamped_to_curve_ends_no_extrapolation():
    c = RateCurve({30: 0.04, 365: 0.05})
    assert c.rate_for_tenor(5).rate == 0.04             # jamais extrapolé sous 30
    assert c.rate_for_tenor(3000).rate == 0.05          # ni au-delà de 365
    assert c.rate_for_tenor(5).fallback_used is False   # courbe réelle, bornée


def test_unsorted_points_are_sorted_internally():
    c = RateCurve({365: 0.05, 30: 0.04, 90: 0.044})
    assert list(c.points) == [30, 90, 365]
    assert c.rate_for_tenor(60).rate == 0.042           # interpole 30→90, pas 365


def test_exact_tenor_returns_exact_point():
    c = RateCurve({30: 0.043, 90: 0.047})
    assert c.rate_for_tenor(30).rate == 0.043
    assert c.rate_for_tenor(90).rate == 0.047


def test_quote_to_dict_contract():
    d = RateCurve({30: 0.04}).rate_for_tenor(30).to_dict()
    assert set(d) == {'rate', 'tenor_days', 'source', 'source_mode',
                      'timestamp', 'fallback_used', 'notes', 'curve_coverage'}
    assert d['tenor_days'] == 30 and d['fallback_used'] is False


def test_rate_sensitivity_documents_how_much_the_rate_matters():
    s = rate_sensitivity(lambda r: r * 100, base_rate=0.045)
    assert s['value_base'] == pytest.approx(4.5)
    assert s['value_up'] == pytest.approx(5.0) and s['value_down'] == pytest.approx(4.0)
    assert s['sensitivity_per_bump'] == pytest.approx(0.5)
    assert s['bump'] == 0.005                           # ±50 bp par défaut


def test_rate_sensitivity_floors_at_zero_and_honest_on_none():
    seen = []
    rate_sensitivity(lambda r: seen.append(r) or 0.0, base_rate=0.002)
    assert min(seen) == 0.0, 'le bump vers le bas ne produit jamais un taux négatif'
    s = rate_sensitivity(lambda r: None, base_rate=0.045)
    assert s['sensitivity_per_bump'] is None, 'prix indisponible → None, pas 0'
