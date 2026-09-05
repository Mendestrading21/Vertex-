"""Stooq — source de secours EOD, en lecture seule.

## Pourquoi cette source existe

Yahoo (yfinance) limite le débit des serveurs de datacenter : `yf.download`
revient VIDE sur une IP cloud. Stooq sert de filet — clôtures quotidiennes,
donc une seule mise à jour utile par jour. Le TTL de 6 h évite de marteler un
endpoint gratuit sans rien y gagner.

## Pourquoi ce module existe

Ce code vivait dans `terminal.py`, qui n'en est pas le propriétaire naturel :
une source de données n'a rien à faire dans l'adaptateur historique que le
CLAUDE.md demande de réduire par strangler pattern. Il rejoint ses pairs dans
`vertex/data_sources/`.

## Ce que le déplacement ne change PAS

Le cache et son TTL restent la propriété de `vertex/app/caches.py`, où leur
politique de fraîcheur est écrite et testée (`POLITIQUE`). Les objets importés
ici sont les MÊMES : mutés en place, jamais réassignés, donc
`stooq._STOOQ_CACHE is caches._STOOQ_CACHE`.

`terminal` réexporte les trois noms publics. Deux bancs remplacent
`terminal._stooq_download` par une doublure (`test_active_source_timeouts`,
`test_scan_timeout_degradation`) : la substitution continue de fonctionner
parce que l'appelant, `_download_universe`, résout le nom dans les globales de
`terminal` au moment de l'appel.

⛔ LECTURE SEULE. Aucune écriture, aucun ordre, aucune donnée de compte.
"""
from __future__ import annotations

import time
from datetime import datetime, timedelta

import pandas as pd

from vertex.app.caches import _SOURCE_BUDGET_STATE, _STOOQ_CACHE, _STOOQ_TTL

#: Plafond d'attente d'une requête Stooq. Explicite : sans lui, une requête
#: pendante bloquerait un scan entier. `test_active_source_timeouts` le vérifie.
STOOQ_REQUEST_TIMEOUT_SECONDS = 8

#: Correspondance des symboles d'indices, matières premières et crypto : Stooq
#: ne parle pas la même langue que Yahoo.
_STOOQ_IDX = {
    '^GSPC': '^spx', '^DJI': '^dji', '^IXIC': '^ndq', '^RUT': '^rut',
    '^VIX': '^vix',
    'GC=F': 'xauusd', 'SI=F': 'xagusd', 'CL=F': 'cl.f', 'BZ=F': 'cb.f',
    'BTC-USD': 'btcusd',
}


def _stooq_symbol(t):
    if t in _STOOQ_IDX:
        return _STOOQ_IDX[t]
    if t.startswith('^'):
        return t[1:].lower()
    return t.lower() + '.us'          # ex: AAPL→aapl.us, BRK-B→brk-b.us


def _stooq_one(t):
    """Télécharge l'historique quotidien d'UN ticker depuis Stooq (CSV)."""
    import urllib.request
    from io import StringIO
    d2 = datetime.now()
    d1 = d2 - timedelta(days=1100)    # ~3 ans → assez pour MM200
    url = (f'https://stooq.com/q/d/l/?s={_stooq_symbol(t)}'
           f'&d1={d1:%Y%m%d}&d2={d2:%Y%m%d}&i=d')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=STOOQ_REQUEST_TIMEOUT_SECONDS) as r:
            txt = r.read().decode('utf-8', 'ignore')
        if not txt or 'Date' not in txt[:60]:   # 'No data' / page HTML → échec
            return t, None
        df = pd.read_csv(StringIO(txt))
        if df.empty or 'Close' not in df.columns or 'Date' not in df.columns:
            return t, None
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']).set_index('Date').sort_index()
        keep = [c for c in ('Open', 'High', 'Low', 'Close', 'Volume') if c in df.columns]
        df = df[keep].dropna(subset=['Close'])
        return (t, df) if not df.empty else (t, None)
    except Exception:
        return t, None


def _stooq_download(tickers):
    """Filet de secours mutualisé + caché 6 h. Renvoie {ticker: DataFrame}.
    Cache FUSIONNÉ : si le cache est frais mais qu'il MANQUE des tickers demandés,
    on ne télécharge que les manquants (au lieu de les affamer pendant 6 h)."""
    now = time.time()
    cache = _STOOQ_CACHE['frames']
    fresh = bool(cache) and (now - _STOOQ_CACHE['ts'] < _STOOQ_TTL)
    todo = [t for t in tickers if not (fresh and t in cache)]
    if fresh and not todo:
        return {t: cache[t] for t in tickers if t in cache}
    out = {}
    try:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=6) as ex:   # doux pour l'endpoint gratuit
            for t, df in ex.map(_stooq_one, todo):
                if df is not None and len(df) >= 60:
                    out[t] = df
    except Exception:
        for t in todo:
            _t, df = _stooq_one(t)
            if df is not None and len(df) >= 60:
                out[_t] = df
    if out:
        merged = dict(cache) if fresh else {}
        merged.update(out)
        _STOOQ_CACHE['frames'] = merged
        _STOOQ_CACHE['ts'] = now if not fresh else _STOOQ_CACHE['ts']
        cache = merged
    _SOURCE_BUDGET_STATE['stooq'] = 'AVAILABLE' if out else ('CACHED' if cache else 'UNAVAILABLE')
    return {t: cache[t] for t in tickers if t in cache} if cache else out


__all__ = ['STOOQ_REQUEST_TIMEOUT_SECONDS', '_STOOQ_IDX',
           '_stooq_symbol', '_stooq_one', '_stooq_download']
