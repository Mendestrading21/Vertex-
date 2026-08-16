"""Validation walk-forward descriptive des décisions Skyler mesurées.

La fonction ne relit ni ne réécrit le ledger et ne modifie aucun score. Elle
sépare les décisions par date de séance figée, puis écarte un embargo égal à
l'horizon mesuré avant chaque bloc de test. Ainsi, un résultat connu après une
décision d'entraînement ne peut pas être confondu avec une preuve disponible au
moment du bloc hors échantillon.
"""
from __future__ import annotations

import math
from datetime import date

from vertex.engines import decision_memory as _memory


HORIZON_SESSIONS = {'H5': 5, 'H10': 10, 'H15': 15, 'H20': 20, 'H60': 60}
MIN_TRAIN_DATES = 20
MIN_OOS_DATES = 10
MIN_FOLDS = 2
DEGRADATION_THRESHOLD = 0.20


def _session_date(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except (TypeError, ValueError):
        return None


def _samples(memory, engine_version, horizon):
    """Résultats mesurés, classés avec la taxonomie mémoire exacte."""
    decisions = {str(row.get('decision_id')): row for row in (memory or {}).get('decisions', [])
                 if isinstance(row, dict) and row.get('engine_version') == engine_version}
    samples, invalid_dates = [], 0
    for outcome in (memory or {}).get('outcomes', []):
        if not isinstance(outcome, dict):
            continue
        record = decisions.get(str(outcome.get('decision_id')))
        measure = (outcome.get('horizons') or {}).get(horizon) or {}
        ret = measure.get('return_pct')
        when = _session_date(record.get('session_date')) if record else None
        if record is None or measure.get('status') != 'MESURE' or not isinstance(ret, (int, float)):
            continue
        if not math.isfinite(float(ret)):
            continue
        if when is None:
            invalid_dates += 1
            continue
        classification = _memory.classify_error(record, float(ret), horizon).get('class')
        samples.append({'session_date': when.isoformat(), 'decision_id': record.get('decision_id'),
                        'hit': classification in ('DECISION_CORRECTE', 'VARIANCE_NORMALE'),
                        'return_pct': float(ret)})
    samples.sort(key=lambda item: (item['session_date'], str(item['decision_id'])))
    return samples, invalid_dates


def _summary(rows):
    count = len(rows)
    if not count:
        return {'n': 0, 'hit_rate': None, 'expectancy_pct': None}
    return {'n': count,
            'hit_rate': round(sum(1 for row in rows if row['hit']) / count, 3),
            'expectancy_pct': round(sum(row['return_pct'] for row in rows) / count, 3)}


def _by_date(samples):
    dates = {}
    for sample in samples:
        dates.setdefault(sample['session_date'], []).append(sample)
    return [(day, dates[day]) for day in sorted(dates)]


def assess(memory, engine_version, *, horizon='H10', min_train_dates=MIN_TRAIN_DATES,
           min_oos_dates=MIN_OOS_DATES, min_folds=MIN_FOLDS):
    """Compare entraînement et futur observé dans des fenêtres non chevauchantes.

    `horizon` est une limite de fuite : l'embargo entre le dernier jour de train
    et le premier jour OOS est au moins égal au nombre de séances du rendement
    mesuré. Les décisions sans date de séance sont refusées du diagnostic plutôt
    que replacées dans un ordre arbitraire d'écriture.
    """
    if horizon not in HORIZON_SESSIONS:
        return {'available': False, 'status': 'INVALID_HORIZON', 'horizon': horizon,
                'allowed': list(HORIZON_SESSIONS), 'read_only': True}
    if min_train_dates < 1 or min_oos_dates < 1 or min_folds < 2:
        return {'available': False, 'status': 'INVALID_CONFIGURATION', 'horizon': horizon,
                'read_only': True}

    samples, invalid_dates = _samples(memory, engine_version, horizon)
    dates = _by_date(samples)
    embargo = HORIZON_SESSIONS[horizon]
    required_dates = min_train_dates + min_folds * (embargo + min_oos_dates)
    base = {'engine_version': engine_version, 'horizon': horizon, 'read_only': True,
            'n_measured': len(samples), 'n_dated_sessions': len(dates),
            'n_excluded_missing_session_date': invalid_dates,
            'min_train_dates': min_train_dates, 'min_oos_dates': min_oos_dates,
            'min_folds': min_folds, 'embargo_sessions': embargo,
            'required_dated_sessions': required_dates}
    if invalid_dates:
        return {**base, 'available': False, 'status': 'TEMPORAL_EVIDENCE_REQUIRED',
                'reason': 'des résultats mesurés n’ont pas de date de séance figée',
                'note': 'aucune décision sans chronologie prouvée n’entre dans une validation hors échantillon'}
    if len(dates) < required_dates:
        return {**base, 'available': False, 'status': 'INSUFFICIENT_SAMPLE',
                'reason': '%d séance(s) datée(s) requise(s) ; %d disponible(s)' % (required_dates, len(dates)),
                'note': 'échantillon insuffisant : aucune conclusion de robustesse ou de surapprentissage'}

    folds, cursor = [], min_train_dates
    while cursor + embargo + min_oos_dates <= len(dates):
        train_dates = dates[:cursor]
        embargo_dates = dates[cursor:cursor + embargo]
        oos_dates = dates[cursor + embargo:cursor + embargo + min_oos_dates]
        train = [row for _, rows in train_dates for row in rows]
        oos = [row for _, rows in oos_dates for row in rows]
        ins = _summary(train)
        outs = _summary(oos)
        degradation = round(ins['hit_rate'] - outs['hit_rate'], 3)
        folds.append({'train_end': train_dates[-1][0],
                      'embargo_start': embargo_dates[0][0], 'embargo_end': embargo_dates[-1][0],
                      'oos_start': oos_dates[0][0], 'oos_end': oos_dates[-1][0],
                      'train': ins, 'out_of_sample': outs,
                      'hit_rate_degradation': degradation,
                      'degradation_flag': degradation >= DEGRADATION_THRESHOLD})
        cursor += embargo + min_oos_dates

    if len(folds) < min_folds:
        return {**base, 'available': False, 'status': 'INSUFFICIENT_SAMPLE',
                'reason': 'moins de %d fenêtre(s) hors échantillon complète(s)' % min_folds,
                'note': 'aucune conclusion de robustesse ou de surapprentissage'}
    degraded = sum(1 for fold in folds if fold['degradation_flag'])
    mean_is = round(sum(fold['train']['hit_rate'] for fold in folds) / len(folds), 3)
    mean_oos = round(sum(fold['out_of_sample']['hit_rate'] for fold in folds) / len(folds), 3)
    status = 'OOS_DEGRADED' if degraded >= math.ceil(len(folds) / 2) else 'OOS_CONSISTENT'
    return {**base, 'available': True, 'status': status, 'folds': folds,
            'n_folds': len(folds), 'n_degraded_folds': degraded,
            'mean_train_hit_rate': mean_is, 'mean_oos_hit_rate': mean_oos,
            'note': ('dégradation répétée entre entraînement et futur observé : revue humaine requise'
                     if status == 'OOS_DEGRADED' else
                     'fenêtres hors échantillon cohérentes à ce stade ; cela ne prouve ni rendement futur ni robustesse définitive')}


__all__ = ['assess', 'HORIZON_SESSIONS']
