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
from vertex.engines.market_context import regime_inputs
from vertex.market.regime_engine import classify_regime
from vertex.observability.diagnostics import data_quality_report, system_diagnostics
from vertex.portfolio import models as _pmodels
from vertex.portfolio import portfolio_guard, risk_engine, stress_tests
from vertex.portfolio.team_engine import team_view
from vertex.strategy import constitution as _constitution
from vertex.strategy import decision_packet as _decision_packet
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
        packet = _decision_packet.build(sym, detail, scan_state)
        resp = _executive.decide(packet, _profile())
        # Fraîcheur RÉELLE du scan (jamais l'heure du navigateur) — le verdict dérive de
        # scan_state['detail'], aussi vieux que le dernier scan.
        if isinstance(resp, dict):
            resp['as_of'] = scan_state.get('scan_ts_h') or scan_state.get('updated')
            resp['decision_packet'] = packet.get('decision_packet') or {}
        return jsonify(resp)

    @bp.route('/api/market/regime')
    def market_regime():
        # La clé `market` du scan est l'horloge (market_status), pas les données —
        # le mapping canonique scan → moteur vit dans market_context.regime_inputs.
        return jsonify(classify_regime(regime_inputs(scan_state)))

    @bp.route('/api/company/twin/<sym>')
    def company_twin_ep(sym):
        """Jumeau analytique entreprise (§16) — champs absents = None, jamais 0."""
        from vertex.companies import company_twin
        return jsonify(company_twin(sym, scan_state))

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
        from vertex.data_sources import ibkr_link as _lien
        return jsonify(system_diagnostics(scan_state=scan_state, ibkr_link=_lien,
                                          alert_engine=ALERTS, ai_audit=_AI_AUDIT,
                                          signal_store=SIGNAL_STORE))

    @bp.route('/api/data-quality')
    def data_quality():
        detail = scan_state.get('detail') or {}
        source = scan_state.get('source') or ''
        is_demo = (source == 'demo')
        # Démo : données synthétiques PRÉSENTES → statut DEMO honnête (≠ MISSING,
        # qui signifie « absente »). Règle d'intégrité : la démo est étiquetée,
        # jamais masquée en donnée réelle ni en absence.
        overall = 'DEMO' if is_demo else ('RECENT' if source else 'MISSING')
        warnings = ['données de démonstration (synthétiques)'] if is_demo else []
        packets = [{'symbol': s,
                    'quality': {'overall': overall, 'warnings': warnings}}
                   for s in list(detail)[:200]]
        report = data_quality_report(packets)
        report['scan_source'] = source or 'aucune'
        report['note'] = ('qualité au niveau scan (source unique) — la provenance '
                          'valeur par valeur arrive avec le routage data_sources')
        return jsonify(report)

    return bp
