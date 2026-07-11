"""vertex.catalysts.earnings_engine — modes earnings (§21).

Interdit d'afficher « 99 % sûr », « garanti », « certain », « sans risque ».
Tenir une option À TRAVERS des résultats exige une activation explicite +
un dossier complet (date confirmée, expected move, IV crush estimé, scénario
gap défavorable, perte max, qualité de données).
"""
from __future__ import annotations

MODES = ('PRE_EARNINGS_RUNUP', 'HOLD_THROUGH_EARNINGS',
         'POST_EARNINGS_REACTION', 'POST_EARNINGS_DRIFT')

CONFIG = {
    'pre_earnings_runup_allowed': True,
    'default_exit_before_announcement': True,
    'hold_through_earnings_default': False,
    'post_earnings_reaction_allowed': True,
    'post_earnings_drift_allowed': True,
}

FORBIDDEN_LANGUAGE = ('99 % sûr', '99% sûr', 'garanti', 'certain', 'sans risque')

HOLD_THROUGH_REQUIRED = (
    'mode_explicitly_enabled',    # activation explicite du mode
    'date_confirmed',             # date confirmée (réconciliée entre sources)
    'expected_move',              # expected move disponible
    'historical_reaction',        # réaction historique connue
    'implied_volatility',         # IV connue
    'iv_crush_estimate',          # IV crush estimé
    'adverse_gap_scenario',       # scénario gap défavorable simulé
    'max_loss_known',             # perte maximale calculée
    'data_quality_ok',            # qualité des données suffisante
)


def sanitize_language(text: str) -> str:
    """Neutralise tout langage de certitude interdit."""
    out = text
    for phrase in FORBIDDEN_LANGUAGE:
        if phrase.lower() in out.lower():
            idx = out.lower().index(phrase.lower())
            out = out[:idx] + 'probabilité estimée, aucune promesse' + out[idx + len(phrase):]
    return out


def evaluate_earnings_plan(earnings_in_days: int | None, config: dict | None = None,
                           hold_through_dossier: dict | None = None) -> dict:
    """Décision de plan autour des résultats pour une option détenue/candidate."""
    cfg = dict(CONFIG)
    cfg.update(config or {})
    plan = {'mode': None, 'exit_before_announcement': False,
            'hold_through_allowed': False, 'missing_requirements': [],
            'notes': []}
    if earnings_in_days is None:
        plan['notes'].append('date de résultats inconnue — aucune décision earnings possible')
        return plan
    if earnings_in_days < 0:
        days_since = -earnings_in_days
        if days_since <= 2 and cfg['post_earnings_reaction_allowed']:
            plan['mode'] = 'POST_EARNINGS_REACTION'
        elif cfg['post_earnings_drift_allowed']:
            plan['mode'] = 'POST_EARNINGS_DRIFT'
        return plan
    if earnings_in_days <= 10:
        dossier = hold_through_dossier or {}
        missing = [k for k in HOLD_THROUGH_REQUIRED if not dossier.get(k)]
        plan['missing_requirements'] = missing
        if not missing and not cfg['hold_through_earnings_default']:
            plan['mode'] = 'HOLD_THROUGH_EARNINGS'
            plan['hold_through_allowed'] = True
            plan['notes'].append('dossier complet — décision spécifique à l’événement requise, '
                                 'résultat jamais garanti')
        else:
            plan['mode'] = 'PRE_EARNINGS_RUNUP' if cfg['pre_earnings_runup_allowed'] else None
            plan['exit_before_announcement'] = cfg['default_exit_before_announcement']
            if missing:
                plan['notes'].append(f'tenir à travers les résultats refusé — manque: {missing}')
    else:
        if cfg['pre_earnings_runup_allowed']:
            plan['mode'] = 'PRE_EARNINGS_RUNUP'
            plan['exit_before_announcement'] = cfg['default_exit_before_announcement']
    return plan
