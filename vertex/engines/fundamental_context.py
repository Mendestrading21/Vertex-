"""Contexte fondamental descriptif issu du scan, sans imputation."""
from __future__ import annotations


def build(symbol, fundamentals):
    data = (fundamentals or {}).get('by_sym') or {}
    row = data.get(str(symbol).upper()) or {}
    if not row:
        return {'available': False, 'reason': 'fondamentaux par titre indisponibles', 'read_only': True}
    sector = row.get('sector')
    peers = ((fundamentals or {}).get('by_sector') or {}).get(sector) or {}
    fields = ('pe', 'fwd_pe', 'pb', 'peg', 'margin', 'growth', 'beta', 'mcap', 'div', 'roe', 'debt_eq')
    values = {key: row.get(key) for key in fields}
    missing = [key for key, value in values.items() if value is None]
    return {'available': True, 'read_only': True, 'source': 'scan.fundamentals',
            'sector': sector, 'industry': row.get('industry'), 'values': values,
            'sector_medians': peers or None, 'missing_fields': missing,
            'note': 'fondamentaux yfinance potentiellement différés ; champs absents non imputés'}
