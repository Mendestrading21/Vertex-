"""
vertex/engines/decision_stack.py — LA DÉCISION STACK : la vérité unique de VERTEX.

Un seul objet. Aucune page n'invente sa propre logique : toutes consomment la
sortie de ce moteur. Il ingère marché + titre + scoring + physique + options +
risque + qualité de données, et produit une décision NORMALISÉE, EXPLICABLE,
avec piste d'audit — jamais une certitude, toujours une aide à la décision.

Analyse uniquement. Aucune exécution. Chaque règle appliquée est tracée.
"""

# ─── Décisions autorisées (label + tonalité UI) ────────────────────────────
DECISIONS = {
    'STRONG_BUY':        ('Achat fort', 'strong-green'),
    'BUY':               ('Achat', 'green'),
    'BUY_PULLBACK':      ('Achat sur repli', 'blue'),
    'WATCH_BREAKOUT':    ('Surveiller la cassure', 'amber'),
    'WAIT':              ('Attendre', 'blue'),
    'TOO_LATE':          ('Trop tard', 'amber'),
    'AVOID':             ('Éviter', 'red'),
    'NO_NEW_RISK':       ('Pas de risque nouveau', 'red'),
    'DATA_INSUFFICIENT': ('Données insuffisantes', 'gray'),
}

_BUYISH = {'STRONG_BUY', 'BUY', 'BUY_PULLBACK'}


