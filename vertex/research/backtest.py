"""vertex.research.backtest — backtest simple avec coûts (§29).

Un backtest N'EST JAMAIS une preuve : il précède le walk-forward et les
contrôles de biais. Voir factory.py pour le cycle complet.
"""
from .factory import apply_costs


def simple_backtest(returns, positions, spread_pct=0.05, slippage_pct=0.05):
    """positions[i] ∈ [0,1] appliquée au rendement i (déjà décalée par l'appelant :
    la position du jour i doit venir des données < i)."""
    n = min(len(returns), len(positions))
    gross = [positions[i] * returns[i] for i in range(n)]
    turnover = sum(abs(positions[i] - positions[i - 1]) for i in range(1, n))
    net = apply_costs(gross, spread_pct, slippage_pct,
                      turnover=turnover / max(n, 1))
    equity, acc = [], 1.0
    for r in net:
        acc *= (1 + r)
        equity.append(round(acc, 6))
    return {'gross_mean': sum(gross) / n if n else None,
            'net_mean': sum(net) / n if n else None,
            'equity': equity, 'turnover': round(turnover, 2),
            'warning': 'backtest historique ≠ validation — walk-forward requis'}
