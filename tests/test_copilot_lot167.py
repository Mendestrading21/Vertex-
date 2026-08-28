"""
LOT 167 — Caractérisation étendue du copilote d'analyse
(`vertex/ai/copilot.py`, ratio 0.37 — les 5 tests existants couvrent
l'ancrage, le repli et le prompt ; ceux-ci figent les LACUNES :
positions du desk, contexte sans symbole, post-mortem, chemin Claude
mocké et ses replis, normalisation). Anthropic entièrement mocké —
aucun appel réseau.
"""

import json
import types

import pytest

from vertex.ai import briefs
from vertex.ai import copilot
from vertex.services import persist


@pytest.fixture(autouse=True)
def _isole(monkeypatch, tmp_path):
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    yield


SS = {'rows': [{'symbol': 'MSFT', 'score': 72}], 'scan_ts': 1700000000,
      'market_ctx': {'roro': 'RISK-ON', 'spy_regime': 'UP'}, 'detail': {}}


class _FakeClient:
    def __init__(self, text=None, raise_=False):
        self.text, self.raise_ = text, raise_

    @property
    def messages(self):
        return self

    def create(self, **kw):
        if self.raise_:
            raise RuntimeError('api down')
        return types.SimpleNamespace(
            content=[types.SimpleNamespace(text=self.text)])


# ── _positions_for : le desk réel, jamais inventé ────────────────────────────

def test_positions_filtre_cap_20_et_stop_du_snapshot():
    trades = [{'sym': 'MSFT', 'type': 'STK', 'qty': 10, 'cost': 1000,
               'entrySnap': {'stop': 420}},
              {'sym': 'AAPL', 'type': 'CALL', 'qty': 1},
              'brut', {'autre': 1}] + \
             [{'sym': 'MSFT', 'qty': i} for i in range(25)]
    persist.save_json('desk_data.json',
                      {'ts': 1, 'data': {'myTrades': json.dumps(trades)}})
    assert len(copilot._positions_for()) == 20            # borné à 20
    msft = copilot._positions_for('MSFT')
    assert len(msft) == 20 and msft[0]['stop'] == 420     # stop du snapshot d'entrée
    assert all(isinstance(x, dict) for x in msft)         # entrées brutes exclues


def test_positions_desk_illisible_liste_vide():
    assert copilot._positions_for() == []                 # pas de blob → []


# ── build_context : sans symbole, et post-mortem inclus ──────────────────────

def test_contexte_sans_symbole_pas_de_positionnement():
    ctx = copilot.build_context(SS)
    assert sorted(ctx) == ['digest', 'positions']         # ni positioning ni flow


def test_postmortem_inclus_quand_trades_clotures():
    persist.save_json('desk_data.json', {'ts': 1, 'data': {
        'myTrades': '[]',
        'myTradesClosed': json.dumps([{'sym': 'AAPL', 'cost': 1000, 'exit': 1300}]),
        'vxJournal': '[]'}})
    #  Lot 25 : le post-mortem (données personnelles) exige l'action
    #  explicite — exclu par défaut, comme les positions.
    assert 'postmortem' not in copilot.build_context(SS)
    ctx = copilot.build_context(SS, avec_positions=True)
    assert ctx['postmortem']['total_pnl'] == 300.0
    assert ctx['postmortem']['trades_n'] == 1


# ── answer : normalisation, chemin Claude mocké, replis ──────────────────────

def test_symbole_majuscules_et_tronque_a_12(monkeypatch):
    monkeypatch.setattr(briefs, 'available', lambda: False)
    d = copilot.answer('Question ?', SS, symbol='msftmsftmsftmsft')
    assert d['symbol'] == 'MSFTMSFTMSFT' and len(d['symbol']) == 12


def test_chemin_claude_succes_etiquete_estimation(monkeypatch):
    import anthropic
    monkeypatch.setattr(briefs, 'available', lambda: True)
    monkeypatch.setattr(anthropic, 'Anthropic',
                        lambda: _FakeClient(text='Synthèse ancrée.'))
    d = copilot.answer('Q ?', SS, symbol='MSFT')
    assert d['source'] == 'claude' and d['answer'] == 'Synthèse ancrée.'
    # L'étiquette dit que c'est une ESTIMATION, jamais une donnée broker.
    assert 'estimation' in d['label'] and 'pas une donnée broker' in d['label']
    assert d['readonly'] is True


def test_claude_texte_vide_ou_exception_repli_deterministe(monkeypatch):
    import anthropic
    monkeypatch.setattr(briefs, 'available', lambda: True)
    monkeypatch.setattr(anthropic, 'Anthropic', lambda: _FakeClient(text=''))
    assert copilot.answer('Q ?', SS)['source'] == 'deterministic'
    monkeypatch.setattr(anthropic, 'Anthropic', lambda: _FakeClient(raise_=True))
    d = copilot.answer('Q ?', SS)
    assert d['ok'] is True and d['source'] == 'deterministic'
    assert 'Moteurs déterministes' in d['label']          # jamais d'exception


def test_contexte_indisponible_erreur_honnete(monkeypatch):
    from vertex.engines import session_digest
    def _boom(*a, **k):
        raise RuntimeError('boom')
    monkeypatch.setattr(session_digest, 'build', _boom)
    d = copilot.answer('Q ?', SS)
    assert d['ok'] is False
    assert d['error'].startswith('contexte indisponible')
    assert d['answer'] is None                            # pas de réponse inventée
