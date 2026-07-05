"""
vertex/engines/reasoning.py — LE MOTEUR DE RAISONNEMENT (Ch. XVIII).

La décision n'est pas une prédiction. Ce module transforme un plan chiffré en
SCÉNARIOS conditionnels (haussier / central / baissier), chacun avec son
déclencheur, sa cible, son invalidation. Il rend explicite ce qui doit se
passer pour que chaque futur se réalise — et ce qui le tuerait.

Règle : la conviction mesure la solidité du dossier AUJOURD'HUI, jamais la
probabilité d'un gain futur. On expose les conditions, on ne promet rien.

Analyse uniquement. Aucune exécution.
"""


def _num(x, d=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return d


def _pct(a, b):
    """Variation en % de b vers a, arrondie — None si base absente."""
    b = _num(b)
    if not b:
        return None
    return round((_num(a) / b - 1) * 100, 1)


def _weights(committee, decision):
    """Poids qualitatifs des scénarios, dérivés de l'accord du comité (jamais des probas dures)."""
    lean = _num((committee or {}).get('lean'), 50) / 100.0
    bull = max(0.15, min(0.6, lean))
    bear = max(0.15, min(0.6, 1 - lean))
    base = max(0.1, 1 - bull - bear)
    total = bull + base + bear
    lab = lambda w: 'plausible' if w >= 0.45 else 'possible' if w >= 0.28 else 'peu probable'
    return {'bull': (round(bull / total * 100), lab(bull / total)),
            'base': (round(base / total * 100), lab(base / total)),
            'bear': (round(bear / total * 100), lab(bear / total))}


def scenarios(detail, committee, decision):
    """Trois futurs conditionnels, avec déclencheur, cible et invalidation."""
    d = detail or {}
    plan = d.get('plan') or {}
    price = _num(d.get('price')) or _num(plan.get('entry'))
    entry, stop = plan.get('entry'), plan.get('stop')
    tp2, tp3 = plan.get('tp2'), plan.get('tp3')
    resistance = plan.get('resistance') or tp2
    w = _weights(committee, decision)
    return [
        {'name': 'Haussier', 'tone': 'green', 'weight': w['bull'][0], 'likelihood': w['bull'][1],
         'trigger': f'Cassure de ${resistance} confirmée par le volume' if resistance
                    else 'Reprise de la tendance avec volume',
         'target': tp3 or tp2, 'move_pct': _pct(tp3 or tp2, price),
         'invalidation': f'Repli sous ${entry}' if entry else 'Perte de la zone d\'entrée'},
        {'name': 'Central', 'tone': 'amber', 'weight': w['base'][0], 'likelihood': w['base'][1],
         'trigger': f'Maintien de la zone ${stop}–${resistance}' if stop and resistance
                    else 'Consolidation dans le range',
         'target': tp2 or resistance, 'move_pct': _pct(tp2 or resistance, price),
         'invalidation': f'Sortie franche du range (sous ${stop})' if stop else 'Sortie de range'},
        {'name': 'Baissier', 'tone': 'red', 'weight': w['bear'][0], 'likelihood': w['bear'][1],
         'trigger': f'Clôture sous ${stop}' if stop else 'Perte du support',
         'target': stop, 'move_pct': _pct(stop, price),
         'invalidation': f'Reprise au-dessus de ${entry}' if entry else 'Reprise de l\'entrée'},
    ]


def invalidations(detail):
    """Ce qui tuerait la thèse — conditions explicites, testables (Ch. XVIII)."""
    d = detail or {}
    plan = d.get('plan') or {}
    out = []
    if plan.get('stop') is not None:
        out.append(f'Clôture journalière sous ${plan["stop"]} (stop de la thèse)')
    if not (d.get('signals') or {}).get('above200', True):
        out.append('Le titre repasse durablement sous la MM200')
    if d.get('distribution'):
        out.append('La distribution s\'accentue (OBV continue de diverger)')
    out.append('Un changement de régime de marché (RISK-ON → RISK-OFF)')
    return out[:4]


def build(detail, committee, decision):
    """Bloc de raisonnement complet attaché à la décision."""
    return {
        'scenarios': scenarios(detail, committee, decision),
        'invalidations': invalidations(detail),
        'conviction_note': ('La conviction reflète la solidité du dossier aujourd\'hui, '
                            'pas la probabilité d\'un gain. Ce sont des scénarios '
                            'conditionnels, pas des prédictions.'),
    }


__all__ = ['build', 'scenarios', 'invalidations']
