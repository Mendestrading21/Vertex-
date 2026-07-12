"""vertex.positions.recalculator — orchestrateur du cycle de vie (§3-§19).

Assemble, pour chaque position : enrichissement (calculs) → cycle de vie
(statut) → santé de thèse → priorité → action analytique → verdict moteur.
Le verdict FINAL canonique reste produit par l'ExecutiveEngine (moteur
unique) ; ce module ne fait qu'orchestrer et présenter. LECTURE SEULE.
"""
from __future__ import annotations

import time

from vertex.positions import calculator, lifecycle, thesis_health
from vertex.positions.repository import load_positions


def _detail_for(scan_state: dict, sym: str) -> dict:
    return ((scan_state or {}).get('detail') or {}).get((sym or '').upper()) or {}


def _quote_for_stock(scan_state, quotes, p):
    """Cote une action : pos-quotes composite d'abord, sinon detail scan."""
    key = '%s||%s|' % (p['symbol'], '')
    q = (quotes or {}).get(key) or (quotes or {}).get(p['symbol'])
    if q and (q.get('spot') is not None or q.get('mark') is not None):
        return {'price': q.get('spot') if q.get('spot') is not None else q.get('mark'),
                'source': 'IBKR/desk', 'stale': False}
    d = _detail_for(scan_state, p['symbol'])
    if d.get('price') is not None:
        return {'price': d['price'], 'source': scan_state.get('source') or 'scan',
                'stale': (scan_state.get('source') == 'demo')}
    return None


def _quote_for_option(quotes, p):
    exp = p.get('expiration') or ''
    strike = p.get('strike') if p.get('strike') is not None else ''
    right = 'P' if p.get('right') == 'PUT' else 'C'
    key = '%s|%s|%s|%s' % (p['symbol'], exp, strike, right)
    q = (quotes or {}).get(key)
    if not q:
        return None, None
    opt_q = {'mark': q.get('mark') if q.get('mark') is not None else q.get('last'),
             'bid': q.get('bid'), 'ask': q.get('ask'), 'iv': q.get('iv'),
             'volume': q.get('vol'), 'oi': q.get('oi'),
             'source': 'IBKR', 'stale': False}
    under = {'price': q.get('spot')} if q.get('spot') is not None else None
    return opt_q, under


