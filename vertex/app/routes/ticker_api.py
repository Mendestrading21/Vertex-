"""vertex/app/routes/ticker_api.py — LA FICHE D'UN TITRE (#779, G1).

- `/options/<sym>`    — le paquet options seul ;
- `/api/ticker/<sym>` — la fiche complète : détail du scan, entreprise, pairs,
  médianes sectorielles, carte des risques, et le paquet options.

⛔ **Analyse seule.** Ces deux routes lisent et comparent ; elles ne préparent
ni ne transmettent aucun ordre.

## La comparaison aux pairs ne fabrique rien

Chaque pair est cherché **dans le cache seul** (`allow_fetch=False`) : ouvrir
une fiche déclencherait sinon quatre appels réseau supplémentaires, et un
throttle sur le titre principal. Un pair absent du cache sort avec ses champs à
`None` — une case vide, jamais une valeur devinée depuis le secteur.

## Chaque bloc a son propre `try`, et c'est délibéré

Le paquet options, la fiche entreprise, les médianes et la carte des risques
échouent **indépendamment**. Un `try` global ferait disparaître la fiche entière
parce que yfinance n'a pas répondu sur une chaîne d'options — alors que le
détail du scan, lui, était disponible. Chaque zone dit son absence sans
emporter les autres.
"""
from __future__ import annotations

from flask import Blueprint, jsonify

from vertex.app.config import DEMO_MODE
from vertex.app.state import scan_state
from vertex.data import company as _company
from vertex.data.universe import UNIVERSE
from vertex.options.pack import options_pack

bp = Blueprint('ticker_api', __name__)

#: Pairs comparés sur la fiche. Au-delà, la table devient illisible et chaque
#: ligne coûte une lecture de cache.
MAX_PAIRS = 4


@bp.route('/options/<sym>')
def opt_ep(sym):
    return jsonify(options_pack(sym.upper()))


@bp.route('/api/ticker/<sym>')
def api_ticker(sym):
    sym = sym.upper()
    try:
        pack = options_pack(sym)
    except Exception as e:
        pack = {'sym': sym, 'error': '%s: %s' % (type(e).__name__, e),
                'contracts': []}
    try:
        comp = _company.get(sym, demo=DEMO_MODE, brief=True)
    except Exception:
        comp = None
    #  Comparaison aux pairs : VRAIES données (scan live + cache entreprise),
    #  zéro invention.
    det_all = scan_state.get('detail') or {}
    peers_data = []
    for p in ((comp or {}).get('peers') or [])[:MAX_PAIRS]:
        pd = det_all.get(p) or {}
        try:
            pc = _company.get(p, demo=DEMO_MODE, allow_fetch=False)   # cache seul → rapide
        except Exception:
            pc = {}
        pf = (pc or {}).get('fundamentals') or {}
        peers_data.append({'symbol': p, 'name': (pc or {}).get('name'),
                           'score': pd.get('score'), 'verdict': pd.get('verdict'),
                           'perf_q': pd.get('perf_q'), 'rev_growth': pf.get('rev_growth'),
                           'margin': pf.get('margin'), 'pe': pf.get('pe'),
                           'roe': pf.get('roe')})
    try:
        _sec_med = _company.sector_medians().get((comp or {}).get('sector')) or {}
    except Exception:
        _sec_med = {}
    #  Carte des risques d'entreprise — depuis fondamentaux réels + médianes.
    try:
        from vertex.company import risk_map as _risk_map
        _det = det_all.get(sym) or {}
        _risk = _risk_map.build(comp, sector_median=_sec_med,
                                earnings_in_days=_det.get('earnings_dte'))
    except Exception:
        _risk = None
    return jsonify({'symbol': sym, 'in_universe': sym in UNIVERSE,
                    'detail': det_all.get(sym), 'peers_data': peers_data,
                    'company': comp, 'pack': pack, 'sector_median': _sec_med,
                    'risk_map': _risk})


__all__ = ['bp', 'MAX_PAIRS']
