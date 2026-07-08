"""
vertex/app/routes/command.py — COMMAND CENTER (Blueprint, Ch. II).

Les deux vues de commandement : /api/command (régime, top actions/options,
alertes du risk manager, décision du jour, exposition) et /api/portefeuille
(portefeuille d'options construit sur un capital donné).

Les moteurs (risk manager, validateur, stratégie options) viennent d'`elio` —
modules purs, sans Flask ; l'état partagé vient de `vertex.app.state`.

Machine de décision — lecture seule, aucun ordre. Logique déplacée verbatim.
"""

from flask import Blueprint, jsonify, request

from elio import portfolio_risk, strategy, validator
from vertex.app.state import scan_state
from vertex.engines import market_lens

bp = Blueprint('command', __name__)

CAPITAL_MIN = 5_000
CAPITAL_MAX = 1_000_000
CAPITAL_DEFAULT = 100_000


def _market_score(mc):
    """Score marché /100 — source unique dans vertex/engines/market_lens.climate()."""
    cl = market_lens.climate(mc)
    return cl['score'] if cl else None


@bp.route('/api/command')
def api_command():
    """VERTEX COMMAND CENTER : consolide régime, top actions/options, alertes,
    décision du jour, exposition. Machine de décision — lecture seule, aucun ordre."""
    mc = scan_state.get('market_ctx') or {}
    cm = scan_state.get('committee') or {}
    st = scan_state.get('strategy') or {}
    detail = scan_state.get('detail') or {}
    score = _market_score(mc)
    reg, roro = mc.get('spy_regime'), mc.get('roro')
    # régime final
    if roro == 'RISK-OFF':
        regime = {'label': '🔴 RISK-OFF', 'color': '#EF4444'}
    elif roro == 'RISK-ON' and reg != 'CHOP':
        regime = {'label': '🟢 RISK-ON', 'color': '#22C55E'}
    else:
        regime = {'label': '🟡 NEUTRE', 'color': '#FFB23F'}
    regime.update({'score': score, 'spy_regime': reg, 'roro': roro})
    # top 5 actions (comité actionnable) + bloc VERTEX (edge probabiliste)
    decisions = cm.get('decisions') or []

    def _vtx(sym):
        v = (detail.get(sym) or {}).get('vertex') or {}
        mc2 = v.get('mc') or {}
        return {'verdict': v.get('verdict'), 'edge': v.get('edge'),
                'p_win': (v.get('ml') or {}).get('p_win'),
                'p_tp1': mc2.get('p_hit_tp1'), 'edge_bps': mc2.get('edge_mean_bps'),
                'no_trade': v.get('no_trade')}
    top_stocks = [{'symbol': d['symbol'], 'verdict': d['verdict'], 'color': d['color'],
                   'conviction': d['conviction'], 'price': d['price'],
                   'rr': (d.get('plan') or {}).get('rr'), 'note': d['note'],
                   'vertex': _vtx(d['symbol'])}
                  for d in decisions if d['verdict'] in ('ACHETER', 'RENFORCER')][:5]
    # top 5 options (meilleure échéance 6 mois)
    top_options = []
    for p in (st.get('picks') or [])[:5]:
        d = p.get('primary', 'CALL')
        legs = (p.get('put') if d == 'PUT' else p.get('call')) or []
        leg = next((l for l in legs if l.get('key') == 'm6'), legs[0] if legs else None)
        if leg:
            sc = leg.get('scenarios') or {}
            top_options.append({'symbol': p['symbol'], 'dir': d, 'label': leg['label'],
                                'strike': leg['strike'], 'premium': leg['premium'],
                                'prob': (sc.get('prob') or {}).get('pct'),
                                'except': (sc.get('except') or {}).get('pct')})
    # alertes rouges (risk manager, niveau marché)
    alerts = []
    if roro == 'RISK-OFF':
        alerts.append(['🔴', 'RISK-OFF', "Marché risk-off — réduire l'exposition, pas de nouveau pari agressif."])
    if reg == 'CHOP':
        alerts.append(['🟠', 'RANGE', 'Marché sans tendance (chop) — les cassures échouent, patience.'])
    vix = mc.get('vix')
    if vix and vix > 22:
        alerts.append(['🟠', 'VOLATILITÉ', f'VIX {round(vix)} élevé — options chères, dimensionner petit.'])
    overext = sum(1 for dd in detail.values() if (dd.get('ext_atr') or 0) >= 3)
    if overext >= 5:
        alerts.append(['🟠', 'EUPHORIE', f'{overext} titres très étendus — ne pas chasser, attendre les replis.'])
    # décision du jour
    n_act = len(top_stocks)
    if roro == 'RISK-OFF' or reg == 'CHOP':
        decision = {'action': 'RÉDUIRE / DÉFENSIF', 'color': '#EF4444',
                    'msg': 'Préserver le capital : cash + couvertures. On n\'attaque pas.'}
    elif n_act >= 2 and (score or 0) >= 55:
        decision = {'action': 'ATTAQUER', 'color': '#22C55E',
                    'msg': f'{n_act} setups validés en marché porteur — déployer avec discipline (R:R ≥ 2:1).'}
    else:
        decision = {'action': 'ATTENDRE / SÉLECTIF', 'color': '#FFB23F',
                    'msg': 'Peu d\'avantage statistique — n\'acheter que l\'exceptionnel, garder du cash.'}
    # RISK MANAGER portefeuille (corrélation / concentration / secteurs)
    try:
        risk = portfolio_risk.build([r['symbol'] for r in (cm.get('decisions') or [])
                                     if r['verdict'] in ('ACHETER', 'RENFORCER')][:8] or
                                    [r['symbol'] for r in (scan_state.get('rows') or [])[:8]],
                                    detail)
    except Exception:
        risk = None
    if risk and risk.get('no_new_risk'):
        if 'correlation_panier_elevee' in risk.get('flags', []):
            alerts.append(['🟠', 'CORRÉLATION', f"Panier trop corrélé ({risk['avg_corr']}) — diversifier avant d'ajouter du risque."])
        if 'concentration_sectorielle' in risk.get('flags', []):
            alerts.append(['🟠', 'CONCENTRATION', f"Secteur {risk.get('max_sector_name')} à {risk.get('max_sector')}% — trop concentré."])
    try:
        valid = validator.build((scan_state.get('portfolio') or {}).get('equity') or [])
    except Exception:
        valid = None
    return jsonify({'regime': regime, 'portfolio_score': score, 'decision': decision,
                    'top_stocks': top_stocks, 'top_options': top_options, 'alerts': alerts,
                    'counts': cm.get('counts') or {}, 'risk': risk, 'validation': valid,
                    'exposure': {'actions': '70-90%', 'options': '10-20%', 'etf': 'tampon / cash'}})


@bp.route('/api/portefeuille')
def api_portefeuille():
    """Portefeuille d'options construit sur un capital (50k/100k/200k…). Analyse only."""
    try:
        cap = int(float(request.args.get('capital', CAPITAL_DEFAULT)))
    except Exception:
        cap = CAPITAL_DEFAULT
    cap = max(CAPITAL_MIN, min(cap, CAPITAL_MAX))
    rows = scan_state.get('rows')
    if not rows:
        return jsonify({})
    try:
        return jsonify(strategy.build_portfolio(rows, scan_state.get('detail'),
                                                market=scan_state.get('market_ctx'), capital=cap))
    except Exception as e:
        return jsonify({'error': f'{type(e).__name__}: {e}'})


__all__ = ['bp']
