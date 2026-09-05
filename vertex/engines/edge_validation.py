"""Validation de l'edge — le score Vertex prédit-il les rendements ?

Backtest **walk-forward**, sans look-ahead. Pour des dates PASSÉES, le score
est recalculé « tel qu'il était » — l'analyse ne voit que l'historique tronqué
à la date évaluée — puis le rendement RÉELLEMENT réalisé ensuite est mesuré
(5 / 21 / 63 jours). Les observations sont regroupées par tranche de score :
c'est ce regroupement qui prouve, ou ne prouve pas, que score élevé = rendement
supérieur.

Sortent de là : les tranches (moyenne et taux de réussite), l'IC de rangs
(Spearman), l'écart haut-bas, la monotonie, et une courbe d'équité
illustrative (panier score ≥ 70 contre équipondéré, rééquilibré ~mensuellement).

## Pourquoi ce module existe

Ce code vivait dans `terminal.py`, l'adaptateur historique que le CLAUDE.md
demande de réduire par strangler pattern. Il y était **sans aucun test** — la
fonction qui répond « notre score vaut-il quelque chose ? » n'était éprouvée
par rien, parce qu'elle appelait directement la collecte réseau et qu'aucun
banc ne pouvait donc la faire tourner.

## Ce que l'extraction change vraiment

`telecharger` et `analyser` sont désormais **injectés**. Ce n'est pas une
élégance : c'est ce qui rend le backtest éprouvable. Avec des séries
fabriquées et un analyseur déterministe, on peut enfin vérifier la propriété
qui compte — qu'aucune information postérieure à la date évaluée n'entre dans
le score — au lieu de la supposer.

`terminal.edge_backtest` reste la porte d'entrée du produit : il fournit ses
quatre dépendances et garde sa signature d'origine, donc `_edge_loop` est
inchangée.

## Ce que ce module NE fait PAS

Il ne décide rien et n'oriente rien. Il mesure une prédictivité passée et la
publie avec son dénominateur (`n_obs`, `n_syms`, `n_dates`). Sous 50
observations il rend `None` plutôt qu'un verdict tiré d'un échantillon qui ne
soutient aucune conclusion.

⛔ LECTURE SEULE. Aucun ordre, aucune exécution. La courbe d'équité est
illustrative et étiquetée comme telle — ce n'est ni une performance réalisée,
ni une promesse.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime

import numpy as np

from vertex.engines.stats import spearman as _spearman

#: Sous ce nombre d'observations, aucune tranche ne porte assez de points pour
#: qu'une moyenne signifie quelque chose. On rend `None` — une absence — plutôt
#: qu'un verdict qui aurait l'air d'un résultat.
OBSERVATIONS_MINIMUM = 50

#: Tranches de score, du haut vers le bas. La borne haute est 101 pour inclure
#: un score de 100.
TRANCHES = [('85-100', 85, 101), ('70-85', 70, 85), ('55-70', 55, 70),
            ('40-55', 40, 55), ('0-40', 0, 40)]


def edge_backtest(*, telecharger, analyser, univers, bench,
                  syms=None, horizons=(5, 21, 63), step=8, lookback=460):
    """Voir le docstring du module. `telecharger` et `analyser` sont
    INJECTÉS : c'est ce qui rend ce backtest éprouvable sans réseau."""
    Hmax = max(horizons)
    syms = syms or list(univers)
    try:
        data = telecharger(syms + [bench], period='3y')
    except Exception:
        return None
    bc = data.get(bench)
    bclose = bc['Close'].dropna() if bc is not None else None
    obs = []
    used = set()
    for sym in syms:
        df = data.get(sym)
        if df is None:
            continue
        df = df.dropna()
        if len(df) < 260 + Hmax:
            continue
        close = df['Close']; n = len(df)
        start = max(260, n - lookback - Hmax)
        for pos in range(start, n - Hmax, step):
            sub = df.iloc[:pos + 1]
            bret = 0.0
            try:
                bi = bclose.index.get_indexer([df.index[pos]], method='ffill')[0]
                if bi > 63:
                    bret = float(bclose.iloc[bi]) / float(bclose.iloc[bi - 63]) - 1
            except Exception:
                pass
            try:
                sc = analyser(sub, bret).get('score')
            except Exception:
                continue
            if sc is None:
                continue
            p0 = float(close.iloc[pos])
            if p0 <= 0:
                continue
            rec = {'d': str(df.index[pos].date()), 's': float(sc)}
            ok = True
            for H in horizons:
                pv = float(close.iloc[pos + H])
                if pv <= 0:
                    ok = False; break
                rec['f%d' % H] = (pv / p0 - 1) * 100
            if ok:
                obs.append(rec); used.add(sym)
    if len(obs) < OBSERVATIONS_MINIMUM:
        return None
    BK = TRANCHES
    out = {'updated': datetime.now().strftime('%H:%M:%S'), 'n_obs': len(obs), 'n_syms': len(used),
           'horizons': list(horizons), 'buckets': {}, 'ic': {}, 'spread': {}, 'monotone': {}}
    for H in horizons:
        key = 'f%d' % H
        rows = []
        for lab, lo, hi in BK:
            vals = [o[key] for o in obs if lo <= o['s'] < hi]
            if vals:
                rows.append({'label': lab, 'lo': lo, 'hi': hi, 'n': len(vals),
                             'mean': round(float(np.mean(vals)), 2),
                             'hit': round(100 * float(np.mean([1.0 if v > 0 else 0.0 for v in vals])))})
            else:
                rows.append({'label': lab, 'lo': lo, 'hi': hi, 'n': 0, 'mean': None, 'hit': None})
        out['buckets'][str(H)] = rows
        out['ic'][str(H)] = _spearman([o['s'] for o in obs], [o[key] for o in obs])
        top = next((r['mean'] for r in rows if r['label'] == '85-100' and r['mean'] is not None), None)
        bot = next((r['mean'] for r in rows if r['label'] == '0-40' and r['mean'] is not None), None)
        out['spread'][str(H)] = round(top - bot, 2) if (top is not None and bot is not None) else None
        ms = [r['mean'] for r in rows[::-1] if r['mean'] is not None]   # tranche basse → haute
        out['monotone'][str(H)] = (all(ms[i] <= ms[i + 1] for i in range(len(ms) - 1)) if len(ms) >= 3 else None)
    # COURBE D'ÉQUITÉ (illustrative) : panier score≥70 vs équipondéré, rééquilibré ~mensuellement
    byd = defaultdict(list)
    for o in obs:
        if 'f21' in o:
            byd[o['d']].append(o)
    picks, last = [], None
    for d in sorted(byd.keys()):
        try:
            dd = datetime.strptime(d, '%Y-%m-%d')
        except Exception:
            continue
        if last is None or (dd - last).days >= 28:
            picks.append(d); last = dd
    eq = [{'t': 0, 'strat': 1.0, 'bench': 1.0}]
    s_eq = b_eq = 1.0
    for d in picks:
        grp = byd[d]
        hi = [o['f21'] for o in grp if o['s'] >= 70]
        if not hi:
            g2 = sorted(grp, key=lambda x: -x['s']); k = max(1, len(g2) // 5); hi = [o['f21'] for o in g2[:k]]
        allr = [o['f21'] for o in grp]
        s_eq *= (1 + float(np.mean(hi)) / 100); b_eq *= (1 + float(np.mean(allr)) / 100)
        eq.append({'t': len(eq), 'strat': round(s_eq, 3), 'bench': round(b_eq, 3)})
    out['equity'] = eq
    out['n_dates'] = len(picks)
    return out


__all__ = ['OBSERVATIONS_MINIMUM', 'TRANCHES', 'edge_backtest']
