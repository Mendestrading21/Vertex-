"""vertex/options/pack.py — LE PAQUET OPTIONS D'UN TITRE (#779, G1).

Tout ce qu'une fiche a besoin de savoir sur les options d'un titre : contrats
retenus, volatilité implicite et historique, contexte IV/HV, Greeks, liquidité.
Servi par `/options/<sym>` et embarqué dans `/api/ticker/<sym>`.

⛔ **Analyse seule.** Ce module lit des chaînes d'options ; il n'en prépare et
n'en transmet aucune.

## Pourquoi il vivait dans le monolithe, et pourquoi il n'y est plus

Mesuré : sur dix-huit symboles utilisés, **trois seulement** étaient locaux à
`terminal.py` — le cache `_OPTALL_CACHE` et les deux coerceurs numériques
`_i`/`_f`. Le cache a rejoint `vertex/app/caches.py`, où vivent les huit autres
caches d'exécution ; les coerceurs sont ici, avec leur unique appelant.

## Ce que `_i` et `_f` protègent

Une chaîne d'options yfinance contient des `NaN` : un strike sans cotation, un
open interest absent. `float('nan')` se propage silencieusement dans toute
arithmétique et ressort en `NaN` dans le JSON — que `JSON.parse` refuse, ce qui
donne une page blanche. Les deux coerceurs coupent la propagation à la source.

`0` plutôt que `None` est ici volontaire et local : ces deux valeurs alimentent
des agrégats (sommes d'open interest, moyennes d'IV) où un `None` ferait échouer
le calcul entier. Ce n'est **pas** un repli servi à l'écran — la fraîcheur et
l'absence sont dites ailleurs, par les champs dédiés du paquet.
"""
from __future__ import annotations

import math
import time
from datetime import datetime

import numpy as np
import yfinance as yf

from vertex.ai import briefs as ai
from vertex.app.caches import _OPTALL_CACHE
from vertex.app.state import scan_state
from vertex.data_sources import fundamentals
from vertex.engines import decide as engine
from vertex.engines import scorecard as ibkr
from vertex.options import legacy_engine as options
from vertex.research import chart_read as research
from vertex.services import news_plus as _news_plus


# ─── coerceurs numériques (voir l'en-tête : ils coupent la propagation NaN) ──
def _i(x):
    try:
        return 0 if x is None or (isinstance(x, float) and math.isnan(x)) else int(x)
    except Exception:
        return 0


def _f(x):
    try:
        return 0.0 if x is None or (isinstance(x, float) and math.isnan(x)) else float(x)
    except Exception:
        return 0.0


