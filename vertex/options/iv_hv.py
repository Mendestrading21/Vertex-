"""Écart descriptif entre volatilité implicite et réalisée, sans signal d'exécution."""
from __future__ import annotations


def describe(implied_volatility_pct, historical_volatility_pct, *, threshold_pct_points=3.0):
    """Retourne un contexte IV-HV uniquement si les deux mesures sont observées."""
    try:
        iv = float(implied_volatility_pct)
        hv = float(historical_volatility_pct)
    except (TypeError, ValueError):
        iv = hv = None
    if iv is None or hv is None or iv < 0 or hv < 0:
        return {
            'available': False, 'status': 'INSUFFICIENT_IV_HV',
            'iv_pct': iv, 'hv_20d_pct': hv, 'gap_pct_points': None, 'ratio': None,
            'read_only': True,
            'note': 'IV ou volatilité réalisée indisponible ; aucun écart n’est inféré',
        }
    gap = iv - hv
    if gap >= threshold_pct_points:
        status = 'IV_ABOVE_HV'
    elif gap <= -threshold_pct_points:
        status = 'IV_BELOW_HV'
    else:
        status = 'IV_NEAR_HV'
    return {
        'available': True, 'status': status,
        'iv_pct': round(iv, 2), 'hv_20d_pct': round(hv, 2),
        'gap_pct_points': round(gap, 2),
        'ratio': round(iv / hv, 4) if hv > 0 else None,
        'threshold_pct_points': float(threshold_pct_points),
        'read_only': True,
        'note': 'écart descriptif IV-HV ; ni prévision ni recommandation',
    }


__all__ = ['describe']
