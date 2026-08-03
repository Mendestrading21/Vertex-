"""vertex/engines/portfolio_stress.py — STRESS-SCÉNARIOS DU PORTEFEUILLE.

Répond à « que perd (ou gagne) mon book si le marché choque de ±X % ? » sur les
positions RÉELLES déclarées au desk, valorisées au PRIX RÉEL du scan.

HONNÊTETÉ (invariant produit) :
- ACTIONS : choc appliqué au prix réel courant → impact P&L exact (qty × prix × choc).
- OPTIONS : EXCLUES du chiffrage (les stresser exige marque + greeks live IBKR ;
  un proxy delta inventé serait un chiffre faux). Elles sont listées à part avec
  la raison + leur coût engagé, et la COUVERTURE du stress est affichée
  (part de la valeur du book réellement stressée).
- Titre sans prix réel → exclu avec raison, jamais valorisé au hasard.
- Choc UNIFORME du marché (beta 1 implicite) — dit explicitement : c'est un ordre
  de grandeur de sensibilité, pas un modèle factoriel.

Fonction pure ; lecture seule, aucun ordre.
"""
from __future__ import annotations

DEFAULT_SHOCKS = (-0.10, -0.05, -0.02, 0.02, 0.05)


def _num(x):
    if isinstance(x, bool):
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if v != v or v in (float('inf'), float('-inf')):
        return None
    return v


def build(positions, prices_by_sym, shocks=DEFAULT_SHOCKS):
    """Stress du book : positions = myTrades (desk), prices_by_sym = prix réels du scan."""
    prices_by_sym = prices_by_sym or {}
    stressed, excluded = [], []
    for t in (positions or []):
        if not isinstance(t, dict):
            continue
        sym = str(t.get('sym') or '?').upper()
        qty = _num(t.get('qty'))
        cost = _num(t.get('cost')) or 0.0
        typ = str(t.get('type') or 'STK').upper()
        if typ != 'STK':
            excluded.append({'sym': sym, 'type': typ, 'cost': cost,
                             'reason': 'option — marque/greeks IBKR requis (jamais estimé)'})
            continue
        px = _num(prices_by_sym.get(sym))
        if qty is None or qty <= 0 or px is None or px <= 0:
            excluded.append({'sym': sym, 'type': typ, 'cost': cost,
                             'reason': 'prix réel indisponible dans le scan courant'})
            continue
        stressed.append({'sym': sym, 'qty': qty, 'price': px,
                         'value': round(qty * px, 2)})

    stressed_value = round(sum(p['value'] for p in stressed), 2)
    excluded_cost = round(sum(e['cost'] for e in excluded), 2)
    total_declared = stressed_value + excluded_cost

    if not stressed:
        return {
            'empty': True, 'scenarios': [], 'positions': [], 'excluded': excluded,
            'stressed_value': 0.0, 'excluded_cost': excluded_cost,
            'coverage_pct': (0 if excluded else None),
            'assumption': 'choc uniforme du marché (beta 1 implicite) — ordre de grandeur, pas un modèle factoriel',
            'narrative': None, 'generator': 'deterministic',
            'reason': ('aucune position action avec prix réel — le stress chiffré exige '
                       'des actions valorisables (les options demandent IBKR live)'),
        }

    scenarios = []
    for sh in shocks:
        s = _num(sh)
        if s is None:
            continue
        impact = round(stressed_value * s, 2)
        rows = [{'sym': p['sym'], 'impact': round(p['value'] * s, 2)} for p in stressed]
        rows.sort(key=lambda r: r['impact'])
        scenarios.append({'shock_pct': round(s * 100, 1), 'impact': impact,
                          'value_after': round(stressed_value + impact, 2),
                          'worst': rows[0] if s < 0 else None,
                          'by_position': rows})

    coverage = round(100 * stressed_value / total_declared) if total_declared > 0 else None
    worst = min((sc for sc in scenarios if sc['shock_pct'] < 0),
                key=lambda sc: sc['impact'], default=None)
    parts = ['%d position(s) action stressée(s), valeur %.0f.' % (len(stressed), stressed_value)]
    if worst:
        parts.append('Au pire choc testé (%.0f %%), impact %.0f%s.' % (
            worst['shock_pct'], worst['impact'],
            (' — %s porte la plus grosse perte (%.0f)' % (worst['worst']['sym'], worst['worst']['impact']))
            if worst.get('worst') else ''))
    if coverage is not None and coverage < 100:
        parts.append('Couverture du stress : %d %% du capital déclaré (les options, %.0f engagés, '
                     'exigent IBKR live pour être stressées honnêtement).' % (coverage, excluded_cost))
    parts.append('Choc uniforme (beta 1) — ordre de grandeur descriptif, pas une prévision ni un conseil.')

    return {
        'empty': False, 'scenarios': scenarios,
        'positions': stressed, 'excluded': excluded,
        'stressed_value': stressed_value, 'excluded_cost': excluded_cost,
        'coverage_pct': coverage,
        'assumption': 'choc uniforme du marché (beta 1 implicite) — ordre de grandeur, pas un modèle factoriel',
        'narrative': ' '.join(parts), 'generator': 'deterministic',
    }


__all__ = ['build', 'DEFAULT_SHOCKS']
