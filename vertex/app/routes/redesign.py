"""vertex/app/routes/redesign.py — routes du Vertex Master Redesign (§10-11).

Huit espaces + fiche canonique + redirections des anciennes routes (avec
conservation du ticker, de la vue et des filtres). Strangler pattern : le
monolithe garde ses APIs, ses pages HTML legacy sont remplacées ici.
"""
from __future__ import annotations

from pathlib import Path

from flask import Blueprint, jsonify, redirect, request, send_from_directory

from vertex.ui.pages import (analysis_page, briefing, intelligence_page,
                             markets_page, opportunities_page, options_intel_page,
                             performance_page, portfolio_page, system_page,
                             tracking_page)

# Anciennes routes → nouvelles destinations (§11). Jamais de suppression sèche.
LEGACY_REDIRECTS = {
    '/daily': '/',
    '/analyse': '/analysis',
    '/news': '/',
    '/calendar': '/opportunities?view=calendar',
    '/semaine': '/markets',
    '/brief': '/',
    '/stocks': '/analysis',
    '/compare': '/analysis?view=compare',
    '/comparateur': '/analysis?view=compare',
    '/entreprises': '/analysis',
    '/analyse-entreprise': '/analysis',
    '/strategie': '/portfolio',
    '/strategy': '/portfolio',
    '/ma-page': '/portfolio?view=watchlist',
    '/moi': '/portfolio?view=watchlist',
    '/watchlist': '/portfolio?view=watchlist',
    '/suivi': '/portfolio?view=watchlist',
    '/suivis': '/portfolio?view=watchlist',
    '/options-lab': '/opportunities?view=options',
    '/options-desk': '/opportunities?view=options',
    '/sectors': '/markets?view=sectors',
    '/heatmap': '/markets?view=sectors',
    '/catalysts': '/opportunities?view=calendar',
    '/catalyseurs': '/opportunities?view=calendar',
    '/anomalies': '/opportunities?view=anomalies',
    '/journal': '/performance?view=journal',
    '/decisions': '/performance?view=journal',
    '/review': '/intelligence?view=committee',
    '/research': '/intelligence?view=research',
    '/equipe': '/intelligence?view=strategy',
    '/equipe-du-mois': '/intelligence?view=strategy',
    '/bordel': '/intelligence',
    '/strategy-os': '/intelligence?view=strategy',
    '/vertex-intelligence': '/intelligence?view=analyst',
    '/health': '/system?view=data',
    '/settings': '/system?view=settings',
    '/parametres': '/system?view=settings',
    '/vault': '/system?view=archive',
    '/archive': '/system?view=archive',
}


VX_STATIC_DIR = Path(__file__).resolve().parents[2] / 'static' / 'vertex'


