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


def test_les_faux_positifs_restent_ecrits_dans_l_instrument():
    """CONTRE-EXEMPLE du réflexe « conclure propre ». Les faux positifs réfutés
    doivent rester écrits : les taire ferait rouvrir la même impasse.

    LOT 35 — la question que ce test gardait comme OUVERTE est désormais
    FERMÉE, par une mesure. Ce test change donc de contenu, pas de nature : il
    garde toujours la trace des impasses, mais l'outil ne doit plus annoncer
    une réserve qu'il a lui-même levée."""
    src = io.open(_OUTIL, encoding='utf-8').read()
    assert 'SVGAnimatedString' in src, (
        'le premier faux positif n\'est plus documenté — celui qui confondait '
        'tous les textes SVG dans un seul seau.')
    assert 'horloge' in src, (
        'le faux positif du lot 35 n\'est plus documenté : une horloge a la '
        'minute qui tombe pendant la mesure, et l\'outil accuse un chiffre.')


def test_le_verdict_ne_pretend_pas_a_l_absence_de_defaut():
    """La formulation compte : ce qui est annoncé doit être exactement ce qui a
    été mesuré. L'outil éprouve la PANNE ; il ne peut rien dire d'une source
    qui MENT (répond bien, avec de mauvais chiffres) — et son verdict ne doit
    donc jamais s'élargir jusque-là."""
    src = io.open(_OUTIL, encoding='utf-8').read()
    assert 'SOUS PANNE PARTIELLE, AUCUN CHIFFRE INVENTE' in src, (
        'le verdict ne dit plus SOUS QUEL REGIME il vaut.')
    for trop in ('le produit est propre', 'aucune donnee fausse',
                 'les chiffres sont justes'):
        assert trop not in src.lower(), (
            'verdict elargi au-dela de la mesure : « %s »' % trop)
