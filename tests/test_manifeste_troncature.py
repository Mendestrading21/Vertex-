"""tests/test_manifeste_troncature.py — contrôle 096 : manifeste d'omission.

Mesuré : le copilote tronquait son contexte par `json.dumps(ctx)[:14000]` —
un couteau en plein JSON (payload INVALIDE) et aucun aveu de ce qui manque.
Cible : bornage par RETRAIT DE SECTIONS ENTIÈRES, ordre de priorité
documenté, manifeste des éléments omis transmis AU MODÈLE (il peut dire
« donnée non transmise » au lieu d'halluciner). Nés ROUGES.
"""
import json

from vertex.ai import copilot


def test_un_contexte_court_part_entier_sans_manifeste():
    payload, omis = copilot._borner_contexte({'digest': {'a': 1}}, max_chars=14000)
    d = json.loads(payload)                      # JSON VALIDE
    assert d['digest'] == {'a': 1}
    assert omis == []
    assert 'manifeste_troncature' not in d


def test_un_contexte_trop_gros_perd_des_sections_entieres_et_l_avoue():
    gros = {'detail': {'price': 100}, 'positioning': {'x': 1},
            'digest': {'d': 2}, 'synthesis': {'narrative': 'n'},
            'flow': ['f' * 400] * 20, 'postmortem': {'p' * 50: 'q' * 4000}}
    payload, omis = copilot._borner_contexte(gros, max_chars=2000)
    d = json.loads(payload)                      # JAMAIS un JSON coupé au couteau
    assert len(payload) <= 2000
    assert omis, 'des sections ont forcément été retirées'
    #  le manifeste est DANS le payload : le modèle sait ce qui manque
    m = d['manifeste_troncature']
    assert m['elements_omis'] == omis
    assert 'budget' in m['raison']
    #  l'essentiel (detail, positioning) survit aux retraits prioritaires
    assert 'detail' in d and 'positioning' in d


def test_l_ordre_de_priorite_sacrifie_le_postmortem_avant_le_positionnement():
    gros = {'positioning': {'x': 'y' * 500}, 'postmortem': {'p': 'q' * 500},
            'detail': {'price': 1}}
    payload, omis = copilot._borner_contexte(gros, max_chars=900)
    assert 'postmortem' in omis
    assert 'positioning' not in omis


def test_answer_utilise_le_bornage(monkeypatch):
    import anthropic
    vus = {}

    class _Client:
        def __init__(self):
            self.messages = self

        def create(self, **kw):
            vus['contenu'] = kw['messages'][0]['content']

            class _M:
                pass
            m = _M(); b = _M(); b.text = 'ok'; m.content = [b]
            return m
    monkeypatch.setattr(copilot.briefs, 'available', lambda: True)
    monkeypatch.setattr(anthropic, 'Anthropic', lambda: _Client())
    from vertex.ai import gateway
    gateway.reset_for_test()
    copilot.answer('q ?', {}, 'AAPL')
    #  le JSON transmis est VALIDE (extrait entre l'en-tête et la question)
    corps = vus['contenu'].split('CONTEXTE JSON (données réelles Vertex) :\n', 1)[1]
    corps = corps.rsplit('\n\nQUESTION :', 1)[0]
    json.loads(corps)
