"""
vertex/data/demo.py — DONNÉES DE VITRINE (mode DÉMO, Ch. II).

Génère un univers OHLCV synthétique déterministe (graine = CRC32 du symbole,
dernier cours ancré sur un niveau réaliste) et un board d'options CALL crédible
mais FICTIF, pour que l'app ne soit jamais vide en démo. Les valeurs sont
reproductibles par graine ; seule la date du dernier jour suit le calendrier.

Extrait verbatim du monolithe. Données SYNTHÉTIQUES — l'UI affiche toujours
l'état « démo ». Analyse uniquement, aucune exécution.
"""

import math
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


_DEMO_BASE = {'SPY': 600.0, '^GSPC': 6000.0, '^IXIC': 20000.0, '^DJI': 44000.0,
              '^RUT': 2300.0, '^VIX': 15.0,
              # prix réalistes pour les 20 titres scannés en démo (vitrine crédible)
              'AAPL': 230.0, 'NVDA': 140.0, 'MSFT': 440.0, 'META': 600.0, 'GOOGL': 180.0,
              'AMZN': 210.0, 'AVGO': 170.0, 'TSLA': 340.0, 'NFLX': 900.0, 'AMD': 140.0,
              'CRM': 330.0, 'COST': 950.0, 'LLY': 800.0, 'JPM': 250.0, 'V': 310.0,
              'MA': 520.0, 'HD': 410.0, 'UNH': 520.0, 'XOM': 110.0, 'WMT': 95.0}


def _demo_one(sym, n=260):
    import zlib
    seed = zlib.crc32(sym.encode('utf-8')) & 0xffffffff
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range(end=datetime.now().date(), periods=n)
    if sym == '^VIX':                       # volatilité : oscille, ne « tend » pas
        close = np.clip(15 + rng.normal(0, 2.2, n) + 3 * np.sin(np.linspace(0, 6, n)), 9, 38)
    else:
        base = _DEMO_BASE.get(sym) or (18.0 + seed % 480)      # 18 → ~500 $
        drift = (rng.random() - 0.42) * 0.0016                 # léger biais haussier
        vol = 0.008 + rng.random() * 0.03
        close = base * np.exp(np.cumsum(rng.normal(drift, vol, n)))
        close = close * (base / close[-1])     # ancre le DERNIER cours sur le prix réaliste
    close = close.astype('float32')
    hi = (close * (1 + rng.random(n).astype('float32') * 0.012)).astype('float32')
    lo = (close * (1 - rng.random(n).astype('float32') * 0.012)).astype('float32')
    op = (close * (1 + (rng.random(n).astype('float32') - 0.5) * 0.01)).astype('float32')
    volm = rng.integers(800_000, 60_000_000, n).astype('float32')
    return pd.DataFrame({'Open': op, 'High': hi, 'Low': lo, 'Close': close, 'Volume': volm}, index=idx)


def _demo_universe(tickers):
    return {t: _demo_one(t) for t in tickers}


