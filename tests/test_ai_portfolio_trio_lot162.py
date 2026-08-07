"""
LOT 162 — Caractérisation du trio zéro-test :
`vertex/ai/audit.py` (journal des appels IA, servi par
strategy_os_api), `vertex/ai/strategy_context.py` (contexte injecté
dans chaque analyse IA — porte les RAPPELS d'invariants) et
`vertex/portfolio/team_roles.py` (rôles de l'équipe §25).

Ces tests figent les bornes mémoire, le contrat du contexte (dont
les rappels READONLY) et la cohérence des rôles — les changer
devient une décision explicite.
"""

from vertex.ai.audit import AIAudit, MAX_ENTRIES
from vertex.ai.strategy_context import build_strategy_context
from vertex.portfolio.team_roles import (ROLE_DESCRIPTIONS, ROLE_TARGETS,
                                         ROLES)


# ═══ ai/audit : journal borné, sans secret ═══

def test_audit_borne_a_200_entrees_les_plus_recentes():
    a = AIAudit()
    for i in range(250):
        a.record(symbol='S%d' % i, source='claude', ok=True)
    s = a.stats()
    assert s['total'] == MAX_ENTRIES == 200      # deque bornée : jamais plus
    assert [e['symbol'] for e in a.recent(3)] == ['S247', 'S248', 'S249']


def test_audit_stats_ok_et_fallbacks_comptes():
    a = AIAudit()
    a.record(symbol='A', source='claude', ok=True)
    a.record(symbol='B', source='deterministic-fallback', ok=False)
    a.record(symbol='C', source='deterministic-fallback', ok=True)
    assert a.stats() == {'total': 3, 'ok': 2, 'fallbacks': 2}


def test_audit_erreurs_tronquees_a_5():
    a = AIAudit()
    a.record(symbol='X', source='claude', ok=False, errors=['e'] * 10)
    assert len(a.recent(1)[0]['errors']) == 5    # borné — pas de fuite verbeuse


def test_audit_vide_honnete():
    a = AIAudit()
    assert a.stats() == {'total': 0, 'ok': 0, 'fallbacks': 0}
    assert a.recent() == []


# ═══ ai/strategy_context : le contexte qui encadre l'IA ═══

def test_contexte_contrat_complet():
    ctx = build_strategy_context()
    assert set(ctx) == {'strategy_id', 'display_name', 'style', 'benchmark',
                        'portfolio_positions', 'max_simultaneous_options',
                        'allowed_final_decisions', 'analysis_order',
                        'dte_preferred', 'reminders'}
    lo, hi = ctx['portfolio_positions']
    assert lo <= hi                                # bornes cohérentes
    dlo, dhi = ctx['dte_preferred']
    assert dlo <= dhi
    assert ctx['allowed_final_decisions']          # jamais vide


def test_contexte_rappels_invariants_readonly():
    # Les 4 rappels d'invariants injectés dans CHAQUE analyse IA — dont
    # la lecture seule absolue. Les affaiblir = décision explicite.
    r = ' | '.join(build_strategy_context()['reminders'])
    assert 'lecture seule absolue' in r and 'aucun ordre' in r
    assert 'moteur exécutif déterministe' in r
    assert 'aucune promesse de performance' in r
    assert 'jamais inventer' in r


# ═══ portfolio/team_roles : cohérence de l'équipe §25 ═══

def test_roles_les_quatre_dans_l_ordre_terrain():
    assert ROLES == ('ATTACKER', 'MIDFIELDER', 'DEFENDER', 'GOALKEEPER')


def test_descriptions_coherentes_avec_les_cibles():
    # Chaque rôle décrit == sa cible d'effectif du modèle (une seule
    # vérité) ; profil non vide partout.
    assert set(ROLE_DESCRIPTIONS) == set(ROLES)
    for role in ROLES:
        assert ROLE_DESCRIPTIONS[role]['count'] == list(ROLE_TARGETS[role])
        assert ROLE_DESCRIPTIONS[role]['profile'].strip()
    # Défense et gardien : pas d'horizon (positions de fond).
    assert ROLE_DESCRIPTIONS['DEFENDER']['horizon_months'] is None
    assert ROLE_DESCRIPTIONS['GOALKEEPER']['horizon_months'] is None
