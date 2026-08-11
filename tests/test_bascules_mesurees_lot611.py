"""LOT 611 — LA COUVERTURE DE LA MESURE RESPONSIVE, ÉPINGLÉE.

Le lot 610 a trouvé un bandeau écrasé à 22 px et l'a corrigé par une règle de
famille. Il n'avait mesuré que **deux largeurs**. Le lot 611 a mesuré **les neuf
bandes** déclarées par les feuilles servies : **144 mesures, zéro fautive**.

Cette conclusion repose sur une hypothèse : **la liste des bascules**. Si
quelqu'un ajoute une `@media (max-width:…)` ailleurs, une bande neuve apparaît —
**non mesurée**, et la phrase « les neuf bandes sont saines » devient périmée
sans que rien ne le dise.

Ce gardien épingle donc **l'ensemble des bascules de largeur des feuilles
servies**. Il n'empêche pas d'en ajouter une : il exige qu'on **re-mesure** et
qu'on mette la liste à jour dans le même geste.

*(Mon propre piège du 611 parlait de « quatre bascules » d'après `responsive.css`
seul ; il y en a **huit**. Un périmètre qui exclut une partie du code conclut
faux — même famille que 605-C. C'est cette erreur que le gardien empêche de
répéter.)*
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CSS_DIR = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css')

# Les bascules de LARGEUR mesurées au lot 611. Les requêtes de préférence
# (`prefers-reduced-motion`) ne sont pas des bascules de largeur.
_BASCULES = (520, 640, 720, 768, 820, 900, 1024, 1280)

# Les largeurs effectivement exercées en navigateur au lot 611 — une par bande.
_MESUREES = (390, 600, 700, 768, 800, 900, 1024, 1180, 1440)


def _bascules_du_depot():
    trouvees = set()
    for nom in sorted(os.listdir(_CSS_DIR)):
        if not nom.endswith('.css'):
            continue
        src = io.open(os.path.join(_CSS_DIR, nom), encoding='utf-8').read()
        for m in re.finditer(r"@media[^{]*?\(\s*max-width\s*:\s*(\d+)px", src):
            trouvees.add(int(m.group(1)))
    return trouvees


def test_les_bascules_de_largeur_sont_celles_qui_ont_ete_mesurees():
    trouvees = _bascules_du_depot()
    neuves = sorted(trouvees - set(_BASCULES))
    disparues = sorted(set(_BASCULES) - trouvees)
    assert not neuves, (
        'Bascule(s) de largeur AJOUTÉE(S) depuis le lot 611 : %s.\n'
        'Une bascule neuve crée une bande neuve, JAMAIS MESURÉE — et la '
        'conclusion « les neuf bandes sont saines » devient périmée en silence.\n'
        'À faire : re-mesurer avec le banc du 611 (chaque bandeau contre son '
        'parent), puis mettre `_BASCULES` et `_MESUREES` à jour.' % neuves)
    assert not disparues, (
        'Bascule(s) RETIRÉE(S) : %s. La couverture du 611 ne correspond plus au '
        'produit ; re-mesurer et mettre la liste à jour.' % disparues)


def test_chaque_bande_a_ete_exercee():
    """Garde-fou de volume (591-C) : si `_MESUREES` se vidait, le test ci-dessus
    passerait encore alors que plus rien n'aurait été exercé."""
    bornes = sorted(_BASCULES)
    bandes = []
    bas = 0
    for b in bornes:
        bandes.append((bas + 1, b))
        bas = b
    bandes.append((bas + 1, 10 ** 6))
    non_couvertes = [(a, b) for a, b in bandes
                     if not any(a <= w <= b for w in _MESUREES)]
    assert not non_couvertes, (
        'bande(s) sans aucune largeur exercée : %s' % non_couvertes)
    assert len(_MESUREES) >= len(bandes), (
        'moins de largeurs exercées (%d) que de bandes (%d)'
        % (len(_MESUREES), len(bandes)))


def test_la_regle_de_famille_du_610_est_toujours_la():
    """La mesure du 611 vaut POUR UN PRODUIT QUI PORTE cette règle. Si elle
    disparaissait, « zéro fautive » ne dirait plus rien."""
    src = io.open(os.path.join(_CSS_DIR, 'layout.css'), encoding='utf-8').read()
    assert '.vx-grid > .vx-error-banner' in src.replace('.vx-grid>', '.vx-grid > ')
    assert '1 / -1' in src
