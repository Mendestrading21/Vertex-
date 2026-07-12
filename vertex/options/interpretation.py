"""vertex.options.interpretation — verdicts de graphiques options (§6/§18).

Transforme les mesures pures (volatilité, expected move, event risk) en
interprétations canoniques (contrat vertex.visualization.schemas). Chaque
fonction répond à UNE question et rend FAVORABLE/NEUTRE/DEFAVORABLE/
BLOQUANT/INCONNU avec ses preuves. Aucun ordre, lecture seule.
"""
from __future__ import annotations

from vertex.visualization.schemas import (
    interpretation, unknown, ST_FAVORABLE, ST_NEUTRE, ST_DEFAVORABLE,
)
from . import volatility as vol
from . import event_risk as ev

_VOL_LIMITS = [
    'IV rank/percentile dépendent de la profondeur d\'historique disponible',
    'vol réalisée close-to-close : ne capture pas le risque intra-journalier',
]


def interpret_volatility(symbol, current_iv, iv_low, iv_high, iv_history=None,
                         closes=None, source='', as_of=None):
    """« Les options sont-elles chères ou bon marché ici ? »"""
    cid = 'options.volatility'
    q = 'Les options de %s sont-elles chères ou bon marché ?' % symbol
    rank = vol.iv_rank(current_iv, iv_low, iv_high)
    pctl = vol.iv_percentile(current_iv, iv_history) if iv_history else None
    rv = vol.realized_vol(closes) if closes else None
    prem = vol.iv_rv_premium(current_iv, rv)
    regime = vol.vol_regime(rank)
    if rank is None and pctl is None:
        return unknown(cid, q, reason='IV rank/percentile indisponibles',
                       source=source, limitations=_VOL_LIMITS)
    pos, neg, unc = [], [], []
    ref = rank if rank is not None else pctl
    label = 'IV rank' if rank is not None else 'IV percentile'
    if regime:
        pos.append('Régime de volatilité : %s (%s %.0f)' % (regime, label, ref))
    if prem is not None:
        if prem > 0:
            neg.append('IV au-dessus de la vol réalisée (prime +%.2f) : premium payé cher' % prem)
        else:
            pos.append('IV sous la vol réalisée (%.2f) : premium relativement bon marché' % prem)
    else:
        unc.append('Vol réalisée indisponible — prime IV/RV non calculable')
    # Verdict pour un ACHETEUR d'options (le desk n'achète que) : IV basse = favorable.
    if ref >= 70:
        status, reading = ST_DEFAVORABLE, 'Volatilité élevée : acheter des primes coûte cher, risque de crush.'
    elif ref <= 35:
        status, reading = ST_FAVORABLE, 'Volatilité basse : primes relativement abordables pour un achat.'
    else:
        status, reading = ST_NEUTRE, 'Volatilité médiane : ni aubaine ni piège sur le prix des primes.'
    conf = 0.6 if (rank is not None and prem is not None) else 0.4
    return interpretation(
        cid, q, reading, status, confidence=conf,
        positive_evidence=pos, negative_evidence=neg, uncertainties=unc,
        strategy_impact=('Favorise l\'achat de convexité.' if status == ST_FAVORABLE
                         else 'Privilégier des structures moins exposées au vega / attendre une détente.'
                         if status == ST_DEFAVORABLE else 'Sélection au cas par cas.'),
        source=source, as_of=as_of, limitations=_VOL_LIMITS)


def interpret_event_risk(symbol, earnings_in_days, ex_dividend_days, right, dte,
                         source='', as_of=None):
    """« Un événement menace-t-il cette position d'ici l'échéance ? »"""
    cid = 'options.event_risk'
    q = 'Un événement menace-t-il l\'option %s d\'ici l\'échéance ?' % symbol
    c = ev.combined(earnings_in_days, ex_dividend_days, right, dte)
    lvl = c['level']
    notes = c['notes']
    if lvl == ev.RISK_UNKNOWN:
        return unknown(cid, q, reason='Dates d\'événement inconnues',
                       source=source)
    pos, neg = [], []
    if lvl in (ev.RISK_HIGH, ev.RISK_MODERATE):
        neg.extend(notes)
    else:
        pos.extend(notes or ['Aucun événement majeur identifié sur la fenêtre.'])
    status = {ev.RISK_HIGH: ST_DEFAVORABLE, ev.RISK_MODERATE: ST_DEFAVORABLE,
              ev.RISK_LOW: ST_NEUTRE, ev.RISK_NONE: ST_FAVORABLE}[lvl]
    reading = {
        ev.RISK_HIGH: 'Événement imminent : risque de crush/gap élevé sur la prime.',
        ev.RISK_MODERATE: 'Événement dans la fenêtre : exposition à surveiller.',
        ev.RISK_LOW: 'Événement lointain : impact limité.',
        ev.RISK_NONE: 'Aucun événement porté d\'ici l\'échéance.',
    }[lvl]
    return interpretation(
        cid, q, reading, status, confidence=0.55,
        positive_evidence=pos, negative_evidence=neg,
        uncertainties=([] if notes else ['Vérifier les dates officielles avant décision']),
        strategy_impact=('Dimensionner en conscience du crush / envisager une échéance qui évite l\'événement.'
                         if status == ST_DEFAVORABLE else 'Pas de contrainte d\'événement particulière.'),
        source=source, as_of=as_of)


__all__ = ['interpret_volatility', 'interpret_event_risk']
