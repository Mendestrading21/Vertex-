"""vertex.options.contract_scorer — score CONTEXTUEL d'un contrat (§20).

Principes anti-défauts :
- un delta 0.25 n'est PAS pénalisé s'il appartient à un setup ultra-convexe validé ;
- un delta 0.80 n'est PLUS favorisé automatiquement (fin du biais historique §6.2) ;
- un OI élevé ne compense pas un mauvais R:R ;
- une prime faible ne compense pas un strike irréaliste ;
- un DTE élevé ne compense pas une IV extrêmement chère.
Le score part de la simulation (R:R, perte planifiée) et module par la
liquidité, la position dans la fenêtre DTE préférée et la cohérence de la
catégorie — multiplicatif pour qu'aucun facteur ne « rachète » un défaut fatal.
"""
from __future__ import annotations

from .models import (ScoredContract, CATEGORY_BALANCED, CATEGORY_DYNAMIC,
                     CATEGORY_ULTRA_CONVEX, CATEGORY_BEARISH_TACTICAL)

# R:R minimal pour qu'un contrat soit présentable (aligné constitution, unique).
MIN_REWARD_RISK = 1.5
GOOD_REWARD_RISK = 2.5


def _dte_fit(dte: int, category_pref: tuple[int, int], profile) -> float:
    lo, hi = category_pref
    if lo <= dte <= hi:
        return 1.0
    d = profile.dte
    if d.absolute_minimum <= dte < lo:
        return 0.75 + 0.25 * (dte - d.absolute_minimum) / max(lo - d.absolute_minimum, 1)
    if hi < dte <= d.absolute_maximum:
        return 0.75 + 0.25 * (d.absolute_maximum - dte) / max(d.absolute_maximum - hi, 1)
    return 0.0


def score_contract(contract: dict, category: str, sim: dict, profile,
                   setup, surface_context: dict | None = None) -> ScoredContract:
    reasons, penalties = [], []
    cat_cfg = profile.category(category)
    rr = sim.get('reward_risk')
    loss = sim.get('worst_planned_loss_pct')
    gain = sim.get('base_expected_gain_pct')
    liq = contract.get('_liquidity') or {}

    # ── socle : qualité du plan simulé ────────────────────────────────
    if rr is None or rr <= 0:
        base = 5.0
        penalties.append('R:R non calculable (simulation incomplète)')
    elif rr < MIN_REWARD_RISK:
        base = 20.0 * rr / MIN_REWARD_RISK
        penalties.append(f'R:R {rr} < {MIN_REWARD_RISK} — un OI élevé ne rachètera pas ça')
    else:
        base = 55.0 + min(35.0, (rr - MIN_REWARD_RISK) / (GOOD_REWARD_RISK - MIN_REWARD_RISK) * 35.0)
        reasons.append(f'R:R simulé {rr}')

    # perte planifiée dans la fourchette de la catégorie ?
    planned = cat_cfg.get('planned_loss_pct')
    if loss is not None and planned:
        lo, hi = planned
        if abs(loss) > hi + 10:
            base *= 0.7
            penalties.append(f'perte au stop {loss}% pire que la fourchette {planned} de {category}')
        elif lo <= abs(loss) <= hi:
            reasons.append(f'perte planifiée {loss}% dans la fourchette {planned}')
    target = cat_cfg.get('target_gain_pct')
    if gain is not None and target and gain >= target[0]:
        reasons.append(f'gain de base simulé {gain}% ≥ objectif {target[0]}%')

    # ── multiplicateurs (aucun ne peut dépasser 1.0 sauf mention) ─────
    # Liquidité : facteur 0.3..1.0 — un OI énorme ne monte PAS au-delà de 1.
    liq_score = liq.get('score', 50)
    liq_mult = 0.3 + 0.7 * (liq_score / 100)
    if liq_score < 60:
        penalties.append(f'liquidité moyenne ({liq_score}/100)')
    else:
        reasons.append(f'liquidité {liq_score}/100')

    # DTE dans la fenêtre préférée de la catégorie
    dte = int(contract.get('dte') or 0)
    pref = tuple(cat_cfg.get('preferred_dte', (profile.dte.preferred_minimum,
                                               profile.dte.preferred_maximum)))
    dte_mult = _dte_fit(dte, pref, profile)
    if dte_mult >= 1.0:
        reasons.append(f'DTE {dte} dans la fenêtre préférée {list(pref)}')
    elif dte_mult > 0:
        penalties.append(f'DTE {dte} hors fenêtre préférée {list(pref)}')

    # IV chère : un DTE long ne compense pas une IV extrême
    iv_mult = 1.0
    ctx = surface_context or {}
    iv_rank = ctx.get('iv_rank')
    if iv_rank is not None and iv_rank >= 85:
        iv_mult = 0.6
        penalties.append(f'IV rank {iv_rank} — payer la peur coûte cher, DTE long ou pas')
    elif ctx.get('iv_rv_premium') is not None and ctx['iv_rv_premium'] > 0.25:
        iv_mult = 0.75
        penalties.append('IV très au-dessus de la vol réalisée')

    # Cohérence de catégorie : ULTRA_CONVEX exige un setup exceptionnel
    cat_mult = 1.0
    if category == CATEGORY_ULTRA_CONVEX:
        if getattr(setup, 'setup_quality', 'STANDARD') != 'EXCEPTIONAL':
            cat_mult = 0.0
            penalties.append('ULTRA_CONVEX réservé aux setups exceptionnels (rare_setup_only)')
        else:
            ext = sim.get('extended_gain_pct')
            if ext is None or ext < 80:
                cat_mult = 0.5
                penalties.append('convexité simulée insuffisante pour un billet ULTRA_CONVEX')
            else:
                reasons.append(f'convexité réelle simulée: +{ext}% au TP2')
    if category == CATEGORY_DYNAMIC:
        reasons.append('catégorie principale du profil (DYNAMIC)')

    # Prime minuscule : jamais une raison d'acheter
    mid = contract.get('mid') or 0
    if mid and mid < 0.10:
        cat_mult = min(cat_mult, 0.3)
        penalties.append('prime quasi nulle — le prix bas n’est pas un argument')

    score = base * liq_mult * dte_mult * iv_mult * cat_mult
    return ScoredContract(contract=contract, category=category,
                          score=max(0.0, min(100.0, score)),
                          reasons=reasons, penalties=penalties,
                          anomalies=contract.get('_anomalies') or [],
                          scenarios=sim, liquidity=liq)
