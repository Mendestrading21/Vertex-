"""LOT 617 — LE PLAFOND DE HAUTEUR DES ÉTATS NE FAISAIT PAS CE QU'ON LUI PRÊTAIT.

`states.css` portait `.vx-state{… max-height:240px; justify-content:center}`, et
l'en-tête du fichier promettait « jamais un rectangle géant vide ».

**Le piège écrit d'avance disait « un plafond sans `overflow` fait DÉBORDER le
contenu ». Il est RÉFUTÉ.** Dans une boîte `flex-column`, les enfants sont
flexibles : un plafond ne rogne pas et ne fait pas déborder — il **comprime**.

Et la compression est **invisible à tout test de débordement**. Trois
instruments successifs ont été nécessaires, les deux premiers répondant
« aucun débordement » :

| instrument | verdict | pourquoi il était aveugle |
| --- | --- | --- |
| `scrollHeight > height` | **0** | `scrollHeight` rendait la valeur **déjà écrêtée** (238) |
| rect des enfants vs rect de la boîte | **0** | les enfants **rétrécissent** au lieu de sortir |
| `scrollHeight` de **chaque enfant** | **trouvé** | l'icône fantôme passait de **41 px à 31 px** |

Effet réel, mesuré à 390 px sur `/journal?view=track-record` : hauteur naturelle
**249 px** contre un plafond de 240, et les 9 px de compression étaient absorbés
**entièrement par l'icône fantôme décorative** (−24 %). **Aucun texte perdu,
aucun chevauchement, aucun rognage.** Un seul état du produit concerné ; **0 des
20 cartes ordinaires** mesurées ne plafonne sa hauteur.

Ce gardien tient les deux faces : le plafond **retiré**, et l'interdiction de le
remplacer par un rognage — ces zones existent pour **dire** pourquoi une donnée
manque, et amputer le motif serait pire que tout ce qui précède.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_STATES = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'states.css')


def _source_sans_commentaires():
    """Les commentaires du lot 617 CITENT `max-height` pour expliquer pourquoi il
    a été retiré : les compter reviendrait à interdire d'en parler."""
    return re.sub(r'/\*.*?\*/', '', io.open(_STATES, encoding='utf-8').read(), flags=re.S)


def _regle_vx_state():
    src = _source_sans_commentaires()
    m = re.search(r'\.vx-state\{([^}]*)\}', src)
    assert m, 'la règle `.vx-state` a disparu de states.css'
    return m.group(1)


def test_les_zones_d_etat_ne_plafonnent_plus_leur_hauteur():
    """Le correctif du 617. Un plafond dans une colonne flexible ne borne pas la
    boîte : il écrase ses enfants, en silence, et aucun test de débordement ne
    peut le voir."""
    regle = _regle_vx_state()
    assert 'max-height' not in regle, (
        '`.vx-state` a repris un `max-height`. Mesuré au lot 617 : dans une boîte '
        '`flex-column`, un plafond ne rogne pas et ne fait pas déborder — il '
        'COMPRIME les enfants flexibles, et la compression est invisible aux tests '
        'de débordement (deux instruments successifs ont répondu « aucun '
        'débordement » à tort). Si la hauteur redevient un sujet, raccourcir le '
        'TEXTE des messages.')


def test_les_zones_d_etat_ne_rognent_pas_leur_contenu():
    """L'INTERDIT QUE CE GARDIEN EXISTE POUR TENIR.

    Le réflexe, face à une zone trop haute, est d'ajouter `overflow:hidden`.
    Ce serait remplacer un texte trop long par un texte **amputé** — sur des
    zones dont le rôle est précisément de dire honnêtement pourquoi une donnée
    manque. Le motif tronqué est pire que la boîte trop haute.
    """
    regle = _regle_vx_state()
    for interdit in ('overflow:hidden', 'overflow: hidden',
                     'overflow-y:hidden', 'overflow-y: hidden'):
        assert interdit not in regle, (
            '`.vx-state` rogne son contenu (%s). Ces zones EXPLIQUENT une donnée '
            'absente : un motif coupé au milieu est un mensonge par omission. '
            'Laisser la boîte grandir, ou raccourcir le message.' % interdit)


def test_la_boite_reste_une_colonne_centree():
    """La mesure du 617 vaut pour cette mise en forme précise.

    C'est parce que la boîte est une `flex-column` que le plafond comprimait au
    lieu de rogner. Changer la mise en forme change le comportement, et rend la
    mesure — donc les deux tests ci-dessus — sans objet.
    """
    regle = _regle_vx_state()
    assert 'flex-direction:column' in regle.replace(' ', ''), (
        '`.vx-state` n\'est plus une colonne flexible : le raisonnement du lot 617 '
        'sur la compression ne s\'applique plus, re-mesurer')
    assert 'display:flex' in regle.replace(' ', ''), (
        '`.vx-state` n\'est plus un conteneur flex — re-mesurer')


def test_l_en_tete_ne_promet_plus_ce_qu_aucune_regle_ne_tient():
    """612-B appliqué à ce fichier.

    L'en-tête promettait « jamais un rectangle géant vide » et s'appuyait sur un
    plafond qui ne pouvait pas le garantir. Le plafond parti, la promesse doit
    partir avec lui — sinon le fichier décrit une intention que rien n'assure.
    """
    src = io.open(_STATES, encoding='utf-8').read()
    entete = src[:src.index('.vx-state{')]
    assert 'jamais un rectangle géant vide.' not in entete.replace('—', '.'), (
        "l'en-tête promet de nouveau « jamais un rectangle géant vide » alors "
        "qu'aucune règle ne le garantit")
    assert 'LOT 617' in entete, (
        "l'en-tête ne dit plus pourquoi le plafond a été retiré — la prochaine "
        'personne le remettra')
