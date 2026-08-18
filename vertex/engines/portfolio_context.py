"""vertex/engines/portfolio_context.py — PORTFOLIOCONTEXT CANONIQUE (SKYLER LOT 7).

Depuis les positions CANONIQUES (vertex.positions.repository — provenance
étiquetée MANUAL/IBKR, simulées exclues), construit le contexte portefeuille :
poids par titre, concentration (HHI, top), bornes 8-15 du profil V2, candidat
(gagnant/perdant, impact marginal), sizing S+/S/A/B.

Règles d'honnêteté :
  - les allocations par niveau sont des PLAFONDS ANALYTIQUES de la Constitution
    V2 — `never_triggers_orders: true`, jamais un ordre ;
  - JAMAIS renforcer un perdant ; un gagnant n'est renforçable qu'APRÈS
    confirmation (liste V2) ; P&L inconnu → renforcement inconnu, pas autorisé ;
  - sans cote : valorisation au COÛT, étiquetée ; sans stops déclarés : budget
    de risque `available: false` (jamais estimé) ;
  - fonction PURE, déterministe. Lecture seule, aucun ordre.
"""
from __future__ import annotations

from vertex.portfolio.correlation import correlation_matrix


def _profile():
    from vertex.strategy.constitution import load_profile
    return load_profile()


def _aligned_returns(series_by_symbol, symbols):
    """Rendements quotidiens strictement alignés sur les dates communes.

    Une liste de clôtures sans dates, ou un recouvrement inférieur à 31 séances,
    ne suffit pas à déclarer une corrélation disponible.
    """
    points = {}
    for symbol in symbols:
        series = (series_by_symbol or {}).get(symbol) or {}
        dates, closes = series.get('dates'), series.get('close')
        if not isinstance(dates, list) or not isinstance(closes, list) or len(dates) != len(closes):
            continue
        values = {}
        for date, close in zip(dates, closes):
            try:
                value = float(close)
            except (TypeError, ValueError):
                continue
            if date and value > 0:
                values[str(date)] = value
        if len(values) >= 31:
            points[symbol] = values
    if len(points) < 2:
        return {}, 'séries datées insuffisantes pour au moins deux positions'
    common = set.intersection(*(set(values) for values in points.values()))
    if len(common) < 31:
        return {}, 'moins de 31 séances communes entre les positions'
    ordered = [date for date in next(iter(points.values())) if date in common]
    out = {}
    for symbol, values in points.items():
        closes = [values[date] for date in ordered]
        returns = [(current / previous - 1.0) for previous, current in zip(closes, closes[1:])
                   if previous > 0]
        if len(returns) >= 30:
            out[symbol] = returns
    return out, (None if len(out) >= 2 else 'rendements alignés insuffisants')