def _num(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def assess_data_quality(detail, *, scan_age_s=None, demo=False):
    """Qualité de donnée du titre : chaque décision porte cette métadonnée."""
    missing = [f for f in ('price', 'score', 'plan') if not detail.get(f)]
    stale = scan_age_s is not None and scan_age_s > 900
    penalty = (25 if missing else 0) + (15 if stale else 0)
    grade = 'A' if not missing and not stale else ('C' if missing else 'B')
    return {
        'source': 'demo-synthetic' if demo else 'scan',
        'age_seconds': scan_age_s,
        'stale': bool(stale),
        'missing_fields': missing,
        'confidence_penalty': min(60, penalty),
        'grade': grade,
        'blocks_decision': bool(missing),
        'warning': ('données synthétiques (démo)' if demo else
                    ('champs manquants' if missing else ('scan rassis' if stale else None))),
    }


def _timing(d):
    if d.get('pullback'):
        return 'PULLBACK'
    if _num(d.get('ext_atr')) >= 4 or _num(d.get('rsi')) >= 78 or _num(d.get('pos52')) >= 95:
        return 'EXTENDED'
    if d.get('breakout'):
        return 'BREAKOUT'
    return 'NEUTRAL'


def _base_decision(d):
    """Décision de base, avant règles de dégradation."""
    v, sc = d.get('verdict'), _num(d.get('score'))
    if v == 'AVOID':
        return 'AVOID'
    if v == 'BUY' and sc >= 80:
        return 'STRONG_BUY'
    if v == 'BUY' and sc >= 66:
        return 'BUY'
    if v in ('BUY', 'WATCH') and sc >= 56:
        return 'WATCH_BREAKOUT'
    if v == 'WAIT':
        return 'WAIT'
    return 'WAIT'


def _market_permission(market, audit):
    """Le marché autorise-t-il la prise de risque ? (vent dominant top-down)."""
    if not market:
        return True
    roro = market.get('roro')
    regime = market.get('spy_regime')
    if roro == 'RISK-OFF':
        audit.append('Marché RISK-OFF → permission de risque réduite.')
        return False
    if regime == 'CHOP':
        audit.append('Marché en range (CHOP) → cassures dégradées.')
    return True


def _apply_rules(decision, d, market, option, portfolio, permission, audit):
    """Applique les règles institutionnelles de dégradation (ordre = priorité)."""
    timing = _timing(d)
    rr = _num((d.get('plan') or {}).get('rr_res'))

    # 1. Corrélation portefeuille excessive → aucun risque nouveau.
    if portfolio and _num(portfolio.get('max_correlation')) >= 0.8 and decision in _BUYISH:
        audit.append('Corrélation portefeuille élevée → NO_NEW_RISK.')
        return 'NO_NEW_RISK'

    # 2. Sur-extension → trop tard, ou achat seulement sur repli.
    if timing == 'EXTENDED' and decision in _BUYISH:
        if _num(d.get('score')) >= 72:
            audit.append('Sur-étendu mais qualité forte → achat sur repli.')
            decision = 'BUY_PULLBACK'
        else:
            audit.append('Sur-étendu → trop tard pour poursuivre.')
            return 'TOO_LATE'

    # 3. Marché sans permission → pas d'achat fort.
    if not permission and decision in _BUYISH:
        audit.append('Sans permission marché → dégradé en surveillance.')
        return 'WATCH_BREAKOUT'

    # 4. Range (CHOP) → une cassure ne se poursuit pas : surveiller.
    if market and market.get('spy_regime') == 'CHOP' and timing == 'BREAKOUT' and decision in _BUYISH:
        audit.append('Cassure en marché de range → surveiller, ne pas poursuivre.')
        decision = 'WATCH_BREAKOUT'

    # 5. Risque/récompense insuffisant → pas d'achat.
    if rr and rr < 1.5 and decision in {'STRONG_BUY', 'BUY'}:
        audit.append(f'R:R {rr:.1f} < 1.5 → pas d\'achat, surveiller.')
        decision = 'WATCH_BREAKOUT'

    # 6. Marché RISK-OFF → jamais d'achat FORT.
    if market and market.get('roro') == 'RISK-OFF' and decision == 'STRONG_BUY':
        audit.append('RISK-OFF → achat fort interdit, dégradé en achat.')
        decision = 'BUY'

    # 7. Distribution cachée → prudence forte.
    if d.get('distribution') and decision in _BUYISH:
        audit.append('Distribution cachée détectée → dégradé en surveillance.')
        decision = 'WATCH_BREAKOUT'

    return decision


def _select_vehicle(d, option, audit):
    """Action vs Option : l'option doit MIEUX coller à la vue que le sous-jacent."""
    if not option:
        return 'ACTION'
    spread, oi = option.get('spread'), option.get('oi')
    iv, iv_rank = _num(option.get('iv')), option.get('iv_rank')
    # On ne pénalise QUE si la donnée de liquidité est réellement connue.
    if (spread is not None and _num(spread) > 8) or (oi is not None and _num(oi) < 200):
        audit.append('Option illiquide (spread/OI) → véhicule ACTION.')
        return 'ACTION'
    if (iv_rank is not None and _num(iv_rank) >= 80) or iv >= 90:
        audit.append('IV chère → véhicule ACTION (option coûteuse).')
        return 'ACTION'
    if d.get('profile') == 'OFFENSIF' and _num(option.get('quality')) >= 60:
        return 'OPTION'
    return 'ACTION'


def _reasons(d, market, option):
    """Forces / faiblesses / bloqueurs / drapeaux de risque — langage clair, borné."""
    pros, cons, blockers, flags = [], [], [], []
    sig = d.get('signals') or {}
    if sig.get('stacked'):
        pros.append('Tendance haussière propre (MM empilées)')
    if d.get('breakout'):
        pros.append('Cassure confirmée par le volume')
    if d.get('pullback'):
        pros.append('Repli sain sur tendance (meilleur R:R)')
    if _num(d.get('rs')) >= 70:
        pros.append(f'Surperforme le marché (RS {int(_num(d.get("rs")))})')
    if (d.get('mtf') or {}).get('state') == 'ALIGNÉ HAUSSIER':
        pros.append('Journalier et hebdo alignés à la hausse')
    if d.get('distribution'):
        cons.append('Distribution cachée (faiblesse sous le capot)')
    if _timing(d) == 'EXTENDED':
        cons.append('Sur-étendu — risque de rappel')
    if market and market.get('spy_regime') == 'CHOP':
        cons.append('Marché de range — cassures fragiles')
    if d.get('verdict') == 'AVOID':
        blockers.append('Signal Vertex à ÉVITER (sous la MM200)')
    if (d.get('anomaly_lvl')) == 'ALERTE':
        flags.append('Radar ALERTE : comportement hors-norme')
    if option and _num(option.get('iv')) >= 90:
        flags.append('IV élevée sur les options')
    return pros[:5], cons[:5], blockers[:5], flags[:5]


def _conviction(d):
    return int(max(0, min(100, round(_num(d.get('score'))))))


def _confidence(d, dq):
    base = _num(d.get('confidence'), 55)
    return int(max(0, min(100, round(base - dq.get('confidence_penalty', 0)))))


def _size_hint(decision, profile):
    table = {
        'STRONG_BUY': {'OFFENSIF': '5-8%', 'DÉFENSIF': '4-6%', 'ÉQUILIBRÉ': '4-7%'},
        'BUY': {'OFFENSIF': '3-5%', 'DÉFENSIF': '3-5%', 'ÉQUILIBRÉ': '3-5%'},
        'BUY_PULLBACK': {'OFFENSIF': '2-4% à l\'entrée sur repli', 'DÉFENSIF': '2-4%', 'ÉQUILIBRÉ': '2-4%'},
    }
    return table.get(decision, {}).get(profile or 'ÉQUILIBRÉ', '0% — observer')


def evaluate(detail, *, symbol=None, market=None, option=None, portfolio=None,
             scan_age_s=None, demo=False):
    """Point d'entrée unique : détail d'un titre → DecisionResult normalisé."""
    d = detail or {}
    audit = []
    dq = assess_data_quality(d, scan_age_s=scan_age_s, demo=demo)

    if dq['blocks_decision']:
        return _result('DATA_INSUFFICIENT', d, dq, symbol=symbol, market=market,
                       vehicle='—', conviction=0, confidence=0, audit=audit,
                       explanation='Données insuffisantes pour décider : ' +
                                   ', '.join(dq['missing_fields']) + '.')

    permission = _market_permission(market, audit)
    decision = _apply_rules(_base_decision(d), d, market, option, portfolio, permission, audit)
    vehicle = 'ACTION' if decision not in _BUYISH else _select_vehicle(d, option, audit)
    conviction = _conviction(d)
    confidence = _confidence(d, dq)
    return _result(decision, d, dq, symbol=symbol, market=market, vehicle=vehicle,
                   conviction=conviction, confidence=confidence, audit=audit,
                   permission=permission)


def _result(decision, d, dq, *, symbol, market, vehicle, conviction, confidence,
            audit, permission=True, explanation=None):
    label, tone = DECISIONS[decision]
    plan = d.get('plan') or {}
    pros, cons, blockers, flags = _reasons(d, market, None) if decision != 'DATA_INSUFFICIENT' else ([], [], [], [])
    if dq.get('warning'):
        flags = (flags + [dq['warning']])[:6]
    expl = explanation or _explain(decision, d, conviction, confidence, audit)
    return {
        'symbol': symbol or d.get('symbol'),
        'final_decision': decision,
        'decision_label': label,
        'decision_tone': tone,
        'conviction': conviction,
        'confidence': confidence,
        'grade': d.get('grade'),
        'market_permission': bool(permission),
        'vehicle': vehicle,
        'timing': _timing(d) if decision != 'DATA_INSUFFICIENT' else None,
        'entry': plan.get('entry'),
        'stop': plan.get('stop'),
        'targets': {'tp1': plan.get('tp1'), 'tp2': plan.get('tp2'), 'tp3': plan.get('tp3')},
        'invalidation': plan.get('stop'),
        'position_size_hint': _size_hint(decision, d.get('profile')),
        'pros': pros,
        'cons': cons,
        'blockers': blockers,
        'risk_flags': flags,
        'data_quality': dq,
        'explanation': expl,
        'audit_trail': audit,
    }


def _explain(decision, d, conviction, confidence, audit):
    label = DECISIONS[decision][0]
    head = f'{label} — conviction {conviction}/100, confiance {confidence}/100.'
    why = audit[0] if audit else 'Lecture technique et structurelle cohérente avec le verdict.'
    return f'{head} {why} Analyse éducative — aucune certitude, aucun ordre.'
