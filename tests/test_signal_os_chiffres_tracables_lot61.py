"""SIGNAL OS · LOT 61 — CHAQUE CHIFFRE PEINT VIENT-IL D'UNE SOURCE ?

Réserve SIGNAL-OS-60 §3 et §5.3, de ma main : *« Il ne sait pas reconnaître un
hôte qui aboutit avec une valeur inventée ou périmée. […] C'est de loin le plus
utile qui manque encore. »*

C'est le seul défaut qui, dans un terminal d'analyse, peut coûter de l'argent
plutôt que de la confiance : **un chiffre plausible, affiché sans source**.

`tools/mesurer_chiffres_tracables.py` capture tout ce que la page **reçoit**,
extrait tout ce qu'elle **affiche**, et demande pour chaque nombre peint : *est-il
dans ce qui est arrivé ?* — exactement, ou à l'arrondi près.

## Le résultat, et ce qu'il vaut

Huit espaces, nominal puis sous panne de `market` et de `skyler` : **aucun
chiffre inventé**. Tous les nombres « inexpliqués » se sont révélés, à la
lecture de leur contexte, des **dérivations nommées par la page elle-même** :

```text
150,42   … mouvement attendu ~1σ (IV·√t) / Sous-jacent / 150,42 …
65       … Concentration élevée : ACN = 65 % du portefeuille …
2 300    … Valeur nette / 2 300 / cash non renseigné …
```

L'outil ne sait pas distinguer « dérivé » de « inventé » — c'est le lecteur qui
tranche, et c'est ce que j'ai fait ici, un par un. Ce qu'il garantit est plus
étroit et vérifiable : **tout chiffre inventé est nécessairement inexpliqué**,
donc la liste des inexpliqués contient tous les défauts de cette famille.

## Deux artefacts d'extraction, corrigés avant de conclure

Le premier passage accusait `2026 12` et `127.0`. Ni l'un ni l'autre n'existe :
c'était **mon propre découpage** qui les fabriquait — l'espace pris pour
séparateur de milliers sur un groupe de deux chiffres (une date), et une adresse
IP coupée en morceaux. Les publier comme trouvailles aurait été accuser le
produit de mes fautes.
"""
import pathlib

import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent
OUTIL = RACINE / 'tools' / 'mesurer_chiffres_tracables.py'


@pytest.fixture(scope='module')
def source():
    return OUTIL.read_text(encoding='utf-8')


def test_le_detecteur_a_un_temoin_qui_fabrique_un_chiffre(source):
    """LE TÉMOIN QUI COMPTE LE PLUS DE TOUTE LA SÉRIE.

    « Zéro inexpliqué » et « je ne sais pas voir » rendent le même chiffre. Le
    mode `--temoin` injecte un nombre qui n'est dans aucune réponse et exige que
    l'outil le dénonce ; sans lui, son silence sur le produit ne vaudrait rien."""
    assert '--temoin' in source, 'le mode temoin a disparu'
    assert '987654' in source, (
        'le chiffre fabrique du temoin a disparu : le detecteur n\'est plus '
        'mis a l\'epreuve, et « zero inexplique » cesse de vouloir dire quelque '
        'chose')
    assert 'PASSE INAPERCU' in source, (
        'l\'outil ne signale plus l\'echec du temoin — il pourrait rendre 0 en '
        'etant aveugle')


def test_les_deux_temoins_de_corpus_sont_en_place(source):
    """Sans réponse capturée, tout serait « inexpliqué » ; si rien ne s'explique,
    c'est l'appariement qui est cassé. Deux façons de rendre un chiffre absurde,
    deux refus de conclure."""
    #  On vise un fragment SANS apostrophe : la source l'echappe (`d\'API`),
    #  et chercher la forme non echappee faisait echouer le test sur un outil
    #  parfaitement correct.
    assert 'AVEUGLE — aucune reponse d' in source, (
        'le refus de conclure sans corpus a disparu')
    assert 'AVEUGLE — AUCUN des %d nombres peints' in source, (
        'le refus de conclure quand rien ne s\'explique a disparu')


def test_les_deux_artefacts_d_extraction_restent_corriges(source):
    """LES FAUTES QUE J'AI FAILLI PUBLIER COMME TROUVAILLES.

    `2026 12` (une date) et `127.0` (un morceau d'adresse) n'ont jamais été
    affichés comme nombres : c'est mon découpage qui les fabriquait."""
    assert 'def _dans_une_suite_pointee(' in source, (
        'la garde contre les adresses et versions a disparu : `127.0.0.1` '
        'redeviendrait quatre faux « inexpliques »')
    assert r'\d{1,3}(?:' in source and r'\d{3})+' in source, (
        'le separateur de milliers n\'exige plus des groupes de TROIS chiffres : '
        '« 2026 12 » redeviendrait un nombre de mon invention')


def test_le_contexte_accompagne_chaque_inexplique(source):
    """Un nombre sans sa phrase n'est pas exploitable. « 58 » ne dit rien ;
    « Fraîcheur 58 s » dit tout — et c'est le contexte qui a permis de classer
    les onze inexpliqués comme des dérivations légitimes."""
    assert 'autour = texte[max(0, i - 45)' in source, (
        'le contexte des nombres inexpliques n\'est plus affiche : la liste '
        'redevient une alarme qu\'on ne peut ni verifier ni classer')


def test_les_limites_restent_ecrites_dans_l_outil(source):
    """Un détecteur qui tait ce qu'il ignore transforme son silence en garantie.
    Trois limites, écrites là où on lit le résultat."""
    for limite in ('Il ne distingue pas « dérivé » de « inventé »',
                   'Il ne juge pas la **fraîcheur**',
                   'jamais les attributs'):
        assert limite in source, (
            'une limite declaree a disparu de l\'en-tete : « %s »' % limite[:50])


def test_l_outil_se_charge_et_expose_son_entree(source):
    """Garde minimale d'intégrité : le module s'importe et offre les deux
    fonctions par lesquelles un gardien futur pourra l'appeler."""
    import importlib
    mod = importlib.import_module('tools.mesurer_chiffres_tracables')
    assert callable(getattr(mod, 'une_page', None))
    assert callable(getattr(mod, '_explique', None))
    #  L'appariement à l'arrondi près : c'est lui qui rend l'outil utilisable.
    #  Sans tolérance, `198,00` peint contre `198.0031` reçu serait « inexplique »
    #  et la liste noierait tout vrai defaut.
    assert mod._explique(198.0, {198.0031}) is True
    assert mod._explique(12.5, {0.125}) is True
    assert mod._explique(987654.321, {1.0, 2.0}) is False
