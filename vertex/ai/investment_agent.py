"""vertex.ai.investment_agent — orchestration de l'analyste IA (§28).

Pipeline : contexte stratégique → prompt → provider → validation stricte →
repli déterministe si échec. Si Claude échoue, Vertex CONTINUE.
"""
from __future__ import annotations

import time

from .audit import AUDIT
from .fallback import deterministic_analysis
from .models import AnalysisRequest, AnalysisResult
from .prompt_builder import build_system_prompt, build_user_prompt
from .provider import AIProvider
from .rate_limits import RateLimiter
from .response_validator import validate_analysis


class InvestmentAgent:
    def __init__(self, provider: AIProvider | None = None,
                 rate_limiter: RateLimiter | None = None,
                 audit=AUDIT) -> None:
        self.provider = provider
        self.rate_limiter = rate_limiter or RateLimiter()
        self.audit = audit

    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        start = time.monotonic()
        errors: list[str] = []
        if self.provider is not None and self.provider.available():
            if not self.rate_limiter.allow():
                errors.append('limite de débit IA atteinte')
            else:
                try:
                    raw = self.provider.analyze(build_system_prompt(),
                                                build_user_prompt(request))
                    ok, verrors = validate_analysis(raw)
                    if ok:
                        result = AnalysisResult(ok=True, source='claude', content=raw,
                                                model=getattr(self.provider, 'model', ''))
                        self.audit.record(symbol=request.symbol, source='claude', ok=True,
                                          duration_ms=(time.monotonic() - start) * 1000,
                                          model=result.model)
                        return result
                    errors.extend(verrors)
                except Exception as exc:
                    errors.append(f'{exc.__class__.__name__}: {exc}')
        else:
            errors.append('fournisseur IA indisponible')
        # Repli déterministe : Vertex continue sans IA.
        result = deterministic_analysis(request.packet)
        result.errors = errors
        self.audit.record(symbol=request.symbol, source=result.source, ok=result.ok,
                          errors=errors, duration_ms=(time.monotonic() - start) * 1000)
        return result
