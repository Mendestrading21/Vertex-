"""
vertex/app/routes/decision_api.py — API DÉCISION (Blueprint, Ch. II).

Expose la DecisionStack par HTTP : décision d'un titre, Morning Brief, et
Committee Review. Premier groupe de routes sorti du monolithe en Blueprint.

L'état partagé (`scan_state`, mode démo) est INJECTÉ à l'enregistrement —
`scan_state` est le même objet dict muté en place par la boucle de scan, donc
les routes voient toujours les données fraîches. Logique déplacée verbatim.

Analyse uniquement. Aucune exécution — ces routes lisent, ne commandent rien.
"""

import time

from flask import Blueprint, jsonify

from vertex.engines import decision_stack as _decision
from vertex.engines import context as _context


def make_blueprint(*, scan_state, demo_mode):
    """Construit le Blueprint API-décision en fermant sur l'état partagé injecté."""
    bp = Blueprint('decision_api', __name__)

    def _scan_age():
        return round(time.time() - scan_state['scan_ts']) if scan_state.get('scan_ts') else None

    def _best_option_for(sym):
        """Meilleur CALL du board pour un titre (véhicule DecisionStack). None si absent."""
        calls = [c for c in (scan_state.get('options_board') or [])
                 if c.get('sym') == sym and c.get('type') == 'CALL' and c.get('quality') is not None]
        if not calls:
            return None
        return max(calls, key=lambda c: c.get('quality', 0))

    def _market_ctx():
        """Contexte marché normalisé pour la DecisionStack (source unique)."""
        mctx = scan_state.get('market_ctx') or {}
        return {'roro': mctx.get('roro'), 'spy_regime': mctx.get('spy_regime'),
                'vix_band': mctx.get('vix_band')}

    def _ctx_for(sym):
        return _context.context_for(sym, scan_state.get('detail') or {})

    def _brief_row(sym, market, scan_age):
        """Une ligne du brief : la décision du comité pour un titre, condensée."""
        detail = dict((scan_state.get('detail') or {}).get(sym) or {})
        detail.setdefault('symbol', sym)
        r = _decision.evaluate(detail, symbol=sym, market=market, option=_best_option_for(sym),
                               scan_age_s=scan_age, demo=demo_mode, context=_ctx_for(sym))
        com = r.get('committee') or {}
        return {
            'symbol': sym, 'decision': r['final_decision'], 'label': r['decision_label'],
            'tone': r['decision_tone'], 'confidence': r['confidence'], 'conviction': r['conviction'],
            'view': com.get('view'), 'agreement': com.get('agreement'),
            'has_contradiction': com.get('has_contradiction', False),
            'devils_advocate': com.get('devils_advocate'),
            'top_pro': (r.get('pros') or [None])[0], 'top_con': (r.get('cons') or [None])[0],
            'price': detail.get('price'),
        }

    def _top_symbols(limit):
        rows = sorted((scan_state.get('rows') or []),
                      key=lambda x: (x.get('score') or 0), reverse=True)
        syms, seen = [], set()
        for x in rows:
            s = x.get('symbol')
            if s and s not in seen:
                seen.add(s)
                syms.append(s)
            if len(syms) >= limit:
                break
        return syms, seen

    @bp.route('/api/decision/<sym>')
    def decision_ep(sym):
        """LA DÉCISION STACK — vérité unique, explicable, par titre. Analyse uniquement."""
        sym = sym.upper()
        detail = dict((scan_state.get('detail') or {}).get(sym) or {})
        detail.setdefault('symbol', sym)
        return jsonify(_decision.evaluate(
            detail, symbol=sym, market=_market_ctx(), option=_best_option_for(sym),
            scan_age_s=_scan_age(), demo=demo_mode, context=_ctx_for(sym)))

    @bp.route('/api/brief')
    def brief_ep():
        """🌅 MORNING BRIEF — le comité passe en revue les meilleurs setups du jour (Ch. XIX)."""
        market, scan_age = _market_ctx(), _scan_age()
        syms, _ = _top_symbols(8)
        briefs = [_brief_row(s, market, scan_age) for s in syms]
        buyish = [b for b in briefs if b['decision'] in ('STRONG_BUY', 'BUY', 'BUY_PULLBACK')]
        watch = [b for b in briefs if b['decision'] in ('WATCH_BREAKOUT', 'WAIT', 'TOO_LATE')]
        avoid = [b for b in briefs if b['decision'] in ('AVOID', 'NO_NEW_RISK')]
        contradictions = [b for b in briefs if b['has_contradiction']]
        mctx = scan_state.get('market_ctx') or {}
        return jsonify({
            'as_of': scan_state.get('scan_ts_h') or scan_state.get('updated'),
            'scan_age': scan_age, 'data_source': 'demo' if demo_mode else 'scan',
            'market': {'roro': mctx.get('roro'), 'spy_regime': mctx.get('spy_regime'),
                       'vix_band': mctx.get('vix_band'), 'breadth': mctx.get('breadth')},
            'setups': briefs,
            'counts': {'buy': len(buyish), 'watch': len(watch), 'avoid': len(avoid),
                       'contradictions': len(contradictions)},
            'contradictions': contradictions,
        })

    @bp.route('/api/committee-review')
    def committee_review_ep():
        """🧠 COMMITTEE REVIEW — le comité passe TOUT l'univers scanné en revue (Ch. XIX)."""
        market, scan_age = _market_ctx(), _scan_age()
        syms, seen = _top_symbols(60)          # borne dure, journalisée côté UI
        reviews = [_brief_row(s, market, scan_age) for s in syms]
        tally = {}
        for b in reviews:
            tally[b['decision']] = tally.get(b['decision'], 0) + 1
        mctx = scan_state.get('market_ctx') or {}
        return jsonify({
            'as_of': scan_state.get('scan_ts_h') or scan_state.get('updated'),
            'scan_age': scan_age, 'data_source': 'demo' if demo_mode else 'scan',
            'market': {'roro': mctx.get('roro'), 'spy_regime': mctx.get('spy_regime'),
                       'vix_band': mctx.get('vix_band')},
            'count': len(reviews), 'capped_at': 60, 'universe_scanned': len(seen),
            'tally': tally, 'reviews': reviews,
        })

    return bp


__all__ = ['make_blueprint']
