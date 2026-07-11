"""vertex.options.recommendation — assemblage de la recommandation options.

Réunit sélection CALL (call_selector), PUT tactique éventuel (bearish_tactical),
plan de gestion des profits (§11) et analyse indépendante du capital (§8.4).
Aucune décision finale ici : la sortie alimente l'executive_engine, seule
couche autorisée à trancher.
"""
from __future__ import annotations

from . import bearish_tactical, call_selector, scenario_pricer
from .models import UnderlyingSetup

# §11 — gestion des profits
SECURE_TRIGGER_GAIN_PCT = 50
SECURE_SHARE_PCT = (60, 70)
RUNNER_SHARE_PCT = (30, 40)
TIME_STOP_SESSIONS = (5, 8)
EXIT_MODES = ('FULL_EXIT', 'PARTIAL_EXIT', 'RUNNER')

RUNNER_KILL_CONDITIONS = (
    'momentum_broken',        # le momentum casse
    'major_resistance',       # résistance majeure atteinte
    'iv_contraction_risk',    # l'IV risque de se contracter
    'catalyst_finished',      # le catalyseur est terminé
    'data_unfavorable',       # les données deviennent défavorables
    'time_insufficient',      # temps restant insuffisant
)


def profit_management_plan(current_gain_pct: float | None,
                           sessions_in_trade: int | None = None,
                           conditions: dict | None = None) -> dict:
    """Plan de gestion : sécurisation à ~+50 %, runner jamais obligatoire, time stop."""
    conditions = conditions or {}
    plan = {'modes_available': list(EXIT_MODES), 'action': 'HOLD',
            'secure_share_pct': None, 'runner_share_pct': None,
            'raise_invalidation': False, 'time_stop_triggered': False,
            'reasons': []}
    kill = [k for k in RUNNER_KILL_CONDITIONS if conditions.get(k)]
    if sessions_in_trade is not None and current_gain_pct is not None \
            and sessions_in_trade >= TIME_STOP_SESSIONS[1] and current_gain_pct <= 0:
        plan['time_stop_triggered'] = True
        plan['action'] = 'REEVALUATE_OR_EXIT'
        plan['reasons'].append(
            f'time stop: aucun mouvement favorable après {sessions_in_trade} séances '
            f'(seuil {TIME_STOP_SESSIONS[0]}-{TIME_STOP_SESSIONS[1]}) — réévaluer même '
            'sans stop prix touché')
        return plan
    if current_gain_pct is not None and current_gain_pct >= SECURE_TRIGGER_GAIN_PCT:
        plan['secure_share_pct'] = list(SECURE_SHARE_PCT)
        plan['raise_invalidation'] = True
        if kill:
            plan['action'] = 'FULL_EXIT'
            plan['runner_share_pct'] = None
            plan['reasons'].append('runner non conservé: ' + ', '.join(kill) +
                                   ' — le runner n’est jamais obligatoire')
        else:
            plan['action'] = 'PARTIAL_EXIT'
            plan['runner_share_pct'] = list(RUNNER_SHARE_PCT)
            plan['reasons'].append(
                f'≈+{SECURE_TRIGGER_GAIN_PCT}% atteint: sécuriser '
                f'{SECURE_SHARE_PCT[0]}-{SECURE_SHARE_PCT[1]}%, conserver '
                f'{RUNNER_SHARE_PCT[0]}-{RUNNER_SHARE_PCT[1]}% en runner, '
                'remonter l’invalidation, réévaluer le momentum')
    elif kill and current_gain_pct is not None and current_gain_pct > 0:
        plan['action'] = 'FULL_EXIT'
        plan['reasons'].append('conditions défavorables: ' + ', '.join(kill))
    return plan


def build_recommendation(call_contracts: list[dict], setup: UnderlyingSetup,
                         profile, put_contracts: list[dict] | None = None,
                         bearish_evidence: dict | None = None,
                         open_options_count: int = 0,
                         open_bearish_count: int = 0,
                         rate_curve=None, surface_context: dict | None = None,
                         capital: float | None = None) -> dict:
    """Recommandation complète. Respecte le maximum de 3 options simultanées."""
    out = {'symbol': setup.symbol, 'calls': None, 'bearish': None,
           'capital_analysis': None, 'profit_management_defaults': {
               'secure_trigger_gain_pct': SECURE_TRIGGER_GAIN_PCT,
               'secure_share_pct': list(SECURE_SHARE_PCT),
               'runner_share_pct': list(RUNNER_SHARE_PCT),
               'time_stop_sessions': list(TIME_STOP_SESSIONS)},
           'blocked': False, 'notes': []}
    max_opts = profile.max_simultaneous_options
    if open_options_count >= max_opts:
        out['blocked'] = True
        out['notes'].append(f'{open_options_count}/{max_opts} options déjà ouvertes — '
                            'aucune nouvelle option proposée')
        return out
    if setup.direction == 'LONG':
        out['calls'] = call_selector.select_calls(
            call_contracts, setup, profile, rate_curve=rate_curve,
            surface_context=surface_context)
        primary = out['calls'].get('primary')
        if primary:
            out['capital_analysis'] = scenario_pricer.capital_free_analysis(
                primary['scenarios'], primary['contract'], capital=capital)
    elif setup.direction == 'SHORT':
        out['bearish'] = bearish_tactical.select_put(
            put_contracts or [], setup, bearish_evidence or {}, profile,
            open_bearish_positions=open_bearish_count, rate_curve=rate_curve)
        sel = out['bearish'].get('selected')
        if sel:
            out['capital_analysis'] = scenario_pricer.capital_free_analysis(
                sel['scenarios'], sel['contract'], capital=capital)
    return out
