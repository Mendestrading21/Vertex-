"""vertex.catalysts.event_engine — catalyseurs non-earnings (§21, §23 event-driven)."""
from __future__ import annotations

EVENT_TYPES = (
    'EARNINGS', 'GUIDANCE_REVISION', 'ANALYST_REVISION_CLUSTER', 'PRODUCT_LAUNCH',
    'INVESTOR_DAY', 'REGULATORY_DECISION', 'MACRO_SENSITIVE_EVENT', 'DIVIDEND',
    'SPLIT', 'INDEX_INCLUSION', 'OTHER',
)


def classify_events(events: list[dict]) -> dict:
    """events: [{'type','date','days_until','confirmed','description'}…]

    Sépare confirmé / non confirmé — un événement non confirmé ne peut pas
    justifier un mode earnings ni un hold-through.
    """
    confirmed, unconfirmed, unknown_type = [], [], []
    for e in events or []:
        etype = (e.get('type') or 'OTHER').upper()
        entry = {'type': etype if etype in EVENT_TYPES else 'OTHER',
                 'date': e.get('date'), 'days_until': e.get('days_until'),
                 'description': e.get('description', '')}
        if etype not in EVENT_TYPES:
            unknown_type.append(etype)
        (confirmed if e.get('confirmed') else unconfirmed).append(entry)
    horizon = [e for e in confirmed
               if e.get('days_until') is not None and 0 <= e['days_until'] <= 30]
    return {'confirmed': confirmed, 'unconfirmed': unconfirmed,
            'within_30d': sorted(horizon, key=lambda e: e['days_until']),
            'unknown_types': unknown_type,
            'has_near_catalyst': bool(horizon)}


def catalyst_summary(events: list[dict], earnings_in_days: int | None = None) -> dict:
    cls = classify_events(events)
    out = {'has_catalyst': cls['has_near_catalyst'] or (
        earnings_in_days is not None and 0 <= earnings_in_days <= 45),
        'next_events': cls['within_30d'][:3],
        'earnings_in_days': earnings_in_days,
        'warnings': []}
    if cls['unconfirmed']:
        out['warnings'].append(f"{len(cls['unconfirmed'])} événement(s) non confirmé(s) — "
                               'jamais utilisés pour tenir une position à travers un événement')
    return out
