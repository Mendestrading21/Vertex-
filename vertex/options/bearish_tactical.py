"""vertex.options.bearish_tactical — moteur PUT tactique RARE, totalement isolé (§10).

Achats de PUTS uniquement — la vente d'options est interdite partout.
Un PUT n'est proposé que si PLUSIEURS preuves convergent ; une simple baisse
journalière ne suffit JAMAIS. Aucun régime RISK-OFF ne produit automatiquement
un PUT : le régime n'est qu'UNE preuve parmi les autres.
Maximum 1 position baissière simultanée (sur les 3 options max du profil).
"""
from __future__ import annotations

from . import contract_filter, contract_scorer, liquidity, scenario_pricer
from .models import CATEGORY_BEARISH_TACTICAL, UnderlyingSetup
from vertex.anomalies import option_anomalies
from vertex.anomalies.models import any_blocking

CONFIG = {
    'enabled': True,
    'frequency': 'RARE',
    'max_simultaneous_bearish_positions': 1,
    'delta_abs_min': 0.30,
    'delta_abs_max': 0.55,
    'preferred_dte': [75, 180],
    'planned_loss_pct': [25, 35],
    'target_gain_pct': [50, 100],
}

# Preuves reconnues et nombre minimal de preuves convergentes.
EVIDENCE_KEYS = (
    'regime_unfavorable',        # régime de marché défavorable
    'relative_weakness',         # sous-jacent faible relativement au marché
    'downtrend_confirmed',       # tendance baissière confirmée
    'support_broken',            # support cassé
    'failed_recovery',           # reprise échouée
    'negative_catalyst',         # catalyseur négatif / dégradation fondamentale
)
MIN_EVIDENCE = 3


def evidence_check(evidence: dict) -> dict:
    """Valide la convergence de preuves. evidence = {clé: bool}."""
    present = [k for k in EVIDENCE_KEYS if evidence.get(k)]
    unknown = [k for k in evidence if k not in EVIDENCE_KEYS]
    ok = len(present) >= MIN_EVIDENCE
    notes = []
    if unknown:
        notes.append(f'preuves ignorées (non reconnues): {unknown}')
    if not ok:
        notes.append(f'{len(present)}/{MIN_EVIDENCE} preuves — une baisse du jour '
                     'ne suffit pas, pas de PUT')
    return {'converges': ok, 'evidence_present': present, 'notes': notes}


def select_put(contracts: list[dict], setup: UnderlyingSetup, evidence: dict,
               profile, open_bearish_positions: int = 0,
               rate_curve=None, holding_days: int = 10) -> dict:
    """Sélectionne AU PLUS un PUT d'achat, seulement si les preuves convergent."""
    out = {'selected': None, 'evidence': evidence_check(evidence), 'notes': []}
    cfg = profile.category(CATEGORY_BEARISH_TACTICAL) or CONFIG
    if not cfg.get('enabled', True):
        out['notes'].append('module baissier désactivé')
        return out
    if open_bearish_positions >= cfg.get('max_simultaneous_bearish_positions', 1):
        out['notes'].append('déjà une position baissière ouverte — maximum atteint')
        return out
    if not out['evidence']['converges']:
        return out
    if setup.direction != 'SHORT':
        out['notes'].append('setup non baissier — module inactif')
        return out

    lo, hi = cfg['delta_abs_min'], cfg['delta_abs_max']
    pref_dte = tuple(cfg.get('preferred_dte', (75, 180)))
    candidates = []
    for c in contracts or []:
        if c.get('right') != 'P':
            continue
        delta = c.get('delta')
        if delta is None or not (lo <= abs(float(delta)) <= hi):
            continue
        dte = c.get('dte')
        if not contract_filter.dte_within_constitution(dte, profile):
            continue
        liq = liquidity.assess(c)
        if not liq['tradeable']:
            continue
        anomalies = option_anomalies.check_contract(c, spot=setup.spot)
        if any_blocking(anomalies):
            continue
        c = dict(c)
        c['_liquidity'] = liq
        c['_anomalies'] = anomalies
        candidates.append(c)
    if not candidates:
        out['notes'].append('aucun PUT liquide dans la bande de delta — pas de position forcée')
        return out

    scored = []
    for c in candidates:
        sim = scenario_pricer.simulate(c, setup, rate_curve=rate_curve,
                                       holding_days=holding_days)
        rr = sim.get('reward_risk')
        if rr is None or rr < contract_scorer.MIN_REWARD_RISK:
            continue  # R:R incompatible → pas de PUT (exigence §10)
        sc = contract_scorer.score_contract(c, CATEGORY_BEARISH_TACTICAL, sim,
                                            profile, setup)
        # bonus fenêtre DTE préférée du module baissier
        dte = int(c.get('dte') or 0)
        if not (pref_dte[0] <= dte <= pref_dte[1]):
            sc.score *= 0.8
            sc.penalties.append(f'DTE {dte} hors fenêtre baissière {list(pref_dte)}')
        scored.append(sc)
    if not scored:
        out['notes'].append('aucun PUT avec simulation favorable et R:R compatible')
        return out
    best = max(scored, key=lambda s: s.score)
    out['selected'] = {'category': CATEGORY_BEARISH_TACTICAL, **best.to_dict()}
    return out
