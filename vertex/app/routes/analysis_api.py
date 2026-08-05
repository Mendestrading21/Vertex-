"""
vertex/app/routes/analysis_api.py — ENDPOINTS D'ANALYSE (Blueprint, Ch. II).

Trois lectures analytiques du scan : le deep-dive VERTEX d'un titre, le
validateur hors-échantillon (walk-forward / DSR / PSR / PBO) et le Risk Manager
de portefeuille. Lisent l'état partagé (`vertex.app.state.scan_state`) — plus
d'injection : le Blueprint importe directement le même objet.

Analyse uniquement, indicatif. Ces routes lisent, ne commandent jamais.
"""

from flask import Blueprint, jsonify

from vertex.engines import quant_engine as vertex
from vertex.validation import out_of_sample as validator
from vertex.portfolio import legacy_basket_risk as portfolio_risk
from vertex.app.state import scan_state

bp = Blueprint('analysis_api', __name__)


@bp.route('/api/vertex/<sym>')
def api_vertex(sym):
    """Deep-dive VERTEX d'un titre : bloc quant complet + décomposition explicable."""
    d = (scan_state.get('detail') or {}).get(sym.upper())
    if not d:
        return jsonify({'ok': False, 'note': 'titre non scanné'})
    v = d.get('vertex')
    if not v:
        return jsonify({'ok': False, 'note': 'vertex indisponible'})
    return jsonify({'ok': True, 'symbol': sym.upper(), 'price': d.get('price'),
                    'grade': d.get('grade'), 'score': d.get('score'),
                    'vertex': v, 'explain': vertex.explain(v, d)})


@bp.route('/api/validator')
def api_validator():
    """VERTEX — validateur hors échantillon (walk-forward, DSR, PSR, PBO). Indicatif."""
    pf = scan_state.get('portfolio') or {}
    eq = pf.get('equity')
    if not eq:
        return jsonify({'ok': False, 'note': 'backtest indisponible (univers/historique insuffisant)'})
    return jsonify(validator.build(eq))


@bp.route('/api/risk')
def api_risk():
    """VERTEX v4 — Risk Manager portefeuille (corrélation, concentration, secteurs).
    Panier = top convictions du scan. Lecture seule, indicatif, aucun ordre."""
    rows = scan_state.get('rows') or []
    detail = scan_state.get('detail') or {}
    syms = [r['symbol'] for r in rows[:10]]
    return jsonify(portfolio_risk.build(syms, detail))


__all__ = ['bp']


@bp.route('/api/anomalies/<sym>')
def api_anomalies(sym):
    """SCANNER D'ANOMALIES DE COURS : spikes |z|≥2, changement de régime de
    volatilité, séquences, extrêmes — sur la série de clôtures RÉELLE du scan.
    Constat statistique descriptif, jamais une prévision. Lecture seule."""
    from vertex.data import series as _series
    from vertex.engines import anomaly as _an
    sym = (sym or '').upper()[:12]
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    closes, src = _series.closes(detail)   # série CANONIQUE uniquement (LOT 4)
    d = _an.scan(closes)
    d['symbol'] = sym
    d['series_source'] = src
    d['as_of'] = scan_state.get('scan_ts_h') or scan_state.get('updated')
    return jsonify(d)


@bp.route('/api/evidence/<sym>')
def api_evidence(sym):
    """LABORATOIRE D'ÉVIDENCE (X2) : que s'est-il RÉELLEMENT passé après les
    spikes passés — rendements forward et MFE/MAE exacts sur la série
    canonique. In-sample, descriptif, jamais un backtest. Lecture seule."""
    from vertex.data import series as _series
    from vertex.engines import evidence_lab as _ev
    sym = (sym or '').upper()[:12]
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    closes, src = _series.closes(detail)
    d = _ev.study(closes)
    d['symbol'] = sym
    d['series_source'] = src
    d['as_of'] = scan_state.get('scan_ts_h') or scan_state.get('updated')
    return jsonify(d)


