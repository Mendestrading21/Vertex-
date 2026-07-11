"""vertex.ai.provider — interface abstraite d'un fournisseur IA."""
from __future__ import annotations


class AIProvider:
    """Contrat minimal : analyze(system, user) -> dict structuré (ou lève)."""

    name = 'abstract'

    def available(self) -> bool:  # pragma: no cover - interface
        return False

    def analyze(self, system_prompt: str, user_prompt: str) -> dict:  # pragma: no cover
        raise NotImplementedError
