"""vertex.options.vol_surface — surface de volatilité par sous-jacent (§18).

Construit : IV par strike / par expiration, skew, smile, term structure,
expected move, percentile & rank d'IV, vol réalisée et prime IV/RV.
Détecte les dislocations (anomalies §17-volatilité) et les zones de meilleur
compromis — le but n'est PAS le contrat le moins cher, mais le meilleur
équilibre convexité / liquidité / temps / delta / theta / IV / R:R.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from vertex.anomalies.models import Anomaly, SEV_INFO, SEV_WARN


@dataclass
class VolSurface:
    symbol: str
    spot: float
    as_of: str = ''
    by_expiry: dict = field(default_factory=dict)      # expiry -> {'dte', 'atm_iv', 'strikes': {strike: iv}}
    term_structure: list = field(default_factory=list) # [(dte, atm_iv)] trié
    skew_by_expiry: dict = field(default_factory=dict) # expiry -> skew (iv_put25d ~ proxy: OTM put - ATM)
    expected_moves: dict = field(default_factory=dict) # expiry -> expected move pct
    iv_percentile: float | None = None
    iv_rank: float | None = None
    realized_vol_20d: float | None = None
    iv_rv_premium: float | None = None
    anomalies: list = field(default_factory=list)
    notes: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {'symbol': self.symbol, 'spot': self.spot, 'as_of': self.as_of,
                'by_expiry': self.by_expiry, 'term_structure': self.term_structure,
                'skew_by_expiry': self.skew_by_expiry, 'expected_moves': self.expected_moves,
                'iv_percentile': self.iv_percentile, 'iv_rank': self.iv_rank,
                'realized_vol_20d': self.realized_vol_20d,
                'iv_rv_premium': self.iv_rv_premium,
                'anomalies': [a.to_dict() for a in self.anomalies],
                'notes': list(self.notes)}


def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    if not n:
        return None
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def realized_vol(closes: list[float], n: int = 20) -> float | None:
    if len(closes) < n + 1:
        return None
    rets = [math.log(b / a) for a, b in zip(closes[-n - 1:], closes[-n:]) if a > 0]
    if len(rets) < 2:
        return None
    m = sum(rets) / len(rets)
    var = sum((r - m) ** 2 for r in rets) / (len(rets) - 1)
    return math.sqrt(var * 252)


def build_surface(symbol: str, spot: float, contracts: list[dict],
                  closes: list[float] | None = None,
                  iv_history: list[float] | None = None,
                  as_of: str = '') -> VolSurface:
    """contracts : lignes normalisées avec 'expiry','dte','strike','right','iv',
    'volume','open_interest'. Seules les IV présentes sont utilisées — rien inventé."""
    surf = VolSurface(symbol=symbol.upper(), spot=float(spot), as_of=as_of)
    if spot <= 0:
        surf.notes.append('spot invalide — surface non construite')
        return surf

    per_expiry: dict[str, dict] = {}
    for c in contracts or []:
        iv = c.get('iv')
        if iv is None or iv <= 0 or iv > 5:
            continue
        exp = c.get('expiry')
        if not exp:
            continue
        slot = per_expiry.setdefault(exp, {'dte': c.get('dte'), 'ivs': [],
                                           'strikes': {}, 'calls': {}, 'puts': {}})
        slot['ivs'].append((abs(c.get('strike', 0) - spot), float(iv)))
        slot['strikes'][float(c['strike'])] = float(iv)
        side = 'calls' if c.get('right') == 'C' else 'puts'
        slot[side][float(c['strike'])] = float(iv)

    for exp, slot in sorted(per_expiry.items()):
        if not slot['ivs']:
            continue
        atm_iv = min(slot['ivs'])[1]  # IV du strike le plus proche du spot
        dte = slot['dte'] or 0
        surf.by_expiry[exp] = {'dte': dte, 'atm_iv': round(atm_iv, 4),
                               'strikes': {k: round(v, 4) for k, v in sorted(slot['strikes'].items())}}
        if dte:
            surf.term_structure.append((int(dte), round(atm_iv, 4)))
            em = atm_iv * math.sqrt(max(dte, 1) / 365.0) * 100
            surf.expected_moves[exp] = round(em, 2)
        # Skew : IV du put ~10 % OTM vs ATM (proxy 25-delta sans Greeks)
        put_strike_target = spot * 0.90
        puts = slot['puts']
        if puts:
            nearest_put = min(puts, key=lambda k: abs(k - put_strike_target))
            if abs(nearest_put - put_strike_target) / spot < 0.06:
                surf.skew_by_expiry[exp] = round(puts[nearest_put] - atm_iv, 4)
        # Dislocations intra-expiration : IV non monotone par gros sauts
        strikes = sorted(slot['strikes'])
        ivs = [slot['strikes'][k] for k in strikes]
        med = _median(ivs)
        for k, iv in zip(strikes, ivs):
            if med and (iv > med * 2.0 or iv < med * 0.45):
                surf.anomalies.append(Anomaly(
                    code='STRIKE_IV_DISLOCATION', severity=SEV_WARN, confidence=0.7,
                    source=f'{symbol} {exp} {k}', observed={'iv': iv, 'median_iv': med},
                    expected={'iv': f'~{med:.2f}'},
                    impact='IV de strike disloquée — cotation ou donnée suspecte'))
        for (k1, iv1), (k2, iv2) in zip(list(zip(strikes, ivs)), list(zip(strikes, ivs))[1:]):
            if iv1 > 0 and abs(iv2 - iv1) / iv1 > 0.35:
                surf.anomalies.append(Anomaly(
                    code='SMILE_DISCONTINUITY', severity=SEV_WARN, confidence=0.6,
                    source=f'{symbol} {exp} {k1}->{k2}',
                    observed={'iv_jump': round(iv2 - iv1, 3)},
                    expected={'smile': 'continu'},
                    impact='discontinuité du smile entre strikes adjacents'))

    surf.term_structure.sort()
    # Term structure : inversion (front > back de beaucoup) & dislocations
    if len(surf.term_structure) >= 2:
        (d1, iv1), (dn, ivn) = surf.term_structure[0], surf.term_structure[-1]
        if iv1 > ivn * 1.25:
            surf.anomalies.append(Anomaly(
                code='TERM_STRUCTURE_INVERSION', severity=SEV_WARN, confidence=0.75,
                source=symbol, observed={'front_iv': iv1, 'back_iv': ivn,
                                         'front_dte': d1, 'back_dte': dn},
                expected={'structure': 'front <= back (contango)'},
                impact='structure inversée — événement pricé sur le front month, '
                       'risque d’IV crush après l’événement'))
            surf.anomalies.append(Anomaly(
                code='IV_CRUSH_RISK', severity=SEV_WARN, confidence=0.7,
                source=symbol, observed={'front_iv': iv1, 'back_iv': ivn},
                expected={}, impact='IV du front month gonflée — crush probable après catalyseur'))
            surf.notes.append('front month surchargé : une expiration plus lointaine offre '
                              'probablement un meilleur compromis IV/temps')
        ivs_ts = [iv for _, iv in surf.term_structure]
        med_ts = _median(ivs_ts)
        for dte, iv in surf.term_structure:
            if med_ts and (iv > med_ts * 1.6 or iv < med_ts * 0.55):
                surf.anomalies.append(Anomaly(
                    code='EXPIRY_IV_DISLOCATION', severity=SEV_WARN, confidence=0.6,
                    source=f'{symbol} dte={dte}', observed={'atm_iv': iv, 'median': med_ts},
                    expected={}, impact='expiration disloquée vs le reste de la courbe'))

    # Skew extrême
    for exp, skew in surf.skew_by_expiry.items():
        atm = surf.by_expiry[exp]['atm_iv']
        if atm and skew is not None and skew / atm > 0.5:
            surf.anomalies.append(Anomaly(
                code='SKEW_OUTLIER', severity=SEV_WARN, confidence=0.6,
                source=f'{symbol} {exp}', observed={'skew': skew, 'atm_iv': atm},
                expected={}, impact='skew extrême — les puts OTM sont très demandés, '
                                    'un strike bas est peu attractif à l’achat'))

    # Vol réalisée + prime IV/RV + percentile/rank
    if closes:
        surf.realized_vol_20d = realized_vol(closes)
    atm_ivs = [v['atm_iv'] for v in surf.by_expiry.values()]
    current_iv = _median(atm_ivs)
    if current_iv is not None and surf.realized_vol_20d:
        surf.iv_rv_premium = round(current_iv - surf.realized_vol_20d, 4)
        if surf.iv_rv_premium > 0.20:
            surf.anomalies.append(Anomaly(
                code='IV_OUTLIER', severity=SEV_INFO, confidence=0.55, source=symbol,
                observed={'iv': current_iv, 'rv_20d': surf.realized_vol_20d},
                expected={}, impact='IV très au-dessus de la vol réalisée — options chères'))
    if iv_history and current_iv is not None and len(iv_history) >= 20:
        below = sum(1 for x in iv_history if x <= current_iv)
        surf.iv_percentile = round(below / len(iv_history) * 100, 1)
        lo, hi = min(iv_history), max(iv_history)
        if hi > lo:
            surf.iv_rank = round((current_iv - lo) / (hi - lo) * 100, 1)
        recent = iv_history[-5:]
        if recent and current_iv > _median(recent) * 1.3:
            surf.anomalies.append(Anomaly(
                code='IV_SPIKE', severity=SEV_WARN, confidence=0.65, source=symbol,
                observed={'iv': current_iv, 'recent_median': _median(recent)},
                expected={}, impact='pic d’IV récent — payer la peur coûte cher'))
    elif iv_history is not None and len(iv_history) < 20:
        surf.notes.append('historique IV insuffisant — IV Rank/percentile non affichés (honnêteté)')

    return surf


def relative_value_zones(surf: VolSurface, preferred_dte: tuple[int, int] = (90, 210)) -> dict:
    """Zones relativement moins chères / anormalement chères de la courbe.

    Compromis, pas prix minimal : privilégie les expirations dans la fenêtre
    DTE préférée dont l'IV est sous la médiane de la courbe.
    """
    if not surf.term_structure:
        return {'cheaper': [], 'expensive': [], 'preferred': []}
    ivs = [iv for _, iv in surf.term_structure]
    med = _median(ivs)
    cheaper = [(d, iv) for d, iv in surf.term_structure if iv < med * 0.95]
    expensive = [(d, iv) for d, iv in surf.term_structure if iv > med * 1.15]
    lo, hi = preferred_dte
    preferred = [(d, iv) for d, iv in surf.term_structure
                 if lo <= d <= hi and iv <= med * 1.05]
    return {'median_iv': med, 'cheaper': cheaper, 'expensive': expensive,
            'preferred': preferred}
