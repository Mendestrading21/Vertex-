"""vertex.tracking.models — modèle canonique d'un suivi (§14)."""
from __future__ import annotations

ST_ACTIVE = 'ACTIVE'
ST_STOPPED = 'STOPPED'
ST_EXPIRED = 'EXPIRED'
ST_DATA_REQUIRED = 'DATA_REQUIRED'
TRACKING_STATUSES = (ST_ACTIVE, ST_STOPPED, ST_EXPIRED, ST_DATA_REQUIRED)

ENTITY_TYPES = ('STOCK', 'ETF', 'CRYPTO', 'OPTION', 'OPPORTUNITY')

# Types de prix de référence — honnêteté : jamais l'ask silencieux.
REF_MID = 'MID'
REF_LAST = 'LAST'
REF_CLOSE = 'CLOSE'
REF_MARK = 'MARK'
REF_FALLBACK = 'FALLBACK'
REFERENCE_TYPES = (REF_MID, REF_LAST, REF_CLOSE, REF_MARK, REF_FALLBACK)


def new_tracking(tracking_id, *, entity_type, symbol, started_at,
                 reference_price=None, reference_price_type='',
                 reference_price_source='', reference_price_timestamp='',
                 reference_currency='USD', contract_id=None, benchmark='SPY',
                 strategy_decision_at_start='', strategy_score_at_start=None,
                 thesis_snapshot_id=None, data_quality=None, status=ST_ACTIVE):
    """Construit un suivi canonique. `is_hypothetical` est TOUJOURS vrai : un
    suivi n'est jamais une position réelle ni un gain encaissé."""
    et = entity_type if entity_type in ENTITY_TYPES else 'STOCK'
    st = status if status in TRACKING_STATUSES else ST_ACTIVE
    if reference_price is None:
        st = ST_DATA_REQUIRED
    return {
        'tracking_id': str(tracking_id),
        'entity_type': et,
        'entity_id': str(symbol).upper(),
        'symbol': str(symbol).upper(),
        'contract_id': contract_id,
        'started_at': started_at,
        'stopped_at': None,
        'status': st,
        'reference_price': reference_price,
        'reference_price_type': reference_price_type,
        'reference_price_source': reference_price_source,
        'reference_price_timestamp': reference_price_timestamp,
        'reference_currency': reference_currency,
        'benchmark': benchmark,
        'benchmark_reference_price': None,
        'strategy_decision_at_start': strategy_decision_at_start,
        'strategy_score_at_start': strategy_score_at_start,
        'thesis_snapshot_id': thesis_snapshot_id,
        'data_quality': data_quality or {},
        'is_hypothetical': True,
        # état vivant (mis à jour par les snapshots) — jamais un gain réel.
        'high_since': reference_price,
        'low_since': reference_price,
        'snapshots': [],
        'final': None,
    }


__all__ = [
    'new_tracking', 'TRACKING_STATUSES', 'ENTITY_TYPES', 'REFERENCE_TYPES',
    'ST_ACTIVE', 'ST_STOPPED', 'ST_EXPIRED', 'ST_DATA_REQUIRED',
    'REF_MID', 'REF_LAST', 'REF_CLOSE', 'REF_MARK', 'REF_FALLBACK',
]