def make_blueprint(scan_state: dict) -> Blueprint:
    bp = Blueprint('redesign', __name__)

    # Les assets du redesign vivent dans vertex/static/vertex/** (architecture
    # cible §9) ; le dossier statique Flask historique reste static/ à la
    # racine. Cette règle, plus spécifique que /static/<path>, sert le
    # sous-arbre vertex/.
    @bp.route('/static/vertex/<path:filename>')
    def vx_static(filename):
        resp = send_from_directory(VX_STATIC_DIR, filename)
        resp.cache_control.max_age = 3600
        return resp

    # ── Espaces principaux ────────────────────────────────────────────
    @bp.route('/')
    def briefing_route():
        return briefing.render(scan_state=scan_state)

    @bp.route('/markets')
    def markets_route():
        return markets_page.render(view=request.args.get('view', 'overview'))

    @bp.route('/opportunities')
    def opportunities_route():
        return opportunities_page.render(view=request.args.get('view', 'radar'),
                                         params=request.args)

    @bp.route('/portfolio')
    def portfolio_route():
        return portfolio_page.render(view=request.args.get('view', 'team'))

    @bp.route('/analysis')
    def analysis_index_route():
        return analysis_page.render_index(view=request.args.get('view', ''))

    @bp.route('/analysis/<sym>')
    def analysis_route(sym):
        return analysis_page.render(sym.upper())

    @bp.route('/performance')
    def performance_route():
        return performance_page.render(view=request.args.get('view', 'overview'),
                                       params=request.args)

    @bp.route('/intelligence')
    def intelligence_route():
        return intelligence_page.render(view=request.args.get('view', 'analyst'))

    @bp.route('/system')
    def system_route():
        return system_page.render(view=request.args.get('view', 'connections'))

    # ── Options Intelligence (§18) — approfondissement d'Opportunités.
    # PAS un 9e espace : le nav reste à huit, cette page se rejoint depuis
    # Opportunités (vue Options), Analyse et la palette.
    @bp.route('/options')
    def options_intel_route():
        return options_intel_page.render(view=request.args.get('view', 'overview'))

    # ── Suivis (§14-18) — approfondissement du Portefeuille, pas un 9e espace.
    @bp.route('/tracking')
    def tracking_route():
        return tracking_page.render()

    # ── Brief éditorial (§21) : paquet structuré → 10 lignes ─────────
    @bp.route('/api/briefing/editorial')
    def briefing_editorial():
        base = briefing.build_editorial(scan_state)
        # Brief quotidien §15 (PRE_MARKET/INTRADAY/CLOSE/WEEKLY) : sections
        # sourcées + actualités RÉELLES validées (news_state) — fusionné sans
        # casser le schéma historique (lines/word_count/...).
        try:
            from vertex.app.state import news_state
            from vertex.market.daily_brief import build_daily_brief
            from vertex.services import persist as _persist
            desk = _persist.load_json('desk_data.json', {}) or {}
            import json as _json
            raw = (desk.get('data') or {}).get('myTrades')
            trades = _json.loads(raw) if isinstance(raw, str) else (raw or [])
            syms = sorted({str(t.get('sym', '')).upper() for t in trades
                           if isinstance(t, dict) and t.get('sym')})
            daily = build_daily_brief(scan_state, news_state, syms)
            base.update({'daily': daily, 'kind': daily['kind'],
                         'sources': daily['sources'],
                         'what_changed_today': daily['what_changed'],
                         'main_risk': daily['main_risk'],
                         'main_opportunity': daily['main_opportunity']})
        except Exception as e:
            base['daily_error'] = str(e)[:120]
        # Brief éditorial narratif (§10) — texte fluide de séance, sourcé, jamais
        # de fait d'actualité inventé. Fusionné sans casser le schéma historique.
        try:
            from vertex.app.state import news_state
            from vertex.market.editorial import build_narrative
            base['editorial'] = build_narrative(scan_state, news_state)
        except Exception as e:
            base['editorial_error'] = str(e)[:120]
        return jsonify(base)

    # ── Simulation d'un contrat (moteur scenario_pricer — §35) ───────
    @bp.route('/api/options/simulate')
    def options_simulate():
        from vertex.options import scenario_pricer
        from vertex.options.models import UnderlyingSetup
        a = request.args
        sym = (a.get('sym') or '').upper()
        detail = (scan_state.get('detail') or {}).get(sym) or {}
        plan = detail.get('plan') or {}
        try:
            spot = float(a.get('spot') or detail.get('price') or 0)
            contract = {
                'symbol': sym, 'right': (a.get('right') or 'C')[:1].upper(),
                'strike': float(a.get('strike')), 'dte': int(a.get('dte') or 0),
                'mid': float(a.get('mid')) if a.get('mid') else None,
                'iv': float(a.get('iv')) if a.get('iv') else None,
                'expiry': a.get('exp') or '',
            }
        except (TypeError, ValueError):
            return jsonify({'error': 'paramètres invalides (sym, strike, dte, mid requis)'}), 400
        if spot <= 0:
            return jsonify({'error': f'{sym}: spot indisponible — simulation refusée '
                                     '(aucune donnée inventée)'}), 422
        notes = []
        # Normalisations documentées : le board historique exprime l'IV en %
        # et le coût en dollars PAR CONTRAT (prime × 100).
        if contract['iv'] and contract['iv'] > 3:
            contract['iv'] = round(contract['iv'] / 100.0, 4)
            notes.append('IV convertie de % en décimal')
        if contract['mid'] and spot and contract['mid'] > spot:
            contract['mid'] = round(contract['mid'] / 100.0, 4)
            notes.append('prime par contrat convertie en prime par action (÷100)')
        setup = UnderlyingSetup(
            symbol=sym, spot=spot,
            invalidation=plan.get('stop'), tp1=plan.get('tp1'),
            tp2=plan.get('tp2'), tp3=plan.get('tp3'))
        try:
            sim = scenario_pricer.simulate(contract, setup)
            analysis = scenario_pricer.capital_free_analysis(sim, contract)
        except Exception as exc:
            return jsonify({'error': f'simulation impossible: {exc}'}), 422
        sim['limitations'] = list(sim.get('limitations') or []) + notes
        return jsonify({'symbol': sym, 'contract': contract, 'sim': sim,
                        'capital_free': analysis})

    # ── Redirections legacy (conservation ticker/vue/filtres) ────────
    def _legacy(target):
        def _view(**kwargs):
            dest = target
            extra = request.query_string.decode()
            if extra:
                dest += ('&' if '?' in dest else '?') + extra
            return redirect(dest, code=301)
        return _view

    for old, new in LEGACY_REDIRECTS.items():
        bp.add_url_rule(old, endpoint=f'legacy_{old.strip("/").replace("-", "_").replace("/", "_")}',
                        view_func=_legacy(new))

    @bp.route('/titre/<sym>')
    @bp.route('/company/<sym>')
    def legacy_titre(sym):
        return redirect(f'/analysis/{sym.upper()}', code=301)

    return bp
