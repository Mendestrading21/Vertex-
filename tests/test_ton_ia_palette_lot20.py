"""tests/test_ton_ia_palette_lot20.py — LOT 20 : violet hors options.

Palette stricte (« une couleur = une signification ») : le violet est
réservé aux OPTIONS. Mesuré : l'encart IA (`data-tone="ai"`, page
Vertex IA) portait un accent violet via glass.css. La couche de vérité
finale (vertex-2-0.css, chargée en dernier) doit le ramener à l'argent
structurel. Né ROUGE.
"""
import os

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CSS = os.path.join(_RACINE, 'vertex', 'static', 'vertex', 'css')


def test_le_ton_ai_n_est_pas_violet_dans_la_couche_finale():
    v2 = open(os.path.join(_CSS, 'vertex-2-0.css'), encoding='utf-8').read()
    assert 'data-tone="ai"' in v2, (
        'vertex-2-0.css (chargée en DERNIER) doit posséder la règle du ton '
        '« ai » — sinon glass.css le laisse violet')
    bloc = v2.split('data-tone="ai"', 1)[1][:200]
    assert '--vx-option' not in bloc and '--vx-violet' not in bloc and '--vx-options' not in bloc, (
        'violet = options uniquement — l\'IA prend l\'argent structurel')