@bp.route('/api/skyler/<sym>')
def api_skyler(sym):
    """SKYLER CORE (LOT 5) : packet typé + décision canonique déterministe
    (score /40, hard gates, scénarios sans probabilité inventée, audit trail).
    Analyse READONLY — jamais un ordre."""
    from vertex.data import series as _series
    from vertex.engines import anomaly as _an, events as _events
    from vertex.engines import market_context as _mcx, skyler_core as _sk
    from vertex.services import news_plus as _np
    from vertex.app.config import DEMO_MODE as _demo
    sym = (sym or '').upper()[:12]
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    closes, _src = _series.closes(detail)
    ano = _an.scan(closes) if closes else None
    market = _mcx.build(scan_state, demo=_demo)
    earnings = []
    try:
        from vertex.app.state import cal_state
        earnings = [e for e in (cal_state.get('items') or [])
                    if str(e.get('sym', '')).upper() == sym]
    except Exception:
        pass
    try:
        from vertex.data import macro_calendar
        macro = macro_calendar.events(horizon_days=30)
    except Exception:
        macro = []
    news = _np.sanitize_news(detail.get('news') or [])
    ev = _events.build(sym, news=news, earnings=earnings, macro=macro, anomaly=ano,
                       as_of=scan_state.get('scan_ts_h') or scan_state.get('updated'))
    as_of = scan_state.get('scan_ts_h') or scan_state.get('updated')
    # OptionsContext (LOT 6) : meilleur candidat LEAPS du board réel, mandat étiqueté.
    from vertex.options import horizon_scanners as _hs
    octx = _hs.options_context(_hs.scan(scan_state.get('options_board') or [],
                                        'LEAPS', sym=sym))
    # PortfolioContext (LOT 7) : positions canoniques du desk + cotes du scan.
    pctx = None
    try:
        from vertex.engines import portfolio_context as _pc
        from vertex.positions.repository import load_positions
        from vertex.services import persist
        pos = load_positions(persist.load_json('desk_data.json', {}) or {})
        quotes = {s: (d or {}).get('price') for s, d in (scan_state.get('detail') or {}).items()
                  if isinstance(d, dict) and d.get('price') is not None}
        pctx = _pc.build(pos, quotes=quotes, sym=sym)
    except Exception:
        pctx = None
    # Red-team PRODUITE (LOT 14) : les 10 questions du comité évaluées sur le
    # packet réel — complete=True seulement si les 10 sont fondées.
    from vertex.engines import red_team as _rt
    packet0 = _sk.build_packet(sym, detail, market=market, events=ev, anomaly=ano,
                               as_of=as_of, demo=_demo, options_ctx=octx, portfolio_ctx=pctx)
    rt_review = _rt.review(packet0, _sk.score40(packet0))
    rt_input = {'complete': rt_review['complete'], 'basis': rt_review['basis']}
    decision = _sk.decide(sym, detail, market=market, events=ev, anomaly=ano,
                          as_of=as_of, demo=_demo, options_ctx=octx, portfolio_ctx=pctx,
                          red_team=rt_input)
    packet = _sk.build_packet(sym, detail, market=market, events=ev, anomaly=ano,
                              as_of=as_of, demo=_demo, options_ctx=octx, portfolio_ctx=pctx,
                              red_team=rt_input)
    # Journal de calibration (LOT 9) : chaque décision servie est enregistrée
    # (dédupliquée par scan) avec le prix du moment — base des résultats ex post.
    try:
        import time as _time
        from vertex.engines import skyler_journal as _sj
        from vertex.services import persist as _persist
        j = _persist.load_json(_sj.JOURNAL_FILE, [])
        j2 = _sj.record(j, decision, price=detail.get('price'), now=round(_time.time()))
        if j2 != j:
            _persist.save_json(_sj.JOURNAL_FILE, j2)
    except Exception:
        pass                                   # le journal ne casse jamais la décision
    # Mémoire décisionnelle institutionnelle (LOT 10) : chaque décision servie
    # est FIGÉE avec sa version de moteur, ses données du moment et l'empreinte
    # de série anti-look-ahead — append-only, jamais réécrite.
    try:
        import time as _time
        from vertex.engines import decision_memory as _dm
        from vertex.services import persist as _persist
        today = _time.strftime('%Y-%m-%d', _time.gmtime())   # date d'observation réelle (UTC)
        mem = _persist.load_json(_dm.MEMORY_FILE, None) or _dm.empty_memory()
        rec = _dm.freeze(decision, packet=packet, price=detail.get('price'),
                         closes=closes, portfolio_ctx=pctx, now=round(_time.time()),
                         session_date=today)
        mem2 = _dm.append_decision(mem, rec)
        if mem2 != mem:
            _persist.save_json(_dm.MEMORY_FILE, mem2)
        # Log de séances (LOT 15) : une clôture observée par jour réel de scan.
        from vertex.engines import session_log as _slog
        if detail.get('price') is not None:
            slog = _persist.load_json(_slog.SESSIONS_FILE, None) or _slog.empty_log()
            slog2 = _slog.record_close(slog, sym, today, detail.get('price'))
            if slog2 != slog:
                _persist.save_json(_slog.SESSIONS_FILE, slog2)
    except Exception:
        pass                                   # la mémoire ne casse jamais la décision
    return jsonify({'symbol': sym, 'as_of': as_of, 'demo': _demo,
                    'packet': packet, 'decision': decision,
                    'red_team_review': rt_review})


