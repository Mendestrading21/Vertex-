"""multileg_lab — analyse de stratégies options MULTI-JAMBES (READONLY).

Payoff à l'échéance, breakevens, gain/perte max (avec détection d'illimité),
probabilité de profit (modèle lognormal risque-neutre) et greeks agrégés — pour
les combinaisons que le scenario_pricer mono-jambe ne couvre pas : verticaux,
straddle/strangle, butterfly, iron condor…

100 % calcul local, AUCUNE dépendance externe (réutilise le Black-Scholes maison de
`options_lab`), AUCUN ordre : Vertex reste en lecture seule. L'UI se contente de tracer
les points renvoyés ici ; ce module ne price que ce qu'on lui donne (primes déclarées).

Convention de jambe : {type:'call'|'put'|'stock', strike, premium, qty}. qty>0 = long
(on paie), qty<0 = short (on encaisse). Les options portent un multiplicateur 100
(1 contrat = 100 actions) ; les actions un multiplicateur 1. Les montants (gain/perte
max, débit net) sont en DOLLARS ; les breakevens sont des niveaux de prix.
"""
from __future__ import annotations

import math

from vertex.engines.options_lab import _ncdf, _npdf

R_DEFAULT = 0.045  # taux sans risque annuel par défaut


def _mult(leg):
    return 100.0 if leg.get('type') in ('call', 'put') else 1.0


def _intrinsic(price, leg):
    """Valeur intrinsèque d'une jambe à l'échéance, par action (avant qty)."""
    t = leg.get('type')
    k = leg.get('strike') or 0.0
    if t == 'call':
        return max(0.0, price - k)
    if t == 'put':
        return max(0.0, k - price)
    return price  # stock : « intrinsèque » = cours


def _pnl(price, legs):
    """P&L de la stratégie à l'échéance, en DOLLARS, pour un cours sous-jacent donné."""
    total = 0.0
    for leg in legs:
        q = leg.get('qty') or 0.0
        m = _mult(leg)
        prem = leg.get('premium') or 0.0
        total += q * m * (_intrinsic(price, leg) - prem)
    return total


def _net_premium(legs):
    """Débit net (>0 = on paie) / crédit net (<0 = on encaisse), en dollars."""
    return sum((leg.get('qty') or 0.0) * _mult(leg) * (leg.get('premium') or 0.0)
               for leg in legs)


def _leg_greeks(spot, leg, T, iv, r=R_DEFAULT):
    """Greeks d'une jambe, déjà multipliés par qty et le multiplicateur (position)."""
    q = leg.get('qty') or 0.0
    m = _mult(leg)
    if leg.get('type') == 'stock':
        return {'delta': q * m, 'gamma': 0.0, 'theta': 0.0, 'vega': 0.0}
    k = leg.get('strike') or 0.0
    right = 'CALL' if leg.get('type') == 'call' else 'PUT'
    if T <= 0 or iv <= 0 or spot <= 0 or k <= 0:
        return {'delta': 0.0, 'gamma': 0.0, 'theta': 0.0, 'vega': 0.0}
    sq = iv * math.sqrt(T)
    d1 = (math.log(spot / k) + (r + iv * iv / 2.0) * T) / sq
    d2 = d1 - sq
    nd1 = _npdf(d1)
    if right == 'CALL':
        delta = _ncdf(d1)
        theta_yr = -(spot * nd1 * iv) / (2.0 * math.sqrt(T)) - r * k * math.exp(-r * T) * _ncdf(d2)
    else:
        delta = _ncdf(d1) - 1.0
        theta_yr = -(spot * nd1 * iv) / (2.0 * math.sqrt(T)) + r * k * math.exp(-r * T) * _ncdf(-d2)
    gamma = nd1 / (spot * sq)
    vega = spot * nd1 * math.sqrt(T)
    scale = q * m
    return {
        'delta': scale * delta,               # par $1 de sous-jacent
        'gamma': scale * gamma,
        'theta': scale * theta_yr / 365.0,    # par jour
        'vega': scale * vega / 100.0,         # par point d'IV (1 %)
    }


def _lognormal_pdf(price, spot, T, iv, r=R_DEFAULT):
    """Densité risque-neutre du cours à l'échéance (S_T lognormal)."""
    if price <= 0 or spot <= 0 or T <= 0 or iv <= 0:
        return 0.0
    sq = iv * math.sqrt(T)
    mu = math.log(spot) + (r - iv * iv / 2.0) * T
    z = (math.log(price) - mu) / sq
    return _npdf(z) / (price * sq)


