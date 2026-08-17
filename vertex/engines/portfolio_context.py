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

    return {
        'available': True, 'generator': 'deterministic',
        'n_positions': n, 'bounds': {'min': pmin, 'max': pmax},
        'in_bounds': bool(pmin <= n <= pmax), 'free_slots': max(0, pmax - n),
        'total_value': round(total, 2), 'weights': weights, 'hhi': hhi,
        'asset_mix': asset_mix,
        'asset_mix_note': ('%d position(s) sans type d’actif canonique — jamais classée(s) par défaut'
                           % unclassified_assets if unclassified_assets else None),
        'top_symbol': top_sym, 'top_weight_pct': weights[top_sym],
        'valuation_note': ('%d position(s) valorisée(s) au coût (cote absente) — jamais un prix inventé'
                           % valued_at_cost if valued_at_cost else None),
        'candidate': candidate, 'sizing': sizing,
        'risk_budget': {'available': False,
                        'reason': 'aucun stop déclaré par position — budget de risque non estimé'},
        'correlations': correlation_context,
        'stress_test': stress_test,
        'provenance': sorted({p.get('source') or 'MANUAL' for p in open_real}),
    }


__all__ = ['build']
