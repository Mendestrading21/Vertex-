"""vertex.options.scenario_pricer — simulateur multi-scénarios (§19).

Scénarios de spot (BEAR/STOP/FLAT/BASE/TP1/TP2/TP3) × temps (0/3/5/10/15/20/28 j)
× IV (−20 %/−10 %/0/+10 %/+20 %). Pricing Black-Scholes AVEC rendement de
dividende, taux par échéance (couche rates), et honnêteté §6.8 : le modèle
européen est une ESTIMATION pour des options américaines — étiquetée
MODEL_ESTIMATE, jamais présentée comme vérité broker.
"""
from __future__ import annotations

import math

from .models import GREEKS_MODEL
from vertex.data_sources.rates import RateCurve

TIME_SCENARIOS_DAYS = (0, 3, 5, 10, 15, 20, 28)
IV_SCENARIOS = (-0.20, -0.10, 0.0, 0.10, 0.20)

LIMITATIONS = [
    'pricing Black-Scholes européen : ESTIMATION pour des options américaines '
    '(exercice anticipé non modélisé) — préférer les valeurs broker quand disponibles',
    'dividendes intégrés via un rendement continu — un dividende exceptionnel '
    'proche de l’échéance peut fausser l’estimation',
    'IV supposée constante par strike dans chaque scénario (pas de déformation de smile)',
]


def _ncdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bs_price(spot: float, strike: float, t_years: float, iv: float,
             rate: float, right: str, dividend_yield: float = 0.0) -> float:
    """Prix BS avec dividende continu. À t=0, valeur intrinsèque."""
    right = right.upper()[:1]
    if t_years <= 0 or iv <= 0:
        return max(0.0, (spot - strike) if right == 'C' else (strike - spot))
    sq = iv * math.sqrt(t_years)
    d1 = (math.log(spot / strike) + (rate - dividend_yield + iv * iv / 2) * t_years) / sq
    d2 = d1 - sq
    if right == 'C':
        return spot * math.exp(-dividend_yield * t_years) * _ncdf(d1) \
            - strike * math.exp(-rate * t_years) * _ncdf(d2)
    return strike * math.exp(-rate * t_years) * _ncdf(-d2) \
        - spot * math.exp(-dividend_yield * t_years) * _ncdf(-d1)


def _implied_vol(price: float, spot: float, strike: float, t_years: float,
                 rate: float, right: str, dividend_yield: float = 0.0) -> float | None:
    """IV par bissection — utilisée seulement si la chaîne ne fournit pas d'IV."""
    if price <= 0 or t_years <= 0:
        return None
    lo, hi = 0.01, 4.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if bs_price(spot, strike, t_years, mid, rate, right, dividend_yield) < price:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 4)


