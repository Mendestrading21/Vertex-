"""tests/test_a11y_lighthouse.py — contrôle 131 : défauts Lighthouse.

Premier passage Lighthouse réel (12 pages, émulation mobile standard) :
a11y 96-100. Trois défauts réels relevés — nés ROUGES :
- heading-order (accueil, simulateur) : le titre de carte vx2 était un
  <h3> directement sous le <h1> de page (saut de niveau) ;
- target-size (performance) : les <summary> des sections repliables
  n'atteignaient pas la taille tactile minimale.
"""
from vertex.ui import vx2


def test_le_titre_de_carte_vx2_est_un_h2():
    html = vx2.surface('x', titre='Test')
    assert '<h2 class="vx2-card-title">' in html
    assert '<h3 class="vx2-card-title">' not in html


def test_les_summary_ont_une_taille_tactile():
    css = open('vertex/static/vertex/css/vertex-2-0.css', encoding='utf-8').read()
    flat = css.replace(' ', '')
    assert 'details>summary{' in flat and 'min-height:24px' in flat, (
        'cible tactile minimale de 24px sur les résumés repliables '
        '(target-size, Lighthouse)')
