"""vertex.research.institutional.signal_ensemble — agrégation des signaux (§23).

Combine facteurs, classements, rotation, PEAD, qualité-croissance, crowding et
régimes de vol en UN contexte institutionnel par titre. ENRICHISSEMENT pur :
la sortie alimente l'executive_engine — elle ne décide rien et ne contourne
jamais la constitution.
"""
from __future__ import annotations

from . import (crowding_proxies, earnings_drift, factor_model, momentum_regimes,
               quality_growth, volatility_regimes)


def institutional_context(stock: dict, bench_returns: list[float] | None = None,
                          market_regime: str = 'UNKNOWN',
                          ranking_entry: dict | None = None) -> dict:
    """stock : superset des entrées des sous-moteurs (returns, fondamentaux,
    crowding inputs, événements). Chaque bloc absent est honnêtement None."""
    rets = stock.get('returns') or []
    factors = factor_model.factor_exposures(stock, bench_returns)
    qg = quality_growth.quality_growth_profile(stock)
    mom = momentum_regimes.momentum_quality(
        (factors.get('MOMENTUM') or {}).get('value'),
        stock.get('momentum_3m'),
        -((factors.get('LOW_VOL') or {}).get('value') or 0) or None,
        market_regime)
    crowd = crowding_proxies.crowding_score(stock)
    vol = volatility_regimes.classify_vol_regime(rets)
    pead = earnings_drift.post_earnings_drift_signal(
        stock.get('earnings_reaction_day1_pct'), stock.get('earnings_surprise_pct'),
        stock.get('days_since_earnings'), stock.get('drift_since_pct'))
    events = earnings_drift.event_signals(stock.get('events') or {})

    positives, cautions = [], []
    if qg['profile'] == 'QUALITY_GROWTH':
        positives.append('profil qualité-croissance')
    if qg['flags']:
        cautions.extend(qg['flags'])
    if mom['quality'] == 'STRONG':
        positives.append('momentum fort ajusté de la volatilité')
    if mom.get('regime_warning'):
        cautions.append(mom['regime_warning'])
    if crowd['crowded']:
        cautions.append('positionnement surchargé (proxies) — sortie de foule brutale possible')
    if pead.get('signal') == 'PEAD_UP':
        positives.append('drift post-résultats haussier en cours')
    if ranking_entry and ranking_entry.get('_composite_pct') is not None:
        pct = ranking_entry['_composite_pct']
        note = f'classement transversal: {pct}e percentile univers'
        if pct >= 75:
            positives.append(note)
        elif pct <= 30:
            cautions.append(note)

    return {'factors': factors, 'quality_growth': qg, 'momentum': mom,
            'crowding': crowd, 'volatility_regime': vol, 'pead': pead,
            'event_signals': events,
            'summary': {'positives': positives, 'cautions': cautions},
            'disclaimer': 'contexte institutionnel = enrichissement — la décision '
                          'finale appartient au moteur exécutif sous constitution'}