def build(positions, quotes=None, sym=None, capital=None, profile=None, series_by_symbol=None):
    """positions : liste canonique (repository.load_positions). quotes : {SYM: px}.
    capital : base de sizing (sinon valeur investie totale). sym : candidat étudié."""
    prof = profile or _profile()
    quotes = quotes or {}
    open_real = [p for p in (positions or [])
                 if isinstance(p, dict) and p.get('is_real') is not False
                 and str(p.get('status') or 'OPEN').upper() != 'CLOSED']
    if not open_real:
        return {'available': False,
                'reason': 'aucune position réelle déclarée (desk/IBKR) — contexte portefeuille indisponible'}

    valued_at_cost = 0
    by_sym = {}
    asset_values = {}
    asset_counts = {}
    unclassified_assets = 0
    for p in open_real:
        s = str(p.get('symbol') or p.get('sym') or '').upper()
        if not s:
            continue
        qty = p.get('quantity') or 0
        px = quotes.get(s)
        if px is not None and qty:
            val = qty * float(px)
        else:
            val = p.get('cost_basis') or 0.0
            valued_at_cost += 1
        asset_type = str(p.get('asset_type') or '').upper()
        if not asset_type:
            asset_type = 'UNCLASSIFIED'
            unclassified_assets += 1
        asset_values[asset_type] = asset_values.get(asset_type, 0.0) + val
        asset_counts[asset_type] = asset_counts.get(asset_type, 0) + 1
        e = by_sym.setdefault(s, {'value': 0.0, 'cost': 0.0, 'qty': 0.0})
        e['value'] += val
        e['cost'] += p.get('cost_basis') or 0.0
        e['qty'] += qty or 0.0

    total = sum(e['value'] for e in by_sym.values())
    if total <= 0:
        return {'available': False, 'reason': 'valeur totale nulle — poids incalculables'}
    weights = {s: round(e['value'] / total * 100, 2) for s, e in by_sym.items()}
    asset_mix = {
        asset: {'value': round(value, 2), 'weight_pct': round(value / total * 100, 2),
                'positions': asset_counts.get(asset, 0)}
        for asset, value in sorted(asset_values.items())
    }
    from vertex.market import sectors
    sector_values, unclassified_sectors = {}, []
    for symbol, position in by_sym.items():
        sector = sectors.SECTOR_MAP.get(symbol)
        if not sector:
            unclassified_sectors.append(symbol)
            continue
        sector_values[sector] = sector_values.get(sector, 0.0) + position['value']
    classified_sector_value = sum(sector_values.values())
    sector_mix = {
        sector: {'value': round(value, 2), 'weight_pct': round(value / total * 100, 2)}
        for sector, value in sorted(sector_values.items())
    }
    sector_coverage = {
        'available': bool(sector_values), 'classified_symbols': sorted(
            symbol for symbol in by_sym if symbol not in unclassified_sectors),
        'unclassified_symbols': sorted(unclassified_sectors),
        'classified_value_pct': round(100 * classified_sector_value / total, 1),
        'unclassified_value_pct': round(100 * (total - classified_sector_value) / total, 1),
        'read_only': True,
        'note': 'seul le référentiel sectoriel existant est utilisé ; aucun secteur par défaut',
    }
    hhi = round(sum((e['value'] / total) ** 2 for e in by_sym.values()), 4)
    top_sym = max(by_sym, key=lambda s: by_sym[s]['value'])

    n = len(by_sym)
    pmin, pmax = prof.portfolio_min_positions, prof.portfolio_max_positions
    max_w = prof.max_stock_weight_pct
    rules = (prof.raw.get('position_rules') or {})
    confirmations = rules.get('add_only_after_confirmation') or []

    # ── Candidat ────────────────────────────────────────────────────────────────
    candidate = None
    if sym:
        s = str(sym).upper()
        held = s in by_sym
        weight = weights.get(s, 0.0)
        pnl_pct = None
        if held:
            e = by_sym[s]
            px = quotes.get(s)
            if px is not None and e['qty'] and e['cost']:
                avg = e['cost'] / e['qty']
                pnl_pct = round((float(px) / avg - 1) * 100, 2) if avg > 0 else None
        is_loser = (None if pnl_pct is None else bool(pnl_pct < 0)) if held else False
        if not held:
            reinforcement = 'NOT_HELD'
        elif is_loser is True:
            reinforcement = False           # JAMAIS renforcer un perdant (V2)
        elif is_loser is False:
            reinforcement = 'AFTER_CONFIRMATION'   # gagnant : preuve exigée, pas un oui aveugle
        else:
            reinforcement = None            # P&L inconnu → inconnu, pas autorisé
        candidate = {'symbol': s, 'held': held, 'weight_pct': weight,
                     'pnl_pct': pnl_pct, 'is_loser': is_loser,
                     'reinforcement_allowed': reinforcement,
                     'reinforcement_conditions': list(confirmations),
                     'note': 'Jamais renforcer un perdant ; gagnant renforçable seulement après confirmation (Constitution V2).'}

    # ── Sizing par niveau (plafonds analytiques V2) ─────────────────────────────
    sizing = None
    lv = prof.raw.get('conviction_levels') or {}
    base = capital if capital is not None else total
    levels = {}
    cand_w = (candidate or {}).get('weight_pct', 0.0) if candidate else 0.0
    for name in ('S_PLUS', 'S', 'A', 'B'):
        cfg = lv.get(name) or {}
        alloc = cfg.get('allocation_pct')
        if not alloc:
            continue
        amounts = [round(base * alloc[0] / 100.0, 2), round(base * alloc[1] / 100.0, 2)]
        resulting = round(cand_w + alloc[1], 2)
        levels[name] = {'allocation_pct': list(alloc), 'amount_range': amounts,
                        'resulting_weight_pct': resulting,
                        'concentration_breach': bool(resulting > max_w)}
    if levels:
        sizing = {'base': base,
                  'base_note': ('capital fourni' if capital is not None
                                else 'valeur investie totale (capital non fourni)'),
                  'levels': levels, 'max_stock_weight_pct': max_w,
                  'never_triggers_orders': True,
                  'note': 'Plafonds ANALYTIQUES de la Constitution V2 — jamais un ordre.'}

    returns, correlation_reason = _aligned_returns(series_by_symbol, list(by_sym))
    correlations = correlation_matrix(returns) if returns else {}
    if returns:
        correlation_context = {
            'available': bool(correlations.get('pairs')),
            'average': correlations.get('average'),
            'high_pairs': correlations.get('high_pairs') or {},
            'pairs': correlations.get('pairs') or {},
            'symbols_covered': correlations.get('symbols_covered') or [],
            'warning': correlations.get('warning'),
            'method': 'rendements journaliers alignés sur dates communes ; minimum 30 rendements',
        }
        if not correlation_context['available']:
            correlation_context['reason'] = 'aucune paire corrélable malgré les séries disponibles'
    else:
        correlation_context = {'available': False,
                               'reason': correlation_reason or 'données de corrélation non branchées'}

    from vertex.portfolio import historical_stress
    stress_test = historical_stress.assess(weights, series_by_symbol)
    measured_risk, unmeasured_risk = [], []
    for position in open_real:
        symbol = str(position.get('symbol') or position.get('sym') or '').upper()
        quantity = position.get('quantity') or 0
        price, stop = quotes.get(symbol), position.get('stop')
        asset_type = str(position.get('asset_type') or '').upper()
        if asset_type == 'OPTION':
            unmeasured_risk.append({'symbol': symbol, 'reason': 'option : perte au stop sous-jacent non valorisable sans grecques de position'})
            continue
        if price is None or stop is None or not quantity:
            unmeasured_risk.append({'symbol': symbol, 'reason': 'cote, stop ou quantité manquant'})
            continue
        try:
            risk_value = (float(price) - float(stop)) * float(quantity)
        except (TypeError, ValueError):
            unmeasured_risk.append({'symbol': symbol, 'reason': 'cote, stop ou quantité non numérique'})
            continue
        if risk_value < 0:
            unmeasured_risk.append({'symbol': symbol, 'reason': 'stop au-dessus de la cote : risque long non interprétable'})
            continue
        measured_risk.append({'symbol': symbol, 'risk_to_stop': round(risk_value, 2)})
    risk_coverage = round(100 * len(measured_risk) / len(open_real), 1) if open_real else 0.0
    risk_budget = {'available': bool(measured_risk), 'read_only': True,
                   'covered_positions': len(measured_risk), 'total_positions': len(open_real),
                   'coverage_pct': risk_coverage,
                   'known_risk_to_stop': round(sum(item['risk_to_stop'] for item in measured_risk), 2) if measured_risk else None,
                   'by_position': measured_risk, 'unmeasured': unmeasured_risk,
                   'note': 'perte jusqu’au stop déclarée ; positions sans preuve de stop ne sont pas estimées'}
    if not measured_risk:
        risk_budget['reason'] = 'aucun stop mesurable — budget de risque non estimé'
    from vertex.portfolio.factor_exposure import portfolio_factor_exposure
    factor_input = {symbol: {'returns': returns.get(symbol) or []} for symbol in by_sym}
    factor_exposure = portfolio_factor_exposure(
        type('Snapshot', (), {'positions': [type('Position', (), {'symbol': symbol})() for symbol in by_sym],
                              'weights': lambda _self: weights})(),
        factor_input,
        returns.get('SPY') if returns else None,
    )
    factor_availability = {
        factor: {'available': (item.get('value') is not None),
                 'coverage_pct': item.get('coverage_pct', 0.0),
                 'reason': (None if item.get('value') is not None else
                            'preuve facteur indisponible pour les positions couvertes')}
        for factor, item in factor_exposure.items()
    }
    factor_coverage = max((item.get('coverage_pct') or 0 for item in factor_exposure.values()), default=0)
    factor_context = {
        'available': bool(returns), 'coverage_pct_max': factor_coverage,
        'factors': factor_exposure,
        'availability': factor_availability,
        'method': 'rendements canoniques alignés ; facteurs fondamentaux absents restent non disponibles',
        'read_only': True, 'never_triggers_orders': True,
    }
    if not returns:
        factor_context['reason'] = correlation_reason or 'rendements canoniques insuffisants'

    return {
        'available': True, 'generator': 'deterministic',
        'n_positions': n, 'bounds': {'min': pmin, 'max': pmax},
        'in_bounds': bool(pmin <= n <= pmax), 'free_slots': max(0, pmax - n),
        'total_value': round(total, 2), 'weights': weights, 'hhi': hhi,
        'asset_mix': asset_mix,
        'sector_mix': sector_mix,
        'sector_coverage': sector_coverage,
        'asset_mix_note': ('%d position(s) sans type d’actif canonique — jamais classée(s) par défaut'
                           % unclassified_assets if unclassified_assets else None),
        'top_symbol': top_sym, 'top_weight_pct': weights[top_sym],
        'valuation_note': ('%d position(s) valorisée(s) au coût (cote absente) — jamais un prix inventé'
                           % valued_at_cost if valued_at_cost else None),
        'candidate': candidate, 'sizing': sizing,
        'risk_budget': risk_budget,
        'correlations': correlation_context,
        'stress_test': stress_test,
        'factor_exposure': factor_context,
        'provenance': sorted({p.get('source') or 'MANUAL' for p in open_real}),
    }


__all__ = ['build']
