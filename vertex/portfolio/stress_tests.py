"""vertex.portfolio.stress_tests — chocs standardisés sur le portefeuille réel (§26)."""
from __future__ import annotations

from .models import PortfolioSnapshot

SCENARIOS = ('SPY_MINUS_5', 'SPY_MINUS_10', 'NASDAQ_MINUS_10', 'VIX_PLUS_50',
             'RATES_PLUS_50BP', 'RATES_MINUS_50BP', 'TOP_SECTOR_MINUS_15',
             'IV_CRUSH', 'EARNINGS_GAP_ADVERSE', 'CORRELATIONS_TO_ONE')


def run_stress_tests(snapshot: PortfolioSnapshot, profile,
                     sector_of: dict | None = None,
                     nasdaq_exposure: dict | None = None,
                     rate_sensitivity_bp: float | None = None,
                     options_vega_value: float | None = None,
                     earnings_positions: list[str] | None = None) -> dict:
    """Impacts estimés en % de l'équité. Hypothèses documentées, pas de fausse précision."""
    eq = snapshot.equity
    out = {'equity': eq, 'scenarios': {}, 'assumptions': [
        'impact via bêta par position (bêta 1.0 si inconnu — documenté)',
        'chocs instantanés sans rebalancement',
    ], 'warnings': []}
    if not eq:
        out['warnings'].append('équité incalculable (prix manquants) — stress tests refusés')
        return out
    sector_of = sector_of or {}
    weights = snapshot.weights()

    def beta_of(p):
        return p.beta if p.beta is not None else 1.0

    def market_shock(pct, only=None):
        impact = 0.0
        for p in snapshot.positions:
            if only is not None and not only(p):
                continue
            impact += (weights.get(p.symbol, 0) / 100) * beta_of(p) * pct
        return round(impact, 2)

    out['scenarios']['SPY_MINUS_5'] = {'impact_pct': market_shock(-5)}
    out['scenarios']['SPY_MINUS_10'] = {'impact_pct': market_shock(-10)}
    ndx = nasdaq_exposure or {}
    out['scenarios']['NASDAQ_MINUS_10'] = {
        'impact_pct': market_shock(-10, only=lambda p: ndx.get(p.symbol, True))}
    vega_val = options_vega_value or 0.0
    out['scenarios']['VIX_PLUS_50'] = {
        'impact_pct': round(market_shock(-4) + (vega_val / eq * 100 if eq else 0), 2),
        'note': 'choc actions modéré + gain/perte vega des options'}
    if rate_sensitivity_bp is not None:
        out['scenarios']['RATES_PLUS_50BP'] = {'impact_pct': round(rate_sensitivity_bp * 50, 2)}
        out['scenarios']['RATES_MINUS_50BP'] = {'impact_pct': round(-rate_sensitivity_bp * 50, 2)}
    else:
        out['scenarios']['RATES_PLUS_50BP'] = {'impact_pct': None,
                                               'note': 'sensibilité taux inconnue — non estimé'}
        out['scenarios']['RATES_MINUS_50BP'] = {'impact_pct': None,
                                                'note': 'sensibilité taux inconnue — non estimé'}
    sector_weights: dict[str, float] = {}
    for p in snapshot.positions:
        sec = p.sector or sector_of.get(p.symbol, 'Inconnu')
        sector_weights[sec] = sector_weights.get(sec, 0) + weights.get(p.symbol, 0)
    if sector_weights:
        top_sec, top_w = max(sector_weights.items(), key=lambda kv: kv[1])
        out['scenarios']['TOP_SECTOR_MINUS_15'] = {
            'impact_pct': round(-15 * top_w / 100, 2), 'sector': top_sec}
    out['scenarios']['IV_CRUSH'] = {
        'impact_pct': round(-abs(vega_val) * 0.3 / eq * 100, 2) if vega_val else 0.0,
        'note': 'contraction d’IV de 30 % sur les options longues détenues'}
    earnings_positions = earnings_positions or []
    gap_w = sum(weights.get(s, 0) for s in earnings_positions)
    out['scenarios']['EARNINGS_GAP_ADVERSE'] = {
        'impact_pct': round(-12 * gap_w / 100, 2),
        'positions': earnings_positions,
        'note': 'gap défavorable de -12 % sur les positions avec résultats imminents'}
    stock_w = sum(w for s, w in weights.items() if s != '_CASH')
    out['scenarios']['CORRELATIONS_TO_ONE'] = {
        'impact_pct': round(-10 * stock_w / 100, 2),
        'note': 'toutes corrélations → 1 : la diversification disparaît, '
                'seul le cash protège (choc -10 % uniforme)'}
    worst = min((v['impact_pct'] for v in out['scenarios'].values()
                 if v.get('impact_pct') is not None), default=None)
    out['worst_case_pct'] = worst
    if worst is not None and worst <= profile.portfolio_max_drawdown_pct:
        out['warnings'].append(f'pire scénario {worst}% dépasse le drawdown max '
                               f'{profile.portfolio_max_drawdown_pct}% — réduire le risque')
    return out
