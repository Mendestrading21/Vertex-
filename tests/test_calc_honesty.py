"""Tests — honnêteté des calculs Greeks (audit système, §21).

Vérifie qu'aucune valeur absente n'est transformée en 0 fabriqué et qu'aucun
label de provenance (BROKER_GREEKS) n'est apposé sans valeurs réelles.
"""
from vertex.positions import calculator
from vertex.portfolio import risk_engine


def _opt(qty=1):
    return {
        'asset_type': 'OPTION', 'symbol': 'AAPL', 'right': 'CALL',
        'strike': 200, 'expiration': '2026-09-18', 'quantity': qty,
        'multiplier': 100, 'cost_total': 500, 'capital_committed': 500,
        'avg_cost': 5.0, 'data_quality': {},
    }


def test_positional_greek_none_when_quantity_unknown():
    """qty=None → Greek positionnel None, jamais 0 fabriqué (mais valeur unitaire gardée)."""
    p = _opt(qty=None)
    calculator.enrich_option(p, {'mark': 6.0, 'iv': 0.3}, None,
                             {'source': 'BROKER_GREEKS', 'delta': 0.5}, {})
    assert p['delta'] is None
    assert p.get('delta_per_option') == 0.5


def test_positional_greek_computed_once_with_quantity():
    p = _opt(qty=2)
    calculator.enrich_option(p, {'mark': 6.0, 'iv': 0.3}, None,
                             {'source': 'BROKER_GREEKS', 'delta': 0.5}, {})
    # 0.5 × 100 × 2 = 100 (multiplicateur appliqué une seule fois)
    assert p['delta'] == 100.0
    assert p['greeks_source'] == 'BROKER_GREEKS'


def test_no_broker_greeks_label_without_values():
    """Sans valeurs de Greeks, la provenance ne doit pas être BROKER_GREEKS."""
    p = _opt(qty=1)
    calculator.enrich_option(p, {'mark': 6.0, 'iv': 0.3}, None, None, {})
    assert p['greeks_source'] == 'UNAVAILABLE'
    assert p['delta'] is None


def test_risk_engine_does_not_coerce_missing_greeks_to_zero():
    """Garde-fou source : l'agrégat Greeks du risk_engine ne doit plus utiliser
    `g.get('delta') or 0` (qui transformait un Greek absent en 0)."""
    import os
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            'vertex/portfolio/risk_engine.py'), encoding='utf-8').read()
    assert "g.get('delta') or 0" not in src
    assert 'greeks_partial' in src  # l'agrégat signale désormais l'incomplétude
