"""vertex.observability.diagnostics — état complet du Strategy OS (§37).

Agrège : latences IBKR, files, cache, âge des données, erreurs de sources,
scans, erreurs IA/navigateur, alertes, anomalies. AUCUN secret exposé.
"""
from __future__ import annotations

from .metrics import METRICS


def system_diagnostics(scan_state: dict | None = None,
                       scheduler=None, alert_engine=None,
                       ai_audit=None, signal_store=None, ibkr_link=None,
                       option_strikes=None, magasins=None) -> dict:
    out = {'metrics': METRICS.snapshot()}
    if scan_state is not None:
        out['scan'] = {
            'rows': len(scan_state.get('rows') or []),
            'source': scan_state.get('source'),
            'options_source': scan_state.get('options_source'),
            #  Le DETAIL par contributeur, pas seulement l'etiquette agregee.
            #  « ibkr+yfinance » dit qu'il y a eu repli ; il ne dit pas sur
            #  combien de titres. Sans ce compte, un repli passant de 3 a 200
            #  symboles se lirait exactement pareil a l'ecran.
            'source_detail': scan_state.get('source_detail'),
            'last_scan_ts': scan_state.get('ts') or scan_state.get('last'),
        }
    if scheduler is not None:
        out['ibkr_scheduler'] = scheduler.status()
    #  Ou en est la decouverte de TWS : port retenu, mode (reel/papier), roles
    #  connectes, et la RAISON quand rien ne repond — sans quoi un « non
    #  connecte » n'indique aucun geste a faire.
    #  INJECTE comme les autres sections : la premiere version importait le
    #  module ici meme, ce qui faisait apparaitre la section sans qu'aucune
    #  source ne soit fournie — `test_observability` l'a refuse, et il a
    #  raison : « rien d'invente sans source » vaut aussi pour un etat vrai.
    if ibkr_link is not None:
        out['ibkr_link'] = ibkr_link.etat()
    if alert_engine is not None:
        out['alerts'] = alert_engine.status()
    if ai_audit is not None:
        out['ai'] = ai_audit.stats()
    if signal_store is not None:
        out['tradingview'] = signal_store.status()
    #  L'ECONOMIE de requetes options. Mesure du 25 aout 2026 : le produit
    #  demandait au courtier des contrats inexistants — 214 refus sur 250
    #  lignes de journal, « tout sauf les multiples de 5 ». Le correctif est
    #  invisible par construction : il se voit dans ce qui N'ARRIVE PLUS.
    #  Sans ce compteur, l'observer exigerait de comparer deux journaux du
    #  courtier a la main, et personne ne le ferait.
    #  INJECTE, comme les autres sections : la section n'apparait pas si
    #  aucune source n'est fournie (« rien d'invente sans source »).
    if option_strikes is not None:
        out['option_strikes'] = option_strikes.statistiques()
    #  Les magasins d'instantanes des routes interactives. Sans p50/p95 ni
    #  hit ratio, le budget de `AUDIT-TOTAL-2026-08-25` P0.1 — p95 chaud
    #  < 400 ms, premiere reponse froide < 1,5 s — ne serait verifiable par
    #  personne apres coup.
    #  INJECTES comme les autres sections : « rien d'invente sans source ».
    if magasins is not None:
        out['instantanes'] = [m.statistiques() for m in magasins]
    return out


def data_quality_report(packets: list | None = None) -> dict:
    """Vue /api/data-quality : qualité par symbole (paquets AnalyticsPacket.to_dict())."""
    packets = packets or []
    by_quality: dict[str, int] = {}
    worst: list = []
    for p in packets:
        q = ((p.get('quality') or {}).get('overall')) or 'MISSING'
        by_quality[q] = by_quality.get(q, 0) + 1
        if q in ('STALE', 'EXPIRED', 'MISSING'):
            worst.append({'symbol': p.get('symbol'), 'quality': q,
                          'warnings': (p.get('quality') or {}).get('warnings', [])[:3]})
    return {'total': len(packets), 'by_quality': by_quality, 'degraded': worst[:20]}
