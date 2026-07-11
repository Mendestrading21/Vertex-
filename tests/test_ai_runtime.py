"""Runtime Claude (§28) : registre d'outils sans ordre, validation stricte,
repli déterministe."""
import pytest

from vertex.ai import tool_registry as TR
from vertex.ai.investment_agent import InvestmentAgent
from vertex.ai.models import AnalysisRequest
from vertex.ai.provider import AIProvider
from vertex.ai.rate_limits import RateLimiter
from vertex.ai.response_validator import validate_analysis


def valid_payload(**kw):
    p = {'summary': 'Thèse haussière portée par les fondamentaux.',
         'bull_case': 'croissance forte',
         'bear_case': 'valorisation tendue',
         'contradictions': ['comité optimiste vs anomalie de distribution'],
         'anomaly_reading': 'volume spike = proxy à confirmer',
         'confidence_comment': 'conviction modérée, données fraîches'}
    p.update(kw)
    return p


# ── Registre d'outils ─────────────────────────────────────────────────
def test_ai_registry_contains_no_order_tool():
    assert not (set(TR.ALLOWED_TOOLS) & set(TR.FORBIDDEN_TOOLS))
    for name in TR.FORBIDDEN_TOOLS:
        assert name not in TR.ALLOWED_TOOLS
    reg = TR.ToolRegistry()
    for name in ('place_order', 'modify_order', 'cancel_order', 'exercise_option',
                 'transfer_cash', 'change_constitution', 'activate_rule',
                 'delete_history'):
        with pytest.raises(TR.ForbiddenToolError):
            reg.register(name, lambda: None)
    with pytest.raises(TR.ForbiddenToolError):
        reg.register('mon_outil_maison', lambda: None)  # hors liste blanche


def test_registry_allows_read_and_proposal_tools():
    reg = TR.ToolRegistry()
    reg.register('get_strategy', lambda: {'ok': True})
    reg.register('propose_alert', lambda **kw: {'status': 'PROPOSED'})
    assert reg.call('get_strategy') == {'ok': True}
    specs = {s['name']: s for s in reg.specs()}
    assert specs['get_strategy']['read_only'] is True
    assert specs['propose_alert']['read_only'] is False


# ── Validation stricte ────────────────────────────────────────────────
def test_valid_response_passes():
    ok, errors = validate_analysis(valid_payload())
    assert ok, errors


def test_missing_keys_and_forbidden_keys_fail():
    ok, errors = validate_analysis({'summary': 'x'})
    assert not ok
    ok2, errors2 = validate_analysis(valid_payload(order={'symbol': 'NVDA'}))
    assert not ok2 and any('interdite' in e for e in errors2)
    ok3, errors3 = validate_analysis(valid_payload(hallucination='libre'))
    assert not ok3 and any('inconnues' in e for e in errors3)


def test_certainty_language_rejected():
    ok, errors = validate_analysis(valid_payload(summary='Ce trade est garanti.'))
    assert not ok
    assert any('certitude' in e for e in errors)


# ── Repli déterministe ────────────────────────────────────────────────
class BrokenProvider(AIProvider):
    name = 'broken'
    def available(self):
        return True
    def analyze(self, s, u):
        raise TimeoutError('API down')


class BadSchemaProvider(AIProvider):
    name = 'bad'
    def available(self):
        return True
    def analyze(self, s, u):
        return {'summary': 'ok seulement'}


class GoodProvider(AIProvider):
    name = 'good'
    model = 'claude-test'
    def available(self):
        return True
    def analyze(self, s, u):
        return valid_payload()


def packet():
    return {'technical': {'reward_risk': 2.2, 'score': 75},
            'fundamental': {'score': 70},
            'scores': {'conviction': 72, 'asymmetry': 48},
            'final_decision': 'ATTENDRE', 'anomalies': [], 'blocking_rules': []}


def test_ai_failure_uses_deterministic_fallback():
    for provider in (None, BrokenProvider(), BadSchemaProvider()):
        agent = InvestmentAgent(provider=provider)
        res = agent.analyze(AnalysisRequest(symbol='NVDA', packet=packet()))
        assert res.ok is True
        assert res.source == 'deterministic-fallback'
        assert 'summary' in res.content
        ok, errs = validate_analysis(res.content)
        assert ok, f'le fallback doit lui-même respecter le schéma: {errs}'


def test_good_provider_used_when_valid():
    agent = InvestmentAgent(provider=GoodProvider())
    res = agent.analyze(AnalysisRequest(symbol='NVDA', packet=packet()))
    assert res.source == 'claude'
    assert res.model == 'claude-test'


def test_rate_limit_forces_fallback():
    agent = InvestmentAgent(provider=GoodProvider(),
                            rate_limiter=RateLimiter(max_calls=1))
    first = agent.analyze(AnalysisRequest(symbol='NVDA', packet=packet()))
    assert first.source == 'claude'
    second = agent.analyze(AnalysisRequest(symbol='AMD', packet=packet()))
    assert second.source == 'deterministic-fallback'
    assert any('débit' in e for e in second.errors)


def test_no_order_execution_path_in_ai_package():
    import inspect
    import vertex.ai.investment_agent, vertex.ai.tool_registry, vertex.ai.prompt_builder
    import vertex.ai.anthropic_provider, vertex.ai.fallback
    src = ''.join(inspect.getsource(m) for m in (
        vertex.ai.investment_agent, vertex.ai.prompt_builder,
        vertex.ai.anthropic_provider, vertex.ai.fallback))
    for needle in ('placeOrder', 'submit_order(', 'transmit_order(',
                   'exercise_option(', 'transfer_cash('):
        assert needle not in src