def _demo_options_board(rows, detail):
    """Board d'options synthétique (mode VITRINE) — crédible mais FICTIF.
    CALL sur les meilleurs titres + PUT sur les plus faibles (et couverture sur
    les leaders), 3 échéances (court/moyen/long), avec liquidité synthétique
    (open interest, volume, spread) pour nourrir le cockpit Options Lab."""
    import zlib
    board = []
    scored = [r for r in rows if r.get('score') is not None]
    top = sorted(scored, key=lambda r: r.get('score', 0), reverse=True)[:12]
    weak = sorted(scored, key=lambda r: r.get('score', 0))[:6]
    BK = [('court', 45, 0.55), ('moyen', 180, 0.42), ('long', 400, 0.32)]

    def _mk(r, right, bk, dte, dlt, rng):
        sym = r['symbol']
        spot = r.get('price') or 100.0
        d = detail.get(sym) or {}
        rs = d.get('rs') or 50
        T = dte / 365.0
        iv = 0.28 + (rng.random() * 0.34)                 # 28 % → 62 %
        sgn = 1 if right == 'CALL' else -1
        strike = round(spot * (1 + sgn * ((0.5 - dlt) * 0.12 + rng.random() * 0.03)), 1)
        em = iv * math.sqrt(T)
        mid = max(0.4, spot * em * (0.55 + dlt * 0.4))
        cost = round(mid * 100)
        be = round(strike + sgn * mid, 2)
        tgt = round(spot * (1 + sgn * em * 1.1), 2)
        pot = round(abs(tgt - be) / max(mid, 0.1) * 100) if (tgt - be) * sgn > 0 else 0
        edge = (be / spot - 1) * sgn
        pop = round(max(12, min(72, 50 - edge * 220 + sgn * (rs - 50) * 0.3)))
        dg = (2 if bk == 'court' else 0) + (1 if iv > 0.55 else 0) + (1 if dlt < 0.4 else 0)
        theta_burn = round((0.9 if bk == 'court' else 0.35 if bk == 'moyen' else 0.16) * (1 + iv), 2)
        base = r.get('score', 50) if right == 'CALL' else (100 - r.get('score', 50))
        quality = round(max(20, min(94, 40 + (base - 50) * 0.7
                                    + sgn * (rs - 50) * 0.2 + pot * 0.05 - dg * 6)))
        # liquidité synthétique : les gros titres liquides ont plus d'OI et un spread serré
        liq = max(0.15, min(1.0, (r.get('score', 50) / 100) + rng.random() * 0.3))
        oi = int(800 + liq * 26000 * (1.3 if bk == 'moyen' else 1.0) * (0.5 + rng.random()))
        vol = int(oi * (0.06 + rng.random() * 0.22))
        spread_pct = round(max(0.6, 9.0 * (1.1 - liq) * (1.5 if bk == 'long' else 1.0)), 1)
        return {
            'sym': sym, 'type': right, 'bucket': bk,
            'exp': (datetime.now() + timedelta(days=dte)).strftime('%Y-%m-%dT00:00:00'),
            'dte': dte, 'strike': strike, 'tgt': tgt, 'spot': round(spot, 2),
            'pop': pop, 'p_tgt': max(8, round(pop * 0.7)), 'danger_n': dg,
            'cost': cost, 'be': be, 'iv': round(iv * 100, 1),
            'delta': round(sgn * (dlt + rng.random() * 0.1), 2),
            'theta_burn': theta_burn, 'pot': pot, 'em_pct': round(em * 100, 1),
            'quality': quality, 'veh': (r.get('vehicle') or None),
            'oi': oi, 'vol': vol, 'spread_pct': spread_pct,
            'why': 'Échéance ' + bk + ' — profil synthétique de démonstration.'}

    for r in top:
        rng = np.random.default_rng(zlib.crc32(r['symbol'].encode()) & 0xffffffff)
        for bk, dte, dlt in BK:
            board.append(_mk(r, 'CALL', bk, dte, dlt, rng))
    # PUT : baissiers sur les titres faibles + couverture (moyen terme) sur 3 leaders
    for r in weak:
        rng = np.random.default_rng((zlib.crc32(r['symbol'].encode()) ^ 0x9E3779B9) & 0xffffffff)
        for bk, dte, dlt in BK[:2]:
            board.append(_mk(r, 'PUT', bk, dte, dlt, rng))
    for r in top[:3]:
        rng = np.random.default_rng((zlib.crc32(r['symbol'].encode()) ^ 0x5DEECE66) & 0xffffffff)
        board.append(_mk(r, 'PUT', 'moyen', 180, 0.35, rng))
    board.sort(key=lambda c: c.get('quality', 0), reverse=True)
    return board


__all__ = ['demo_one', 'demo_universe', 'demo_options_board', 'DEMO_BASE']

DEMO_BASE = _DEMO_BASE
demo_one = _demo_one
demo_universe = _demo_universe
demo_options_board = _demo_options_board
