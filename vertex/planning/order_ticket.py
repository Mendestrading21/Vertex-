"""vertex.planning.order_ticket — dimensionnement & ticket d'ordre (READONLY).

Calcule une quantité suggérée à partir d'un budget de risque, contrôle le poids
maximum (15 %) et le R:R (≥ 2:1), puis compose un TICKET DE PRÉPARATION à
recopier manuellement dans IBKR. Aucune transmission — Vertex n'exécute jamais.
Purs et testables. Donnée manquante → None + avertissement (jamais un chiffre
inventé).
"""
from __future__ import annotations

BUY = 'ACHAT'
SIDES = (BUY,)              # le desk n'achète que (actions + options long)

MAX_STOCK_WEIGHT_PCT = 15.0
MIN_REWARD_RISK = 2.0
STOCK_MULT = 1
OPTION_MULT = 100

# Étiquette d'honnêteté — un ticket n'est jamais un ordre passé.
DISCLAIMER = ('PRÉPARATION UNIQUEMENT — Vertex est en lecture seule et ne '
              'transmet aucun ordre. À saisir manuellement dans IBKR.')


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def size_position(account_value, risk_pct, entry, stop, *, is_option=False,
                  multiplier=None, premium=None):
    """Dimensionne une position selon un budget de risque.

    account_value : valeur du compte. risk_pct : % du compte risqué sur ce
    trade (ex. 1.0). entry/stop : prix du sous-jacent. is_option : si vrai, le
    risque = prime engagée (perte max = prime), la quantité = contrats.
    Rend qty, capital à risque, capital déployé, poids projeté, avertissements.
    """
    av = _num(account_value)
    rp = _num(risk_pct)
    e = _num(entry)
    s = _num(stop)
    warnings = []
    if av is None or av <= 0 or rp is None or rp <= 0:
        return {'qty': None, 'reason': 'compte ou budget de risque invalide',
                'warnings': ['compte/risk_pct requis']}
    risk_budget = av * rp / 100.0

    if is_option:
        mult = multiplier or OPTION_MULT
        prem = _num(premium)
        if prem is None or prem <= 0:
            return {'qty': None, 'reason': 'prime indisponible — dimensionnement impossible',
                    'warnings': ['prime requise pour une option']}
        # Perte max option = prime engagée par contrat = premium × multiplicateur.
        cost_per_contract = prem * mult
        qty = int(risk_budget // cost_per_contract)
        capital_at_risk = round(qty * cost_per_contract, 2)
        capital_deployed = capital_at_risk        # la prime EST le capital engagé
    else:
        mult = multiplier or STOCK_MULT
        if e is None or s is None or e <= 0:
            return {'qty': None, 'reason': 'entrée/stop indisponibles',
                    'warnings': ['entrée et stop requis']}
        per_share_risk = e - s
        if per_share_risk <= 0:
            return {'qty': None, 'reason': 'stop au-dessus de l\'entrée — risque non défini',
                    'warnings': ['le stop doit être sous l\'entrée pour un achat']}
        qty = int(risk_budget // (per_share_risk * mult))
        capital_at_risk = round(qty * per_share_risk * mult, 2)
        capital_deployed = round(qty * e * mult, 2)

    weight_pct = round(capital_deployed / av * 100.0, 2) if av else None
    if qty < 1:
        warnings.append('budget de risque insuffisant pour 1 unité')
    if weight_pct is not None and weight_pct > MAX_STOCK_WEIGHT_PCT and not is_option:
        warnings.append('poids projeté %.1f %% > maximum stratégie %.0f %% — réduire la taille'
                        % (weight_pct, MAX_STOCK_WEIGHT_PCT))
    return {
        'qty': qty,
        'risk_budget': round(risk_budget, 2),
        'capital_at_risk': capital_at_risk,
        'capital_deployed': capital_deployed,
        'weight_pct': weight_pct,
        'per_unit_risk': round((e - s), 4) if (not is_option and e is not None and s is not None) else None,
        'is_option': bool(is_option),
        'warnings': warnings,
    }


def _rr(entry, stop, target):
    e, s, t = _num(entry), _num(stop), _num(target)
    if None in (e, s, t) or (e - s) <= 0:
        return None
    return round((t - e) / (e - s), 2)


def build_ticket(symbol, *, side=BUY, qty=None, entry=None, stop=None,
                 tp1=None, tp2=None, tp3=None, is_option=False, contract_id=None,
                 right=None, strike=None, expiry=None, limit_price=None,
                 account_value=None, risk_pct=None, premium=None,
                 rr_res=None):
    """Compose un TICKET DE PRÉPARATION (jamais transmis) + le texte à copier.

    Applique les garde-fous stratégie : R:R ≥ 2:1 et poids ≤ 15 % → le ticket
    reçoit `blocked=True` avec la raison (sans jamais empêcher l'affichage —
    c'est une aide à la décision, pas une exécution)."""
    sym = str(symbol or '').upper()
    side = side if side in SIDES else BUY
    blockers = []
    warnings = []

    sizing = None
    if qty is None and account_value is not None and risk_pct is not None:
        sizing = size_position(account_value, risk_pct, entry, stop,
                               is_option=is_option, premium=premium)
        qty = sizing.get('qty')
        warnings += sizing.get('warnings', [])

    # Garde-fou R:R (actions : sur le sous-jacent).
    rr = _num(rr_res)
    if rr is None and not is_option:
        rr = _rr(entry, stop, tp1 or tp2)
    if rr is not None and rr < MIN_REWARD_RISK:
        blockers.append('R:R %.1f < %.1f (minimum stratégie)' % (rr, MIN_REWARD_RISK))
    if not is_option and (stop is None):
        blockers.append('invalidation (stop) absente — pas de préparation offensive')

    # Garde-fou poids.
    if sizing and sizing.get('weight_pct') is not None and not is_option \
            and sizing['weight_pct'] > MAX_STOCK_WEIGHT_PCT:
        blockers.append('poids projeté %.1f %% > %.0f %%' % (sizing['weight_pct'], MAX_STOCK_WEIGHT_PCT))

    lim = _num(limit_price) or _num(entry)
    copy_lines = ['# %s' % DISCLAIMER, 'ACTION: %s (analyse seule)' % side, 'TICKER: %s' % sym]
    if is_option:
        copy_lines += ['TYPE: OPTION %s' % (right or ''),
                       'STRIKE: %s' % (strike if strike is not None else '—'),
                       'EXPIRATION: %s' % (expiry or '—')]
        if contract_id:
            copy_lines.append('CONID/CONTRAT: %s' % contract_id)
    copy_lines += ['QUANTITE: %s' % (qty if qty is not None else '—'),
                   'PRIX LIMITE: %s' % (lim if lim is not None else '—'),
                   'STOP (référence, non transmis): %s' % (stop if stop is not None else '—')]
    if tp1 is not None:
        copy_lines.append('OBJECTIFS: TP1 %s / TP2 %s / TP3 %s' % (tp1, tp2 if tp2 is not None else '—', tp3 if tp3 is not None else '—'))

    return {
        'symbol': sym,
        'side': side,
        'is_option': bool(is_option),
        'contract_id': contract_id,
        'qty': qty,
        'limit_price': lim,
        'stop': _num(stop),
        'targets': {'tp1': _num(tp1), 'tp2': _num(tp2), 'tp3': _num(tp3)},
        'reward_risk': rr,
        'sizing': sizing,
        'blocked': bool(blockers),
        'blockers': blockers,
        'warnings': warnings,
        'readonly': True,
        'transmitted': False,               # invariant : jamais transmis
        'disclaimer': DISCLAIMER,
        'copy_text': '\n'.join(copy_lines),
    }


__all__ = ['size_position', 'build_ticket', 'SIDES', 'MAX_STOCK_WEIGHT_PCT',
           'MIN_REWARD_RISK', 'DISCLAIMER']
