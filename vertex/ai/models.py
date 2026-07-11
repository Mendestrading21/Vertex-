"""vertex.ai.models — structures d'échange avec l'analyste IA."""
from __future__ import annotations

from dataclasses import dataclass, field

# Schéma STRICT de la réponse d'analyse (§28) — toute réponse est validée.
ANALYSIS_RESPONSE_SCHEMA = {
    'required': {
        'summary': str,          # synthèse de la thèse
        'bull_case': str,        # arguments haussiers
        'bear_case': str,        # avocat du diable
        'contradictions': list,  # contradictions relevées entre moteurs
        'anomaly_reading': str,  # lecture des anomalies
        'confidence_comment': str,
    },
    'optional': {
        'catalyst_view': str,
        'scenario_comparison': str,
        'questions_for_user': list,
        'proposed_notes': list,
    },
    'forbidden_keys': ('order', 'orders', 'execute', 'trade_now', 'position_size_final'),
}


@dataclass
class AnalysisRequest:
    symbol: str
    packet: dict = field(default_factory=dict)      # sorties des moteurs déterministes
    question: str = ''
    user_notes: str = ''


@dataclass
class AnalysisResult:
    ok: bool
    source: str                  # 'claude' | 'deterministic-fallback'
    content: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)
    model: str = ''
