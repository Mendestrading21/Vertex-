"""
vertex/data_sources/fundamentals.py — Fondamentaux par titre (yfinance tk.info) + médianes par secteur.

Permet de juger la VALORISATION d'un titre vs ses pairs : P/E du titre comparé au
P/E médian de son secteur (cher / dans la moyenne / décoté), marges, croissance, beta.

⚠️ tk.info est LENT et parfois incomplet (champs None) → tourné dans un thread dédié,
rafraîchi toutes les ~6 h. Étiqueter : fondamentaux yfinance, peuvent dater.
"""
import statistics
from concurrent.futures import ThreadPoolExecutor

import yfinance as yf

from vertex.market import sectors


def _f(v):
    try:
        return float(v) if v is not None else None
    except Exception:
        return None


def _one(s):
    """Fondamentaux d'UN titre via tk.info. Secteur : SECTOR_MAP sinon yfinance (couvre TOUT l'univers)."""
    try:
        info = yf.Ticker(s).info or {}
    except Exception:
        return s, None
    sec = sectors.SECTOR_MAP.get(s) or info.get('sector')
    return s, {
        'pe': _f(info.get('trailingPE')),
        'fwd_pe': _f(info.get('forwardPE')),
        'pb': _f(info.get('priceToBook')),
        'peg': _f(info.get('pegRatio') or info.get('trailingPegRatio')),
        'margin': _f(info.get('profitMargins')),
        'growth': _f(info.get('revenueGrowth')),
        'beta': _f(info.get('beta')),
        'mcap': _f(info.get('marketCap')),
        'div': _f(info.get('dividendYield')),
        'roe': _f(info.get('returnOnEquity')),
        'debt_eq': _f(info.get('debtToEquity')),
        'sector': sec,
        'industry': info.get('industry'),
        'name': info.get('shortName') or info.get('longName'),
    }


def build(symbols):
    """tk.info pour CHAQUE titre (parallélisé) → {by_sym:{sym:{...}}, by_sector:{sec:{median_pe,...}}}.
    Couvre TOUT l'univers passé (plus seulement la watchlist cœur)."""
    by_sym = {}
    try:
        with ThreadPoolExecutor(max_workers=8) as ex:        # 176× tk.info en série = trop lent
            for s, v in ex.map(_one, list(symbols)):
                if v is not None:
                    by_sym[s] = v
    except Exception:
        for s in symbols:                                     # repli séquentiel si l'executor casse
            _s, v = _one(s)
            if v is not None:
                by_sym[_s] = v

    by_sector = {}
    allsecs = set(v.get('sector') for v in by_sym.values() if v.get('sector'))
    for sec in allsecs:
        members = [v for k, v in by_sym.items() if v.get('sector') == sec]
        pes = [v['pe'] for v in members if v.get('pe') and 0 < v['pe'] < 250]
        fwd = [v['fwd_pe'] for v in members if v.get('fwd_pe') and 0 < v['fwd_pe'] < 250]
        mg = [v['margin'] for v in members if v.get('margin') is not None]
        gr = [v['growth'] for v in members if v.get('growth') is not None]
        if pes or fwd:
            by_sector[sec] = {
                'median_pe': round(statistics.median(pes), 1) if pes else None,
                'median_fwd_pe': round(statistics.median(fwd), 1) if fwd else None,
                'median_margin': round(statistics.median(mg) * 100, 1) if mg else None,
                'median_growth': round(statistics.median(gr) * 100, 1) if gr else None,
                'n': len(members),
            }
    return {'by_sym': by_sym, 'by_sector': by_sector}


def valuation(pe, sector_median_pe):
    """Étiquette de valorisation d'un P/E vs la médiane de son secteur."""
    if not pe or not sector_median_pe or sector_median_pe <= 0:
        return None
    r = pe / sector_median_pe
    if r >= 1.3:
        return {'label': 'cher (premium)', 'ratio': round(r, 2), 'tone': 'warn'}
    if r <= 0.75:
        return {'label': 'décoté', 'ratio': round(r, 2), 'tone': 'good'}
    return {'label': 'dans la moyenne', 'ratio': round(r, 2), 'tone': 'neutral'}
