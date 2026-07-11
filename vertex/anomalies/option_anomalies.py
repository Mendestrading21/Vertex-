"""vertex.anomalies.option_anomalies — anomalies OPTIONS par contrat et par surface (§17).

Vocabulaire honnête imposé : jamais « achat institutionnel » quand le côté
initiateur est inconnu — « activité inhabituelle », « proxy de demande »,
« signal à confirmer ».
"""
from __future__ import annotations

import math

from .models import Anomaly, SEV_INFO, SEV_WARN, SEV_BLOCK

WIDE_SPREAD_PCT = 12.0        # spread bid/ask relatif au mid
LOW_OI = 100
LOW_VOLUME = 5
STALE_QUOTE_S = 3600


def _add(out, code, sev, conf, source, observed, expected, impact, blocking=False):
    out.append(Anomaly(code=code, severity=sev, confidence=conf, source=source,
                       observed=observed, expected=expected, impact=impact,
                       blocking=blocking))


def check_contract(c: dict, spot: float | None = None,
                   quote_age_s: float | None = None) -> list[Anomaly]:
    """c = ligne de contrat normalisée (voir ibkr_option_chain.contract_row)."""
    out: list[Anomaly] = []
    src = f"{c.get('symbol', '?')} {c.get('expiry', '?')} {c.get('strike', '?')}{c.get('right', '?')}"
    bid, ask, mid = c.get('bid'), c.get('ask'), c.get('mid')

    # ── Qualité du contrat ────────────────────────────────────────────
    if bid in (None, 0):
        _add(out, 'ZERO_BID', SEV_BLOCK, 0.9, src, {'bid': bid}, {'bid': '> 0'},
             'aucun acheteur affiché — sortie potentiellement impossible au prix espéré',
             blocking=True)
    if ask in (None, 0):
        _add(out, 'ZERO_ASK', SEV_BLOCK, 0.9, src, {'ask': ask}, {'ask': '> 0'},
             'aucun vendeur affiché — cotation inutilisable', blocking=True)
    if bid and ask and ask > 0:
        if bid > ask:
            _add(out, 'CROSSED_OPTION_MARKET', SEV_BLOCK, 0.95, src,
                 {'bid': bid, 'ask': ask}, {'bid': '<= ask'},
                 'marché d’option croisé — donnée non fiable', blocking=True)
        elif mid:
            spread_pct = (ask - bid) / mid * 100
            if spread_pct >= WIDE_SPREAD_PCT:
                _add(out, 'WIDE_SPREAD', SEV_WARN, min(0.9, spread_pct / 40), src,
                     {'spread_pct': round(spread_pct, 1)}, {'spread_pct': f'< {WIDE_SPREAD_PCT}'},
                     'spread large — coût de friction élevé, R:R réel dégradé')
    if quote_age_s is not None and quote_age_s > STALE_QUOTE_S:
        _add(out, 'STALE_QUOTE', SEV_BLOCK, 0.85, src,
             {'age_seconds': int(quote_age_s)}, {'age_seconds': f'<= {STALE_QUOTE_S}'},
             'cotation rassise — interdit de décider dessus', blocking=True)
    oi, vol = c.get('open_interest'), c.get('volume')
    if oi is not None and oi < LOW_OI:
        _add(out, 'LOW_OPEN_INTEREST', SEV_WARN, 0.8, src, {'open_interest': oi},
             {'open_interest': f'>= {LOW_OI}'}, 'intérêt ouvert faible — liquidité fragile')
    if vol is not None and vol < LOW_VOLUME:
        _add(out, 'LOW_VOLUME', SEV_INFO, 0.7, src, {'volume': vol},
             {'volume': f'>= {LOW_VOLUME}'}, 'volume du jour quasi nul')
    last = c.get('last')
    if last is not None and mid and mid > 0:
        dev = abs(last - mid) / mid
        if dev >= 0.25:
            _add(out, 'ABNORMAL_LAST_VS_MID', SEV_WARN, 0.6, src,
                 {'last': last, 'mid': round(mid, 4)}, {'deviation': '< 25%'},
                 'dernier échange loin du mid — cotation possiblement décalée dans le temps')

    # ── Valeur intrinsèque / valeur temps ─────────────────────────────
    if spot and mid and c.get('strike') is not None and c.get('right') in ('C', 'P'):
        intrinsic = max(0.0, (spot - c['strike']) if c['right'] == 'C' else (c['strike'] - spot))
        time_value = mid - intrinsic
        if time_value < -0.02 * max(mid, 0.05):
            _add(out, 'NEGATIVE_TIME_VALUE', SEV_BLOCK, 0.85, src,
                 {'mid': round(mid, 4), 'intrinsic': round(intrinsic, 4)},
                 {'time_value': '>= 0'},
                 'valeur temps négative — cotation incohérente ou exercice imminent',
                 blocking=True)
        if ask is not None and ask > 0 and intrinsic > 0 and ask < intrinsic * 0.98:
            _add(out, 'INTRINSIC_VALUE_VIOLATION', SEV_BLOCK, 0.9, src,
                 {'ask': ask, 'intrinsic': round(intrinsic, 4)}, {'ask': '>= intrinsèque'},
                 'prix sous la valeur intrinsèque — arbitrage impossible, donnée fausse',
                 blocking=True)

    # ── Greeks ────────────────────────────────────────────────────────
    delta, gamma, theta, vega = c.get('delta'), c.get('gamma'), c.get('theta'), c.get('vega')
    right = c.get('right')
    if delta is not None:
        if right == 'C' and not (0 <= delta <= 1):
            _add(out, 'GREEK_SIGN_ERROR', SEV_BLOCK, 0.9, src, {'delta': delta},
                 {'delta': '[0,1] pour un CALL'}, 'delta hors bornes — Greeks non fiables',
                 blocking=True)
        if right == 'P' and not (-1 <= delta <= 0):
            _add(out, 'GREEK_SIGN_ERROR', SEV_BLOCK, 0.9, src, {'delta': delta},
                 {'delta': '[-1,0] pour un PUT'}, 'delta hors bornes — Greeks non fiables',
                 blocking=True)
    if gamma is not None and gamma < 0:
        _add(out, 'GREEK_SIGN_ERROR', SEV_BLOCK, 0.9, src, {'gamma': gamma},
             {'gamma': '>= 0 (option longue)'}, 'gamma négatif — Greeks non fiables', blocking=True)
    if theta is not None and theta > 0.01:
        _add(out, 'THETA_OUTLIER', SEV_WARN, 0.7, src, {'theta': theta},
             {'theta': '<= 0 (option longue)'}, 'theta positif inattendu pour une option achetée')
    if vega is not None and vega < 0:
        _add(out, 'VEGA_OUTLIER', SEV_WARN, 0.7, src, {'vega': vega},
             {'vega': '>= 0'}, 'vega négatif inattendu')
    model = c.get('model_greeks') or {}
    if delta is not None and model.get('delta') is not None:
        gap = abs(delta - model['delta'])
        if gap >= 0.12:
            _add(out, 'BROKER_MODEL_GREEK_DIVERGENCE', SEV_WARN, 0.6, src,
                 {'broker_delta': delta, 'model_delta': model['delta']},
                 {'gap': '< 0.12'},
                 'Greeks broker et modèle en désaccord — étiqueter la source et vérifier')
    return out


