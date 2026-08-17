"""SIGNAL OS · LOT 30 — LA PANNE PARTIELLE, ET CE QUE JE N'AI PAS PU DÉCIDER.

Le lot 29 avait éprouvé les pannes **globales** et laissé une réserve écrite :
« une panne PARTIELLE est un régime différent, où un chiffre faux peut se
glisser entre des chiffres justes sans qu'aucun état d'erreur ne s'affiche ».

## Ce qui est mesuré, et sûr

Carte de **qui appelle quoi** (mesurée, pas supposée), puis six sources coupées
une à une — seules les vues concernées étant jugées.

**0 fuite technique, 0 erreur de page**, sur les six.

## Ce que je n'ai PAS pu décider

La question du « chiffre faux silencieux » n'est pas décidable sur le jeu de
démonstration. Trois méthodes essayées, trois familles de **faux positifs** que
j'ai dû réfuter :

1. comparer toutes les cellules avant/après — `e.className` vaut
   `[object SVGAnimatedString]` pour **tout** texte SVG, donc des valeurs sans
   rapport tombaient dans le même seau ;
2. ajouter un rang de fratrie à la clé — elle glisse dès que l'ordre de rendu
   change et désigne une autre cellule ;
3. exiger qu'une vue « signale » son manque — plusieurs sources n'apportent
   **rien** en démo (aucune position à valoriser pour `/api/pos-quotes`), donc
   leur panne ne peut rien changer : l'absence de signal n'y prouve rien.

Le seul candidat concret — une KPI de Système passant de « 8/8 » à « 0 » — a été
**réfuté en regardant l'écran** : la valeur est identique avec et sans panne.

> Conclure « propre » aurait affirmé plus que ce que la mesure permet. La
> réserve du lot 29 est donc **partiellement** levée, et le reste est écrit
> comme ouvert.
"""

import io
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OUTIL = os.path.join(_ROOT, 'tools', 'mesurer_panne_partielle.py')


def test_l_instrument_de_panne_partielle_est_conserve():
    assert os.path.isfile(_OUTIL), 'l\'instrument de panne partielle a disparu'
    src = io.open(_OUTIL, encoding='utf-8').read()
    assert 'CIBLES = ' in src and "'/scan'" in src, (
        'la liste des sources éprouvées a disparu.')
    assert 'concernees = [u for u, s in usage.items() if cible in s]' in src, (
        'l\'instrument ne juge plus SEULEMENT les vues qui appellent la source '
        'coupée : il accuserait des vues qui n\'ont rien à voir avec elle.')


def test_la_carte_qui_appelle_quoi_est_mesuree_et_non_supposee():
    """Le point de méthode : sans cette carte, on juge des vues au hasard.
    C'est elle qui rend le verdict interprétable."""
    src = io.open(_OUTIL, encoding='utf-8').read()
    assert "pg.on('request', _req)" in src, (
        'la carte « qui appelle quoi » n\'est plus mesurée : elle redeviendrait '
        'une supposition, et le verdict porterait sur des vues sans rapport.')


def test_les_limites_sont_ecrites_dans_l_instrument():
    """CONTRE-EXEMPLE du réflexe « conclure propre ». Trois faux positifs ont
    été réfutés ; les taire aurait laissé croire que la question est réglée,
    et le prochain lecteur aurait rouvert la même impasse."""
    src = io.open(_OUTIL, encoding='utf-8').read()
    assert 'NE PEUT PAS decider' in src, (
        'la limite de la mesure a disparu de l\'instrument : son verdict se '
        'lirait comme une preuve d\'absence de défaut.')
    assert 'SVGAnimatedString' in src, (
        'le premier faux positif n\'est plus documenté — celui qui confondait '
        'tous les textes SVG dans un seul seau.')
    assert 'reste OUVERTE' in src, (
        'le verdict de l\'outil ne dit plus que la question du « chiffre faux '
        'silencieux » reste ouverte.')


def test_le_verdict_ne_pretend_pas_a_l_absence_de_defaut():
    """La formulation compte : « aucune fuite ni erreur » est ce qui a été
    mesuré ; « le produit est propre » ne l'est pas."""
    src = io.open(_OUTIL, encoding='utf-8').read()
    assert "'AUCUNE FUITE NI ERREUR sous panne partielle." in src, (
        'le verdict a été élargi au-delà de ce que l\'instrument mesure.')
