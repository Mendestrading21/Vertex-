"""vertex/engines/evidence_lab.py — LABORATOIRE D'ÉVIDENCE (SKYLER X2).

Question : « que s'est-il RÉELLEMENT passé après les événements passés ? »

Pour chaque spike historique (|z| ≥ 2, détecté par le moteur anomalies sur la
série de clôtures RÉELLE), on mesure — arithmétique exacte, aucune projection :

  - rendement forward à 1, 5 et 10 barres après l'événement ;
  - MFE (meilleure excursion) et MAE (pire excursion) sur les 10 barres suivantes ;

puis on agrège par direction (spikes haussiers / baissiers) en MÉDIANES.

Honnêteté : IN-SAMPLE et DESCRIPTIF — ce n'est PAS un backtest de stratégie
(aucune règle d'entrée/sortie simulée, aucun coût) ; un événement trop récent
(moins de 10 barres d'avenir) est compté NON MESURABLE, jamais extrapolé ;
série trop courte → indisponible. Fonction pure, déterministe. Aucun ordre.
"""
from __future__ import annotations

MIN_POINTS = 41          # 40 rendements — assez pour des spikes ET de l'avenir mesurable
HORIZON = 10             # barres d'avenir requises pour MFE/MAE


def _median(xs):
    xs = sorted(xs)
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2.0


def _bucket(events, closes):
    fwd1, fwd5, fwd10, mfe, mae = [], [], [], [], []
    for i in events:
        base = closes[i]
        fwd1.append((closes[i + 1] / base - 1) * 100)
        fwd5.append((closes[i + 5] / base - 1) * 100)
        fwd10.append((closes[i + 10] / base - 1) * 100)
        window = closes[i + 1:i + 1 + HORIZON]
        mfe.append((max(window) / base - 1) * 100)
        mae.append((min(window) / base - 1) * 100)
    r = lambda v: (round(v, 2) if v is not None else None)
    return {
        'n_measured': len(events),
        'median_fwd_1_pct': r(_median(fwd1)),
        'median_fwd_5_pct': r(_median(fwd5)),
        'median_fwd_10_pct': r(_median(fwd10)),
        'median_mfe_pct': r(_median(mfe)),
        'median_mae_pct': r(_median(mae)),
    }


def study(closes):
    """Statistiques ex post des spikes historiques d'une série de clôtures réelle."""
    from vertex.engines import anomaly as _an
    d = _an.scan(closes)
    if d.get('empty') or d['points'] < MIN_POINTS:
        return {'available': False,
                'reason': 'série trop courte (%s points, %d requis) — aucune statistique inventée'
                          % (d.get('points', 0), MIN_POINTS)}
    cl = d['closes']
    n = len(cl)
    spikes = [e for e in d['events'] if e.get('kind') == 'spike']
    measurable_up, measurable_down, unmeasurable = [], [], 0
    for e in spikes:
        i = e['i']
        if i + HORIZON < n:
            (measurable_up if e['ret_pct'] >= 0 else measurable_down).append(i)
        else:
            unmeasurable += 1
    measured = len(measurable_up) + len(measurable_down)
    return {
        'available': True, 'points': n,
        'n_events': len(spikes), 'n_unmeasurable': unmeasurable,
        'event_coverage': {'measured_events': measured, 'total_events': len(spikes),
                           'unmeasured_events': unmeasurable,
                           'coverage_pct': round(100 * measured / len(spikes), 1) if spikes else 0.0,
                           'read_only': True,
                           'note': 'événements trop récents exclus des médianes et jamais extrapolés'},
        'up': _bucket(measurable_up, cl),
        'down': _bucket(measurable_down, cl),
        'horizon_bars': HORIZON,
        'generator': 'deterministic',
        'note': 'Statistiques IN-SAMPLE sur la fenêtre du scan — descriptif, PAS un backtest '
                'de stratégie (aucune règle simulée, aucun coût) ; médianes exactes, '
                'événements trop récents comptés non mesurables.',
    }


__all__ = ['study']