@bp.route('/api/skyler/sweep')
def api_skyler_sweep():
    """BALAYAGE SKYLER (X1) : le moteur canonique appliqué à tous les titres
    scannés, classé par score /40 — gate plafonnante visible par ligne.
    Ne journalise jamais. Lecture seule."""
    from vertex.app.config import DEMO_MODE as _demo
    from vertex.engines import skyler_sweep as _sw
    earnings_by_sym = {}
    try:
        from vertex.app.state import cal_state
        for e in (cal_state.get('items') or []):
            s = str(e.get('sym', '')).upper()
            if s:
                earnings_by_sym.setdefault(s, []).append(e)
    except Exception:
        pass
    return jsonify(_sw.sweep(scan_state, demo=_demo, earnings_by_sym=earnings_by_sym))


@bp.route('/api/skyler/calibration')
def api_skyler_calibration():
    """CALIBRATION EX POST (LOT 9) : comptages exacts du journal des décisions +
    rendements réels depuis le prix enregistré. Brier honnêtement indisponible
    tant qu'aucune probabilité calibrée n'existe. Lecture seule."""
    from vertex.engines import skyler_journal as _sj
    from vertex.services import persist as _persist
    journal = _persist.load_json(_sj.JOURNAL_FILE, [])
    quotes = {s: (d or {}).get('price') for s, d in (scan_state.get('detail') or {}).items()
              if isinstance(d, dict) and d.get('price') is not None}
    out = _sj.calibration(journal, quotes=quotes)
    out['as_of'] = scan_state.get('scan_ts_h') or scan_state.get('updated')
    from vertex.app.config import DEMO_MODE as _demo
    out['demo'] = _demo
    return jsonify(out)


@bp.route('/api/skyler/memory')
def api_skyler_memory():
    """MÉMOIRE DÉCISIONNELLE INSTITUTIONNELLE (LOT 10) : décisions figées
    (immuables, séparées par version de moteur), résultats mesurés UNIQUEMENT
    aux horizons déclarés depuis les séances strictement postérieures (aucun
    look-ahead), classification déterministe des erreurs, biais récurrents et
    recommandations en attente de validation humaine. Lecture seule."""
    from vertex.data import series as _series
    from vertex.engines import decision_memory as _dm
    from vertex.services import persist as _persist
    from vertex.app.config import DEMO_MODE as _demo
    mem = _persist.load_json(_dm.MEMORY_FILE, None) or _dm.empty_memory()
    # Passe de mesure (LOT 15) : le log de séances DATÉES est autoritaire quand
    # il couvre le titre (comptage de séances réel) ; l'empreinte de fin de
    # série reste le secours pour les anciens records. Non mesurable = dit.
    from vertex.engines import session_log as _slog
    slog = _persist.load_json(_slog.SESSIONS_FILE, None)
    changed = False
    detail_all = scan_state.get('detail') or {}
    for r in mem['decisions']:
        after = _slog.closes_after_date(slog, r.get('symbol'), r.get('session_date'))
        if after is None:                      # log muet sur ce titre → secours empreinte
            closes, _src = _series.closes(detail_all.get(r.get('symbol')) or {})
            after = _dm.sessions_after(closes, r.get('tail_at_decision'))
        if after:
            mem2 = _dm.append_outcome(mem, _dm.measure(r, after))
            if mem2 != mem:
                mem, changed = mem2, True
    if changed:
        try:
            _persist.save_json(_dm.MEMORY_FILE, mem)
        except Exception:
            pass
    patterns = _dm.detect_patterns(mem)
    aggs = _dm.aggregates(mem)
    return jsonify({
        'generator': 'deterministic',
        'as_of': scan_state.get('scan_ts_h') or scan_state.get('updated'),
        'demo': _demo,
        'n_decisions': len(mem['decisions']),
        'n_outcomes': len(mem['outcomes']),
        'decisions': mem['decisions'][-50:],
        'outcomes': mem['outcomes'][-50:],
        'aggregates': aggs,
        'patterns': patterns,
        'recommendations': _dm.recommendations(patterns, aggs),
        'note': 'Mémoire immuable — décisions historiques jamais réécrites, résultats '
                'séparés par version de moteur, aucune recalibration automatique.',
    })


