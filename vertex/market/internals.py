"""Baromètre du marché — internals et breadth agrégés depuis un scan.

Répond à « comment va le marché dans son ensemble ? » à partir des lignes
DÉJÀ calculées par le scan : avances/déclins, part au-dessus des moyennes
50 et 200 jours, plus-hauts et plus-bas 52 semaines, surachat/survente,
distribution des scores, répartition des verdicts, breadth sectorielle, et un
indice de santé composite.

## Pourquoi ce module existe

Ce code vivait dans `terminal.py`, l'adaptateur historique que le CLAUDE.md
demande de réduire par strangler pattern. C'est une agrégation de marché ;
`vertex/market/` en est le propriétaire naturel, aux côtés de `sectors` et
`context`.

## Ce que la fonction NE fait PAS

Aucune collecte : elle ne lit ni réseau, ni cache, ni horloge. Tout entre par
ses arguments et tout sort par sa valeur de retour. C'est ce qui la rend
testable sans serveur, et c'est pourquoi elle n'avait aucune raison de rester
dans le monolithe.

Elle n'invente rien non plus : une valeur absente reste absente
(`avg_rsi=None` quand aucune ligne ne porte de RSI), elle n'est jamais
remplacée par un zéro. Un secteur de moins de cinq titres est écarté de la
breadth sectorielle plutôt que publié sur un échantillon qui ne dit rien.

⛔ LECTURE SEULE. Aucun ordre, aucune exécution.
"""
from __future__ import annotations

from vertex.data.universe import _GICS_SECTOR

#: Un secteur sous ce nombre de titres ne produit pas une breadth lisible :
#: un secteur à deux titres afficherait 0 %, 50 % ou 100 %, trois valeurs qui
#: ne disent rien du secteur et beaucoup du hasard.
SECTEUR_MIN = 5


def market_internals(rows, detail, breadth):
    """Agrège les internals d'un scan. `rows` : lignes du scan ; `detail` :
    signaux par symbole ; `breadth` : la breadth déjà calculée en amont."""
    n = len(rows) or 1
    up = sum(1 for r in rows if (r.get('change') or 0) > 0)
    dn = sum(1 for r in rows if (r.get('change') or 0) < 0)
    a50 = a200 = 0
    for r in rows:
        sg = (detail.get(r['symbol']) or {}).get('signals') or {}
        if sg.get('above50'):
            a50 += 1
        if sg.get('above200'):
            a200 += 1
    nh = sum(1 for r in rows if (r.get('pos52') or 0) >= 95)
    nl = sum(1 for r in rows if (r.get('pos52') if r.get('pos52') is not None else 100) <= 5)
    rsis = [r.get('rsi') for r in rows if r.get('rsi') is not None]
    ob = sum(1 for x in rsis if x >= 70)
    ov = sum(1 for x in rsis if x <= 30)
    dist = [0] * 10
    for r in rows:
        s = r.get('score')
        if s is not None:
            dist[min(9, max(0, int(s // 10)))] += 1
    nb = sum(1 for r in rows if r.get('verdict') == 'BUY')
    nw = sum(1 for r in rows if r.get('verdict') in ('WATCH', 'WAIT'))
    na = sum(1 for r in rows if r.get('verdict') == 'AVOID')
    pa50 = round(100 * a50 / n)
    pa200 = round(100 * a200 / n)
    advpct = round(100 * up / max(1, up + dn))
    health = max(0, min(100, round(0.30 * pa50 + 0.25 * pa200 + 0.25 * breadth + 0.20 * advpct)))
    sec = {}
    for r in rows:
        s = _GICS_SECTOR.get(r['symbol'])
        if not s:
            continue
        sg = (detail.get(r['symbol']) or {}).get('signals') or {}
        d = sec.setdefault(s, [0, 0])
        d[1] += 1
        if sg.get('above50'):
            d[0] += 1
    sectors_breadth = sorted([{'sector': s, 'pct': round(100 * v[0] / v[1]), 'n': v[1]}
                              for s, v in sec.items() if v[1] >= SECTEUR_MIN],
                             key=lambda x: -x['pct'])
    return {'n': n, 'up': up, 'dn': dn, 'pct_a50': pa50, 'pct_a200': pa200, 'nh': nh, 'nl': nl,
            'pct_ob': round(100 * ob / max(1, len(rsis))), 'pct_os': round(100 * ov / max(1, len(rsis))),
            'avg_rsi': round(sum(rsis) / len(rsis)) if rsis else None, 'dist': dist,
            'nb': nb, 'nw': nw, 'na': na, 'advpct': advpct, 'breadth': breadth,
            'health': health, 'sectors': sectors_breadth}


__all__ = ['SECTEUR_MIN', 'market_internals']
