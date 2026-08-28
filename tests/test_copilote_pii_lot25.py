"""tests/test_copilote_pii_lot25.py — LOT 25 : minimisation PII du copilote.

Contrat IA (ai-decision-contract) : « le portefeuille est exclu par défaut
et minimisé seulement après action explicite ». Le copilote transmettait
positions déclarées ET post-mortem du journal à CHAQUE question. Nés
ROUGES. L'exclusion est DITE au modèle (sinon Claude répondrait « aucune
position » — un mensonge) et le repli ne compte jamais une chaîne.
"""
import json

from vertex.ai import copilot


def test_les_positions_sont_exclues_par_defaut():
    ctx = copilot.build_context({}, None)
    assert not isinstance(ctx.get('positions'), list), (
        'les positions déclarées ne partent plus dans le prompt sans action explicite')
    assert 'postmortem' not in ctx
    #  et l'exclusion est DITE : le modèle ne doit pas conclure « aucune position »
    assert 'NON_TRANSMISES' in json.dumps(ctx, ensure_ascii=False, default=str)


def test_l_action_explicite_les_transmet():
    ctx = copilot.build_context({}, None, avec_positions=True)
    assert isinstance(ctx.get('positions'), list)


def test_la_route_lit_l_action_explicite(monkeypatch):
    import terminal
    vus = {}
    from vertex.ai import copilot as cp

    def _spy(question, scan_state, symbol=None, avec_positions=False):
        vus['avec'] = avec_positions
        return {'ok': True, 'answer': 'x', 'source': 'deterministic',
                'model': None, 'symbol': symbol, 'label': 'l', 'readonly': True}
    monkeypatch.setattr(cp, 'answer', _spy)
    c = terminal.app.test_client()
    c.post('/api/copilot/ask', json={'question': 'q'})
    assert vus['avec'] is False
    c.post('/api/copilot/ask', json={'question': 'q', 'avec_positions': True})
    assert vus['avec'] is True


def test_le_repli_ne_compte_jamais_la_chaine_d_exclusion():
    #  ctx['positions'] est une chaîne quand exclues : len() la compterait.
    txt = copilot._fallback({'positions': 'NON_TRANSMISES (vie privée)'}, None)
    assert 'position(s) déclarée(s)' not in txt


def test_les_deux_panneaux_ui_offrent_le_choix_explicite():
    from vertex.ui.pages import analysis_page
    html = analysis_page.render(sym='NVDA')
    assert 'avec_positions' in html, 'panneau copilote du dossier Analyse'
    js = open('vertex/static/vertex/js/pages/options-gex.js', encoding='utf-8').read()
    assert 'avec_positions' in js, 'panneau copilote GEX'
