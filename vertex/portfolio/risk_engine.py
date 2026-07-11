"""vertex.portfolio.risk_engine — risque du portefeuille RÉEL (§26, corrige §6.9).

Calcule sur les positions réelles (IBKR/desk) ou simulées explicitement
transmises — JAMAIS sur les candidats du scanner (ce vieux comportement vit
encore dans legacy_basket_risk.py pour les vues « panier », clairement nommé).
"""
from __future__ import annotations

from .correlation import correlation_matrix
from .models import PortfolioSnapshot

MAX_STOCK_WEIGHT_DEFAULT = 15.0


def portfolio_risk(snapshot: PortfolioSnapshot, profile,
                   returns_by_symbol: dict | None = None,
                   sector_of: dict | None = None,
                   options_greeks: list[dict] | None = None) -> dict:
    """Rapport de risque complet sur positions réelles/simulées explicites."""
    if snapshot.provenance not in ('REAL', 'SIMULATED'):
        raise ValueError('risque calculable uniquement sur positions réelles ou '
                         f'simulées explicites (reçu: {snapshot.provenance!r})')
    weights = snapshot.weights()
    sector_of = sector_of or {}
    warnings: list[str] = []

    # Poids & concentration
    stock_weights = {s: w for s, w in weights.items() if s != '_CASH'}
    overweight = {s: w for s, w in stock_weights.items()
                  if w > profile.max_stock_weight_pct}
    for s, w in overweight.items():
        warnings.append(f'{s}: poids {w}% > max {profile.max_stock_weight_pct}%')
    hhi = round(sum((w / 100) ** 2 for w in stock_weights.values()), 4)

    # Secteurs
    sector_weights: dict[str, float] = {}
    for p in snapshot.positions:
        sec = p.sector or sector_of.get(p.symbol, 'Inconnu')
        w = weights.get(p.symbol, 0)
        sector_weights[sec] = round(sector_weights.get(sec, 0) + w, 2)
    top_sector = max(sector_weights.items(), key=lambda kv: kv[1]) if sector_weights else None
    if top_sector and top_sector[1] > 40:
        warnings.append(f'secteur {top_sector[0]} à {top_sector[1]}% (> 40%)')

    # Bêta pondéré
    betas = [(weights.get(p.symbol, 0) / 100, p.beta) for p in snapshot.positions
             if p.beta is not None]
    beta = round(sum(w * b for w, b in betas), 2) if betas else None

    # Corrélations
    corr = correlation_matrix(returns_by_symbol or {})
    if corr.get('warning'):
        warnings.append(corr['warning'])

    # Drawdown & règle -25 %
    dd = snapshot.drawdown_pct
    no_new_risk = False
    if dd is not None and dd <= profile.portfolio_max_drawdown_pct:
        no_new_risk = True
        warnings.append(f'drawdown portefeuille {dd}% ≤ {profile.portfolio_max_drawdown_pct}% '
                        '— AUCUN nouveau risque, AUCUNE nouvelle option, revue obligatoire')

    # Drawdown par titre (-20 %)
    per_stock_dd = {}
    for p in snapshot.positions:
        if p.avg_cost and p.last_price:
            pl = round((p.last_price / p.avg_cost - 1) * 100, 1)
            per_stock_dd[p.symbol] = pl
            if pl <= profile.stock_max_drawdown_pct:
                warnings.append(f'{p.symbol}: {pl}% ≤ {profile.stock_max_drawdown_pct}% '
                                '— revue de position obligatoire')

    # Exposition options agrégée
    greeks = {'delta': None, 'gamma': None, 'theta': None, 'vega': None,
              'open_options': 0}
    if options_greeks:
        greeks = {'delta': round(sum(g.get('delta') or 0 for g in options_greeks), 3),
                  'gamma': round(sum(g.get('gamma') or 0 for g in options_greeks), 4),
                  'theta': round(sum(g.get('theta') or 0 for g in options_greeks), 3),
                  'vega': round(sum(g.get('vega') or 0 for g in options_greeks), 3),
                  'open_options': len(options_greeks)}
        if greeks['open_options'] > profile.max_simultaneous_options:
            no_new_risk = True
            warnings.append(f"{greeks['open_options']} options ouvertes > maximum "
                            f'{profile.max_simultaneous_options}')

    return {'provenance': snapshot.provenance, 'as_of': snapshot.as_of,
            'equity': snapshot.equity, 'weights': weights,
            'sector_weights': sector_weights, 'hhi': hhi, 'beta': beta,
            'correlations': {'average': corr.get('average'),
                             'high_pairs': corr.get('high_pairs')},
            'drawdown_pct': dd, 'per_stock_pl_pct': per_stock_dd,
            'options_exposure': greeks, 'overweight': overweight,
            'no_new_risk': no_new_risk, 'warnings': warnings}
