"""
vertex/engines/evidence.py — LE COMITÉ D'ANALYSTES (couche de preuves).

Chaque analyste est indépendant et ne connaît qu'un domaine (marché, structure,
technique, momentum, options, risque, qualité de données). Il produit des
PREUVES atomiques — jamais une décision. La DecisionStack synthétise ensuite.

Règle non négociable (Ch. IV / Loi 14) : les CONTRADICTIONS sont exposées,
jamais cachées. Chaque preuve porte sa force, son domaine, son signe.
"""

POSITIVE = 'positive'
NEGATIVE = 'negative'
NEUTRAL = 'neutral'
UNKNOWN = 'unknown'
CONTRADICTORY = 'contradictory'


def _ev(kind, text, strength, source):
    return {'kind': kind, 'text': text, 'strength': int(max(0, min(100, strength))), 'source': source}


def _num(x, d=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return d


def market_analyst(market):
    if not market:
        return []
    out = []
    if market.get('roro') == 'RISK-ON':
        out.append(_ev(POSITIVE, 'Marché RISK-ON — appétit pour le risque', 70, 'Marché'))
    if market.get('roro') == 'RISK-OFF':
        out.append(_ev(NEGATIVE, 'Marché RISK-OFF — aversion au risque', 80, 'Marché'))
    if market.get('spy_regime') == 'TREND':
        out.append(_ev(POSITIVE, 'Régime de marché en tendance', 60, 'Marché'))
    if market.get('spy_regime') == 'CHOP':
        out.append(_ev(NEGATIVE, 'Marché en range — cassures fragiles', 55, 'Marché'))
    return out


def structure_analyst(d):
    out = []
    phy = (d.get('physics') or {}).get('state')
    if phy == 'TENDANCE FRACTALE':
        out.append(_ev(POSITIVE, 'Structure fractale persistante (mémoire longue)', 65, 'Physique'))
    elif phy == 'CHAOS':
        out.append(_ev(NEGATIVE, 'Structure chaotique — mouvement imprévisible', 70, 'Physique'))
    mtf = (d.get('mtf') or {}).get('state')
    if mtf == 'ALIGNÉ HAUSSIER':
        out.append(_ev(POSITIVE, 'Journalier et hebdomadaire alignés à la hausse', 75, 'Multi-horizons'))
    elif mtf == 'REBOND CONTRE-TENDANCE':
        out.append(_ev(NEGATIVE, 'Rebond à contre-courant de l\'hebdo baissier', 65, 'Multi-horizons'))
    elif mtf == 'ALIGNÉ BAISSIER':
        out.append(_ev(NEGATIVE, 'Journalier et hebdomadaire alignés à la baisse', 75, 'Multi-horizons'))
    return out


def technical_analyst(d):
    out = []
    sig = d.get('signals') or {}
    if sig.get('stacked'):
        out.append(_ev(POSITIVE, 'Moyennes mobiles empilées (tendance propre)', 65, 'Technique'))
    if d.get('breakout'):
        out.append(_ev(POSITIVE, 'Cassure confirmée par le volume', 70, 'Technique'))
    if d.get('pullback'):
        out.append(_ev(POSITIVE, 'Repli sain sur tendance (meilleur R:R)', 68, 'Technique'))
    if not sig.get('above200', True):
        out.append(_ev(NEGATIVE, 'Sous la MM200 — tendance de fond fragile', 70, 'Technique'))
    if d.get('distribution'):
        out.append(_ev(NEGATIVE, 'Distribution cachée (OBV/prix divergents)', 65, 'Technique'))
    if _num(d.get('ext_atr')) >= 4:
        out.append(_ev(NEGATIVE, f'Sur-étendu ({_num(d.get("ext_atr")):.1f} ATR)', 60, 'Technique'))
    return out


def momentum_analyst(d):
    out = []
    rs = _num(d.get('rs'), 50)
    if rs >= 70:
        out.append(_ev(POSITIVE, f'Surperforme le marché (force relative {int(rs)})', 65, 'Momentum'))
    elif rs <= 35:
        out.append(_ev(NEGATIVE, f'Sous-performe le marché (force relative {int(rs)})', 60, 'Momentum'))
    if d.get('rsi_div') == 'bear':
        out.append(_ev(NEGATIVE, 'Divergence RSI baissière', 55, 'Momentum'))
    return out


def options_analyst(option):
    if not option:
        return []
    out = []
    if _num(option.get('quality')) >= 65:
        out.append(_ev(POSITIVE, 'Option de bonne qualité disponible', 55, 'Options'))
    if _num(option.get('iv')) >= 90:
        out.append(_ev(NEGATIVE, 'IV élevée — options coûteuses', 60, 'Options'))
    sp = option.get('spread')
    if sp is not None and _num(sp) > 8:
        out.append(_ev(NEGATIVE, 'Option illiquide (spread large)', 55, 'Options'))
    return out


def risk_analyst(d, portfolio):
    out = []
    rr = _num((d.get('plan') or {}).get('rr_res'))
    if rr and rr >= 2:
        out.append(_ev(POSITIVE, f'Risque/récompense favorable ({rr:.1f}:1)', 60, 'Risque'))
    elif rr and rr < 1.5:
        out.append(_ev(NEGATIVE, f'Risque/récompense faible ({rr:.1f}:1)', 65, 'Risque'))
    if d.get('anomaly_lvl') == 'ALERTE':
        out.append(_ev(NEGATIVE, 'Radar ALERTE — comportement hors-norme', 60, 'Risque'))
    if portfolio and _num(portfolio.get('max_correlation')) >= 0.8:
        out.append(_ev(NEGATIVE, 'Corrélation élevée avec le portefeuille', 70, 'Portefeuille'))
    return out


def data_quality_analyst(dq):
    if not dq:
        return []
    if dq.get('missing_fields'):
        return [_ev(UNKNOWN, 'Champs de données manquants', 50, 'Qualité données')]
    if dq.get('stale'):
        return [_ev(NEGATIVE, 'Données rassies — confiance réduite', 45, 'Qualité données')]
    return []


def _contradictions(d, items):
    """Expose les tensions internes (jamais cachées) — Loi 14."""
    out = []
    strong_price = _num(d.get('pos52'), 0) >= 80 or (d.get('signals') or {}).get('above200')
    weak_mom = _num(d.get('rs'), 50) <= 40 or d.get('rsi_div') == 'bear'
    if strong_price and weak_mom:
        out.append(_ev(CONTRADICTORY, 'Prix fort mais momentum faible — tension à surveiller', 60, 'Synthèse'))
    if (d.get('physics') or {}).get('state') == 'CHAOS' and (d.get('signals') or {}).get('stacked'):
        out.append(_ev(CONTRADICTORY, 'Tendance affichée mais structure chaotique', 55, 'Synthèse'))
    return out


def gather(detail, *, market=None, option=None, portfolio=None, data_quality=None):
    """Réunit toutes les preuves des analystes, catégorisées, avec contradictions."""
    d = detail or {}
    items = (market_analyst(market) + structure_analyst(d) + technical_analyst(d)
             + momentum_analyst(d) + options_analyst(option)
             + risk_analyst(d, portfolio) + data_quality_analyst(data_quality))
    items += _contradictions(d, items)
    buckets = {POSITIVE: [], NEGATIVE: [], NEUTRAL: [], UNKNOWN: [], CONTRADICTORY: []}
    for it in items:
        buckets[it['kind']].append(it)
    for k in buckets:
        buckets[k].sort(key=lambda x: x['strength'], reverse=True)
    buckets['balance'] = (sum(x['strength'] for x in buckets[POSITIVE])
                          - sum(x['strength'] for x in buckets[NEGATIVE]))
    buckets['has_contradiction'] = bool(buckets[CONTRADICTORY])
    return buckets


__all__ = ['gather', 'POSITIVE', 'NEGATIVE', 'NEUTRAL', 'UNKNOWN', 'CONTRADICTORY']
