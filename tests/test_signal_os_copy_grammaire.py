"""SIGNAL OS · JOURNAL — la règle du lot Options, généralisée aux huit espaces.

Le lot Options avait trouvé cinq `.vx-card-title` formulés en question, et le
gardien écrit **comme une propriété** (« un titre ne se termine pas par ? ») en
avait trouvé un cinquième que je n'avais pas vu.

La même propriété, appliquée aux **huit** pages, en trouve d'autres :

| page | sous-titre | titre |
| --- | --- | --- |
| `analysis_page.py` | `Cette entreprise et cette opportunité méritent-elles du capital maintenant ?` | — |
| `performance_page.py` | `Suis-je en train de devenir un meilleur investisseur ?` | `Post-mortem — que disent mes sorties ?` |
| `system_page.py` | `Le système est-il en bonne santé et branché sur du réel ?` | — |
| les cinq autres | *conformes* | *conformes* |

`COPY.md` § Sous-titres : « Maximum une ligne. **Expliquer ce que la zone aide à
décider.** » Les trois exemples qu'il donne sont des **orientations**, pas des
questions : « Régime, risque et leadership. », « Exposition, risque et prochaine
décision. », « Convexité, volatilité et risque événementiel. »

Cinq espaces sur huit le faisaient déjà. Trois posaient la question à
l'utilisateur au lieu de lui dire où il est.

## Pourquoi la question n'est pas perdue

La question **de la page** vit dans `PAGES.md` et dans le docstring du module —
c'est une boussole de conception. Le sous-titre, lui, est lu à chaque visite : il
doit **orienter**, pas interroger. Pour un GRAPHIQUE, en revanche, `CHARTS.md`
exige la question — et elle a son élément, `.vx-chart-question`.

## Portée

Ce gardien lit les **sources de page**. Un titre construit à l'exécution en
JavaScript lui échappe : il ne prouve donc pas « aucun titre-question dans
Vertex », seulement « aucun dans les huit gabarits de page ».
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PAGES = os.path.join(_ROOT, 'vertex', 'ui', 'pages')

_HUIT = ('briefing.py', 'markets_page.py', 'opportunities_page.py',
         'analysis_page.py', 'portfolio_page.py', 'options_intel_page.py',
         'performance_page.py', 'system_page.py')


def _source(nom):
    src = io.open(os.path.join(_PAGES, nom), encoding='utf-8').read()
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    return re.sub(r'<!--.*?-->', '', src, flags=re.S)


def _finit_par_question(texte):
    return texte.replace('&nbsp;', ' ').replace('&#160;', ' ').rstrip().endswith('?')


def test_aucun_sous_titre_ne_pose_une_question():
    """Le sous-titre oriente ; il n'interroge pas l'utilisateur."""
    fautifs = []
    for nom in _HUIT:
        for sub in re.findall(r'<div class="vx-sub">(.*?)</div>',
                              _source(nom), flags=re.S):
            if _finit_par_question(sub):
                fautifs.append('%s : %s' % (nom, ' '.join(sub.split())[:70]))
    assert not fautifs, (
        'sous-titre(s) formulés en question — `COPY.md` demande d\'expliquer ce '
        'que la zone aide à décider :\n  ' + '\n  '.join(fautifs))


def test_aucun_titre_de_carte_ne_pose_une_question():
    """Généralisation du gardien Options aux huit espaces."""
    fautifs = []
    for nom in _HUIT:
        for t in re.findall(r'<span class="vx-(?:card|chart)-title">([^<]*)</span>',
                            _source(nom)):
            if _finit_par_question(t):
                fautifs.append('%s : %s' % (nom, t))
    assert not fautifs, (
        'titre(s) formulés en question — la question a son propre élément '
        '(`.vx-chart-question`) :\n  ' + '\n  '.join(fautifs))


def test_les_huit_espaces_ont_bien_un_sous_titre():
    """CONTRE-EXEMPLE. Les deux tests ci-dessus passeraient si l'on supprimait
    les sous-titres. Le but est de les REFORMULER, pas de les faire taire."""
    # PAS « le fichier contient un vx-sub quelque part » : trois pages en ont
    # plusieurs (en-têtes de sous-vues), et une première version de ce test
    # restait verte alors que le sous-titre DE LA PAGE avait été supprimé.
    # On exige un `vx-sub` dans les 400 caractères qui suivent le premier `<h1>`.
    sans = []
    for nom in _HUIT:
        src = _source(nom)
        m = re.search(r'<h1[^>]*>', src)
        if not m or 'class="vx-sub"' not in src[m.end():m.end() + 400]:
            sans.append(nom)
    assert not sans, (
        'espace(s) dont l\'en-tête de page n\'a plus de sous-titre : %s — '
        'reformuler n\'est pas supprimer.' % sans)


def test_les_questions_du_journal_sont_deplacees_et_non_perdues():
    """`Post-mortem — que disent mes sorties ?` : le titre nomme, la question
    descend d'un cran. `CHARTS.md` exige qu'un graphique dise à quoi il répond."""
    src = _source('performance_page.py')
    assert '<span class="vx-card-title">Post-mortem</span>' in src \
        or '<span class="vx-chart-title">Post-mortem</span>' in src, (
        'le post-mortem ne porte plus de nom d\'objet.')
    assert 'Que disent mes sorties' in src, (
        'la question a été supprimée au lieu d\'être déplacée.')


def test_le_possessif_a_disparu_des_titres():
    """Cohérence de ton : « Mes positions » est devenu « Positions » au lot 04.
    « Ma progression » était le dernier possessif du produit."""
    fautifs = []
    for nom in _HUIT:
        for t in re.findall(r'<span class="vx-(?:card|chart)-title">([^<]*)</span>',
                            _source(nom)):
            if re.match(r'^(Ma|Mon|Mes)\s', t.strip()):
                fautifs.append('%s : %s' % (nom, t))
    assert not fautifs, (
        'titre(s) au possessif — le produit l\'a retiré partout ailleurs :\n  '
        + '\n  '.join(fautifs))