def check_activity(c: dict, avg_volume: float | None = None,
                   prev_open_interest: float | None = None,
                   dte: int | None = None) -> list[Anomaly]:
    """Activité inhabituelle — TOUJOURS présentée comme proxy à confirmer."""
    out: list[Anomaly] = []
    src = f"{c.get('symbol', '?')} {c.get('expiry', '?')} {c.get('strike', '?')}{c.get('right', '?')}"
    vol, oi = c.get('volume'), c.get('open_interest')
    if vol and oi and oi > 0 and vol / oi >= 3:
        _add(out, 'VOLUME_TO_OI_SPIKE', SEV_INFO, 0.6, src,
             {'volume': vol, 'open_interest': oi, 'ratio': round(vol / oi, 1)},
             {}, 'volume >> intérêt ouvert — activité inhabituelle (proxy de demande, '
                 'côté initiateur INCONNU — signal à confirmer)')
    if oi is not None and prev_open_interest:
        change = (oi - prev_open_interest) / prev_open_interest
        if abs(change) >= 0.5:
            _add(out, 'OPEN_INTEREST_CHANGE', SEV_INFO, 0.6, src,
                 {'oi_change_pct': round(change * 100, 1)}, {},
                 'variation d’intérêt ouvert marquée — positions en construction ou en sortie (proxy)')
    if vol and avg_volume and avg_volume > 0 and vol / avg_volume >= 5:
        _add(out, 'UNUSUAL_CONTRACT_ACTIVITY', SEV_INFO, 0.6, src,
             {'volume': vol, 'avg_volume': avg_volume}, {},
             'activité inhabituelle sur ce contrat — signal à confirmer, côté initiateur inconnu')
    if dte is not None and vol and avg_volume and avg_volume > 0:
        if dte <= 7 and vol / avg_volume >= 4:
            _add(out, 'FRONT_EXPIRY_ACTIVITY_CLUSTER', SEV_INFO, 0.55, src,
                 {'dte': dte, 'volume': vol}, {},
                 'grappe d’activité sur l’échéance courte — souvent spéculatif/couverture')
    delta = c.get('delta')
    if delta is not None and abs(delta) <= 0.10 and vol and avg_volume and avg_volume > 0 \
            and vol / avg_volume >= 4:
        _add(out, 'FAR_OTM_ACTIVITY_CLUSTER', SEV_INFO, 0.55, src,
             {'delta': delta, 'volume': vol}, {},
             'activité inhabituelle très OTM — proxy de pari extrême, à confirmer')
    return out


