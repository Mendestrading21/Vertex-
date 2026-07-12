"""vertex/app/routes/strategy_os_api.py — API du Vertex Strategy OS (Ch. §36-37).

Expose les nouveaux moteurs : constitution, décision exécutive unique, régime
de marché, anomalies, équipe, diagnostics, qualité de données, alertes.
Lecture seule — aucune route n'écrit ailleurs que dans la mémoire stratégique
(propositions) et rien ne peut toucher un ordre.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request

from vertex.alerts.engine import AlertEngine
from vertex.anomalies.stock_anomalies import detect_stock_anomalies
from vertex.ai.audit import AUDIT as _AI_AUDIT
from vertex.data_sources.tradingview_signal_store import SIGNAL_STORE
from vertex.market.regime_engine import classify_regime
from vertex.observability.diagnostics import data_quality_report, system_diagnostics
from vertex.portfolio import models as _pmodels
from vertex.portfolio import portfolio_guard, risk_engine, stress_tests
from vertex.portfolio.team_engine import team_view
from vertex.strategy import constitution as _constitution
from vertex.strategy import executive_engine as _executive

ALERTS = AlertEngine()


def make_blueprint(scan_state: dict) -> Blueprint:
    bp = Blueprint('strategy_os', __name__)

    def _profile():
        return _constitution.load_profile()

    @bp.route('/api/strategy/profile')
    def strategy_profile():
        p = _profile()
        return jsonify({'strategy_id': p.strategy_id, 'display_name': p.display_name,
                        'version': p.version, 'style': p.style,
                        'versions_available': _constitution.list_versions(),
                        'profile': p.raw})

    @bp.route('/api/strategy/decision/<sym>')
    def strategy_decision(sym):
        sym = sym.upper()
        detail = (scan_state.get('detail') or {}).get(sym) or {}
        if not detail:
            # 200 + available:false : état applicatif honnête (pas une erreur
            # transport) — un 404 pollue la console navigateur à chaque fiche.
            return jsonify({'available': False,
                            'error': f'{sym} absent du scan courant',
                            'final_decision': 'ATTENDRE',
                            'reason': 'aucune donnée — impossible de décider'}), 200
        plan = detail.get('plan') or {}
        source = scan_state.get('source') or ''
        packet = {
            'symbol': sym,
            'fundamental': {'score': detail.get('st_fund') or detail.get('fund_score')},
            'catalysts': {'score': 60 if detail.get('earnings_dte') is not None else None},
            'technical': {'score': detail.get('score'),
                          'reward_risk': detail.get('rr') or (plan.get('rr') if isinstance(plan, dict) else None),
                          'timing_score': detail.get('st_timing'),
                          'overextended': (detail.get('ext_atr') or 0) >= 2.5},
            'sentiment': {'score': detail.get('rs')},
            'anomalies': [],
            'data_quality': {'overall': 'RECENT' if source and source != 'demo' else 'MISSING',
                             'actionable_allowed': bool(source and source != 'demo')},
            'reconciliation': {'actionable_allowed': True},
            'guard': {'blocking_rules': [], 'mandatory_reviews': []},
        }
        try:
            market = scan_state.get('market') or {}
            inputs = {'index_trend': {'TREND': 'UP', 'CHOP': 'FLAT'}.get(market.get('regime'),
                                                                         market.get('spy_trend')),
                      'breadth_pct': market.get('breadth'), 'vix': market.get('vix')}
            packet['market_regime'] = classify_regime(inputs)
        except Exception:
            packet['market_regime'] = {}
        return jsonify(_executive.decide(packet, _profile()))

    @bp.route('/api/market/regime')
    def market_regime():
        market = scan_state.get('market') or {}
        inputs = {
            'index_trend': {'TREND': 'UP', 'CHOP': 'FLAT'}.get(market.get('regime'),
                                                               market.get('spy_trend')),
            'breadth_pct': market.get('breadth'),
            'vix': market.get('vix'),
            'leadership': ('CYCLICAL' if market.get('risk') == 'Risk-On'
                           else 'DEFENSIVE' if market.get('risk') == 'Risk-Off' else None),
        }
        return jsonify(classify_regime(inputs))

    @bp.route('/api/anomalies/<sym>')
    def anomalies_for(sym):
        sym = sym.upper()
        detail = (scan_state.get('detail') or {}).get(sym) or {}
        series = detail.get('series') or {}
        closes = series.get('close') or []
        bars = [{'date': '', 'open': c, 'high': c, 'low': c, 'close': c,
                 'volume': None} for c in closes]
        found = detect_stock_anomalies(sym, bars) if len(bars) >= 30 else []
        return jsonify({'symbol': sym,
                        'anomalies': [a.to_dict() for a in found],
                        'note': ('série close-only du scan : gaps/volumes non couverts '
                                 'sur cette route' if bars else 'aucune série disponible')})

    @bp.route('/api/portfolio/team', methods=['GET', 'POST'])
    def portfolio_team():
        """GET : message d'usage. POST : positions EXPLICITES {positions:[...], cash}."""
        if request.method == 'GET':
            return jsonify({'usage': 'POST {positions: [{symbol, quantity, avg_cost, '
                                     'last_price, sector, beta}], cash, peak_equity, '
                                     'simulated: bool} — le risque ne se calcule que sur '
                                     'des positions réelles ou simulées explicites'})
        body = request.get_json(silent=True) or {}
        positions = [_pmodels.Position(
            symbol=str(p.get('symbol', '')).upper(), quantity=float(p.get('quantity') or 0),
            avg_cost=p.get('avg_cost'), last_price=p.get('last_price'),
            sector=p.get('sector', ''), beta=p.get('beta'),
            sec_type=p.get('sec_type', 'STK')) for p in body.get('positions') or []]
        cash = float(body.get('cash') or 0)
        peak = body.get('peak_equity')
        if body.get('simulated'):
            snap = _pmodels.simulated(positions, cash=cash, peak_equity=peak)
        else:
            snap = _pmodels.PortfolioSnapshot(positions=positions, cash=cash,
                                              provenance='REAL', peak_equity=peak)
        profile = _profile()
        risk = risk_engine.portfolio_risk(snap, profile)
        return jsonify({'team': team_view(snap, profile), 'risk': risk,
                        'guard': portfolio_guard.guard_rules(risk, profile),
                        'stress': stress_tests.run_stress_tests(snap, profile)})

    @bp.route('/api/alerts/active')
    def alerts_active():
        return jsonify({'active': ALERTS.active_alerts(), 'status': ALERTS.status()})

    @bp.route('/api/system/diagnostics')
    def diagnostics():
        return jsonify(system_diagnostics(scan_state=scan_state,
                                          alert_engine=ALERTS, ai_audit=_AI_AUDIT,
                                          signal_store=SIGNAL_STORE))

    @bp.route('/api/data-quality')
    def data_quality():
        detail = scan_state.get('detail') or {}
        source = scan_state.get('source') or ''
        packets = [{'symbol': s,
                    'quality': {'overall': 'RECENT' if source and source != 'demo'
                                else 'MISSING',
                                'warnings': []}} for s in list(detail)[:200]]
        report = data_quality_report(packets)
        report['scan_source'] = source or 'aucune'
        report['note'] = ('qualité au niveau scan (source unique) — la provenance '
                          'valeur par valeur arrive avec le routage data_sources')
        return jsonify(report)

    return bp
