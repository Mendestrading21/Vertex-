"""SIGNAL OS · « AUCUN GRAPHIQUE SANS QUESTION NI CONCLUSION » (CHARTS.md).

## TROIS fausses accusations, dont une que j'avais déjà appliquée

**Premier relevé : 12 graphiques rendus, 12 en échec.** Un taux pareil trahit
l'instrument, pas le produit — et c'était le cas trois fois de suite.

1. Le Chart Shell rend la question dans `.vx-chart-question` **uniquement quand
   il n'y a pas de conclusion** ; sinon elle part en `.vx-sr-only`, délibérément,
   pour ne pas la répéter au-dessus de la conclusion. Mon relevé mesurait
   l'absence **visuelle** et la prenait pour une absence. 12 → 3.

2. « Put long » : mon relevé lisait la carte la plus **interne**. Un niveau
   au-dessus, la carte hôte porte le titre et la question visible. 3 → 2.

3. **Celle-ci, je l'avais déjà corrigée dans le produit avant de la vérifier.**
   J'avais conclu que la conclusion du payoff doublait celle de sa carte hôte et
   je l'avais retirée. Mais `querySelector` **traverse les descendants** : en
   interrogeant la carte hôte, je relisais la conclusion **du graphique** et je
   la comptais à deux niveaux. La carte hôte n'en a jamais eu. Mesuré après le
   retrait : 2 questions, **zéro conclusion** sur toute la vue. Rétabli.

La leçon n'est pas « mieux mesurer » : c'est que **j'ai modifié le produit sur
la foi d'un relevé que je n'avais pas contre-vérifié**, alors que les deux
accusations précédentes du même relevé venaient d'être invalidées.

Ce fichier garde donc la règle **telle que le produit l'implémente** : la
question compte qu'elle soit visible ou réservée aux lecteurs d'écran, et elle
peut être portée par la carte hôte.

## Ce que le même relevé a trouvé de vrai

- **Marchés / breadth** — « Tendance de participation » avait une question et
  aucune conclusion. Conclusion désormais **dérivée** de la série tracée
  (premier vs dernier point de « > MM200 »), et **omise** si les bornes
  manquent : une conclusion générique aurait été pire que pas de conclusion.
- **Portefeuille / risque** — le donut « Secteurs » était monté dans une carte
  **bâtie à la main** par la page, qui n'en portait ni l'une ni l'autre. Le seul
  graphique du produit dans ce cas.
(Le troisième « défaut » de ma liste initiale — la conclusion dupliquée du
payoff — n'existait pas : voir ci-dessus.)

## Portée dite

Ces tests lisent les **sources** (pages et builders JS). Le relevé au navigateur
qui les a motivés vit dans `docs/refactor/validation/SIGNAL-OS-12-GRAPHIQUES.md` :
un test de source ne peut pas voir un graphique que personne n'appelle.
"""

import io
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lire(*parts):
    return io.open(os.path.join(_ROOT, *parts), encoding='utf-8').read()


def test_le_chart_shell_garde_la_question_meme_quand_elle_est_invisible():
    """LA propriété qui a annulé ma première accusation.

    Si quelqu'un « simplifiait » ce ternaire en ne rendant la question que
    lorsqu'elle est visible, toutes les questions des graphiques CONCLUANTS
    disparaîtraient du document — invisibles à l'écran ET absentes pour les
    lecteurs d'écran, sans qu'aucune page ne change.
    """
    core = _lire('vertex', 'static', 'vertex', 'js', 'charts', 'chart-core.js')
    assert 'opts.question && !opts.conclusion' in core, (
        'la règle de rendu de la question a changé de forme — vérifier qu\'une '
        'question accompagnée d\'une conclusion reste dans le document.')
    assert 'vx-sr-only">${opts.question}' in core, (
        'la question n\'est plus rendue pour les lecteurs d\'écran quand une '
        'conclusion existe : elle disparaît purement et simplement.')


def test_la_tendance_de_participation_conclut_sur_ses_propres_donnees():
    """Contre-exemple inclus : la conclusion doit être OMISE quand les bornes
    manquent. Une phrase générique (« la participation évolue ») serait pire
    qu'une absence — elle aurait l'air d'une mesure."""
    src = _lire('vertex', 'ui', 'pages', 'markets_page.py')
    bloc = src[src.index("'vx-mk-breadth-trend'"):]
    bloc = bloc[:bloc.index('emptyCard')]
    assert 'conclusion:cclBreadth' in bloc, (
        '« Tendance de participation » n\'a plus de conclusion.')
    assert "a200.length>1" in src, (
        'la conclusion ne teste plus qu\'elle a DEUX bornes : elle peut '
        'désormais être calculée sur une série trop courte.')
    assert "cclBreadth=''" in src or "let cclBreadth=''" in src, (
        'la conclusion n\'a plus de valeur vide par défaut — elle risque '
        'd\'afficher une phrase quand la donnée manque.')


def test_le_donut_sectoriel_porte_question_et_conclusion():
    """Ce donut était le seul graphique du produit monté dans une carte bâtie à
    la main, donc sans le gabarit qui impose les deux."""
    src = _lire('vertex', 'ui', 'pages', 'portfolio_page.py')
    entete = src[src.index('<span class="vx-card-title">Secteurs</span>'):]
    entete = entete[:entete.index('Greeks agrégés')]
    assert 'vx-chart-question' in entete, 'le donut sectoriel a perdu sa question'
    assert 'pf-sector-ccl' in entete, 'le donut sectoriel a perdu sa conclusion'
    assert "_c.textContent=_se.length" in src or "if(_c&&_se.length" in src, (
        'la conclusion du donut ne vérifie plus qu\'elle a des secteurs à '
        'nommer : elle peut afficher une part calculée sur rien.')


def test_le_payoff_garde_sa_conclusion_car_personne_d_autre_ne_la_porte():
    """L'INVERSE de ce que j'avais écrit, et la troisième fausse accusation de
    ce lot — la seule sur laquelle j'avais déjà agi.

    J'ai cru à un doublon avec la carte hôte « Payoff à l'échéance » et j'ai
    retiré la conclusion du graphique. Mon relevé interrogeait les DESCENDANTS
    de la carte hôte : `querySelector` traverse, il y lisait donc la conclusion
    DU GRAPHIQUE et la comptait à deux niveaux. La carte hôte n'en a jamais eu.

    Mesuré après le retrait : 2 questions, **zéro conclusion** sur toute la vue.
    Ce n'était pas un doublon en moins, c'était la seule conclusion en moins.
    """
    src = _lire('vertex', 'static', 'vertex', 'js', 'pages', 'options-structure.js')
    bloc = src[src.index('title: esc(s.label),'):]
    bloc = bloc[:bloc.index('height: 260')]
    assert 'conclusion: concl' in bloc, (
        'le graphique de payoff a perdu sa conclusion — et personne d\'autre '
        'ne la porte : la vue Structures se retrouve sans conclusion du tout.')
