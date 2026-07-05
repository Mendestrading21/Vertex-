"""
vertex/engines/backtest.py — FORWARD-TEST PAPER (Ch. II).

Rejoue la stratégie « top N titres score>=smin, rebalance quotidien, signal
d'HIER (zéro lookahead) » sur l'historique de la WATCHLIST et renvoie la courbe
d'équité + les métriques de vérité (Sharpe, Sortino, CAGR, expectancy, maxDD…).

Extrait verbatim du monolithe. Analyse uniquement, aucune exécution — c'est un
test PAPIER, il ne passe aucun ordre.
"""

import math

import pandas as pd

from vertex.data.universe import WATCHLIST
from vertex.engines import indicators


def backtest(data, lb=126, top_n=5, smin=58, eq0=100000.0):
    """Forward-test PAPER : top N titres score>=smin, rebalance quotidien, signal d'HIER (zéro lookahead)."""
    closes, scores = {}, {}
    for sym in WATCHLIST:
        try:
            df = data[sym].dropna()
            if len(df) < 210:
                continue
            c = df['Close']
            e20, e50, e200 = c.ewm(span=20).mean(), c.ewm(span=50).mean(), c.ewm(span=200).mean()
            rsi = indicators.rsi(c)
            roc = (c / c.shift(21) - 1) * 100
            trend = ((e20 > e50).astype(int) + (e50 > e200).astype(int) + (c > e50).astype(int)) / 3 * 100
            mom = (50 + (rsi - 50) * 0.6 + roc.clip(-25, 25)).clip(0, 100)
            scores[sym] = 0.55 * trend + 0.45 * mom
            closes[sym] = c
        except Exception:
            continue
    if len(closes) < 3:
        return None
    idx = None
    for s in closes:
        idx = closes[s].index if idx is None else idx.intersection(closes[s].index)
    idx = idx[-lb:]
    rets = pd.DataFrame({s: closes[s].pct_change() for s in closes}).reindex(idx).fillna(0.0)
    sig = pd.DataFrame({s: scores[s] for s in closes}).reindex(idx).shift(1)
    eq, dr, journal, entry_px = [eq0], [], [], {}
    prev = set()
    for date in idx:
        row = sig.loc[date].dropna()
        held = set(row[row >= smin].nlargest(top_n).index.tolist())
        r = float(rets.loc[date, list(held)].mean()) if held else 0.0
        r = 0.0 if math.isnan(r) else r
        dr.append(r)
        eq.append(eq[-1] * (1 + r))
        for s in held - prev:
            entry_px[s] = float(closes[s].loc[date])
            journal.append({'sym': s, 'action': 'BUY', 'date': date.strftime('%m-%d'), 'price': round(entry_px[s], 2), 'pnl': None})
        for s in prev - held:
            px = float(closes[s].loc[date])
            pnl = (px / entry_px.get(s, px) - 1) * 100 if entry_px.get(s) else 0
            journal.append({'sym': s, 'action': 'SELL', 'date': date.strftime('%m-%d'), 'price': round(px, 2), 'pnl': round(pnl, 2)})
        prev = held
    eq = eq[1:]
    drs = pd.Series(dr)
    peak = pd.Series(eq).cummax()
    closed = [j for j in journal if j['action'] == 'SELL']
    wins = [j for j in closed if (j['pnl'] or 0) > 0]
    losses = [j for j in closed if (j['pnl'] or 0) <= 0]
    # ── FONCTION DE VÉRITÉ ÉLARGIE (Sortino, CAGR, expectancy, turnover) ────────
    years = max(len(idx) / 252.0, 1e-9)
    down = drs[drs < 0]
    sortino = round(float(drs.mean() / down.std() * math.sqrt(252)), 2) if len(down) > 1 and down.std() else 0
    cagr = round(((eq[-1] / eq0) ** (1 / years) - 1) * 100, 2) if eq[-1] > 0 else 0
    pnls = [j['pnl'] or 0 for j in closed]
    expectancy = round(sum(pnls) / len(pnls), 2) if pnls else 0          # % moyen / trade
    avg_win = round(sum(j['pnl'] for j in wins) / len(wins), 2) if wins else 0
    avg_loss = round(sum(j['pnl'] for j in losses) / len(losses), 2) if losses else 0
    turnover = round(len(closed) / years / max(top_n, 1), 1)            # rotations/slot/an
    return {
        'dates': [d.strftime('%Y-%m-%d') for d in idx], 'equity': [round(x) for x in eq],
        'balance': round(eq[-1], 2), 'total': round((eq[-1] / eq0 - 1) * 100, 2),
        'sharpe': round(float(drs.mean() / drs.std() * math.sqrt(252)), 2) if drs.std() else 0,
        'sortino': sortino, 'cagr': cagr, 'expectancy': expectancy,
        'avg_win': avg_win, 'avg_loss': avg_loss, 'turnover': turnover,
        'maxdd': round(float((pd.Series(eq) / peak - 1).min() * 100), 2),
        'ath': round((max(eq) / eq0 - 1) * 100, 2), 'atl': round((min(eq) / eq0 - 1) * 100, 2),
        'trades': len(closed), 'winrate': round(len(wins) / len(closed) * 100) if closed else 0,
        'holdings': sorted(prev), 'journal': list(reversed(journal))[:40], 'top_n': top_n,
    }


__all__ = ['backtest']
