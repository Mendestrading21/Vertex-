"""LOT 612 — LES DEUX SEUILS DE CIBLE TACTILE, ET CE QU'ILS COUVRENT.

Mesuré en vrai Chromium à **390 px**, sur cinq écrans en état d'échec :

| famille | boutons | hauteur |
| --- | --- | --- |
| dans les bandeaux d'état | **20** | **32 px** |
| hors bandeaux (témoin, même page, même largeur) | **42** | 32 px (**20**) et 40 px (22) |

**Les boutons des bandeaux ne sont pas un angle mort** : 20 autres boutons du
produit sont au même 32 px. C'est une règle générale des actions **secondaires**,
appliquée uniformément — pas un oubli.

Ce que le lot 612 a corrigé n'est donc **pas le seuil**, mais **sa description** :
l'en-tête annonçait « Cibles tactiles ≥ 40px » **deux lignes au-dessus** d'un
`.vx-btn-sm{min-height:32px}`.

Ce gardien épingle les **deux** seuils. Il ne juge pas lequel est bon — il
empêche qu'un seul des deux bouge en silence, et que l'en-tête recommence à
annoncer autre chose que ce que le bloc fait.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CSS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'responsive.css')

# Les deux seuils, mesurés au lot 612.
_PRIMAIRE = 40
_SECONDAIRE = 32


def _bloc_tactile():
    """Le fragment qui porte les deux règles de hauteur minimale."""
    src = io.open(_CSS, encoding='utf-8').read()
    i = src.index('.vx-btn,.vx-tab,.vx-chip{min-height:')
    return src[max(0, i - 900):i + 200]


def test_le_seuil_des_actions_primaires_est_inchange():
    src = io.open(_CSS, encoding='utf-8').read()
    m = re.search(r"\.vx-btn,\.vx-tab,\.vx-chip\{min-height:(\d+)px\}", src)
    assert m, 'règle des actions primaires introuvable'
    assert int(m.group(1)) == _PRIMAIRE, (
        'seuil des actions PRIMAIRES passé de %d à %s px — mesure du lot 612 '
        'périmée, re-mesurer avant de publier' % (_PRIMAIRE, m.group(1)))


def test_le_seuil_des_actions_secondaires_est_inchange():
    src = io.open(_CSS, encoding='utf-8').read()
    m = re.search(r"\.vx-btn-sm\{min-height:(\d+)px\}", src)
    assert m, 'règle des actions secondaires introuvable'
    assert int(m.group(1)) == _SECONDAIRE, (
        'seuil des actions SECONDAIRES passé de %d à %s px. Ce seuil touche 40 '
        'boutons mesurés (20 dans les bandeaux, 20 ailleurs) : le changer est '
        'une décision de design, à documenter et re-mesurer.'
        % (_SECONDAIRE, m.group(1)))


def test_l_en_tete_ne_reannonce_pas_un_seuil_unique():
    """Le défaut corrigé au 612 : un en-tête qui promet « ≥ 40px » juste avant
    une exemption à 32. Une description qui contredit son bloc est la faute que
    la boucle corrige depuis le 602 — dire une chose, en faire une autre."""
    bloc = _bloc_tactile()
    entete = bloc[:bloc.index('.vx-btn,.vx-tab,.vx-chip{min-height:')]
    dernier_commentaire = entete[entete.rfind('/*'):] if '/*' in entete else ''
    assert 'exemption' in dernier_commentaire.lower() \
        or 'secondaire' in dernier_commentaire.lower(), (
        "l'en-tête doit dire que le bloc porte DEUX seuils, pas un — sinon il "
        "décrit une intention et non le code")


def test_les_deux_seuils_sont_nommes_dans_le_code():
    """Garde-fou de volume (591-C) : si les deux règles disparaissaient, les
    tests ci-dessus lèveraient une erreur d'introuvable plutôt que de passer à
    vide — mais si une seule restait, ce test le dit clairement."""
    src = io.open(_CSS, encoding='utf-8').read()
    n = len(re.findall(r"min-height:(?:%d|%d)px" % (_PRIMAIRE, _SECONDAIRE), src))
    assert n >= 2, (
        'attendu au moins deux règles de hauteur minimale (primaire ET '
        'secondaire), mesuré %d' % n)
