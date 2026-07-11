"""vertex.scanner.scan_budget — budget d'un cycle de scan (entonnoir §14/§22).

Empêche le scanner de tout charger : chaque étage a un plafond de candidats,
seuls les survivants passent aux étages coûteux (options en dernier).
"""
from __future__ import annotations

DEFAULT_BUDGET = {
    'fundamental': 400,     # étage 1 : filtre large
    'catalysts': 200,
    'technical': 120,
    'sentiment': 80,
    'anomalies': 60,
    'portfolio': 40,
    'options': 15,          # SEULEMENT les finalistes déclenchent les chaînes
    'risk': 15,
    'decision': 10,
}


class ScanBudget:
    def __init__(self, overrides: dict | None = None) -> None:
        self.limits = dict(DEFAULT_BUDGET)
        self.limits.update(overrides or {})
        self.used: dict[str, int] = {}

    def cap(self, stage: str, candidates: list) -> list:
        limit = self.limits.get(stage, len(candidates))
        kept = candidates[:limit]
        self.used[stage] = len(kept)
        return kept

    def report(self) -> dict:
        return {'limits': dict(self.limits), 'used': dict(self.used)}