def recalculate_all(scan_state: dict, desk_blob: dict | None = None,
                    quotes: dict | None = None,
                    ibkr_positions: list | None = None) -> dict:
    """Recalcule TOUTES les positions ouvertes et le portefeuille agrégé."""
    positions = load_positions(desk_blob, ibkr_positions)
    positions = [p for p in positions if p.get('status') != 'CLOSED']

    for p in positions:
        d = _detail_for(scan_state, p.get('symbol') or p.get('underlying_symbol'))
        if p['asset_type'] == 'OPTION':
            oq, uq = _quote_for_option(quotes, p)
            greeks = None
            if oq and oq.get('iv') is not None:
                greeks = {'source': 'BROKER_GREEKS'} if ibkr_positions else None
            calculator.enrich_option(p, oq, uq, greeks, d)
            p['lifecycle_status'] = lifecycle.option_status(p)
        else:
            calculator.enrich_stock(p, _quote_for_stock(scan_state, quotes, p),
                                    detail=d)
            p['lifecycle_status'] = lifecycle.stock_status(p)
        th = thesis_health.assess(p, d, p.get('thesis_health')
                                  if isinstance(p.get('thesis_health'), str) else None)
        p['thesis_health'] = th['overall_status']
        p['thesis_detail'] = th
        p['priority'] = lifecycle.priority(p)
        p['analytic_action'] = lifecycle.action_for(p)

    calculator.portfolio_weights(positions)

    # Verdict moteur (ExecutiveEngine) pour les actions scannées
    try:
        from vertex.strategy import executive_engine as _ee
        from vertex.market.regime_engine import classify_regime
        market = scan_state.get('market') or {}
        regime = classify_regime({'index_trend': market.get('spy_trend'),
                                  'breadth_pct': market.get('breadth'),
                                  'vix': market.get('vix')})
        for p in positions:
            d = _detail_for(scan_state, p.get('symbol') or p.get('underlying_symbol'))
            if not d:
                continue
            plan = d.get('plan') or {}
            packet = {'symbol': p['symbol'],
                      'fundamental': {'score': d.get('st_fund') or d.get('fund_score')},
                      'catalysts': {'score': 60 if d.get('earnings_dte') is not None else None},
                      'technical': {'score': d.get('score'),
                                    'reward_risk': p.get('remaining_rr') or d.get('rr')
                                    or (plan.get('rr') if isinstance(plan, dict) else None),
                                    'timing_score': d.get('st_timing'),
                                    'thesis_invalidated': p.get('thesis_health') == 'INVALIDATED'},
                      'sentiment': {'score': d.get('rs')},
                      'data_quality': {'overall': 'RECENT' if scan_state.get('source') not in (None, 'demo') else 'MISSING',
                                       'actionable_allowed': scan_state.get('source') not in (None, 'demo')},
                      'reconciliation': {'actionable_allowed': True},
                      'guard': {'blocking_rules': [], 'mandatory_reviews': []},
                      'position_held': True,
                      'position_pl_pct': p.get('unrealized_pnl_pct'),
                      'market_regime': regime}
            verdict = _ee.decide(packet)
            p['decision'] = verdict['final_decision']
            p['decision_blocking'] = verdict.get('blocking_rules', [])
    except Exception:
        pass

    return {'positions': positions, 'portfolio': aggregate(positions),
            'updated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}


def aggregate(positions: list[dict]) -> dict:
    """Recalcul portefeuille (§23) — compteurs CALLS/PUTS séparés."""
    stocks = [p for p in positions if p['asset_type'] != 'OPTION']
    opts = [p for p in positions if p['asset_type'] == 'OPTION']
    calls = [p for p in opts if p.get('right') == 'CALL']
    puts = [p for p in opts if p.get('right') == 'PUT']

    def _sum(lst, field):
        vals = [p[field] for p in lst if p.get(field) is not None]
        return round(sum(vals), 2) if vals else None

    invested = _sum(positions, 'cost_basis') or 0
    invested += _sum(positions, 'capital_committed') or 0
    value = None
    marked = [p for p in positions if p.get('market_value') is not None]
    if marked and len(marked) == len(positions):
        value = round(sum(p['market_value'] for p in positions), 2)
    pl = round(value - invested, 2) if (value is not None and invested) else None

    # Greeks globaux — uniquement si TOUTES les options cotées avec Greeks broker
    delta = theta = None
    opt_greeks = [p for p in opts if p.get('delta') is not None]
    if opts and len(opt_greeks) == len(opts):
        delta = round(sum(p['delta'] for p in opts), 2)
        theta = round(sum(p['theta'] for p in opts if p.get('theta') is not None), 2)

    return {
        'value': value, 'value_at_cost': round(invested, 2) if invested else None,
        'unrealized_pnl': pl,
        'unrealized_pnl_pct': round(pl / invested * 100, 2) if (pl is not None and invested) else None,
        'stocks_count': len(stocks), 'stocks_max': 10,
        'calls_count': len(calls), 'puts_count': len(puts), 'puts_max': 1,
        'options_count': len(opts), 'options_max': 3,
        'delta_global': delta, 'theta_global': theta,
        'greeks_note': 'Greeks agrégés uniquement si toutes les options ont des Greeks broker (jamais estimés en agrégat).',
        'positions_needing_action': [
            {'position_id': p['position_id'], 'symbol': p['symbol'],
             'asset_type': p['asset_type'], 'priority': p.get('priority'),
             'status': p.get('lifecycle_status'), 'action': p.get('analytic_action'),
             'decision': p.get('decision'), 'pl_pct': p.get('unrealized_pnl_pct'),
             'updated_at': p.get('last_updated_at')}
            for p in sorted(positions, key=lambda x: {'P0_CRITICAL': 0, 'P1_HIGH': 1,
                                                      'P2_NORMAL': 2, 'P3_LOW': 3}.get(x.get('priority'), 4))
            if p.get('priority') in ('P0_CRITICAL', 'P1_HIGH')],
    }


__all__ = ['recalculate_all', 'aggregate']
