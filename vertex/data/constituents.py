"""
vertex/data/constituents.py — constituants LIVE des 3 indices US (donnee + I/O reseau borne).

Recupere S&P 500 + Nasdaq 100 + Dow Jones (Wikipedia, avec User-Agent), normalise les tickers
pour yfinance (BRK.B -> BRK-B), met en cache disque (rafraichi si > TTL), et retombe sur un
snapshot statique embarque si le reseau echoue -> le demarrage n'est JAMAIS bloque.

LECTURE SEULE. Aucun ordre, aucune ecriture marche. Un ticker invalide est simplement ignore
plus loin par le chargeur yfinance (chargement par lots robustes).
"""
import io
import json
import os
import time

from vertex.data._constituents_static import SP_SP500, SP_NDX100, SP_DOW30

_STATIC = {'sp500': SP_SP500, 'ndx100': SP_NDX100, 'dow30': SP_DOW30}

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_CACHE_FILE = os.path.join(_ROOT, 'constituents_cache.json')
_TTL = 12 * 3600   # 12 h : au-dela on retente un fetch live au demarrage
_TIMEOUT = 15      # s par requete Wikipedia
_UA = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/140 Safari/537.36')}
_SOURCES = {
    'sp500':  ('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', 'Symbol', 'Symbol'),
    'ndx100': ('https://en.wikipedia.org/wiki/Nasdaq-100', 'Ticker', 'Ticker'),
    'dow30':  ('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average', 'Symbol', 'Symbol'),
}


def _norm(sym):
    """Normalise un ticker pour yfinance : maj, trim, points -> tirets (BRK.B -> BRK-B)."""
    return str(sym).strip().upper().replace('.', '-')


def _clean(lst):
    """Ne garde que des tickers plausibles (1-6 lettres, un tiret autorise), dedupliques."""
    out = []
    for x in lst:
        t = _norm(x)
        if t and 1 <= len(t) <= 6 and t.replace('-', '').isalpha():
            out.append(t)
    return list(dict.fromkeys(out))


def _fetch_one(url, match, col):
    import pandas as pd
    import requests
    r = requests.get(url, headers=_UA, timeout=_TIMEOUT)
    r.raise_for_status()
    df = pd.read_html(io.StringIO(r.text), match=match)[0]
    return _clean(df[col].tolist())


def _fetch_all():
    res = {}
    for key, (url, match, col) in _SOURCES.items():
        res[key] = _fetch_one(url, match, col)
    # garde-fou : listes trop courtes = parsing casse -> on refuse, le fallback prend le relais
    if len(res['sp500']) < 400 or len(res['ndx100']) < 80 or len(res['dow30']) < 25:
        raise ValueError('listes constituants incompletes (parsing Wikipedia)')
    return res


def _load_cache():
    try:
        with open(_CACHE_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def _save_cache(data):
    try:
        with open(_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception:
        pass


def get_index_members(force=False):
    """Rend {sp500, ndx100, dow30, union, source, ts}. Ne leve jamais d'exception.

    Ordre de resolution : cache frais (< TTL) -> fetch live -> cache perime -> snapshot statique.
    `force=True` ignore le cache et retente un fetch live (utilise par le bouton "Analyser tout").
    """
    cache = _load_cache()
    now = time.time()
    if cache and not force and (now - cache.get('_ts', 0) < _TTL):
        data, source = cache, 'cache'
    else:
        try:
            data = _fetch_all()
            data['_ts'] = now
            _save_cache(data)
            source = 'live'
        except Exception:
            if cache:
                data, source = cache, 'cache-stale'
            else:
                data, source = dict(_STATIC, _ts=0), 'static'
    sp = data.get('sp500') or _STATIC['sp500']
    ndx = data.get('ndx100') or _STATIC['ndx100']
    dow = data.get('dow30') or _STATIC['dow30']
    union = list(dict.fromkeys(sp + ndx + dow))
    return {'sp500': sp, 'ndx100': ndx, 'dow30': dow, 'union': union,
            'source': source, 'ts': data.get('_ts', 0)}


__all__ = ['get_index_members']
