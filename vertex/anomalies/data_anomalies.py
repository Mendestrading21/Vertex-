"""vertex.anomalies.data_anomalies — anomalies de DONNÉES (§15).

Vérifie l'intégrité de ce qu'on s'apprête à analyser : une donnée douteuse
vaut moins qu'une donnée absente. Les anomalies bloquantes interdisent
ACTIONABLE en aval.
"""
from __future__ import annotations

import datetime as _dt

from .models import Anomaly, SEV_INFO, SEV_WARN, SEV_BLOCK
from vertex.data_sources.provenance import parse_iso

STALE_AFTER_S = 3600          # cotation intrajournalière sans mise à jour
FROZEN_TICKS = 20             # N valeurs strictement identiques consécutives
DELAYED_AFTER_S = 900         # marqué différé au-delà de 15 min en mode LIVE


def _anom(code, severity, confidence, source, observed, expected, impact, blocking=False):
    return Anomaly(code=code, severity=severity, confidence=confidence, source=source,
                   observed=observed, expected=expected, impact=impact, blocking=blocking)


def check_quote(quote: dict, now: _dt.datetime | None = None) -> list[Anomaly]:
    """quote: {'source','price','bid','ask','timestamp','mode'}"""
    out: list[Anomaly] = []
    src = quote.get('source', '')
    now = now or _dt.datetime.now(_dt.timezone.utc)
    price = quote.get('price')
    if price is not None:
        if price < 0:
            out.append(_anom('NEGATIVE_PRICE', SEV_BLOCK, 0.99, src,
                             {'price': price}, {'price': '> 0'},
                             'prix négatif — donnée corrompue', blocking=True))
        elif price == 0:
            out.append(_anom('ZERO_PRICE', SEV_BLOCK, 0.95, src,
                             {'price': 0}, {'price': '> 0'},
                             'prix nul — donnée corrompue ou instrument mort', blocking=True))
    ts = parse_iso(quote.get('timestamp', ''))
    if ts is not None:
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=_dt.timezone.utc)
        age = (now - ts).total_seconds()
        if age > STALE_AFTER_S:
            out.append(_anom('STALE_DATA', SEV_BLOCK, 0.9, src,
                             {'age_seconds': int(age)}, {'age_seconds': f'<= {STALE_AFTER_S}'},
                             'cotation rassise — décision interdite dessus', blocking=True))
        elif quote.get('mode') == 'LIVE' and age > DELAYED_AFTER_S:
            out.append(_anom('DELAYED_DATA', SEV_WARN, 0.7, src,
                             {'age_seconds': int(age)}, {'age_seconds': f'<= {DELAYED_AFTER_S}'},
                             'source déclarée LIVE mais en retard — traiter comme différée'))
    bid, ask = quote.get('bid'), quote.get('ask')
    if bid is not None and ask is not None and bid > 0 and ask > 0:
        if bid > ask:
            out.append(_anom('CROSSED_MARKET', SEV_BLOCK, 0.95, src,
                             {'bid': bid, 'ask': ask}, {'bid': '<= ask'},
                             'marché croisé — cotation non fiable', blocking=True))
        elif bid == ask:
            out.append(_anom('LOCKED_MARKET', SEV_WARN, 0.8, src,
                             {'bid': bid, 'ask': ask}, {'bid': '< ask'},
                             'marché verrouillé — liquidité anormale'))
    return out