def check_economics(c: dict, spot: float | None, expected_move_pct: float | None = None,
                    dte: int | None = None, rate: float = 0.0,
                    counterpart_mid: float | None = None) -> list[Anomaly]:
    """Relations économiques : parité, breakeven, theta vs mouvement attendu, prime suspecte."""
    out: list[Anomaly] = []
    src = f"{c.get('symbol', '?')} {c.get('expiry', '?')} {c.get('strike', '?')}{c.get('right', '?')}"
    mid, strike, right = c.get('mid'), c.get('strike'), c.get('right')
    if None in (mid, strike, spot) or right not in ('C', 'P'):
        return out

    # Parité put-call (approx sans dividende) : C - P ≈ S - K·e^{-rT}
    if counterpart_mid is not None and dte:
        T = max(dte, 1) / 365.0
        call_mid = mid if right == 'C' else counterpart_mid
        put_mid = counterpart_mid if right == 'C' else mid
        parity_gap = (call_mid - put_mid) - (spot - strike * math.exp(-rate * T))
        if abs(parity_gap) > max(0.02 * spot, 0.5):
            _add(out, 'PUT_CALL_PARITY_WARNING', SEV_WARN, 0.6, src,
                 {'parity_gap': round(parity_gap, 3)}, {'parity_gap': '≈ 0'},
                 'écart de parité put-call — dividende non intégré, cotation décalée ou donnée fausse')

    # Breakeven vs mouvement attendu
    if right == 'C':
        breakeven_pct = (strike + mid - spot) / spot * 100
    else:
        breakeven_pct = (spot - (strike - mid)) / spot * 100
    if expected_move_pct is not None and expected_move_pct > 0:
        ratio = breakeven_pct / expected_move_pct
        if ratio > 2.2:
            _add(out, 'BREAKEVEN_UNREALISTIC', SEV_WARN, min(0.9, ratio / 4), src,
                 {'breakeven_pct': round(breakeven_pct, 1),
                  'expected_move_pct': round(expected_move_pct, 1)},
                 {'ratio': '<= 2.2'},
                 'breakeven très au-delà du mouvement attendu — pari improbable')
        theta = c.get('theta')
        if theta is not None and mid > 0 and dte:
            daily_burn_pct = abs(theta) / mid * 100
            em_daily = expected_move_pct / max(math.sqrt(dte), 1)
            if daily_burn_pct > 0 and em_daily > 0 and daily_burn_pct / em_daily > 1.5:
                _add(out, 'THETA_TO_EXPECTED_MOVE_IMBALANCE', SEV_WARN, 0.6, src,
                     {'daily_theta_pct': round(daily_burn_pct, 2),
                      'daily_expected_move_pct': round(em_daily, 2)}, {},
                     'le temps coûte plus vite que le mouvement attendu ne rapporte')
    # Prime suspecte
    if mid < 0.05:
        _add(out, 'PREMIUM_TOO_CHEAP_TO_BE_TRUSTED', SEV_WARN, 0.7, src,
             {'mid': mid}, {'mid': '>= 0.05'},
             'prime quasi nulle — le marché price un billet de loterie ; '
             'ne JAMAIS sélectionner ce contrat parce qu’il est « pas cher »')
    if expected_move_pct is not None and expected_move_pct > 0 and spot:
        premium_pct = mid / spot * 100
        if premium_pct > expected_move_pct * 1.5:
            _add(out, 'PREMIUM_TOO_EXPENSIVE_FOR_SETUP', SEV_WARN, 0.6, src,
                 {'premium_pct_of_spot': round(premium_pct, 1),
                  'expected_move_pct': round(expected_move_pct, 1)}, {},
                 'prime supérieure au mouvement attendu — setup non rentable même s’il a raison')
    return out
