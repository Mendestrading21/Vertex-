"""vertex.portfolio.portfolio_guard — garde-fous du portefeuille (§26).

Traduit le rapport de risque en règles BLOQUANTES pour le moteur décisionnel :
à -25 % de drawdown → aucun nouveau risque, aucune nouvelle option, revue.
"""
from __future__ import annotations


def guard_rules(risk_report: dict, profile) -> dict:
    blocking: list[str] = []
    reviews: list[str] = []
    dd = risk_report.get('drawdown_pct')
    if risk_report.get('no_new_risk'):
        blocking.append('NO_NEW_RISK')
    if dd is not None and dd <= profile.portfolio_max_drawdown_pct:
        blocking.append('PORTFOLIO_DRAWDOWN_LIMIT')
        reviews.append('revue obligatoire du portefeuille (drawdown maximal atteint)')
    opts = risk_report.get('options_exposure') or {}
    if (opts.get('open_options') or 0) >= profile.max_simultaneous_options:
        blocking.append('MAX_OPTIONS_REACHED')
    for sym, pl in (risk_report.get('per_stock_pl_pct') or {}).items():
        if pl <= profile.stock_max_drawdown_pct:
            reviews.append(f'revue obligatoire: {sym} ({pl}%)')
    return {'new_stock_allowed': not blocking,
            'new_option_allowed': not blocking,
            'blocking_rules': blocking,
            'mandatory_reviews': reviews,
            'warnings': list(risk_report.get('warnings') or [])}