def check_bars(bars: list[dict], source: str = '') -> list[Anomaly]:
    """bars quotidiennes triées par date: [{'date','open','high','low','close','volume'}…]"""
    out: list[Anomaly] = []
    if not bars:
        return out
    seen_dates: dict[str, int] = {}
    prev_date = None
    frozen_run = 1
    for i, b in enumerate(bars):
        d = str(b.get('date') or '')
        o, h, l, c = b.get('open'), b.get('high'), b.get('low'), b.get('close')
        if None not in (o, h, l, c):
            if not (l <= o <= h and l <= c <= h and l <= h):
                out.append(_anom('IMPOSSIBLE_OHLC', SEV_BLOCK, 0.95, source,
                                 {'date': d, 'ohlc': [o, h, l, c]},
                                 {'rule': 'low <= open,close <= high'},
                                 'barre incohérente — historique non fiable', blocking=True))
            if min(o, h, l, c) <= 0:
                out.append(_anom('ZERO_PRICE' if min(o, h, l, c) == 0 else 'NEGATIVE_PRICE',
                                 SEV_BLOCK, 0.95, source, {'date': d},
                                 {'prices': '> 0'}, 'prix nul/négatif dans l’historique',
                                 blocking=True))
        if d:
            seen_dates[d] = seen_dates.get(d, 0) + 1
            if prev_date is not None and d < prev_date:
                out.append(_anom('OUT_OF_ORDER_BARS', SEV_WARN, 0.9, source,
                                 {'date': d, 'after': prev_date}, {'order': 'croissant'},
                                 'barres désordonnées — re-trier avant analyse'))
            prev_date = d
        if i > 0 and c is not None and bars[i - 1].get('close') == c \
                and b.get('volume') == bars[i - 1].get('volume'):
            frozen_run += 1
        else:
            frozen_run = 1
        if frozen_run == FROZEN_TICKS:
            out.append(_anom('FROZEN_DATA', SEV_WARN, 0.7, source,
                             {'identical_bars': frozen_run, 'until': d},
                             {'identical_bars': f'< {FROZEN_TICKS}'},
                             'série figée — flux probablement gelé'))
    dups = {d: n for d, n in seen_dates.items() if n > 1}
    if dups:
        out.append(_anom('DUPLICATE_BARS', SEV_WARN, 0.9, source,
                         {'dates': sorted(dups)[:5]}, {'duplicates': 0},
                         'barres dupliquées — dédupliquer avant indicateurs'))
    # Trous : jours ouvrés manquants (approximation lun-ven)
    dates = sorted(x for x in seen_dates if len(x) == 10)
    missing = 0
    for a, b2 in zip(dates, dates[1:]):
        try:
            da = _dt.date.fromisoformat(a)
            db = _dt.date.fromisoformat(b2)
        except ValueError:
            continue
        gap = sum(1 for k in range(1, (db - da).days)
                  if (da + _dt.timedelta(days=k)).weekday() < 5)
        missing += gap
    if missing > 2:
        out.append(_anom('MISSING_BARS', SEV_WARN, 0.6, source,
                         {'missing_business_days': missing}, {'missing_business_days': '<= 2'},
                         'historique troué — indicateurs faussés (jours fériés non modélisés)'))
    return out


def check_option_quote(q: dict, source: str = '') -> list[Anomaly]:
    """Anomalies de données sur UNE cotation d'option (bid/ask/timestamps)."""
    out: list[Anomaly] = []
    bid, ask = q.get('bid'), q.get('ask')
    if bid is not None and ask is not None and bid > 0 and 0 < ask < bid:
        out.append(_anom('BID_ABOVE_ASK', SEV_BLOCK, 0.95, source,
                         {'bid': bid, 'ask': ask}, {'bid': '<= ask'},
                         'cotation option croisée — contrat inutilisable', blocking=True))
    return out


def check_cross_source(symbol: str, reconciliation_report) -> list[Anomaly]:
    """Traduit un rapport de réconciliation (§13) en anomalies standard."""
    mapping = {'SOURCE_DISAGREEMENT': 'SOURCE_DISAGREEMENT',
               'TIMESTAMP_MISMATCH': 'TIMESTAMP_MISMATCH',
               'SPLIT_MISMATCH': 'SPLIT_MISMATCH',
               'CURRENCY_MISMATCH': 'CURRENCY_MISMATCH',
               'MULTIPLIER_MISMATCH': 'MULTIPLIER_MISMATCH',
               'CONTRACT_MAPPING_ERROR': 'CONTRACT_MAPPING_ERROR',
               'BID_ABOVE_ASK': 'BID_ABOVE_ASK',
               'EARNINGS_DATE_DIVERGENCE': 'TIMESTAMP_MISMATCH'}
    out = []
    for inc in reconciliation_report.inconsistencies:
        code = mapping.get(inc.code, inc.code)
        out.append(_anom(code, inc.severity, 0.8, symbol, inc.observed, {},
                         inc.detail, blocking=inc.severity >= 3))
    return out
