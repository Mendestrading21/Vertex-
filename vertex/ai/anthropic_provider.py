"""vertex.ai.anthropic_provider — fournisseur Anthropic (optionnel).

Import paresseux : l'app démarre et fonctionne sans clé ni dépendance.
"""
from __future__ import annotations

import json
import os

from .health import resolve_model
from .provider import AIProvider

MAX_TOKENS = 2000


class AnthropicProvider(AIProvider):
    name = 'anthropic'

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY', '')
        # Résolution partagée avec /api/ai/status (VERTEX_AI_MODEL > ANTHROPIC_MODEL).
        self.model = model or resolve_model()
        self._client = None

    def available(self) -> bool:
        if not self.api_key:
            return False
        try:
            import anthropic  # noqa: F401
            return True
        except ImportError:
            return False

    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client

    def analyze(self, system_prompt: str, user_prompt: str) -> dict:
        client = self._get_client()
        msg = client.messages.create(
            model=self.model, max_tokens=MAX_TOKENS, system=system_prompt,
            messages=[{'role': 'user', 'content': user_prompt}])
        text = ''.join(block.text for block in msg.content
                       if getattr(block, 'type', '') == 'text')
        start, end = text.find('{'), text.rfind('}')
        if start < 0 or end <= start:
            raise ValueError('réponse sans JSON structuré')
        return json.loads(text[start:end + 1])
