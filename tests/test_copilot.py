"""tests/test_copilot.py — copilote d'analyse : ancrage réel + honnêteté + READONLY."""
import pytest

from vertex.ai import copilot
from vertex.services import persist


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    yield


def _scan_state():
    return {
        'rows': [{'symbol': 'MSFT', 'score': 72, 'price': 440}],
        'market_ctx': {'vix': 15.2, 'roro': 'RISK-ON', 'spy_regime': 'UP'},
        'committee': {'decisions': []},
        'detail': {'MSFT': {'price': 440, 'score': 72, 'earnings_in_days': 3}},
        'options_board': [
            {'sym': 'MSFT', 'type': 'CALL', 'strike': 460, 'gamma': 0.05, 'oi': 5000,
             'vol': 500, 'cost': 2000, 'spot': 440, 'dte': 21, 'iv': 30.0},
        ],
        'scan_ts': 1700000000,
    }


def test_context_is_grounded_in_real_numbers():
    ctx = copilot.build_context(_scan_state(), 'MSFT')
    assert ctx['positioning']['symbol'] == 'MSFT'
    assert ctx['positioning']['net_gex_total'] is not None
    assert ctx['synthesis']['bias'] in ('haussier', 'baissier', 'neutre')
    assert ctx['detail']['price'] == 440
    #  Lot 25 : positions exclues par défaut (vie privée), transmises sur
    #  action explicite seulement — et l'exclusion est DITE au modèle.
    assert 'NON_TRANSMISES' in str(ctx['positions'])
    ctx2 = copilot.build_context(_scan_state(), 'MSFT', avec_positions=True)
    assert isinstance(ctx2['positions'], list)


def test_answer_fallback_without_key_is_honest(monkeypatch):
    from vertex.ai import briefs
    monkeypatch.setattr(briefs, 'available', lambda: False)
    d = copilot.answer('Que dit le positionnement ?', _scan_state(), symbol='MSFT')
    assert d['ok'] is True
    assert d['source'] == 'deterministic'
    assert d['readonly'] is True
    assert 'ANTHROPIC_API_KEY' in d['answer']        # honnêteté : dit que Claude est absent
    assert 'ordre' not in (d['answer'] or '').lower() or 'aucun ordre' in (d['answer'] or '').lower() or 'aucune recommandation' in (d['answer'] or '').lower()


def test_empty_question_rejected():
    d = copilot.answer('', _scan_state())
    assert d['ok'] is False


def test_question_capped():
    d = copilot.answer('x' * 2000, _scan_state())
    assert d['ok'] is True          # traitée mais bornée (pas de crash)


def test_system_prompt_forbids_orders():
    assert 'JAMAIS' in copilot._SYSTEM and 'ordre' in copilot._SYSTEM
