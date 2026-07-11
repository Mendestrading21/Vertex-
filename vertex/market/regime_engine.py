"""vertex.market.regime_engine — régimes de marché multidimensionnels (§24).

Un régime ne déclenche JAMAIS automatiquement un trade : il module les
priorités de setups, les seuils, la taille recommandée (si capital fourni),
la confiance et les exigences de confirmation.
"""
from __future__ import annotations

REGIMES = ('TREND_UP', 'TREND_DOWN', 'CHOP', 'RISK_ON', 'RISK_OFF', 'PANIC',
           'EUPHORIA', 'VOLATILITY_EXPANSION', 'VOLATILITY_COMPRESSION',
           'MEAN_REVERSION', 'TRANSITION', 'UNKNOWN')


def classify_regime(inputs: dict) -> dict:
    """inputs (tous optionnels — l'absence dégrade honnêtement vers UNKNOWN) :
    index_trend ('UP'/'DOWN'/'FLAT'), breadth_pct (0-100), vix, vix_percentile,
    realized_vol_ratio (récent/normal), yield_curve_bps, dollar_trend,
    credit_spread_trend, dispersion, leadership ('CYCLICAL'/'DEFENSIVE'/'MIXED'),
    momentum_pct, volume_trend.
    """
    dims_used = [k for k, v in (inputs or {}).items() if v is not None]
    if len(dims_used) < 3:
        return {'regime': 'UNKNOWN', 'secondary': [], 'dimensions_used': dims_used,
                'confidence': 0.0,
                'notes': ['moins de 3 dimensions disponibles — régime inconnu (honnête)'],
                'adjustments': _adjustments('UNKNOWN')}

    trend = inputs.get('index_trend')
    breadth = inputs.get('breadth_pct')
    vix = inputs.get('vix')
    vix_pct = inputs.get('vix_percentile')
    rv_ratio = inputs.get('realized_vol_ratio')
    leadership = inputs.get('leadership')
    momentum = inputs.get('momentum_pct')

    secondary: list[str] = []
    votes: dict[str, float] = {}

    def vote(regime, w):
        votes[regime] = votes.get(regime, 0) + w

    if vix is not None and vix >= 35:
        vote('PANIC', 3)
    elif vix is not None and vix >= 26:
        vote('RISK_OFF', 2)
    elif vix is not None and vix <= 14:
        vote('RISK_ON', 1)
    if trend == 'UP':
        vote('TREND_UP', 2)
        if breadth is not None and breadth < 40:
            secondary.append('BREADTH_DIVERGENCE')
            vote('TRANSITION', 1)
    elif trend == 'DOWN':
        vote('TREND_DOWN', 2)
    else:
        vote('CHOP', 1.5)
    if breadth is not None:
        if breadth >= 70:
            vote('RISK_ON', 1.5)
        elif breadth <= 30:
            vote('RISK_OFF', 1.5)
    if leadership == 'CYCLICAL':
        vote('RISK_ON', 1)
    elif leadership == 'DEFENSIVE':
        vote('RISK_OFF', 1)
    if rv_ratio is not None:
        if rv_ratio >= 1.6:
            vote('VOLATILITY_EXPANSION', 1.5)
        elif rv_ratio <= 0.6:
            vote('VOLATILITY_COMPRESSION', 1.5)
    if momentum is not None and vix is not None:
        if momentum >= 90 and vix <= 15:
            vote('EUPHORIA', 2)
    if inputs.get('credit_spread_trend') == 'WIDENING':
        vote('RISK_OFF', 1.5)
    if inputs.get('dispersion') is not None and inputs['dispersion'] >= 0.7 \
            and trend in (None, 'FLAT'):
        vote('MEAN_REVERSION', 1.5)

    regime = max(votes, key=votes.get) if votes else 'UNKNOWN'
    total = sum(votes.values()) or 1
    confidence = round(votes.get(regime, 0) / total, 2)
    ordered = sorted(votes, key=votes.get, reverse=True)
    if len(ordered) >= 2 and votes[ordered[1]] >= votes[ordered[0]] * 0.85:
        secondary.append(ordered[1])
        # PANIC ne se dilue jamais en TRANSITION (sécurité d'abord) ; idem si le
        # second régime raconte la même histoire de risque (RISK_OFF/TREND_DOWN).
        same_family = {ordered[0], ordered[1]} <= {'PANIC', 'RISK_OFF', 'TREND_DOWN'} \
            or {ordered[0], ordered[1]} <= {'RISK_ON', 'TREND_UP', 'EUPHORIA'}
        if confidence < 0.4 and regime != 'PANIC' and not same_family:
            regime = 'TRANSITION'
    return {'regime': regime, 'secondary': secondary, 'dimensions_used': dims_used,
            'confidence': confidence, 'votes': votes, 'notes': [],
            'adjustments': _adjustments(regime)}


def _adjustments(regime: str) -> dict:
    """Ce que le régime MODULE (jamais un ordre, jamais un trade automatique)."""
    base = {'setup_priority': 'BALANCED', 'score_threshold_shift': 0,
            'size_factor_if_capital': 1.0, 'confidence_factor': 1.0,
            'confirmation_required': 1, 'new_risk_allowed': True}
    table = {
        'TREND_UP': {'setup_priority': 'BREAKOUT_PULLBACK'},
        'TREND_DOWN': {'setup_priority': 'DEFENSIVE', 'score_threshold_shift': 10,
                       'size_factor_if_capital': 0.6, 'confirmation_required': 2},
        'CHOP': {'setup_priority': 'MEAN_REVERSION', 'score_threshold_shift': 8,
                 'size_factor_if_capital': 0.7, 'confirmation_required': 2},
        'RISK_ON': {'setup_priority': 'MOMENTUM'},
        'RISK_OFF': {'setup_priority': 'QUALITY_DEFENSIVE', 'score_threshold_shift': 12,
                     'size_factor_if_capital': 0.5, 'confirmation_required': 2},
        'PANIC': {'setup_priority': 'CAPITAL_PRESERVATION', 'score_threshold_shift': 25,
                  'size_factor_if_capital': 0.25, 'confirmation_required': 3,
                  'new_risk_allowed': False},
        'EUPHORIA': {'setup_priority': 'TAKE_PROFITS', 'score_threshold_shift': 15,
                     'size_factor_if_capital': 0.5, 'confirmation_required': 2},
        'VOLATILITY_EXPANSION': {'score_threshold_shift': 10,
                                 'size_factor_if_capital': 0.6},
        'VOLATILITY_COMPRESSION': {'setup_priority': 'BREAKOUT_WATCH'},
        'MEAN_REVERSION': {'setup_priority': 'MEAN_REVERSION'},
        'TRANSITION': {'score_threshold_shift': 8, 'confirmation_required': 2},
        'UNKNOWN': {'score_threshold_shift': 15, 'size_factor_if_capital': 0.5,
                    'confirmation_required': 2},
    }
    base.update(table.get(regime, {}))
    return base
