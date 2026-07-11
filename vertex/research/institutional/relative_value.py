"""vertex.research.institutional.relative_value — valeur relative entre pairs (§23).

INFORMATION uniquement : jamais de short automatique, jamais de pair-trade créé.
"""
from __future__ import annotations


def peer_dispersion(stock: dict, peers: list[dict]) -> dict:
    """stock/peers : {'symbol','pe','revenue_growth','margin','momentum_3m'}."""
    out = {'symbol': stock.get('symbol'), 'vs_peers': {}, 'notes': [
        'valeur relative = information de contexte — aucun pair-trade automatique']}
    if len(peers) < 2:
        out['notes'].append('moins de 2 pairs — comparaison non significative')
        return out
    for key, label in (('pe', 'valorisation'), ('revenue_growth', 'croissance'),
                       ('margin', 'marge'), ('momentum_3m', 'momentum')):
        mine = stock.get(key)
        vals = [p.get(key) for p in peers if p.get(key) is not None]
        if mine is None or not vals:
            out['vs_peers'][key] = None
            continue
        med = sorted(vals)[len(vals) // 2]
        spread = mine - med
        out['vs_peers'][key] = {'value': mine, 'peer_median': med,
                                'spread': round(spread, 4), 'label': label}
    growth = out['vs_peers'].get('revenue_growth')
    pe = out['vs_peers'].get('pe')
    if growth and pe and growth['spread'] > 0.05 and pe['spread'] < 0:
        out['notes'].append('croissance supérieure aux pairs avec valorisation inférieure — '
                            'dispersion favorable à creuser')
    return out
