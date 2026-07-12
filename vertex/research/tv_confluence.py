"""vertex.research.tv_confluence — confluence signal TradingView × verdict Vertex.

Un signal TradingView est une INFORMATION directionnelle. Cette table canonique
dit s'il CONFIRME, CONTREDIT ou est NEUTRE face au verdict du moteur Vertex —
sans jamais devenir un ordre. Pur et testable ; la carte d'analyse en miroir
utilise la même correspondance.
"""
from __future__ import annotations

# Direction implicite de chaque signal (cf. ALLOWED_SIGNALS du store).
BULLISH_SIGNALS = frozenset({
    'SUPPORT_RECLAIM', 'BREAKOUT_CONFIRMED', 'BREAKOUT_RETEST',
    'MOMENTUM_ACCELERATION', 'VOLUME_EXPANSION', 'TREND_ALIGNMENT',
})
BEARISH_SIGNALS = frozenset({'FAILED_BREAKOUT', 'THESIS_INVALIDATION'})
# Neutres/contextuels : CORRECTION_DEEP, VOLATILITY_COMPRESSION/EXPANSION.

# Verdicts moteur haussiers / prudents (vocabulaire décisionnel Vertex).
_BULLISH_VERDICTS = ('ACHETER', 'BUY', 'STRONG_BUY', 'RENFORCER', 'ACCUMULER', 'BUY_PULLBACK')
_BEARISH_VERDICTS = ('AVOID', 'ÉVITER', 'EVITER', 'ALLÉGER', 'ALLEGER', 'SORTIR',
                     'RÉDUIRE', 'REDUIRE', 'NO_NEW_RISK', 'VENDRE', 'REFUSÉ', 'REFUSE',
                     'REJETÉ', 'REJETE')

CONFIRM = 'CONFIRME'
CONTRADICT = 'CONTREDIT'
NEUTRAL = 'NEUTRE'


def signal_direction(signal: str) -> str:
    """'BULLISH' / 'BEARISH' / 'NEUTRAL' pour un code signal."""
    s = str(signal or '').strip().upper()
    if s in BULLISH_SIGNALS:
        return 'BULLISH'
    if s in BEARISH_SIGNALS:
        return 'BEARISH'
    return 'NEUTRAL'


def verdict_stance(verdict: str) -> str:
    """Posture du verdict moteur : 'BULLISH' / 'BEARISH' / 'NEUTRAL'."""
    v = str(verdict or '').strip().upper()
    if not v:
        return 'NEUTRAL'
    # Baissier d'abord : plus sûr — jamais un faux CONFIRME si un verdict prudent
    # contient par hasard un mot haussier en sous-chaîne (« NE PAS ACHETER »).
    if any(b in v for b in _BEARISH_VERDICTS):
        return 'BEARISH'
    if any(b in v for b in _BULLISH_VERDICTS):
        return 'BULLISH'
    return 'NEUTRAL'


def confluence(signal: str, verdict: str) -> dict:
    """Confronte un signal TV au verdict moteur.

    Rend {state: CONFIRME|CONTREDIT|NEUTRE, signal_dir, verdict_stance, note}.
    Jamais un ordre — c'est une lecture de cohérence, pas une décision."""
    sd = signal_direction(signal)
    vs = verdict_stance(verdict)
    if sd == 'NEUTRAL' or vs == 'NEUTRAL':
        state = NEUTRAL
        note = 'Signal contextuel ou verdict neutre — pas de confluence directionnelle.'
    elif sd == vs:
        state = CONFIRM
        note = 'Le signal TradingView va dans le sens du verdict moteur.'
    else:
        state = CONTRADICT
        note = 'Le signal TradingView contredit le verdict moteur — prudence, réévaluer.'
    return {'state': state, 'signal_dir': sd, 'verdict_stance': vs, 'note': note}


def summarize(signals, verdict: str) -> dict:
    """Agrège la confluence sur plusieurs signaux d'un même titre."""
    rows = []
    confirms = contradicts = 0
    for s in signals or []:
        code = s.get('signal') if isinstance(s, dict) else s
        c = confluence(code, verdict)
        if c['state'] == CONFIRM:
            confirms += 1
        elif c['state'] == CONTRADICT:
            contradicts += 1
        rows.append({'signal': code, **c})
    if contradicts and not confirms:
        overall = CONTRADICT
    elif confirms and not contradicts:
        overall = CONFIRM
    elif confirms or contradicts:
        overall = 'MIXTE'
    else:
        overall = NEUTRAL
    return {'overall': overall, 'confirms': confirms, 'contradicts': contradicts,
            'rows': rows, 'verdict': verdict or None}


__all__ = ['signal_direction', 'verdict_stance', 'confluence', 'summarize',
           'CONFIRM', 'CONTRADICT', 'NEUTRAL', 'BULLISH_SIGNALS', 'BEARISH_SIGNALS']
