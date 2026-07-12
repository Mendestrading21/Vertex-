"""vertex.opportunities.funnel — entonnoir & rôles stratégiques (§11-12).

L'univers complet (des centaines de titres) est scanné en arrière-plan mais
n'envahit JAMAIS l'interface. Cet entonnoir compte, étape par étape, combien de
dossiers survivent — Univers → Éligible → Radar → Prioritaire → Actionnable →
Suivi → Position. Zéro actionnable est un résultat VALIDE (jamais de remplissage
artificiel). Chaque opportunité reçoit un rôle d'équipe (§12). Pur et testable.
"""
from __future__ import annotations

# Rôles stratégiques (§12).
ROLE_ATTACK = 'ATTAQUE'
ROLE_MID = 'MILIEU'
ROLE_DEFENSE = 'DÉFENSE'
ROLE_RESERVE = 'RÉSERVE'
ROLES = (ROLE_ATTACK, ROLE_MID, ROLE_DEFENSE, ROLE_RESERVE)

# Seuils d'étapes (alignés sur bucketOf de la page Opportunités).
RADAR_MIN = 56
PRIORITY_MIN = 66
ACTIONABLE_MIN = 72

_BUYISH = {'BUY', 'ACHETER', 'STRONG_BUY', 'ACHETER FORT', 'RENFORCER'}


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def is_actionable(row):
    """Actionnable = R:R validé (≥ 2 via rr_ok) ET score ≥ 72 ET verdict d'achat."""
    score = _num(row.get('score'))
    if score is None or score < ACTIONABLE_MIN:
        return False
    if not row.get('rr_ok'):
        return False
    v = str(row.get('verdict') or row.get('vx_verdict') or '').upper()
    return any(b in v for b in _BUYISH)


def classify_role(row):
    """Classe un dossier : ATTAQUE / MILIEU / DÉFENSE / RÉSERVE (§12).

    ETF / véhicule non-action / candidat non confirmé → RÉSERVE. Sinon selon
    croissance+momentum+asymétrie (attaque), qualité+leadership (milieu), ou
    profil défensif (défense)."""
    veh = str(row.get('vehicle') or '').upper()
    profile = str(row.get('profile') or '').upper()
    if 'ETF' in veh or 'ETF' in profile or profile in ('RÉSERVE', 'RESERVE', 'CASH'):
        return ROLE_RESERVE
    score = _num(row.get('score'))
    if score is None:
        return ROLE_RESERVE
    mom = _num(row.get('st_mom')) or 0
    fund = _num(row.get('st_fund')) or 0
    # Un score réel de 0 doit être conservé (0 or 50 == 50 fausserait le rôle) :
    # défaut neutre 50 seulement quand la donnée est absente (None).
    risk = _num(row.get('st_risk'))
    risk = 50 if risk is None else risk
    asym = _num(row.get('vx_asym')) or 0
    rs = _num(row.get('rs'))
    rs = 50 if rs is None else rs
    growth = _num(row.get('perf_q')) or 0
    # Défense : profil explicite ou risque faible + momentum modéré.
    if 'DÉFENS' in profile or 'DEFENS' in profile:
        return ROLE_DEFENSE
    # Attaque : momentum + asymétrie + croissance forts.
    if (mom >= 60 or growth >= 12) and (asym >= 55 or rs >= 65):
        return ROLE_ATTACK
    # Milieu : qualité/leadership solides sans profil offensif marqué.
    if fund >= 55 or rs >= 55:
        return ROLE_MID
    # Faible risque, peu de momentum → rôle stabilisateur.
    if risk <= 40:
        return ROLE_DEFENSE
    return ROLE_MID


def build_funnel(rows, *, followed=0, positions=0):
    """Compte l'entonnoir + la répartition par rôle. `rows` = scan_state['rows'].

    followed/positions : comptes réels (suivis actifs, positions déclarées)."""
    rows = rows or []
    scored = [r for r in rows if _num(r.get('score')) is not None]
    radar = [r for r in scored if _num(r.get('score')) >= RADAR_MIN]
    priority = [r for r in scored if _num(r.get('score')) >= PRIORITY_MIN]
    actionable = [r for r in scored if is_actionable(r)]

    role_counts = {r: 0 for r in ROLES}
    for r in priority:                       # rôles calculés sur les dossiers prioritaires
        role_counts[classify_role(r)] += 1

    stages = [
        {'key': 'universe', 'label': 'Univers analysé', 'count': len(rows)},
        {'key': 'eligible', 'label': 'Éligibles', 'count': len(scored)},
        {'key': 'radar', 'label': 'Radar', 'count': len(radar)},
        {'key': 'priority', 'label': 'Prioritaires', 'count': len(priority)},
        {'key': 'actionable', 'label': 'Actionnables', 'count': len(actionable)},
        {'key': 'followed', 'label': 'Suivis', 'count': int(followed or 0)},
        {'key': 'positions', 'label': 'Positions', 'count': int(positions or 0)},
    ]
    return {
        'stages': stages,
        'roles': [{'role': r, 'count': role_counts[r]} for r in ROLES],
        'actionable_symbols': [r.get('symbol') for r in
                               sorted(actionable, key=lambda x: _num(x.get('score')) or 0,
                                      reverse=True)[:5]],
        'zero_actionable_is_valid': True,
        'note': ('Aucun dossier actionnable aujourd\'hui — c\'est un résultat valide, '
                 'pas un manque à remplir.') if not actionable else None,
    }


__all__ = ['build_funnel', 'classify_role', 'is_actionable', 'ROLES',
           'ROLE_ATTACK', 'ROLE_MID', 'ROLE_DEFENSE', 'ROLE_RESERVE']
