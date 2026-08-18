"""vertex/engines/skyler_sweep.py — BALAYAGE SKYLER DE L'UNIVERS (X1).

Applique le moteur canonique `skyler_core.decide` à TOUS les titres scannés et
classe par score /40. Le MarketContext est calculé UNE fois et partagé (même
photo de marché pour tout le classement). Chaque ligne porte la décision, le
niveau, la gate plafonnante (VISIBLE dans le classement — jamais masquée), le
catalyseur daté le plus proche et l'invalidation réelle.

Invariants : déterministe (mêmes entrées → même classement, tri secondaire par
symbole) ; vide honnête ; ne journalise JAMAIS (le journal de calibration ne
s'alimente que sur consultation individuelle d'une fiche) ; le contexte
portefeuille est volontairement omis (classement d'univers, pas d'étude de
candidat — dit dans la note). Lecture seule, aucun ordre.
"""
from __future__ import annotations


def sweep(scan_state, demo=False, limit=50, earnings_by_sym=None):
    """Classement Skyler de tous les titres du scan. `earnings_by_sym` optionnel
    ({SYM: [items cal]}) — absent = catalyseurs earnings simplement omis."""
    from vertex.data import series as _series
    from vertex.engines import anomaly_context as _anctx, events as _events
    from vertex.engines import market_context as _mcx, skyler_core as _sk
    from vertex.engines import decision_evidence as _evidence
    from vertex.options import horizon_scanners as _hs
    from vertex.services import news_plus as _np

    scan_state = scan_state or {}
    detail_map = scan_state.get('detail') or {}
    as_of = scan_state.get('scan_ts_h') or scan_state.get('updated')
    if not detail_map:
        return {'n': 0, 'rows': [], 'as_of': as_of, 'market_regime': None,
                'generator': 'deterministic',
                'reason': 'aucun titre scanné — classement indisponible'}

    market = _mcx.build(scan_state, demo=demo)
    board = scan_state.get('options_board') or []
    earnings_by_sym = earnings_by_sym or {}

    rows = []
    for sym in sorted(detail_map):
        det = detail_map.get(sym) or {}
        if not isinstance(det, dict) or det.get('score') is None:
            continue                       # pas de dossier technique → pas de ligne inventée
        closes, _src = _series.closes(det)
        ano = _anctx.build(sym, det, benchmark_detail=detail_map.get('SPY') or {}) if closes else None
        ev = _events.build(sym, news=_np.sanitize_news(det.get('news') or []),
                           earnings=earnings_by_sym.get(sym, []), macro=None,
                           anomaly=ano, as_of=as_of)
        octx = _hs.swing_3_6m_context(board, sym=sym)
        dqctx, recctx = _evidence.for_symbol(scan_state, sym, det)
        d = _sk.decide(sym, det, market=market, events=ev, anomaly=ano,
                       as_of=as_of, demo=demo, options_ctx=octx,
                       data_quality_ctx=dqctx, reconciliation_ctx=recctx)
        sc = d.get('score') or {}
        rows.append({
            'symbol': sym,
            'decision': d.get('decision'),
            'score_total': sc.get('total'),
            'level': d.get('level'),
            'capped_by_gate': d.get('capped_by_gate'),
            'catalyst': d.get('catalyst'),
            'invalidation': d.get('invalidation'),
            'max_risk_pct': d.get('max_risk_pct'),
            'insufficient_blocks': len(sc.get('insufficient_blocks') or []),
        })

    rows.sort(key=lambda r: (-(r['score_total'] or 0), r['symbol']))
    return {
        'n': len(rows), 'rows': rows[:limit], 'as_of': as_of,
        'market_regime': (market.get('regime') or {}).get('label'),
        'demo': bool(demo), 'generator': 'deterministic',
        'note': 'Classement analytique par le moteur canonique — contexte options Swing 3–6M '
                'et contexte portefeuille omis (étude de candidat sur la fiche Analyse) ; '
                'un score ne déclenche jamais un ordre.',
    }


__all__ = ['sweep']