def _breakevens(legs, grid, pnls):
    """Prix où le P&L croise zéro (interpolation linéaire entre points de grille)."""
    bes = []
    for i in range(1, len(grid)):
        a, b = pnls[i - 1], pnls[i]
        if a == 0.0:
            bes.append(round(grid[i - 1], 2))
        elif (a < 0.0) != (b < 0.0):  # changement de signe
            x0, x1 = grid[i - 1], grid[i]
            be = x0 + (x1 - x0) * (0.0 - a) / (b - a)
            bes.append(round(be, 2))
    # dédoublonnage (croisements ~ identiques)
    out = []
    for be in bes:
        if not out or abs(be - out[-1]) > 1e-6:
            out.append(be)
    return out


def analyze_strategy(legs, spot, iv, days_to_exp, r=R_DEFAULT, name=None):
    """Analyse complète d'une stratégie multi-jambes.

    Retourne un dict JSON-sérialisable ; toute donnée manquante => None honnête
    (jamais un chiffre inventé). Renvoie {'available': False, ...} si l'entrée est
    insuffisante pour un calcul honnête.
    """
    legs = [l for l in (legs or []) if l and l.get('type') in ('call', 'put', 'stock')
            and (l.get('qty') or 0.0) != 0.0]
    if not legs or not spot or spot <= 0:
        return {'available': False, 'reason': 'jambes ou cours sous-jacent manquants.'}
    # primes requises pour un P&L honnête (sinon on ne devine pas la prime)
    if any(l.get('type') in ('call', 'put') and l.get('premium') is None for l in legs):
        return {'available': False, 'reason': 'prime manquante sur une jambe — pas de P&L inventé.'}

    T = max(0.0, (days_to_exp or 0) / 365.0)
    strikes = [l['strike'] for l in legs if l.get('strike')]
    hi = max([spot] + strikes) * 3.0
    steps = 480
    grid = [hi * i / steps for i in range(steps + 1)]  # inclut 0
    pnls = [_pnl(p, legs) for p in grid]

    max_profit = max(pnls)
    max_loss = min(pnls)
    # illimité vers le haut si la pente terminale (au-delà de tous les strikes) est > 0
    right_slope = sum((l.get('qty') or 0.0) * _mult(l)
                      for l in legs if l.get('type') in ('call', 'stock'))
    profit_unbounded = right_slope > 1e-9
    # perte : le cours ne peut pas descendre sous 0 => toujours bornée (P&L(0) inclus)
    breakevens = _breakevens(legs, grid, pnls)

    # Probabilité de profit : intègre la densité lognormale sur les zones P&L >= 0.
    pop = None
    if T > 0 and iv and iv > 0:
        pgrid_hi = spot * math.exp(5.0 * iv * math.sqrt(T))
        pn = 1200
        pg = [pgrid_hi * i / pn for i in range(1, pn + 1)]  # évite 0
        dens = [_lognormal_pdf(p, spot, T, iv, r) for p in pg]
        step = pgrid_hi / pn
        total = sum(dens) * step
        if total > 0:
            prof = sum(d for p, d in zip(pg, dens) if _pnl(p, legs) >= 0.0) * step
            pop = round(prof / total * 100.0, 1)

    # Greeks agrégés (position)
    g = {'delta': 0.0, 'gamma': 0.0, 'theta': 0.0, 'vega': 0.0}
    have_iv = bool(iv and iv > 0 and T > 0)
    if have_iv:
        for leg in legs:
            lg = _leg_greeks(spot, leg, T, iv, r)
            for k in g:
                g[k] += lg[k]
        g = {k: round(v, 4) for k, v in g.items()}
    else:
        g = None

    net = _net_premium(legs)
    # Courbe payoff pour le tracé : ~80 points autour de la zone utile (0.4x → 1.8x spot).
    lo_c, hi_c = spot * 0.4, min(hi, spot * 1.8)
    cn = 80
    payoff = [{'price': round(lo_c + (hi_c - lo_c) * i / cn, 2),
               'pnl': round(_pnl(lo_c + (hi_c - lo_c) * i / cn, legs), 2)}
              for i in range(cn + 1)]

    return {
        'available': True,
        'name': name,
        'spot': round(spot, 2),
        'iv': round(iv, 4) if iv else None,
        'days_to_exp': days_to_exp,
        'legs': [{'type': l['type'], 'strike': l.get('strike'),
                  'premium': l.get('premium'), 'qty': l.get('qty')} for l in legs],
        'net_premium': round(net, 2),          # >0 débit (on paie) · <0 crédit (on encaisse)
        'is_credit': net < 0,
        'max_profit': None if profit_unbounded else round(max_profit, 2),
        'max_profit_unbounded': profit_unbounded,
        'max_loss': round(max_loss, 2),        # toujours borné (cours >= 0)
        'breakevens': breakevens,
        'probability_of_profit': pop,          # % (modèle lognormal, estimation)
        'greeks': g,                           # position (delta $1, theta/jour, vega/1%IV)
        'payoff': payoff,
        'model_note': 'Payoff à l’échéance ; PoP = modèle lognormal risque-neutre — estimation, pas une promesse.',
    }