def simulate(contract: dict, setup, rate_curve: RateCurve | None = None,
             holding_days: int = 10) -> dict:
    """Simule le contrat sur la grille scénarios × temps × IV.

    contract : ligne normalisée (mid/iv/delta/dte/right/strike, greeks_source).
    setup : UnderlyingSetup (spot, invalidation, TP1-3, dividende, expected move).
    Sortie : structure §19 (current/at_stop/at_tp1..3, time_decay, iv_sensitivity,
    worst_planned_loss_pct, base_expected_gain_pct, reward_risk, model_source,
    limitations).
    """
    spot = float(setup.spot)
    strike = float(contract['strike'])
    right = contract.get('right', 'C')
    dte = int(contract.get('dte') or 0)
    mid = contract.get('mid')
    iv = contract.get('iv')
    rate_curve = rate_curve or RateCurve()
    rate_q = rate_curve.rate_for_tenor(max(dte, 1))
    rate = rate_q.rate
    q = float(setup.dividend_yield or 0.0)

    result = {'current': {}, 'at_stop': None, 'at_tp1': None, 'at_tp2': None,
              'at_tp3': None, 'time_decay': [], 'iv_sensitivity': [],
              'worst_planned_loss_pct': None, 'base_expected_gain_pct': None,
              'extended_gain_pct': None, 'reward_risk': None,
              'model_source': GREEKS_MODEL,
              'rate': rate_q.to_dict(), 'limitations': list(LIMITATIONS)}
    if not mid or mid <= 0 or dte <= 0 or spot <= 0:
        result['limitations'].append('données de contrat insuffisantes — simulation refusée '
                                     '(pas de chiffre inventé)')
        return result

    if iv is None or iv <= 0:
        iv = _implied_vol(mid, spot, strike, dte / 365.0, rate, right, q)
        if iv is None:
            result['limitations'].append('IV indisponible et non inversible — simulation refusée')
            return result
        result['limitations'].append('IV recalculée depuis le mid (FALLBACK_ESTIMATE)')
        result['model_source'] = 'FALLBACK_ESTIMATE'

    em_pct = setup.expected_move_pct
    if em_pct is None:
        em_pct = iv * math.sqrt(holding_days / 365.0) * 100

    # ── grille de scénarios de spot ───────────────────────────────────
    stop = setup.invalidation
    spots = {
        'BEAR': spot * (1 - 1.5 * em_pct / 100),
        'STOP': stop if stop else spot * (1 - em_pct / 100),
        'FLAT': spot,
        'BASE': spot * (1 + em_pct / 100) if right == 'C' else spot * (1 - em_pct / 100),
        'TP1': setup.tp1, 'TP2': setup.tp2, 'TP3': setup.tp3,
    }

    def value(s, days_elapsed, iv_shift=0.0):
        t = max(dte - days_elapsed, 0) / 365.0
        return bs_price(s, strike, t, iv * (1 + iv_shift), rate, right, q)

    def pnl_pct(v):
        return round((v - mid) / mid * 100, 1)

    scen_out = {}
    for name, s in spots.items():
        if s is None:
            scen_out[name] = None
            continue
        by_time = {}
        for days in TIME_SCENARIOS_DAYS:
            if days > dte:
                continue
            v = value(s, days)
            by_time[days] = {'value': round(v, 3), 'pnl_pct': pnl_pct(v)}
        scen_out[name] = {'spot': round(float(s), 2), 'by_time_days': by_time}
    result['current'] = scen_out.get('FLAT')
    result['at_stop'] = scen_out.get('STOP')
    result['at_tp1'] = scen_out.get('TP1')
    result['at_tp2'] = scen_out.get('TP2')
    result['at_tp3'] = scen_out.get('TP3')
    result['scenarios'] = scen_out

    # ── décomposition temps (spot inchangé) ───────────────────────────
    result['time_decay'] = [
        {'days': d, 'value': round(value(spot, d), 3), 'pnl_pct': pnl_pct(value(spot, d))}
        for d in TIME_SCENARIOS_DAYS if d <= dte]

    # ── sensibilité IV (au scénario BASE, horizon de détention) ───────
    base_spot = spots['BASE']
    h = min(holding_days, dte)
    result['iv_sensitivity'] = [
        {'iv_shift_pct': int(sh * 100),
         'value': round(value(base_spot, h, sh), 3),
         'pnl_pct': pnl_pct(value(base_spot, h, sh))}
        for sh in IV_SCENARIOS]

    # ── métriques de plan ─────────────────────────────────────────────
    if stop:
        stop_pnls = [v['pnl_pct'] for d, v in scen_out['STOP']['by_time_days'].items()
                     if d <= holding_days]
        if stop_pnls:
            result['worst_planned_loss_pct'] = min(stop_pnls)
    base_pnl = scen_out['BASE']['by_time_days'].get(h) or \
        list(scen_out['BASE']['by_time_days'].values())[-1]
    result['base_expected_gain_pct'] = base_pnl['pnl_pct']
    tp2 = scen_out.get('TP2')
    if tp2 and tp2['by_time_days']:
        ext = tp2['by_time_days'].get(h) or list(tp2['by_time_days'].values())[-1]
        result['extended_gain_pct'] = ext['pnl_pct']
    loss = result['worst_planned_loss_pct']
    gain = result['base_expected_gain_pct']
    if loss is not None and loss < 0 and gain is not None and gain > 0:
        result['reward_risk'] = round(gain / abs(loss), 2)
    return result


def capital_free_analysis(sim: dict, contract: dict, capital: float | None = None) -> dict:
    """Analyse indépendante du capital (§8.4). Nombre de contrats SEULEMENT si
    un capital est explicitement fourni — jamais inventé."""
    mid = contract.get('mid') or 0
    cost_per_contract = mid * 100 if mid else None
    out = {'estimated_gain_pct': sim.get('base_expected_gain_pct'),
           'estimated_extended_gain_pct': sim.get('extended_gain_pct'),
           'estimated_loss_pct': sim.get('worst_planned_loss_pct'),
           'reward_risk': sim.get('reward_risk'),
           'cost_per_contract': round(cost_per_contract, 2) if cost_per_contract else None,
           'risk_per_contract': None, 'contracts': None}
    loss = sim.get('worst_planned_loss_pct')
    if cost_per_contract and loss is not None:
        out['risk_per_contract'] = round(cost_per_contract * abs(loss) / 100, 2)
    if capital is not None and cost_per_contract:
        out['contracts'] = int(capital // cost_per_contract)
        out['capital_provided'] = capital
    return out
