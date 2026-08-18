"""SIGNAL OS · OPTIONS — un en-tête différent des sept autres, et des titres qui
posaient la question au lieu de nommer la chose.

## 1. Une seule grammaire d'en-tête pour les huit espaces

Mesuré sur les huit fichiers de page :

| classe du sous-titre | pages |
| --- | --- |
| `<div class="vx-sub">` | **7** |
| `<p class="vx-page-lead__summary">` | **1** — Options |

Options portait en plus un `vx-page-lead__eyebrow` (« Intelligence de
convexité ») qu'**aucune autre page ne possède**, et qui ne disait rien de plus
que le `<h1>Options</h1>` situé juste dessous.

Deux noms de classe pour un même rôle, c'est un composant dupliqué pour changer
le look — `VALIDATION.md` le refuse explicitement, et `SKILL.md` §7 demande un
seul shell.

**Ce qui est conservé** : le bouclier « Analyse uniquement · aucun ordre ». C'est
le seul élément du bloc qui porte une information, et elle est produit.

## 2. Un titre nomme un objet ; la question a son propre élément

`COPY.md` : « Préférer des noms d'objets ou de décisions. »

| avant | forme | après |
| --- | --- | --- |
| `GEX quotidien — le gamma s'empile-t-il ?` | question **dans** le titre, alors qu'un `.vx-chart-question` existait déjà dessous | `GEX quotidien` |
| `Scanner LEAPS — quels contrats longue échéance sont conformes ?` | idem | `Scanner LEAPS` |
| `Les options sont-elles chères ?` | le titre **était** la question, sans nom d'objet | `Prix de la volatilité` + question déplacée |
| `Un événement menace-t-il l'échéance ?` | idem | `Risque événementiel` + question déplacée |

Les deux premiers **disaient deux fois la même chose** à deux lignes d'écart.
Les deux derniers ne nommaient rien : impossible de savoir de quoi parle la carte
sans lire la réponse.

## 3. Un doublon mesuré

À 1440 px sur la vue Structure :

| | |
| --- | --- |
| 1182 px | carte **« Payoff à l'échéance »** · *Où gagne / perd la structure selon le cours ?* |
| 1254 px | graphique **« Payoff à l'échéance — Put long »** · *Où gagne / perd la structure ?* |

Même titre et même question, 72 px plus bas, dans une formulation à peine
différente. Le graphique ne garde que ce qu'il **ajoute** : quelle structure est
tracée.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PAGES = os.path.join(_ROOT, 'vertex', 'ui', 'pages')
_OPT = os.path.join(_PAGES, 'options_intel_page.py')
_STRUCT = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js', 'pages',
                       'options-structure.js')

_HUIT = ('briefing.py', 'markets_page.py', 'opportunities_page.py',
         'analysis_page.py', 'portfolio_page.py', 'options_intel_page.py',
         'performance_page.py', 'system_page.py')


def _lire(p):
    return io.open(p, encoding='utf-8').read()


def _sans_commentaires(src):
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    return re.sub(r'<!--.*?-->', '', src, flags=re.S)


def test_les_huit_espaces_partagent_une_grammaire_d_en_tete():
    """Le test ne fige pas une classe : il exige qu'il n'y en ait qu'UNE.

    Si un jour `vx-page-lead__summary` devient le standard, ce test le dira en
    échouant sur les sept autres — ce qui est la bonne conversation à avoir.
    """
    avec_sub, avec_summary = [], []
    for nom in _HUIT:
        src = _sans_commentaires(_lire(os.path.join(_PAGES, nom)))
        if 'class="vx-sub"' in src:
            avec_sub.append(nom)
        if 'vx-page-lead__summary' in src:
            avec_summary.append(nom)
    assert not avec_summary, (
        '%d page(s) emploient `vx-page-lead__summary` pendant que %d emploient '
        '`vx-sub` : deux noms de classe pour un même rôle. %s'
        % (len(avec_summary), len(avec_sub), avec_summary))
    assert len(avec_sub) == len(_HUIT), (
        'espace(s) sans sous-titre : %s'
        % sorted(set(_HUIT) - set(avec_sub)))


def test_l_eyebrow_solitaire_a_disparu():
    """Il n'existait que sur Options et répétait le titre juste dessous."""
    src = _sans_commentaires(_lire(_OPT))
    assert 'vx-page-lead__eyebrow' not in src, (
        'Options réintroduit un ornement d\'en-tête que les sept autres espaces '
        'n\'ont pas.')


def test_le_bouclier_lecture_seule_reste():
    """CONTRE-EXEMPLE. Simplifier un en-tête ne doit pas emporter le seul de ses
    éléments qui porte une information produit — READONLY est un invariant."""
    src = _lire(_OPT)
    # DANS L'EN-TETE, pas n'importe où dans le fichier : les deux chaînes
    # existent ailleurs (docstring, autres vues), et une première version de ce
    # test passait donc au vert alors que le bouclier avait été retiré du bloc.
    i = src.index('_HEADER = """')
    entete = src[i:src.index('%%TABS%%', i)]
    assert 'vx-readonly-shield' in entete and 'aucun ordre' in entete, (
        'la mention « Analyse uniquement · aucun ordre » a disparu de l\'en-tête '
        'Options en même temps que la décoration.')


def test_les_titres_nomment_un_objet():
    src = _sans_commentaires(_lire(_OPT))
    for titre in ('<span class="vx-card-title">GEX quotidien</span>',
                  '<span class="vx-card-title">Scanner LEAPS</span>',
                  '<span class="vx-card-title">Prix de la volatilité</span>',
                  '<span class="vx-card-title">Risque événementiel</span>'):
        assert titre in src, 'titre non nommé : %s' % titre


def test_les_questions_ne_sont_plus_dans_les_titres():
    """Un `.vx-card-title` qui se termine par « ? » pose la question au lieu de
    nommer la chose."""
    src = _sans_commentaires(_lire(_OPT))
    fautifs = [t for t in re.findall(r'<span class="vx-card-title">([^<]*)</span>', src)
               if t.rstrip().rstrip('&nbsp;').endswith('?')]
    assert not fautifs, (
        'titre(s) formulés en question : %s — la question a son propre élément '
        '(`.vx-chart-question`).' % fautifs)


def test_les_questions_deplacees_sont_toujours_la():
    """CONTRE-EXEMPLE. Raccourcir un titre ne doit pas supprimer la question :
    `CHARTS.md` exige qu'un graphique dise à quoi il répond."""
    src = _sans_commentaires(_lire(_OPT))
    for question in ('Les options sont-elles chères ?',
                     "Un événement menace-t-il l'échéance ?"):
        assert question in src, (
            'la question « %s » a disparu au lieu d\'être déplacée.' % question)


def test_le_graphique_ne_repete_plus_le_cadre():
    """La carte hôte dit « Payoff à l'échéance » ; le graphique le répétait
    72 px plus bas, question comprise."""
    js = _sans_commentaires(_lire(_STRUCT))
    assert "title: 'Payoff" not in js and 'title: "Payoff' not in js, (
        'le graphique de payoff répète de nouveau le titre de sa carte hôte.')
    assert 'title: esc(s.label)' in js, (
        'le graphique ne porte plus le libellé de la structure tracée — il ne '
        'dit alors plus rien du tout.')
    # La carte hôte, elle, garde titre ET question.
    page = _sans_commentaires(_lire(_OPT))
    assert '<span class="vx-card-title">Payoff à l\'échéance</span>' in page
