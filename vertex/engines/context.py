"""
vertex/engines/context.py — CONTEXTE RELATIF (analyse transversale, Ch. IX/XVIII).

Un chiffre seul ne dit rien : « RS 75 » n'a de sens que RELATIVEMENT à l'univers
et au secteur. Ce moteur situe un titre parmi tous les titres scannés — percentile
sur chaque dimension, rang dans son secteur — pour transformer des valeurs isolées
en information exploitable par le comité.

Pur, sans état, sans dépendance externe. Analyse uniquement.
"""

# (clé, libellé, plus_haut_est_meilleur)
DIMENSIONS = [
    ('score', 'Qualité globale', True),
    ('rs', 'Force relative', True),
    ('mom', 'Momentum', True),
    ('setup_quality', 'Qualité du setup', True),
    ('pos52', 'Position dans le range 52 sem', True),
]


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _pct_rank(values, x):
    """Percentile de x dans `values` (0-100), méthode mid-rank. None si indéterminé."""
    vals = [v for v in values if v is not None]
    if not vals or x is None:
        return None
    below = sum(1 for v in vals if v < x)
    equal = sum(1 for v in vals if v == x)
    return round((below + 0.5 * equal) / len(vals) * 100)


def _standing(pct, higher_better=True):
    """Qualifie une position (percentile) en langage clair."""
    if pct is None:
        return 'inconnu'
    p = pct if higher_better else 100 - pct
    return ('leader' if p >= 90 else 'fort' if p >= 70 else 'médian' if p >= 40
            else 'faible' if p >= 15 else 'retardataire')


def _values(detail_map, key):
    return [_num(d.get(key)) for d in detail_map.values()]


def context_for(sym, detail_map):
    """Situe `sym` parmi tous les titres scannés : percentiles + rang sectoriel."""
    d = (detail_map or {}).get(sym)
    if not d:
        return None
    peers_sector = {s: v for s, v in detail_map.items()
                    if v.get('sector') and v.get('sector') == d.get('sector')}
    dims = []
    for key, label, hb in DIMENSIONS:
        val = _num(d.get(key))
        if val is None:
            continue
        pu = _pct_rank(_values(detail_map, key), val)
        ps = _pct_rank(_values(peers_sector, key), val) if len(peers_sector) >= 3 else None
        dims.append({'key': key, 'label': label, 'value': round(val, 1),
                     'pct_universe': pu, 'pct_sector': ps,
                     'standing': _standing(pu, hb)})
    # rang sectoriel par score (1 = meilleur)
    sector_rank = None
    if len(peers_sector) >= 2:
        ranked = sorted(peers_sector.items(),
                        key=lambda kv: (_num(kv[1].get('score')) or -1), reverse=True)
        order = [s for s, _ in ranked]
        if sym in order:
            sector_rank = order.index(sym) + 1
    # Pairs du secteur (par score), pour situer nommément le titre parmi ses semblables.
    peers = []
    if len(peers_sector) >= 2:
        for s, v in sorted(peers_sector.items(), key=lambda kv: (_num(kv[1].get('score')) or -1),
                           reverse=True)[:5]:
            sc = _num(v.get('score'))
            if sc is not None:
                peers.append({'symbol': s, 'score': int(sc), 'is_self': s == sym})
    return {
        'symbol': sym, 'universe_n': len(detail_map), 'sector': d.get('sector'),
        'sector_n': len(peers_sector) or None, 'sector_rank': sector_rank,
        'dimensions': dims, 'peers': peers,
        'headline': _headline(dims, d.get('sector'), sector_rank, len(peers_sector)),
    }


def _headline(dims, sector, sector_rank, sector_n):
    """Une phrase de situation : où se situe le titre, d'un coup d'œil."""
    sc = next((x for x in dims if x['key'] == 'score'), None)
    parts = []
    if sc and sc['pct_universe'] is not None:
        parts.append('Top %d%% de l\'univers' % (100 - sc['pct_universe'])
                     if sc['pct_universe'] >= 50 else
                     'Bas %d%% de l\'univers' % sc['pct_universe'])
    if sector and sector_rank and sector_n:
        parts.append('#%d/%d dans %s' % (sector_rank, sector_n, sector))
    return ' · '.join(parts) or None


__all__ = ['context_for', 'DIMENSIONS']
