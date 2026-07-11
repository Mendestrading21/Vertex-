"""vertex.ai.fallback — repli déterministe quand Claude échoue (§28).

Vertex continue SANS IA : la synthèse est composée mécaniquement depuis les
sorties des moteurs déterministes. Moins élégant, jamais bloquant.
"""
from __future__ import annotations

from .models import AnalysisResult


def deterministic_analysis(packet: dict) -> AnalysisResult:
    tech = packet.get('technical') or {}
    fund = packet.get('fundamental') or {}
    anomalies = packet.get('anomalies') or []
    scores = packet.get('scores') or {}
    decision = packet.get('final_decision', 'ATTENDRE')

    bull, bear = [], []
    if (fund.get('score') or 0) >= 65:
        bull.append('fondamental solide')
    elif fund.get('score') is not None and fund['score'] < 45:
        bear.append('fondamental fragile')
    if tech.get('reward_risk') and tech['reward_risk'] >= 2:
        bull.append(f"R:R structurel {tech['reward_risk']}")
    if tech.get('overextended'):
        bear.append('titre surétendu')
    blocking = packet.get('blocking_rules') or []
    if blocking:
        bear.append(f'règles bloquantes actives: {blocking}')
    codes = [a.get('code') if isinstance(a, dict) else getattr(a, 'code', '?')
             for a in anomalies]

    content = {
        'summary': f"Analyse déterministe (IA indisponible) — décision moteur: {decision}. "
                   f"Conviction {scores.get('conviction', 'n/d')}, "
                   f"asymétrie {scores.get('asymmetry', 'n/d')}.",
        'bull_case': ' · '.join(bull) or 'aucun argument haussier fort relevé par les moteurs',
        'bear_case': ' · '.join(bear) or 'aucun signal d’alerte majeur relevé par les moteurs',
        'contradictions': [],
        'anomaly_reading': f'anomalies détectées: {codes}' if codes else 'aucune anomalie détectée',
        'confidence_comment': 'synthèse mécanique sans interprétation IA — '
                              'les chiffres des moteurs font foi',
    }
    return AnalysisResult(ok=True, source='deterministic-fallback', content=content)
