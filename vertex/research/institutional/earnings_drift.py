"""vertex.research.institutional.earnings_drift — PEAD et event-driven (§23)."""
from __future__ import annotations


def post_earnings_drift_signal(reaction_day1_pct: float | None,
                               surprise_pct: float | None,
                               days_since_earnings: int | None,
                               drift_since_pct: float | None = None) -> dict:
    """Post-Earnings Announcement Drift : information de contexte, pas un trade."""
    out = {'signal': None, 'strength': 0.0, 'notes': []}
    if None in (reaction_day1_pct, days_since_earnings):
        out['notes'].append('données de réaction earnings manquantes')
        return out
    if not (1 <= days_since_earnings <= 45):
        out['notes'].append('hors fenêtre PEAD (1-45 séances)')
        return out
    aligned = surprise_pct is None or (surprise_pct * reaction_day1_pct) >= 0
    if reaction_day1_pct >= 4 and aligned:
        out['signal'] = 'PEAD_UP'
        out['strength'] = min(1.0, reaction_day1_pct / 10)
        if drift_since_pct is not None and drift_since_pct < 0:
            out['strength'] *= 0.5
            out['notes'].append('drift entamé à contre-sens — signal affaibli')
    elif reaction_day1_pct <= -4 and aligned:
        out['signal'] = 'PEAD_DOWN'
        out['strength'] = min(1.0, abs(reaction_day1_pct) / 10)
    else:
        out['notes'].append('réaction initiale trop faible ou incohérente avec la surprise')
    return out


def event_signals(events: dict) -> list[dict]:
    """events : {'guidance_change_pct', 'analyst_revisions_30d', 'product_launch_in_days',
    'investor_day_in_days', 'regulatory_decision_in_days', 'macro_sensitive'}"""
    out = []
    g = events.get('guidance_change_pct')
    if g is not None and abs(g) >= 5:
        out.append({'type': 'GUIDANCE_REVISION', 'direction': 'UP' if g > 0 else 'DOWN',
                    'magnitude': abs(g)})
    rev = events.get('analyst_revisions_30d')
    if rev is not None and rev >= 4:
        out.append({'type': 'ANALYST_REVISION_CLUSTER', 'count': rev})
    for key, etype in (('product_launch_in_days', 'PRODUCT_LAUNCH'),
                       ('investor_day_in_days', 'INVESTOR_DAY'),
                       ('regulatory_decision_in_days', 'REGULATORY_DECISION')):
        d = events.get(key)
        if d is not None and 0 <= d <= 30:
            out.append({'type': etype, 'in_days': d})
    if events.get('macro_sensitive'):
        out.append({'type': 'MACRO_SENSITIVE_EVENT'})
    return out
