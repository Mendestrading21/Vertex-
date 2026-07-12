"""vertex.positions.calculator — calculs canoniques (§10-§12).

Règles : donnée absente → None (jamais 0) ; multiplicateur appliqué UNE
fois ; Greeks positionnels signés (long CALL Δ>0, long PUT Δ<0, theta
généralement <0, gamma/vega >0 pour un long) ; toute incohérence de signe
est signalée dans data_quality.
"""
from __future__ import annotations


def _n(v):
    return v is not None


def enrich_stock(p: dict, quote: dict | None, spy_change: float | None = None,
                 detail: dict | None = None) -> dict:
    """quote: {price, source, ts, stale}. detail: contexte scan (atr, rsi…)."""
    q = quote or {}
    price = q.get('price')
    p['current_price'] = price
    p['price_source'] = q.get('source')
    p['price_stale'] = bool(q.get('stale'))
    qty, cost = p.get('quantity'), p.get('cost_basis')
    if _n(price) and _n(qty):
        p['market_value'] = round(price * qty, 2)
    if _n(p.get('market_value')) and _n(cost):
        p['unrealized_pnl'] = round(p['market_value'] - cost, 2)
        p['unrealized_pnl_pct'] = round(p['unrealized_pnl'] / cost * 100, 2) if cost else None
    # Distances plan
    stop, tp1 = p.get('stop'), p.get('tp1')
    if _n(price) and _n(stop):
        p['risk_to_stop_pct'] = round((stop / price - 1) * 100, 2)
        if _n(qty):
            p['risk_to_stop'] = round((price - stop) * qty, 2)
        atr = (detail or {}).get('atr')
        p['stop_distance_atr'] = round((price - stop) / atr, 2) if atr else None
    if _n(price) and _n(tp1):
        p['reward_to_tp1'] = round((tp1 / price - 1) * 100, 2)
    for k, tp in (('reward_to_tp2', p.get('tp2')), ('reward_to_tp3', p.get('tp3'))):
        p[k] = round((tp / price - 1) * 100, 2) if (_n(price) and _n(tp)) else None
    # R:R restant = potentiel vers TP1 / risque vers stop (au cours ACTUEL)
    if (_n(price) and _n(stop) and _n(tp1) and price > stop):
        p['remaining_rr'] = round((tp1 - price) / (price - stop), 2)
    d = detail or {}
    p['rsi'] = d.get('rsi')
    p['rel_volume'] = d.get('rvol')
    p['ext_atr'] = d.get('ext_atr')
    p['sector'] = d.get('sector') or p.get('sector')
    if d.get('earnings_dte') is not None:
        p['days_to_earnings'] = d['earnings_dte']
    p['data_quality']['overall'] = ('STALE' if p['price_stale'] else
                                    'OK' if _n(price) else 'MISSING_PRICE')
    return p


