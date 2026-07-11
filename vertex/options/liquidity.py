"""vertex.options.liquidity — évaluation de liquidité d'un contrat."""
from __future__ import annotations

MIN_OPEN_INTEREST = 200
MIN_VOLUME = 10
MAX_SPREAD_PCT = 10.0
GOOD_SPREAD_PCT = 4.0


def assess(contract: dict) -> dict:
    """Retourne {'score': 0..100, 'tradeable': bool, 'issues': [...]}."""
    issues: list[str] = []
    score = 100.0
    bid, ask, mid = contract.get('bid'), contract.get('ask'), contract.get('mid')
    oi, vol = contract.get('open_interest'), contract.get('volume')

    if not bid or not ask or bid <= 0 or ask <= 0:
        return {'score': 0.0, 'tradeable': False,
                'issues': ['bid/ask absent — contrat non traitable']}
    spread_pct = (ask - bid) / mid * 100 if mid else 100.0
    if spread_pct > MAX_SPREAD_PCT:
        issues.append(f'spread {spread_pct:.1f}% > {MAX_SPREAD_PCT}%')
        score -= 45
    elif spread_pct > GOOD_SPREAD_PCT:
        score -= (spread_pct - GOOD_SPREAD_PCT) / (MAX_SPREAD_PCT - GOOD_SPREAD_PCT) * 25
    if oi is None:
        issues.append('intérêt ouvert inconnu')
        score -= 15
    elif oi < MIN_OPEN_INTEREST:
        issues.append(f'OI {oi} < {MIN_OPEN_INTEREST}')
        score -= 30
    if vol is None:
        score -= 5
    elif vol < MIN_VOLUME:
        issues.append(f'volume {vol} < {MIN_VOLUME}')
        score -= 10
    score = max(0.0, min(100.0, score))
    return {'score': round(score, 1), 'spread_pct': round(spread_pct, 2),
            'tradeable': score >= 40 and spread_pct <= MAX_SPREAD_PCT,
            'issues': issues}
