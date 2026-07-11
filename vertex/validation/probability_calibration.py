"""vertex.validation.probability_calibration — calibration des probabilités (§30).

Toute probabilité affichée doit être calibrée. Sinon : « Confiance insuffisante ».
"""
from __future__ import annotations

import math

MIN_SAMPLE = 50
MAX_BRIER_FOR_DISPLAY = 0.30
MAX_CALIBRATION_GAP = 0.15    # écart moyen |prévu - observé| par décile
INSUFFICIENT = 'Confiance insuffisante'


def brier_score(forecasts: list[float], outcomes: list[int]) -> float | None:
    n = min(len(forecasts), len(outcomes))
    if n == 0:
        return None
    return round(sum((f - o) ** 2 for f, o in zip(forecasts[-n:], outcomes[-n:])) / n, 4)


def log_loss(forecasts: list[float], outcomes: list[int]) -> float | None:
    n = min(len(forecasts), len(outcomes))
    if n == 0:
        return None
    eps = 1e-9
    total = 0.0
    for f, o in zip(forecasts[-n:], outcomes[-n:]):
        f = min(max(f, eps), 1 - eps)
        total += -(o * math.log(f) + (1 - o) * math.log(1 - f))
    return round(total / n, 4)


def reliability_by_decile(forecasts: list[float], outcomes: list[int]) -> list[dict]:
    pairs = sorted(zip(forecasts, outcomes))
    if not pairs:
        return []
    out = []
    for d in range(10):
        bucket = [(f, o) for f, o in pairs if d / 10 <= f < (d + 1) / 10 or (d == 9 and f == 1.0)]
        if not bucket:
            continue
        mean_f = sum(f for f, _ in bucket) / len(bucket)
        mean_o = sum(o for _, o in bucket) / len(bucket)
        out.append({'decile': d, 'n': len(bucket), 'forecast': round(mean_f, 3),
                    'observed': round(mean_o, 3), 'gap': round(abs(mean_f - mean_o), 3)})
    return out


def temporal_stability(forecasts: list[float], outcomes: list[int]) -> dict:
    n = min(len(forecasts), len(outcomes))
    if n < 2 * MIN_SAMPLE:
        return {'stable': None, 'note': 'échantillon trop court pour juger la stabilité'}
    half = n // 2
    b1 = brier_score(forecasts[:half], outcomes[:half])
    b2 = brier_score(forecasts[half:n], outcomes[half:n])
    return {'stable': abs((b1 or 0) - (b2 or 0)) < 0.08,
            'brier_first_half': b1, 'brier_second_half': b2}


def calibration_report(forecasts: list[float], outcomes: list[int]) -> dict:
    n = min(len(forecasts), len(outcomes))
    rel = reliability_by_decile(forecasts[:n], outcomes[:n])
    gaps = [r['gap'] for r in rel if r['n'] >= 5]
    return {'sample_size': n,
            'brier': brier_score(forecasts, outcomes),
            'log_loss': log_loss(forecasts, outcomes),
            'reliability': rel,
            'mean_gap': round(sum(gaps) / len(gaps), 3) if gaps else None,
            'temporal': temporal_stability(forecasts, outcomes)}


def display_probability(prob: float | None, report: dict | None,
                        out_of_distribution: bool = False,
                        data_stale: bool = False,
                        model_in_drift: bool = False) -> dict:
    """Décide si une probabilité PEUT être affichée. Sinon 'Confiance insuffisante'."""
    reasons = []
    if prob is None:
        reasons.append('probabilité non calculée')
    if report is None:
        reasons.append('aucune mesure de calibration')
    else:
        if report['sample_size'] < MIN_SAMPLE:
            reasons.append(f"échantillon {report['sample_size']} < {MIN_SAMPLE}")
        if report['brier'] is not None and report['brier'] > MAX_BRIER_FOR_DISPLAY:
            reasons.append(f"Brier {report['brier']} > {MAX_BRIER_FOR_DISPLAY}")
        if report['mean_gap'] is not None and report['mean_gap'] > MAX_CALIBRATION_GAP:
            reasons.append(f"écart de calibration {report['mean_gap']} > {MAX_CALIBRATION_GAP}")
    if out_of_distribution:
        reasons.append('contexte hors distribution')
    if data_stale:
        reasons.append('données rassises')
    if model_in_drift:
        reasons.append('modèle en drift')
    if reasons:
        return {'display': INSUFFICIENT, 'probability': None, 'reasons': reasons}
    return {'display': f'{prob:.0%}', 'probability': prob, 'reasons': []}
