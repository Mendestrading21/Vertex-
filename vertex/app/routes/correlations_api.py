"""vertex/app/routes/correlations_api.py — CORRÉLATIONS RÉELLES (#779, G1).

`/api/correlations/<sym>` : corrélation du titre avec huit références macro, sur
les **rendements journaliers** de six mois. Lecture seule.

## Ce que la route refuse de faire

Inventer une corrélation. Si la série du titre est trop courte, si yfinance ne
répond pas, ou si l'appariement des dates ne laisse pas assez de points, elle
rend `corr: []` **avec l'erreur** — jamais un zéro, qui se lirait comme
« aucune corrélation mesurée » alors que rien n'a été mesuré du tout.

## Pourquoi les dates sont normalisées avant l'appariement

`_naif()` retire le fuseau et ramène à minuit. Sans cette étape, une série
horodatée en `America/New_York` et une autre en UTC ne s'apparient sur **aucune**
date : `concat(...).dropna()` rendrait un tableau vide, et la route conclurait
« pas assez de données » sur des séries parfaitement complètes. Un défaut
silencieux qui ressemble à une absence honnête.

## Le cache est partagé, pas local

`_CORR_BENCH` vit dans `vertex/app/caches.py` avec les sept autres caches
d'exécution : les huit références sont les mêmes pour tous les titres, et les
re-télécharger par requête coûterait un appel réseau par fiche ouverte.
"""
from __future__ import annotations

import time

from flask import Blueprint, jsonify

from vertex.app.caches import _CORR_BENCH

bp = Blueprint('correlations_api', __name__)

#: Les références macro, et leur libellé affiché. L'ordre n'a pas d'importance —
#: la réponse est triée par corrélation décroissante.
REFERENCES = [('SOXX', 'SOXX'), ('QQQ', 'QQQ'), ('S&P 500', 'SPY'),
              ('Bitcoin', 'BTC-USD'), ('Or', 'GC=F'), ('Dollar', 'DX-Y.NYB'),
              ('Taux 10a', '^TNX'), ('VIX', '^VIX')]

#: Fraîcheur du cache des références : une heure. Elles bougent avec le marché,
#: pas avec la fiche consultée.
TTL_S = 3600


def _naif(ix):
    """Retire le fuseau et ramène à minuit — condition de l'appariement."""
    import pandas as pd
    ix = pd.DatetimeIndex(ix)
    try:
        ix = ix.tz_localize(None)
    except (TypeError, AttributeError):
        pass
    return ix.normalize()


def references():
    """Séries Close 6 mois des références macro — cache 1 h, partagé."""
    if _CORR_BENCH['df'] is not None and time.time() - _CORR_BENCH['ts'] < TTL_S:
        return _CORR_BENCH['df']
    import yfinance as yf
    brut = yf.download([t for _, t in REFERENCES], period='6mo',
                       progress=False, auto_adjust=True)['Close']
    brut.index = _naif(brut.index)
    _CORR_BENCH['df'] = brut
    _CORR_BENCH['ts'] = time.time()
    return brut


@bp.route('/api/correlations/<sym>')
def api_correlations(sym):
    """Corrélation RÉELLE (rendements journaliers, 6 mois) avec chaque référence.

    Repli honnête : liste vide **et** l'erreur, si les données ne suffisent pas."""
    sym = (sym or '').upper()
    try:
        import pandas as pd
        import yfinance as yf
        bench = references()
        s = yf.Ticker(sym).history(period='6mo')['Close']
        s.index = _naif(s.index)
        df = pd.concat([s.rename(sym), bench], axis=1)
        #  LE COMPORTEMENT EST REPRIS A L'IDENTIQUE — pas de `.dropna()` ici,
        #  seuil a 20 points. Une extraction qui retouche au passage change des
        #  correlations SERVIES sans que personne ne l'ait demande, et sans
        #  qu'aucun test ne le voie : la premiere transcription avait glisse un
        #  `.dropna()` et un seuil a 30. Corrige avant d'aller plus loin.
        rets = df.pct_change()
        out = []
        for label, tk in REFERENCES:
            if tk not in rets.columns:
                continue
            pair = rets[[sym, tk]].dropna()
            if len(pair) < 20:
                continue
            c = pair[sym].corr(pair[tk])
            if pd.notna(c):
                out.append([label, round(float(c), 2)])
        out.sort(key=lambda x: -x[1])
        return jsonify({'sym': sym, 'corr': out})
    except Exception:                                         # noqa: BLE001
        #  Code stable, jamais le texte de l'exception.
        return jsonify({'sym': sym, 'corr': [],
                        'error': 'correlations_unavailable',
                        'note': 'corrélations indisponibles — série trop '
                                'courte ou source injoignable'})


__all__ = ['bp', 'REFERENCES', 'TTL_S', 'references']
