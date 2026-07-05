"""
vertex/engines/analysis.py — LE CŒUR ANALYTIQUE (Ch. II).

analyse() transforme un DataFrame OHLCV en fiche technique complète : tendances,
régime, momentum, anomalies, profil, scoring (elio), rétroaction physique &
multi-horizons, plan (stop structurel + R:R). Extrait verbatim du monolithe —
même logique, désormais isolée et testable (test de non-régression « golden »).

Analyse uniquement. Aucune exécution.
"""

import math

import numpy as np
import pandas as pd

from elio import scoring, config, pivots, physics, timeframe, vertex
from vertex.engines import indicators


def analyse(df, bench_ret, fund=None):
    c = df['Close'].dropna()
    last = float(c.iloc[-1])
    e20 = float(c.ewm(span=20).mean().iloc[-1])
    e50 = float(c.ewm(span=50).mean().iloc[-1])
    e200 = float(c.ewm(span=200).mean().iloc[-1])
    # SMA avec repli sur l'EWM quand l'historique est trop court (< 50/200 barres) :
    # évite les NaN qui casseraient le JSON de /scan pour les titres récemment cotés.
    s50 = float(c.rolling(50).mean().iloc[-1]);  s50 = e50 if math.isnan(s50) else s50
    s200 = float(c.rolling(200).mean().iloc[-1]);  s200 = e200 if math.isnan(s200) else s200
    s50p = float(c.rolling(50).mean().iloc[-2]) if len(c) > 1 else s50
    s50p = s50 if math.isnan(s50p) else s50p
    s200p = float(c.rolling(200).mean().iloc[-2]) if len(c) > 1 else s200
    s200p = s200 if math.isnan(s200p) else s200p
    atr = float(indicators.atr(df).iloc[-1])
    rsi_s = indicators.rsi(c)
    r = float(rsi_s.iloc[-1])
    roc = (last / float(c.iloc[-21]) - 1) * 100 if len(c) > 21 else 0.0
    # Certains flux (indices/ETF via Stooq) n'ont pas de colonne Volume → repli à 0 plutôt qu'un KeyError.
    _v = df['Volume'] if 'Volume' in df.columns else pd.Series([0.0] * len(df), index=df.index)
    vol = float(_v.iloc[-1]) if len(_v) else 0.0
    volavg = float(_v.tail(20).mean()) if len(_v) else 0.0
    volavg = 0.0 if math.isnan(volavg) else volavg
    hi = float(c.tail(252).max()); lo = float(c.tail(252).min())
    pos = (last - lo) / (hi - lo) * 100 if hi > lo else 50.0

    stack = int(e20 > e50) + int(e50 > e200) + int(last > e50)
    trend = stack / 3 * 100
    sym_ret = (last / float(c.iloc[-63]) - 1) if len(c) > 63 else 0.0
    rs = float(np.clip(50 + (sym_ret - bench_ret) * 200, 0, 100))
    volx = vol / volavg if volavg else 1.0
    atr_pct = atr / last * 100 if last else 0.0
    ext_atr = (last - e20) / atr if atr else 0.0
    chg = (last / float(c.iloc[-2]) - 1) * 100 if len(c) > 1 else 0.0

    # RÉGIME : ADX (force de tendance) + Choppiness (bruit) → filtre les faux signaux en range
    adx = indicators.adx(df)
    tr14 = pd.concat([df['High'] - df['Low'], (df['High'] - c.shift()).abs(),
                      (df['Low'] - c.shift()).abs()], axis=1).max(axis=1).tail(14).sum()
    rng14 = float(df['High'].tail(14).max() - df['Low'].tail(14).min())
    chop = float(100 * math.log10(tr14 / rng14) / math.log10(14)) if rng14 > 0 else 50.0
    regime = 'TREND' if adx >= 25 and chop < 50 else 'CHOP' if chop >= 60 else 'NEUTRAL'
    # DIVERGENCE RSI réelle (pente prix vs pente RSI sur 20 barres) — pas un proxy
    win = 20
    bear_div = (last >= float(c.iloc[-win:-1].max())) and (r < float(rsi_s.iloc[-win:-1].max()) - 3)
    bull_div = (last <= float(c.iloc[-win:-1].min())) and (r > float(rsi_s.iloc[-win:-1].min()) + 3)
    rsi_div = 'bear' if bear_div else 'bull' if bull_div else None

    # QUALITÉ DE TENDANCE : les MM montent-elles VRAIMENT (pente) — pas juste empilées ?
    ma50_rising = s50 > s50p
    ma200_rising = s200 > s200p
    # une structure empilée mais à pente plate/baissière = tendance qui s'essouffle → on la pénalise
    trend_quality = round(trend * (1.0 if ma50_rising else 0.72))

    # SQUEEZE DE VOLATILITÉ (Bollinger 20) : largeur de bande dans son plus-bas 6 mois
    # → compression = énergie qui s'accumule, cassure souvent imminente.
    bb_mid = c.rolling(20).mean()
    bb_wid = (c.rolling(20).std() / bb_mid * 100).dropna()
    bb_now = float(bb_wid.iloc[-1]) if len(bb_wid) else None
    bb_rank = round(float((bb_wid.tail(126) <= bb_now).mean() * 100)) if (bb_now is not None and len(bb_wid) >= 20) else None
    squeeze = bool(bb_rank is not None and bb_rank <= 20)

    # CASSURE CONFIRMÉE : nouveau plus-haut 20 jours porté par le volume (≥ 1.5× la moyenne).
    hi20 = float(c.tail(21).iloc[:-1].max()) if len(c) > 21 else last
    breakout = bool(last >= hi20 and volx >= 1.5)

    # ACCUMULATION / DISTRIBUTION via OBV (On-Balance Volume) — lecture du « smart money ».
    # OBV qui monte pendant que le prix stagne = accumulation cachée (haussier).
    # OBV qui baisse pendant que le prix monte = distribution cachée (faiblesse sous le capot).
    obv = (np.sign(c.diff().fillna(0.0)) * _v).cumsum()
    obv_slope = float(obv.iloc[-1] - obv.iloc[-20]) if len(obv) > 20 else 0.0
    px_slope20 = (last - float(c.iloc[-20])) if len(c) > 20 else 0.0
    accumulation = bool(obv_slope > 0 and px_slope20 <= 0.01 * last)
    distribution = bool(obv_slope < 0 and px_slope20 > 0.01 * last)

    # REPLI SUR TENDANCE (buy-the-dip sain) : fond haussier + MM50 qui monte + RSI redescendu
    # + cours revenu près de la MM20/MM50 → entrée à moindre risque sur une tendance intacte.
    uptrend = last > s50 and last > s200
    near_ma = (abs(last - e20) < 1.0 * atr or abs(last - s50) < 1.2 * atr) if atr else False
    pullback = bool(uptrend and ma50_rising and 40 <= r <= 56 and near_ma and not breakout)

    # PROFIL OFFENSIF / DÉFENSIF — la NATURE du titre (comment le jouer).
    # Offensif = nerveux, fort beta, momentum ample → gros potentiel (options court/moyen).
    # Défensif = stable, faible beta, dividende, secteur défensif → sécurité (actions / LEAPS).
    _beta = (fund or {}).get('beta')
    _div = (fund or {}).get('div')
    _sec = ((fund or {}).get('sector') or (fund or {}).get('industry') or '')
    _DEF = ('Utilities', 'Consumer Defensive', 'Consumer Staples', 'Healthcare', 'Health Care', 'Real Estate', 'Utility')
    _OFF = ('Technology', 'Consumer Cyclical', 'Consumer Discretionary', 'Energy', 'Communication', 'Semiconduct')
    _off = (2 if atr_pct >= 3.2 else 0) + (2 if (_beta is not None and _beta >= 1.25) else 0) \
        + (1 if abs(roc) >= 12 else 0) + (2 if any(s in _sec for s in _OFF) else 0)
    _def = (2 if atr_pct <= 1.7 else 0) + (2 if (_beta is not None and _beta <= 0.9) else 0) \
        + (2 if (_div is not None and _div >= 0.02) else (1 if _div else 0)) + (2 if any(s in _sec for s in _DEF) else 0)
    if _off - _def >= 2:
        profile, profile_hint = 'OFFENSIF', 'titre nerveux → gros potentiel : options court/moyen (1-8 sem) pour le levier'
    elif _def - _off >= 2:
        profile, profile_hint = 'DÉFENSIF', 'titre stable → sécurité : actions ou LEAPS long, dividende, faible drawdown'
    else:
        profile, profile_hint = 'ÉQUILIBRÉ', 'polyvalent → actions ou options moyennes (1-3 mois) selon la conviction'

    # ─── RADAR D'ANOMALIES VERTEX — repère l'INHABITUEL que l'œil rate : un prix,
    # un volume ou une volatilité STATISTIQUEMENT hors-norme est une information.
    # Gap, z-score extrême, pic de volume, expansion de range, choc de volatilité.
    anomalies = []
    o = df['Open']
    prev_close = float(c.iloc[-2]) if len(c) > 2 else last
    gap_pct = round((float(o.iloc[-1]) - prev_close) / prev_close * 100, 2) if prev_close else 0.0
    gap_atr = round((float(o.iloc[-1]) - prev_close) / atr, 2) if atr else 0.0
    if abs(gap_atr) >= 0.8:
        anomalies.append({'k': 'gap', 'sev': int(min(3, max(1, round(abs(gap_atr))))),
                          'lbl': ('⤒ Gap haussier ' if gap_atr > 0 else '⤓ Gap baissier ')
                          + f'{gap_pct:+.1f}% ({abs(gap_atr):.1f} ATR)'})
    sd20 = float(c.rolling(20).std().iloc[-1]) if len(c) > 20 else 0.0
    zc = round((last - e20) / sd20, 2) if sd20 else 0.0
    if abs(zc) >= 2.2:
        anomalies.append({'k': 'zscore', 'sev': int(min(3, max(1, round(abs(zc)) - 1))),
                          'lbl': f'σ Prix à {zc:+.1f}σ de la MM20 (extrême statistique)'})
    vser = _v.tail(60)
    vmean = float(vser.mean()); vstd = float(vser.std()) or 1.0
    vz = round((vol - vmean) / vstd, 2)
    if vz >= 2.5:
        anomalies.append({'k': 'volspike', 'sev': int(min(3, max(1, round(vz) - 1))),
                          'lbl': f'🔊 Volume anormal ({volx:.1f}× — z {vz:+.1f})'})
    tr = float(df['High'].iloc[-1] - df['Low'].iloc[-1])
    rng_x = round(tr / atr, 2) if atr else 0.0
    if rng_x >= 2.0:
        anomalies.append({'k': 'range', 'sev': int(min(3, max(1, round(rng_x) - 1))),
                          'lbl': f'↔ Barre élargie ({rng_x:.1f}× ATR) — volatilité qui explose'})
    if bb_rank is not None and bb_rank >= 90:
        anomalies.append({'k': 'volshock', 'sev': 2, 'lbl': f'💥 Volatilité au plus-haut 6 mois (rang {bb_rank}%)'})
    if rsi_div == 'bear':
        anomalies.append({'k': 'divbear', 'sev': 2, 'lbl': '⚠️ Divergence RSI baissière (prix haut, momentum en repli)'})
    elif rsi_div == 'bull':
        anomalies.append({'k': 'divbull', 'sev': 1, 'lbl': '↗️ Divergence RSI haussière (prix bas, momentum qui remonte)'})
    if distribution:
        anomalies.append({'k': 'distrib', 'sev': 2, 'lbl': '🔴 Distribution cachée (OBV/prix divergent)'})
    if ext_atr >= 4:
        anomalies.append({'k': 'ext', 'sev': int(min(3, max(1, round(ext_atr) - 3))),
                          'lbl': f'🌡️ Sur-extension {ext_atr:.1f} ATR au-dessus de la MM20'})
    anomaly_score = int(min(100, sum(a['sev'] for a in anomalies) * 16))
    anomaly_lvl = ('CALME' if anomaly_score < 25 else 'ACTIF' if anomaly_score < 55 else 'ALERTE')

    # signaux booléens (style checklist)
    sig = {
        'above20': last > e20, 'above50': last > s50, 'above200': last > s200,
        'stacked': e20 > e50 > e200,
        'golden': (s50 > s200) and (s50p <= s200p or s50 > s200),
        'goldenNow': (s50p <= s200p) and (s50 > s200),
        'momCross': e20 > e50,
        'rsiBull': r >= 50, 'volUp': vol > volavg,
    }
    sigcount = sum(1 for k in ('above20', 'above50', 'above200', 'stacked', 'golden', 'momCross', 'volUp') if sig[k])

    # SCORING MODULAIRE (elio.scoring) : technique/momentum/fondamental/risque → global + grade + verdict
    ind = {'above20': sig['above20'], 'above50': sig['above50'], 'above200': sig['above200'],
           'stacked': sig['stacked'], 'golden': sig['golden'], 'rsi': r, 'roc': roc,
           'rs': rs, 'pos52': pos, 'volx': volx, 'atr_pct': atr_pct, 'ext_atr': ext_atr}
    sc = scoring.compose(ind, fund=fund)
    score, grade, mom = sc['global'], sc['grade'], sc['momentum']
    base_score = score
    # ─── BOUCLE DE RÉTROACTION PHYSIQUE : le cerveau physique MODIFIE le score ───
    # La structure fractale/entropique du titre renforce ou tempère la conviction.
    try:
        _phys = physics.analyze(c)
    except Exception:
        _phys = None
    try:
        phys_adj, phys_adj_why = physics.score_adjust(_phys, ext_atr=ext_atr, rsi=r)
    except Exception:
        phys_adj, phys_adj_why = 0, ''
    if _phys is not None:
        _phys['adj'] = phys_adj
        _phys['adj_why'] = phys_adj_why
    # ─── CONFLUENCE MULTI-HORIZONS : la tendance hebdo (vent dominant) pèse aussi ───
    try:
        _mtf = timeframe.analyze(c, sig['above50'], sig['above200'], r)
    except Exception:
        _mtf = None
    mtf_adj = int((_mtf or {}).get('adj') or 0)
    # Ajustement structurel combiné (physique + multi-horizons), borné pour rester sain.
    struct_adj = int(max(-12, min(10, phys_adj + mtf_adj)))
    if struct_adj:
        score = int(max(0, min(100, base_score + struct_adj)))
        try:
            grade = config.grade(score)
        except Exception:
            pass
    verdict = config.verdict(score, trend, regime)

    # PLAN — stop sur STRUCTURE (dernier swing-low réel), R:R réel vers la résistance
    low = df['Low']
    Np = 10
    piv = [i for i in range(len(low) - Np - 1, max(len(low) - 60, Np), -1)
           if float(low.iloc[i]) == float(low.iloc[i - Np:i + Np + 1].min())]
    swing_low = float(low.iloc[piv[0]]) if piv else float(low.tail(20).min())
    struct_stop = swing_low - 0.25 * atr
    stop = max(struct_stop, last - 2.5 * atr)              # respecte la structure, plafonne le risque
    if last - stop < 0.8 * atr:                            # stop trop serré (bruit) → plancher ATR
        stop, stop_type = last - 1.2 * atr, 'ATR (structure trop proche)'
    else:
        stop_type = 'structure' if struct_stop > last - 2.5 * atr else 'ATR (plafond risque)'
    risk = last - stop
    recent_high = float(df['High'].tail(40).max())
    rr_res = (recent_high - last) / risk if risk > 0 else 0.0
    headroom = (recent_high - last) / atr if atr else 0.0
    setup_quality = round(float(np.clip(40 + rr_res * 20 + min(headroom, 4) * 5
                                        - max(0.0, (last - recent_high) / atr) * 15
                                        + (9 if breakout else 0)          # cassure confirmée = meilleure entrée
                                        + (6 if squeeze else 0)           # compression = coup à venir
                                        + (7 if pullback else 0)          # repli sain sur tendance = entrée à moindre risque
                                        + (5 if accumulation else 0)      # accumulation OBV = smart money qui charge
                                        - (10 if distribution else 0)     # distribution cachée = piège
                                        - (8 if not ma50_rising else 0),  # MM50 qui ne monte pas = setup fragile
                                        0, 100)))
    plan = {'entry': round(last, 2), 'stop': round(stop, 2),
            'tp1': round(last + risk, 2), 'tp2': round(last + 2 * risk, 2),
            'tp3': round(last + 3 * risk, 2), 'rr': 3.0, 'atr': round(atr, 2),
            'stop_type': stop_type, 'stop_dist_atr': round(risk / atr, 2) if atr else 0,
            'resistance': round(recent_high, 2), 'rr_res': round(rr_res, 1),
            'setup_quality': setup_quality}

    # série pour le mini-chart (120 dernières barres)
    cc = c.tail(120)
    ema20s = cc.ewm(span=20).mean()
    sma50s = c.rolling(50).mean().tail(120)
    rsi120 = rsi_s.tail(120)
    series = {
        'dates': [d.strftime('%m-%d') for d in cc.index],
        'close': [round(float(x), 2) for x in cc.values],
        'ema20': [round(float(x), 2) for x in ema20s.values],
        'sma50': [None if math.isnan(x) else round(float(x), 2) for x in sma50s.values],
        'rsi': [None if math.isnan(x) else round(float(x), 1) for x in rsi120.values],
    }
    try:
        struct = pivots.structure(df, atr)
    except Exception:
        struct = None
    result = {
        'structure': struct,
        'price': round(last, 2), 'change': round(chg, 2), 'score': score, 'grade': grade, 'verdict': verdict,
        'trend': round(trend), 'mom': round(mom), 'rs': round(rs), 'rsi': round(r),
        'roc': round(roc, 1), 'pos52': round(pos), 'sigcount': sigcount,
        'ma20': round(e20, 2), 'ma50': round(s50, 2), 'ma200': round(s200, 2),
        'volx': round(volx, 2), 'atr_pct': round(atr_pct, 2), 'ext_atr': round(ext_atr, 2),
        'regime': regime, 'adx': round(adx), 'chop': round(chop), 'rsi_div': rsi_div,
        'trend_quality': trend_quality, 'ma50_rising': ma50_rising, 'ma200_rising': ma200_rising,
        'bb_rank': bb_rank, 'squeeze': squeeze, 'breakout': breakout,
        'accumulation': accumulation, 'distribution': distribution, 'pullback': pullback,
        'profile': profile, 'profile_hint': profile_hint,
        'anomalies': anomalies, 'anomaly_score': anomaly_score, 'anomaly_lvl': anomaly_lvl,
        'gap_pct': gap_pct, 'zscore': zc, 'vol_z': vz,
        'setup_quality': setup_quality, 'confidence': sc.get('confidence'),
        'signals': sig, 'sub': sc,
        'plan': plan, 'series': series,
    }
    try:
        result['vertex'] = vertex.evaluate(result)
    except Exception:
        result['vertex'] = None
    result['physics'] = _phys                     # cerveau physique (déjà calculé + injecté dans le score)
    result['mtf'] = _mtf                           # confluence multi-horizons (journalier × hebdo)
    result['base_score'] = base_score             # score AVANT rétroaction structurelle
    result['phys_adj'] = phys_adj                 # contribution de la physique
    result['mtf_adj'] = mtf_adj                    # contribution multi-horizons
    result['struct_adj'] = struct_adj             # ajustement structurel total appliqué (transparence)
    return result


__all__ = ['analyse']
