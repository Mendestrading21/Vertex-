"""tests/test_primitive_deborde_lot33.py — LOT 33 : le pied de primitive déborde.

Mesuré au navigateur (Portefeuille peuplé) : l'hôte du treemap est figé à
260 px (dimensionné pour le SVG seul) mais la primitive ajoute tête et
pied DEDANS → scrollHeight 294, le pied saigne sur « Composition du
capital ». La primitive libère la hauteur figée de son hôte et donne au
SVG sa hauteur en pixels — le conteneur suit alors son contenu. Né ROUGE.
"""


def _js():
    return open('vertex/static/vertex/js/charts/chart-core.js', encoding='utf-8').read()


def test_les_primitives_liberent_la_hauteur_figee_de_l_hote():
    js = _js()
    assert js.count("el.style.height = ''") >= 2, (
        'treemap ET waterfall doivent libérer la hauteur figée : la tête et '
        'le pied vivent dans l\'hôte, un height figé fait saigner le pied '
        'sur le bloc suivant (mesuré : 294 px de contenu dans 260 px)')


def test_le_svg_porte_sa_hauteur_en_pixels():
    js = _js()
    assert 'width="100%" height="100%" preserveAspectRatio="none"' not in js, (
        'un SVG à 100 % d\'un hôte figé ne laisse aucune place au pied')
    assert 'height="${H}"' in js
