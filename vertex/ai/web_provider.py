"""vertex.ai.web_provider — Claude avec RECHERCHE WEB réelle (citations).

Quand l'app n'a pas d'accès live au marché, ce provider laisse Claude aller
chercher la VRAIE donnée du jour via l'outil de recherche web côté serveur
Anthropic, puis renvoie le texte AVEC ses citations (liens réels). Aucune
donnée n'est jamais inventée : ce qui remonte porte ses sources, et l'appelant
(enrichment) l'emballe en provenance « claude_web · différé · estimation ».

Lecture seule absolue : l'outil web ne fait que LIRE le web. Import paresseux —
l'app démarre sans clé ni dépendance ; sans clé, `available()` est False et
aucun chiffre n'est produit (repli honnête, jamais de fabrication).
"""
from __future__ import annotations

import json
import os

from .provider import AIProvider

MODEL = os.environ.get('VERTEX_AI_MODEL', os.environ.get('ANTHROPIC_MODEL', 'claude-sonnet-5'))
MAX_TOKENS = 3000
# L'outil de recherche web côté serveur Anthropic (lecture seule).
WEB_TOOL_TYPE = 'web_search_20250305'
DEFAULT_MAX_SEARCHES = 5


class ClaudeWebProvider(AIProvider):
    """Provider Anthropic + outil web_search. `research()` renvoie texte+citations."""

    name = 'claude_web'

    def __init__(self, api_key: str | None = None, model: str = MODEL,
                 max_searches: int = DEFAULT_MAX_SEARCHES) -> None:
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY', '')
        self.model = model
        self.max_searches = max_searches
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

    # ── extraction défensive (testable avec un faux message) ──────────────
    @staticmethod
    def _extract(msg) -> dict:
        """Rend {text, citations:[{title,url}], searches} depuis un message SDK."""
        text_parts: list[str] = []
        citations: list[dict] = []
        seen = set()
        searches = 0
        for block in getattr(msg, 'content', None) or []:
            btype = getattr(block, 'type', '') or (block.get('type', '') if isinstance(block, dict) else '')
            if btype == 'text':
                txt = getattr(block, 'text', None) or (block.get('text') if isinstance(block, dict) else '')
                if txt:
                    text_parts.append(txt)
                cits = getattr(block, 'citations', None) or (block.get('citations') if isinstance(block, dict) else None)
                for c in cits or []:
                    url = getattr(c, 'url', None) or (c.get('url') if isinstance(c, dict) else None)
                    title = getattr(c, 'title', None) or (c.get('title') if isinstance(c, dict) else None)
                    if url and url not in seen:
                        seen.add(url)
                        citations.append({'title': (title or url)[:200], 'url': url})
            elif btype in ('server_tool_use', 'web_search_tool_result'):
                searches += 1
        return {'text': ''.join(text_parts), 'citations': citations,
                'searches': searches}

    def research(self, system_prompt: str, user_prompt: str) -> dict:
        """Appelle Claude+web. Rend {text, citations, model, searches}. Lève sur échec."""
        client = self._get_client()
        msg = client.messages.create(
            model=self.model, max_tokens=MAX_TOKENS, system=system_prompt,
            messages=[{'role': 'user', 'content': user_prompt}],
            tools=[{'type': WEB_TOOL_TYPE, 'name': 'web_search',
                    'max_uses': self.max_searches}])
        out = self._extract(msg)
        out['model'] = getattr(msg, 'model', self.model)
        return out

    def research_json(self, system_prompt: str, user_prompt: str) -> dict:
        """Comme research() mais extrait aussi le 1er objet JSON du texte (structuré)."""
        out = self.research(system_prompt, user_prompt)
        text = out.get('text') or ''
        start, end = text.find('{'), text.rfind('}')
        out['data'] = None
        if 0 <= start < end:
            try:
                out['data'] = json.loads(text[start:end + 1])
            except (ValueError, TypeError):
                out['data'] = None
        return out

    # Compat interface AIProvider.analyze (non utilisée pour le web).
    def analyze(self, system_prompt: str, user_prompt: str) -> dict:
        return self.research_json(system_prompt, user_prompt)


__all__ = ['ClaudeWebProvider', 'WEB_TOOL_TYPE', 'MODEL']