# ─── Presets de stratégies : construit des jambes depuis 1-2 strikes déclarés ───

def build_preset(kind, spot, ref, prem=None):
    """Construit les jambes d'une stratégie canonique autour de `ref` (map de contrats).

    `ref` : {'atm':{'strike','call','put'}, 'otm_call':{...}, 'otm_put':{...}} — primes par
    action déclarées (jamais inventées). Renvoie une liste de jambes ou None si données
    insuffisantes. Sert de commodité UI ; l'utilisateur peut aussi passer des jambes libres.
    """
    def leg(t, node, key, qty):
        if not node or node.get('strike') is None or node.get(key) is None:
            return None
        return {'type': t, 'strike': node['strike'], 'premium': node[key], 'qty': qty}

    atm = (ref or {}).get('atm'); oc = (ref or {}).get('otm_call'); op = (ref or {}).get('otm_put')
    legs = None
    if kind == 'long_call':
        legs = [leg('call', atm, 'call', 1)]
    elif kind == 'long_put':
        legs = [leg('put', atm, 'put', 1)]
    elif kind == 'straddle':
        legs = [leg('call', atm, 'call', 1), leg('put', atm, 'put', 1)]
    elif kind == 'strangle':
        legs = [leg('call', oc, 'call', 1), leg('put', op, 'put', 1)]
    elif kind == 'bull_call_spread':
        legs = [leg('call', atm, 'call', 1), leg('call', oc, 'call', -1)]
    elif kind == 'bear_put_spread':
        legs = [leg('put', atm, 'put', 1), leg('put', op, 'put', -1)]
    elif kind == 'iron_condor':
        legs = [leg('put', op, 'put', 1), leg('put', atm, 'put', -1),
                leg('call', atm, 'call', -1), leg('call', oc, 'call', 1)]
    if not legs or any(l is None for l in legs):
        return None
    return legs


STRATEGY_LABELS = {
    'long_call': 'Call long', 'long_put': 'Put long', 'straddle': 'Straddle (ATM)',
    'strangle': 'Strangle (OTM)', 'bull_call_spread': 'Spread haussier (call)',
    'bear_put_spread': 'Spread baissier (put)', 'iron_condor': 'Iron condor',
}
_STRATEGY_ORDER = ['bull_call_spread', 'bear_put_spread', 'iron_condor', 'straddle',
                   'strangle', 'long_call', 'long_put']


# Adéquation directionnelle de base par stratégie (0 = contre-indiqué, 1 = idéal).
_FIT = {
    'long_call':        {'bullish': 1.00, 'bearish': 0.00, 'neutral': 0.20},
    'bull_call_spread': {'bullish': 0.90, 'bearish': 0.00, 'neutral': 0.30},
    'long_put':         {'bullish': 0.00, 'bearish': 1.00, 'neutral': 0.20},
    'bear_put_spread':  {'bullish': 0.00, 'bearish': 0.90, 'neutral': 0.30},
    'iron_condor':      {'bullish': 0.25, 'bearish': 0.25, 'neutral': 1.00},
    'straddle':         {'bullish': 0.45, 'bearish': 0.45, 'neutral': 0.55},
    'strangle':         {'bullish': 0.45, 'bearish': 0.45, 'neutral': 0.55},
}
_BIAS_LABEL = {'bullish': 'haussier', 'bearish': 'baissier', 'neutral': 'neutre'}