def options_pack(sym):
    from vertex.options import iv_hv as _iv_hv
    out = {'sym': sym, 'iv': None, 'ivrank': None, 'earnings': None, 'error': None,
           'name': None, 'sector': None, 'mcap': None, 'pe': None, 'beta': None,
           'news': [], 'news_why': None, 'contracts': [],
           'net_gex': None, 'regime': None, 'call_wall': None, 'put_wall': None, 'gamma_flip': None,
           'hv_20d': None, 'iv_hv_context': _iv_hv.describe(None, None)}
    try:
        tk = yf.Ticker(sym)
        try:
            spot = float(tk.fast_info['lastPrice'])
        except Exception:
            spot = float(tk.history(period='1d')['Close'].iloc[-1])
        out['spot'] = round(spot, 2)
        # infos société EN DIRECT (yfinance .info — lent/flaky → try)
        try:
            info = tk.info or {}
            out['name'] = info.get('shortName') or info.get('longName')
            out['sector'] = info.get('sector')
            out['mcap'] = info.get('marketCap')
            out['pe'] = info.get('trailingPE')
            out['beta'] = info.get('beta')
        except Exception:
            pass
        # comparaison fondamentale vs MÉDIANE DU SECTEUR (cache fundamentals)
        _fd = scan_state.get('fundamentals') or {}
        _fs = (_fd.get('by_sym') or {}).get(sym) or {}
        _fsec = (_fd.get('by_sector') or {}).get(_fs.get('sector') or out.get('sector')) or {}
        out['fund'] = _fs
        out['sector_median_pe'] = _fsec.get('median_pe')
        out['sector_median_margin'] = _fsec.get('median_margin')
        out['sector_median_growth'] = _fsec.get('median_growth')
        out['valuation'] = fundamentals.valuation(_fs.get('pe') or out.get('pe'), _fsec.get('median_pe'))
        # news (pourquoi ça bouge) + traduction FR live — assainies (XSS, rendu innerHTML client)
        out['news'] = options.news_for(tk)
        out['news'], out['news_why'] = ai.fr_news(sym, out['news'])
        out['news'] = _news_plus.sanitize_news(out['news'])
        # HV-rank proxy (yfinance ne donne pas l'IV-rank historique)
        h = tk.history(period='1y')['Close']
        ret = np.log(h / h.shift(1)).dropna()
        hv = ret.rolling(20).std() * math.sqrt(252) * 100
        out['hv_20d'] = round(float(hv.iloc[-1]), 2) if len(hv.dropna()) else None
        out['ivrank'] = round(float((hv.rank(pct=True).iloc[-1]) * 100)) if len(hv.dropna()) else None
        # earnings (+ jours avant résultats, pour la pénalité options court terme)
        edte = None
        try:
            cal = tk.calendar
            ed = None
            if isinstance(cal, dict):
                ed = cal.get('Earnings Date')
                ed = ed[0] if isinstance(ed, (list, tuple)) and ed else ed
            out['earnings'] = str(ed)[:10] if ed is not None else '—'
            if ed is not None:
                try:
                    edte = (datetime.strptime(str(ed)[:10], '%Y-%m-%d') - datetime.now()).days
                    edte = edte if edte >= 0 else None
                except Exception:
                    edte = None
        except Exception:
            out['earnings'] = '—'
        out['earnings_dte'] = edte
        # meilleures options CALL par bucket (court/moyen/long) pour CE titre.
        # FAST-PATH : si la rotation univers a déjà analysé ce titre (<6 h), on sert le
        # cache immédiatement (la file IBKR peut être occupée par le board → timeouts).
        _rc = _OPTALL_CACHE.get(sym) or {}
        if _rc.get('contracts') and time.time() - (_rc.get('ts') or 0) < 6 * 3600:
            out['contracts'] = _rc['contracts']
            out['contracts_cached'] = True
        else:
            screened = options.best_for_symbol(sym, spot, spot * 1.12, 'call', max_n=2,
                                               buckets=('court', 'moyen', 'long'), earnings_dte=edte,
                                               include_diagnostics=True)
            out['contracts'] = screened['contracts']
            out['option_price_rejections'] = screened['price_rejections']
            out['option_price_rejection_count'] = screened['price_rejection_count']
            if out['contracts']:                       # réchauffe la rotation au passage
                _OPTALL_CACHE[sym] = {'ts': time.time(), 'contracts': out['contracts']}
        out.setdefault('option_price_rejections', [])
        out.setdefault('option_price_rejection_count', 0)
        out['option_board_coverage'] = options.board_coverage(out['contracts'])
        out['best_pick'] = options.recommend(out['contracts'])   # LA meilleure entre les 3
        out['best_two'] = options.recommend_top(out['contracts'], 2)   # le TOP 2 des échéances (#1/#2)
        _d = scan_state['detail'].get(sym)
        out['chart_read'] = research.chart_read(_d)               # analyse graphique (texte FR)
        out['chart_verdict'] = research.chart_verdict(_d)
        out['decision'] = engine.decide(_d, out)                  # MOTEUR DE DÉCISION (synthèse)
        _fu = ((scan_state.get('fundamentals') or {}).get('by_sym') or {}).get(sym) or {}
        out['ibkr'] = ibkr.verdict(_d, out, _fu)                  # VERDICT IBKR (/40 + niveau + timing)
        # OPTIONS DESK : scénarios + breakeven + expected move sur le contrat recommandé
        if out.get('best_pick'):
            _plan = (_d or {}).get('plan') or {}
            _lv = {'stop': _plan.get('stop'), 'tp1': _plan.get('tp1'),
                   'tp2': _plan.get('tp2'), 'tp3': _plan.get('tp3')}
            out['scenarios'] = options.scenarios(out['best_pick'], spot, _lv)
            out['breakeven'] = options.breakeven_check(out['best_pick'], spot)
            _em = out['best_pick'].get('em_pct') or 0
            out['expected_move'] = {'pct': _em, 'lo': round(spot * (1 - _em / 100), 2),
                                    'hi': round(spot * (1 + _em / 100), 2)}
        # chaîne d'options → ATM IV + GEX
        exps = list(tk.options)[:2]
        lo, hi = spot * 0.9, spot * 1.1
        agg, atm_ivs = {}, []
        now = datetime.now()
        for exp in exps:
            T = max((datetime.strptime(exp, '%Y-%m-%d') - now).days, 0) / 365.0
            T = max(T, 0.5 / 365.0)
            ch = tk.option_chain(exp)
            for is_call, dfo in ((True, ch.calls), (False, ch.puts)):
                for _, row in dfo.iterrows():
                    K = _f(row['strike'])
                    if K < lo or K > hi:
                        continue
                    iv = _f(row.get('impliedVolatility')); oi = _i(row.get('openInterest'))
                    if iv <= 0 or oi <= 0:
                        continue
                    if is_call and abs(K - spot) <= spot * 0.03 and 0.03 < iv < 3.0:
                        atm_ivs.append(iv)
                    g = options.gamma(spot, K, T, iv)
                    d = agg.setdefault(K, {'cg': 0., 'pg': 0.})
                    d['cg' if is_call else 'pg'] += g * oi
        out['iv'] = round(float(np.median(atm_ivs)) * 100, 1) if atm_ivs else None
        out['iv_hv_context'] = _iv_hv.describe(out['iv'], out['hv_20d'])
        if agg:
            ks = sorted(agg)
            scale = 100.0 * spot * spot * 0.01
            gx = [(K, scale * (agg[K]['cg'] - agg[K]['pg'])) for K in ks]
            net = sum(v for _, v in gx)
            out['net_gex'] = net
            out['regime'] = 'POSITIF' if net > 0 else 'NÉGATIF'
            out['call_wall'] = round(max((k for k in ks if k >= spot), default=ks[-1],
                                         key=lambda k: agg[k]['cg']), 2)
            out['put_wall'] = round(max((k for k in ks if k <= spot), default=ks[0],
                                        key=lambda k: agg[k]['pg']), 2)
            cum, flip = 0., None
            pk = ks[0]
            for K, v in gx:
                nc = cum + v
                if flip is None and cum * nc < 0:
                    flip = pk + (K - pk) * (-cum / (nc - cum))
                pk, cum = K, nc
            out['gamma_flip'] = round(flip, 2) if flip else (out['put_wall'] if net > 0 else out['call_wall'])
    except Exception:                                         # noqa: BLE001
        #  Code stable, jamais le texte de l'exception : ce pack est SERVI par
        #  `/options/<sym>`, et `f'{type(e).__name__}: {e}'` y livrait
        #  `IndexError: single positional indexer is out-of-bounds` au client.
        out['error'] = 'options_pack_unavailable'
        out['note'] = ('chaîne d’options indisponible pour ce titre — '
                       'aucune donnée n’est inférée')
    return out


__all__ = ['options_pack']
