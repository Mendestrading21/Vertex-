"""vertex.observability.diagnostics — état complet du Strategy OS (§37).

Agrège : latences IBKR, files, cache, âge des données, erreurs de sources,
scans, erreurs IA/navigateur, alertes, anomalies. AUCUN secret exposé.
"""
from __future__ import annotations

from .metrics import METRICS


def system_diagnostics(scan_state: dict | None = None,
                       scheduler=None, alert_engine=None,
                       ai_audit=None, signal_store=None) -> dict:
    out = {'metrics': METRICS.snapshot()}
    if scan_state is not None:
        out['scan'] = {
            'rows': len(scan_state.get('rows') or []),
            'source': scan_state.get('source'),
            'options_source': scan_state.get('options_source'),
            'last_scan_ts': scan_state.get('ts') or scan_state.get('last'),
        }
    if scheduler is not None:
        out['ibkr_scheduler'] = scheduler.status()
    if alert_engine is not None:
        out['alerts'] = alert_engine.status()
    if ai_audit is not None:
        out['ai'] = ai_audit.stats()
    if signal_store is not None:
        out['tradingview'] = signal_store.status()
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