def enrich_option(p: dict, quote: dict | None, underlying_quote: dict | None = None,
                  greeks: dict | None = None, detail: dict | None = None) -> dict:
    """quote: {mark, bid, ask, iv, volume, oi, source}. greeks: broker/model
    avec étiquette. Tout absent = None honnête."""
    q = quote or {}
    mult = p.get('multiplier') or 100.0
    qty = p.get('quantity')
    for k in ('bid', 'ask', 'last', 'iv', 'volume'):
        if q.get(k) is not None:
            p[k] = q[k]
    if q.get('oi') is not None:
        p['open_interest'] = q['oi']
    mark = q.get('mark') if q.get('mark') is not None else q.get('last')
    if mark is None and _n(p.get('bid')) and _n(p.get('ask')):
        mark = (p['bid'] + p['ask']) / 2
        p['mid'] = round(mark, 4)
    p['mark'] = mark
    if _n(mark) and _n(qty):
        p['market_value'] = round(mark * mult * qty, 2)
    cap = p.get('capital_committed')
    if _n(p.get('market_value')) and _n(cap):
        p['unrealized_pnl'] = round(p['market_value'] - cap, 2)
        p['unrealized_pnl_pct'] = round(p['unrealized_pnl'] / cap * 100, 2) if cap else None
    if _n(p.get('bid')) and _n(p.get('ask')):
        p['spread_absolute'] = round(p['ask'] - p['bid'], 4)
        mid = (p['ask'] + p['bid']) / 2
        p['spread_pct'] = round(p['spread_absolute'] / mid * 100, 2) if mid else None
    if _n(p.get('volume')) and _n(p.get('open_interest')) and p['open_interest']:
        p['volume_oi_ratio'] = round(p['volume'] / p['open_interest'], 3)

    u = underlying_quote or {}
    spot = u.get('price')
    p['underlying_price'] = spot
    K, right, avg = p.get('strike'), p.get('right'), p.get('average_cost')
    if _n(spot) and _n(K):
        intr = max(0.0, spot - K) if right == 'CALL' else max(0.0, K - spot)
        p['intrinsic_value'] = round(intr, 4)
        if _n(mark):
            p['extrinsic_value'] = round(mark - intr, 4)
        p['moneyness'] = round(spot / K, 4)
    if _n(K) and _n(avg):
        p['breakeven'] = round(K + avg, 4) if right == 'CALL' else round(K - avg, 4)

    # Greeks POSITIONNELS : par-option × multiplicateur × quantité (signés)
    g = greeks or {}
    p['greeks_source'] = g.get('source', 'UNAVAILABLE')
    issues = p['data_quality'].setdefault('issues', [])
    for name in ('delta', 'gamma', 'theta', 'vega'):
        per = g.get(name)
        if per is None:
            p[name] = None
            continue
        p[name] = round(per * mult * (qty or 0), 4)
        p[f'{name}_per_option'] = per
    # Cohérence des signes (long uniquement — le desk modélise l'achat)
    dpo = g.get('delta')
    if dpo is not None:
        if right == 'CALL' and dpo < 0:
            issues.append('DELTA_SIGN_INCONSISTENT')
        if right == 'PUT' and dpo > 0:
            issues.append('DELTA_SIGN_INCONSISTENT')
    if g.get('gamma') is not None and g['gamma'] < 0:
        issues.append('GAMMA_SIGN_INCONSISTENT')
    if g.get('vega') is not None and g['vega'] < 0:
        issues.append('VEGA_SIGN_INCONSISTENT')

    # Divergence broker/modèle (§12)
    bd, md = g.get('broker_delta'), g.get('model_delta')
    if bd is not None and md is not None and abs(bd - md) >= 0.12:
        issues.append('BROKER_MODEL_GREEK_DIVERGENCE')

    p['data_quality']['overall'] = ('OK' if _n(mark) else 'MISSING_MARK')
    if q.get('stale'):
        p['data_quality']['overall'] = 'STALE'
    return p


def portfolio_weights(positions: list[dict]) -> list[dict]:
    """Poids = valeur (ou coût si non cotée, étiqueté) / total."""
    total = 0.0
    for p in positions:
        v = p.get('market_value')
        if v is None:
            v = p.get('cost_basis') or p.get('capital_committed')
        if v is not None:
            total += v
    for p in positions:
        v = p.get('market_value')
        based_on_cost = v is None
        if v is None:
            v = p.get('cost_basis') or p.get('capital_committed')
        p['weight_pct'] = round(v / total * 100, 2) if (v is not None and total) else None
        p['weight_based_on_cost'] = based_on_cost if p['weight_pct'] is not None else None
    return positions


def mae_mfe(cost_basis: float, values: list[float]) -> dict:
    """MAE/MFE en % depuis la série de valeurs de la position (déclarée)."""
    if not values or not cost_basis:
        return {'mae': None, 'mfe': None, 'drawdown_from_peak': None}
    rel = [(v / cost_basis - 1) * 100 for v in values]
    peak = values[0]
    dd = 0.0
    for v in values:
        peak = max(peak, v)
        dd = min(dd, (v / peak - 1) * 100)
    return {'mae': round(min(rel), 2), 'mfe': round(max(rel), 2),
            'drawdown_from_peak': round(dd, 2)}


__all__ = ['enrich_stock', 'enrich_option', 'portfolio_weights', 'mae_mfe']