def _kg_build():
    """Assemble le Knowledge Graph depuis les sources réelles de l'état partagé :
    univers scanné, watchlist sectorielle statique, séries canoniques, calendrier
    earnings/macro, positions desk. Aucune relation inventée."""
    from vertex.data import series as _series
    from vertex.engines import knowledge_graph as _kg
    from vertex.market.sectors import SECTOR_MAP
    from vertex.app.config import DEMO_MODE as _demo
    detail_all = scan_state.get('detail') or {}
    symbols = sorted(detail_all.keys())
    closes_by_sym = {}
    for s in symbols:
        closes, _src = _series.closes(detail_all.get(s) or {})
        if closes:
            closes_by_sym[s] = closes
    events_by_sym = {}
    try:
        from vertex.app.state import cal_state
        for e in (cal_state.get('items') or []):
            s = str(e.get('sym', '')).upper()
            if s and e.get('dte') is not None:
                events_by_sym.setdefault(s, []).append(
                    {'kind': 'earnings', 'label': 'Résultats %s' % s,
                     'dte': e.get('dte'), 'source': 'calendar.earnings'})
    except Exception:
        pass
    positions = None
    try:
        from vertex.positions.repository import load_positions
        from vertex.services import persist
        positions = load_positions(persist.load_json('desk_data.json', {}) or {})
    except Exception:
        positions = None
    return _kg.build(symbols, sector_map=SECTOR_MAP, closes_by_sym=closes_by_sym,
                     events_by_sym=events_by_sym, positions=positions,
                     as_of=scan_state.get('scan_ts_h') or scan_state.get('updated'),
                     demo=_demo)


@bp.route('/api/skyler/graph')
def api_skyler_graph():
    """KNOWLEDGE GRAPH INSTITUTIONNEL (LOT 11) : sociétés, secteurs, catalyseurs
    et portefeuille reliés uniquement par des sources réelles tracées — chaque
    arête porte provenance et niveau de preuve ; dépendances cachées (≥ 2 liens
    indépendants) et questions de recherche (relations non documentées, jamais
    inventées). Lecture seule."""
    return jsonify(_kg_build())


@bp.route('/api/skyler/graph/<sym>')
def api_skyler_graph_sym(sym):
    """PROPAGATION D'IMPACT EXPLICABLE (LOT 11) : chemins depuis un titre,
    chaque saut justifié par la relation et la base de l'arête. Lecture seule."""
    from vertex.engines import knowledge_graph as _kg
    sym = (sym or '').upper()[:12]
    g = _kg_build()
    return jsonify({'symbol': sym, 'generator': 'deterministic',
                    'as_of': g['as_of'], 'demo': g['demo'],
                    'engine_version': g['engine_version'],
                    'paths': _kg.propagate(g, 'company:%s' % sym, max_hops=2),
                    'hidden_dependencies': [d for d in g['hidden_dependencies']
                                            if sym in d['symbols']],
                    'research_questions': [q for q in g['research_questions']
                                           if q['symbol'] == sym]})


@bp.route('/api/events/<sym>')
def api_events(sym):
    """TIMELINE D'ÉVÉNEMENTS NORMALISÉE (SKYLER LOT 4) : news assainies et
    dédupliquées, earnings/macro du calendrier réel, anomalies statistiques —
    faits distingués des interprétations, impact suggéré par mots-clés
    transparents seulement. Lecture seule."""
    from vertex.data import series as _series
    from vertex.engines import anomaly as _an, events as _events
    from vertex.services import news_plus as _np
    sym = (sym or '').upper()[:12]
    detail = (scan_state.get('detail') or {}).get(sym) or {}
    closes, _src = _series.closes(detail)
    ano = _an.scan(closes) if closes else None
    earnings = []
    try:
        from vertex.app.state import cal_state
        earnings = [e for e in (cal_state.get('items') or [])
                    if str(e.get('sym', '')).upper() == sym]
    except Exception:
        earnings = []
    macro = []
    try:
        from vertex.data import macro_calendar
        macro = macro_calendar.events(horizon_days=30)
    except Exception:
        macro = []
    # XSS : titres externes assainis AU POINT DE SORTIE (rendus innerHTML client).
    news = _np.sanitize_news(detail.get('news') or [])
    d = _events.build(sym, news=news, earnings=earnings, macro=macro, anomaly=ano,
                      as_of=scan_state.get('scan_ts_h') or scan_state.get('updated'))
    d['demo'] = bool(scan_state.get('source') == 'demo')
    return jsonify(d)
