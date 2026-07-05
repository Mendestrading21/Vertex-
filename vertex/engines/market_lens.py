"""
vertex/engines/market_lens.py — PRISME MARCHÉ & SECTEUR (Ch. IX/XI).

Un titre ne se négocie pas dans le vide. Ce moteur situe une décision aux TROIS
niveaux — marché, secteur, titre — pour dire si le vent est dans le dos ou de
face : climat de marché, position du secteur, force du titre, et leur alignement.

Pur, sans état. Analyse uniquement.
"""


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def climate(market):
    """Score de climat 0-100 (régime + risk-on/off + largeur + VIX) → label + couleur."""
    if not market:
        return None
    br = market.get('breadth') or {}
    reg, ro, vb = market.get('spy_regime'), market.get('roro'), market.get('vix_band')
    s = (35 if reg == 'TREND' else 18 if reg == 'NEUTRAL' else 6 if reg == 'CHOP' else 14)
    s += (25 if ro == 'RISK-ON' else 2 if ro == 'RISK-OFF' else 12)
    a50 = br.get('above50')
    s += round((a50 if a50 is not None else 50) / 100 * 25)
    s += (15 if vb == 'calme' else 2 if vb == 'stress' else 8)
    s = max(0, min(100, round(s)))
    label, col = (('FAVORABLE', '#22C55E') if s >= 62 else
                  ('NEUTRE', '#FFB23F') if s >= 40 else ('DANGEREUX', '#EF4444'))
    return {'score': s, 'label': label, 'col': col}


def sector_standing(sectors, sector_name):
    """Rang du secteur du titre parmi les secteurs scannés (par score moyen)."""
    if not sectors or not sector_name:
        return None
    ranked = sorted(sectors, key=lambda x: (_num(x.get('avg_score')) or -1), reverse=True)
    for i, s in enumerate(ranked):
        if s.get('sector') == sector_name:
            n = len(ranked)
            return {'name': sector_name, 'rank': i + 1, 'n': n,
                    'avg_score': _num(s.get('avg_score')), 'avg_change': _num(s.get('avg_change')),
                    'in_favor': (i + 1) <= max(1, n // 3)}          # tiers supérieur = porteur
    return None


def build(*, market, sectors, sector_name, stock_pct):
    """Prisme aux trois niveaux + lecture d'alignement (vent dans le dos / de face)."""
    cl = climate(market)
    sec = sector_standing(sectors, sector_name)
    stock_strong = stock_pct is not None and stock_pct >= 70
    lights = {
        'market': bool(cl and cl['score'] >= 62),
        'sector': bool(sec and sec['in_favor']),
        'stock': bool(stock_strong),
    }
    n_green = sum(1 for v in lights.values() if v)
    if n_green == 3:
        alignment, tone = 'aligné', 'green'
        head = 'Vent dans le dos : titre fort, secteur porteur, marché favorable.'
    elif lights['stock'] and n_green == 1:
        alignment, tone = 'à contre-courant', 'amber'
        head = 'Titre fort mais à contre-courant de son secteur / du marché — prudence.'
    elif n_green >= 2:
        alignment, tone = 'partiellement aligné', 'blue'
        head = 'Alignement partiel entre le titre, son secteur et le marché.'
    else:
        alignment, tone = 'défavorable', 'red'
        head = 'Contexte défavorable aux trois niveaux — le dossier rame à contre-courant.'
    return {'climate': cl, 'sector': sec, 'stock_strong': stock_strong,
            'lights': lights, 'alignment': alignment, 'tone': tone, 'headline': head}


__all__ = ['build', 'climate', 'sector_standing']
