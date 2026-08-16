"""SIGNAL OS · LE ROGNAGE SILENCIEUX — les deux mécanismes trouvés, tenus.

L'instrument vit dans `tools/mesurer_rognage_silencieux.py` : il a besoin d'un
navigateur et d'un serveur, donc il ne tourne pas dans la suite. Ce fichier tient
les **corrections** qu'il a motivées, pour qu'un retour en arrière soit visible
sans avoir à relancer un navigateur.

## Ce que l'instrument a trouvé

| site | mécanisme | mesure |
| --- | --- | --- |
| Marchés · cartes macro | `grid-template-columns:1fr auto` + aire figée à 120 px | 5 px à 1440, 20-22 px à 390 |
| Marchés · carte macro FLAT | rangée **flex** : `min-width:auto` empêche la réduction | 20 px à 390 |
| Portefeuille · Surveillance | `.vx-truncate` dont le `white-space` est remis à `normal` en mode cartes | **37 px verticaux** à 390 |

Les trois partagent une propriété : **rien à l'écran ne dit qu'un mot est
coupé**. Pas d'ellipse, pas de barre de défilement. C'est ce qui les rend
invisibles à la relecture comme au test de débordement de page.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _css(nom):
    return io.open(os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', nom),
                   encoding='utf-8').read()


def _regle(css, selecteur):
    """Le bloc de déclarations d'UNE règle, sélecteur compris.

    Quatre de mes premières assertions cherchaient une déclaration dans TOUT le
    fichier : `flex-wrap:wrap` y figure des dizaines de fois, donc la retirer de
    la règle visée restait vert. Et `'.vx-table-cards td.vx-truncate' in css`
    restait vrai après un renommage en `td.vx-truncateX` — la chaîne cherchée
    est un PRÉFIXE de la chaîne mutée. Huitième fois que la portée me trompe
    dans cette refonte ; le motif ne varie pas.
    """
    bloc = None
    for m in re.finditer(re.escape(selecteur) + r'\s*\{([^}]*)\}', css):
        bloc = m.group(1)
        break
    if bloc is None:
        return None
    # Les COMMENTAIRES sont retirés. Piège rencontré ici même : mon commentaire
    # explicatif contient `minmax(0,1fr)` pour dire pourquoi la règle l'emploie,
    # si bien que le test restait vert après suppression de la DÉCLARATION.
    # Un test qui lit sa propre justification ne lit pas le code.
    return re.sub(r'/\*.*?\*/', '', bloc, flags=re.S)


def test_la_carte_macro_a_une_colonne_reductible():
    """`1fr` ne descend pas sous la largeur min-content de son contenu ;
    `minmax(0,1fr)` si. La différence entre les deux est exactement la
    différence entre une carte qui s'adapte et une carte qui coupe."""
    css = _css('neon-glass.css')
    bloc = _regle(css, '.vx-content[data-space="markets"] .vx-mk-macro')
    assert bloc is not None, 'la règle de la carte macro a disparu'
    assert 'grid-template-columns:minmax(0,1fr)' in bloc, (
        'la carte macro est revenue à une piste `1fr` : elle ne peut plus se '
        'réduire, et son overflow:hidden coupera le libellé sans le dire.')


def test_l_aire_de_la_carte_macro_se_reduit_avec_elle():
    """Une largeur FIXE dans une carte fluide est un rognage différé : il
    n'apparaît qu'en dessous d'une certaine largeur d'écran."""
    css = _css('neon-glass.css')
    bloc = _regle(css, '.vx-content[data-space="markets"] .vx-mk-macro .m-area')
    assert bloc is not None, 'la règle de l\'aire a disparu'
    assert 'min(120px' in bloc, (
        'l\'aire de la carte macro est redevenue une largeur fixe.')


def test_la_variante_flat_peut_passer_a_la_ligne():
    """CONTRE-EXEMPLE des deux tests précédents : la variante FLAT est en
    `flex`, donc le `minmax(0,1fr)` de la grille ne la protège pas. Elle a
    fallu la traiter séparément — et c'est le genre de détail qu'un correctif
    « sur la famille » manque."""
    css = _css('neon-glass.css')
    P = '.vx-content[data-space="markets"] .vx-mk-macro--flat '
    saut = _regle(css, P + '.mf-row,\n  ' + P + '.m-head')
    assert saut is not None and 'flex-wrap:wrap' in saut, (
        'la variante FLAT de la carte macro ne peut plus passer à la ligne. '
        '(`flex-wrap:wrap` doit être DANS cette règle : il figure des dizaines '
        'de fois ailleurs dans la feuille.)')
    reduc = _regle(css, P + '.m-val,\n  ' + P + '.m-name')
    assert reduc is not None and 'min-width:0' in reduc, (
        'les éléments de la variante FLAT ne sont plus réductibles : un flex '
        'item ne descend pas sous son min-content sans `min-width:0`.')


def test_une_cellule_tronquee_cesse_de_l_etre_en_mode_cartes():
    """Le mécanisme le plus retors des trois : `.vx-table-cards td` remet
    `white-space:normal` — avec une spécificité supérieure à `.vx-truncate` —
    donc le texte passe à la ligne, mais `overflow:hidden` et le `max-width` en
    ligne restent. La troncature à une ligne cesse d'être à une ligne, et ce
    qui dépasse est perdu VERTICALEMENT.
    """
    css = _css('tables.css')
    bloc = _regle(css, '.vx-table-cards td.vx-truncate')
    assert bloc is not None, (
        'la règle qui désactive la troncature en mode cartes a disparu : une '
        'cellule tronquée y perd du texte verticalement, sans ellipse. '
        '(Un simple `in css` restait vert sur un renommage en `truncateX` — '
        'la chaîne cherchée en est un préfixe.)')
    assert 'overflow:visible' in bloc, 'le débordement est de nouveau caché'
    assert 'max-width:none' in bloc, (
        'le `max-width` en ligne n\'est plus neutralisé : la cellule reste '
        'étroite et le texte continue de se replier dans une boîte trop petite.')


def test_l_instrument_est_conserve_avec_son_faux_positif_documente():
    """Un instrument qui disparaît laisse la dette revenir en silence — et
    celui-ci a mis six lots à exister. Son exclusion `.vx-sr-only` est aussi
    importante que sa mesure : sans elle, il rend 21 à 24 faux positifs et
    aucun signal."""
    outil = os.path.join(_ROOT, 'tools', 'mesurer_rognage_silencieux.py')
    assert os.path.isfile(outil), 'l\'instrument de rognage a disparu'
    src = io.open(outil, encoding='utf-8').read()
    # Portée : le CODE, pas la prose. « vx-sr-only » et « scrollHeight »
    # figurent aussi dans l'en-tête explicatif de l'outil — les y chercher
    # laissait passer leur retrait du code mesuré.
    code = src.split('JS = """', 1)[-1].split('"""', 1)[0]
    assert "classList.contains('vx-sr-only')" in code, (
        'l\'exclusion des textes réservés aux lecteurs d\'écran a sauté du '
        'CODE : l\'instrument va accuser l\'accessibilité (21 à 24 faux '
        'positifs mesurés) et noyer le signal réel.')
    # La COMPARAISON, pas la mention : `e.scrollHeight` figure aussi dans la
    # ligne qui rapporte l'écart, donc neutraliser le test le laissait vert.
    assert 'const debX = e.scrollWidth' in code and 'const debY = e.scrollHeight' in code, (
        'l\'instrument ne mesure plus les deux axes dans son code : le '
        'rognage VERTICAL était précisément celui que personne ne voyait.')
