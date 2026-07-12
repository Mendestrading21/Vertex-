"""vertex.options.pulse — widgets de synthèse Options/Volatilité (§7/§14).

Widgets compacts calculés depuis le tableau d'options réel : OPTION PULSE
(CALLS/PUTS/theta/IV/DTE) et VOLATILITY PULSE (IV médiane, dispersion,
compression). Chaque métrique absente rend None (jamais un zéro inventé).
Lecture seule.
"""
from __future__ import annotations


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _avg(xs):
    xs = [v for v in xs if v is not None]
    return round(sum(xs) / len(xs), 2) if xs else None


def _median(xs):
    xs = sorted(v for v in xs if v is not None)
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 else round((xs[n // 2 - 1] + xs[n // 2]) / 2, 4)


def option_pulse(board):
    """CALLS/PUTS, IV moyenne, DTE moyen, theta burn moyen. board = options_board."""
    board = board or []
    calls = [c for c in board if str(c.get('type', '')).upper() == 'CALL']
    puts = [c for c in board if str(c.get('type', '')).upper() == 'PUT']
    return {
        'calls': len(calls),
        'puts': len(puts),
        'call_put_ratio': (round(len(calls) / len(puts), 2) if puts else None),
        'avg_iv': _avg([_num(c.get('iv')) for c in board]),
        'avg_dte': _avg([_num(c.get('dte')) for c in board]),
        'avg_theta_burn': _avg([_num(c.get('theta_burn')) for c in board]),
        'symbols': len({c.get('sym') for c in board if c.get('sym')}),
        'empty': not board,
    }


def volatility_pulse(board):
    """IV médiane, min/max, dispersion (proxy compression/expansion)."""
    board = board or []
    ivs = [(_num(c.get('iv')) or 0) for c in board if isinstance(c.get('iv'), (int, float))]
    ivs = [v for v in ivs if v > 0]
    if not ivs:
        return {'median_iv': None, 'min_iv': None, 'max_iv': None,
                'dispersion': None, 'state': 'INCONNU', 'empty': True}
    med = _median(ivs)
    lo, hi = min(ivs), max(ivs)
    disp = round(hi - lo, 1)
    # dispersion faible → régime compressé ; élevée → expansion/skew fort.
    if disp <= 8:
        state = 'COMPRESSION'
    elif disp >= 25:
        state = 'EXPANSION'
    else:
        state = 'NORMALE'
    return {'median_iv': round(med, 1), 'min_iv': round(lo, 1), 'max_iv': round(hi, 1),
            'dispersion': disp, 'state': state, 'empty': False}


__all__ = ['option_pulse', 'volatility_pulse']