def rank_strategies(strategies, bias='neutral'):
    """Note et classe les stratégies par ADÉQUATION au contexte (heuristique TRANSPARENTE,
    aide à la décision — pas une promesse). Score = 45 % alignement directionnel +
    30 % probabilité de profit + 25 % reward/risk. Marque la mieux adaptée `recommended`.
    Modifie et renvoie la liste triée."""
    bias = bias if bias in ('bullish', 'bearish', 'neutral') else 'neutral'
    for s in strategies:
        fit = _FIT.get(s.get('kind'), {}).get(bias, 0.4)
        pop = (s.get('probability_of_profit') or 0.0) / 100.0
        # reward/risk normalisé (illimité → plafonné à 1) ; perte bornée
        loss = abs(s.get('max_loss') or 0.0)
        if s.get('max_profit_unbounded'):
            rr = 1.0
        elif loss > 0 and s.get('max_profit') is not None:
            rr = min(1.0, (s['max_profit'] / loss) / 2.0)
        else:
            rr = 0.0
        score = 0.45 * fit + 0.30 * pop + 0.25 * rr
        s['fit_score'] = round(score * 100, 1)
        bits = ['aligné ' + _BIAS_LABEL[bias] if fit >= 0.7 else
                ('neutre au biais' if fit >= 0.4 else 'peu aligné au biais')]
        if s.get('probability_of_profit') is not None:
            bits.append('PoP %s%%' % s['probability_of_profit'])
        if rr >= 0.5:
            bits.append('R:R favorable')
        s['fit_reason'] = ' · '.join(bits)
    strategies.sort(key=lambda s: s.get('fit_score', 0), reverse=True)
    for i, s in enumerate(strategies):
        s['recommended'] = (i == 0)
    return strategies


def strategies_for_symbol(board, sym, spot, iv_hint=None, bias='neutral'):
    """Construit + analyse les stratégies canoniques réalisables depuis le BOARD réel.

    Le board porte `cost` = prime PAR CONTRAT (×100) → convertie en prime/action.
    Choisit l'échéance la plus proche de ~35 DTE, un strike ATM et des strikes OTM,
    puis renvoie l'analyse de chaque preset constructible. Rien d'inventé : un preset
    dont un contrat manque est simplement omis.
    """
    contracts = [c for c in (board or []) if c.get('sym') == sym and c.get('strike') is not None]
    if not contracts or not spot or spot <= 0:
        return {'available': False, 'reason': 'aucun contrat pour ce titre dans le board.'}

    # échéance la plus proche de 35 DTE avec assez de strikes
    by_exp = {}
    for c in contracts:
        by_exp.setdefault(c.get('exp'), []).append(c)
    best = None
    for exp, cs in by_exp.items():
        dtes = [c.get('dte') for c in cs if c.get('dte') is not None]
        if not dtes:
            continue
        score = abs(dtes[0] - 35)
        if best is None or score < best[0]:
            best = (score, exp, cs, dtes[0])
    if best is None:
        return {'available': False, 'reason': 'échéance exploitable introuvable.'}
    _, exp, cs, dte = best

    strikes = sorted({c['strike'] for c in cs})
    atm_strike = min(strikes, key=lambda k: abs(k - spot))

    def at(typ, strike):
        if strike is None:
            return None
        return next((c for c in cs if c.get('type') == typ and c.get('strike') == strike
                     and c.get('cost') is not None), None)

    def prem(c):
        return (c.get('cost') or 0.0) / 100.0 if c else None

    otm_call_strike = min([k for k in strikes if k > atm_strike],
                          key=lambda k: abs(k - spot * 1.06), default=None)
    otm_put_strike = min([k for k in strikes if k < atm_strike],
                         key=lambda k: abs(k - spot * 0.94), default=None)
    atm_call, atm_put = at('CALL', atm_strike), at('PUT', atm_strike)
    otm_call, otm_put = at('CALL', otm_call_strike), at('PUT', otm_put_strike)

    ref = {
        'atm': {'strike': atm_strike, 'call': prem(atm_call), 'put': prem(atm_put)},
        'otm_call': ({'strike': otm_call_strike, 'call': prem(otm_call)} if otm_call else None),
        'otm_put': ({'strike': otm_put_strike, 'put': prem(otm_put)} if otm_put else None),
    }
    iv = iv_hint if (iv_hint and iv_hint > 0) else ((atm_call or atm_put or {}).get('iv'))

    out = []
    for kind in _STRATEGY_ORDER:
        legs = build_preset(kind, spot, ref)
        if not legs:
            continue
        an = analyze_strategy(legs, spot, iv, dte, name=STRATEGY_LABELS.get(kind, kind))
        if an.get('available'):
            an['kind'] = kind
            an['label'] = STRATEGY_LABELS.get(kind, kind)
            out.append(an)
    rank_strategies(out, bias)  # classe par adéquation au contexte, marque la recommandée
    return {'available': bool(out), 'sym': sym, 'spot': round(spot, 2),
            'exp': exp, 'dte': dte, 'iv': round(iv, 4) if iv else None,
            'bias': bias, 'atm_strike': atm_strike, 'strategies': out,
            'reason': None if out else 'primes insuffisantes dans le board pour construire une stratégie.'}
