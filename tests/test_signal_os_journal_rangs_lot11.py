"""SIGNAL OS · JOURNAL — LES SIX RANGS ET LES CINQ VISUALISATIONS, MESURÉS.

Le lot 07 avait écrit, en toutes lettres : « la structure du Journal n'a PAS été
reconstruite … rien de tout cela n'a été vérifié ». Ce fichier est la
vérification, et il fige ce qu'elle a trouvé.

## Rangs — `PAGES.md` §7

| rang demandé | état mesuré |
| --- | --- |
| 1. Track record séparant signaux et positions réelles | **couvert** — `track-record` oppose « Moteur · verdicts théoriques » et « Journal · trades déclarés », et écrit « Aucun chiffre ne passe de l'une à l'autre » |
| 2. Décisions récentes | **couvert** — `journal` |
| 3. Résultats par grade / setup / horizon | **PARTIEL** — « Rendement moyen +20 séances par verdict » ; un verdict n'est ni un grade, ni un setup, ni un horizon |
| 4. Erreurs répétées | **couvert** — « Erreurs récurrentes » |
| 5. Learnings | **couvert** — « Leçons apprises » |
| 6. Notes et historique | **couvert** — `track-record` + « Mémoire décisionnelle » |

## Visualisations — le conflit, et pourquoi il n'est PAS résolu par duplication

`PAGES.md` §7 demande cinq visualisations dont **equity curve** et **drawdown**.
Elles ne sont pas dans le Journal. Ce n'est pas un oubli : `equityCard` et
`drawdownCard` existent au registre et sont appelées par **Portefeuille**, où
elles ont été migrées.

Dupliquer reviendrait à entretenir **deux courbes d'équité**, donc deux vérités
possibles sur le même capital. La règle « une donnée = un seul domicile » prime
sur la liste des visualisations — et c'est cette règle-là qu'un gardien doit
tenir.

Ce qui manquait est **plus étroit que je ne l'ai d'abord écrit**. J'allais
publier « le Journal ne dit nulle part où elles sont » ; en comptant les
occurrences, il le dit **deux fois** — dans la vue `overview` et dans un état
vide. Mais **pas dans `progression`**, c'est-à-dire pas dans la vue qui POSE la
question. Une adresse écrite ailleurs que là où l'on cherche ne sert personne :
c'est ce trou-là que le relais du lot 11 comble, et rien de plus.

| visualisation demandée | état |
| --- | --- |
| equity curve | domiciliée **Portefeuille** · relais depuis `progression` |
| drawdown | domiciliée **Portefeuille** · relais depuis `progression` |
| distribution de résultats | **présente** (`overview`) |
| win/loss par bucket | **PARTIEL** — moyenne par verdict, pas un win/loss |
| calibration score→résultat | carte présente, **aucun tracé** — le Brier est déclaré indisponible tant qu'il n'est pas mesurable, ce qui est honnête |

## Portée dite

Ces tests lisent la **source de page**. Un titre construit à l'exécution en
JavaScript leur échappe — les trois graphiques du Journal sont dans ce cas et
sont vérifiés par leur site d'appel, pas par leur rendu.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_JOURNAL = os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'performance_page.py')
_PORTFOLIO = os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'portfolio_page.py')


def _lire(p):
    return io.open(p, encoding='utf-8').read()


# Rang → un libellé qui le matérialise dans la source. Ce n'est pas une liste de
# souhaits : chaque entrée a été VUE au navigateur avant d'être écrite ici.
_RANGS = {
    '1. track record séparé': ('Moteur &middot; verdicts th&eacute;oriques',
                               'Journal &middot; trades d&eacute;clar&eacute;s'),
    '2. décisions récentes': ('Chronologie des d&eacute;cisions',),
    '4. erreurs répétées': ('Erreurs récurrentes',),
    '5. learnings': ('Leçons apprises',),
    '6. notes et historique': ('M&eacute;moire d&eacute;cisionnelle',),
}


def test_les_rangs_couverts_le_restent():
    """Un rang qui disparaît ne se voit pas : la page reste belle, elle répond
    juste à une question de moins."""
    src = _lire(_JOURNAL)
    manquants = []
    # Portée : le libellé doit être un TITRE DE CARTE. Cherché dans tout le
    # fichier, « Erreurs récurrentes » y figure DEUX fois — titre et texte
    # d'état vide — donc renommer le titre laissait le test vert. Mutation
    # vérifiée : c'est le septième piège de portée de cette refonte.
    # `<h2>` autant que `.vx-card-title` : la Chronologie est un titre de VUE,
    # pas de carte, et l'exclure aurait fait échouer un rang pourtant couvert —
    # un gardien trop étroit accuse aussi faussement qu'un gardien trop large.
    titres = set(re.findall(r'<span class="vx-card-title">([^<]+)</span>', src)) \
        | set(re.findall(r'<h2[^>]*>([^<]+)</h2>', src))
    for rang, libelles in _RANGS.items():
        for lib in libelles:
            if lib not in titres:
                manquants.append('%s → %r' % (rang, lib))
    assert not manquants, (
        'des rangs de PAGES.md §7 ont perdu leur matérialisation :\n  '
        + '\n  '.join(manquants))


def test_les_deux_sources_de_l_historique_restent_separees():
    """LE rang 1, et l'invariant le plus fort de cette page : la mesure du
    moteur et les déclarations de l'utilisateur ne se mélangent pas. La page
    l'ÉCRIT ; si la phrase disparaît, c'est que quelqu'un a fusionné les deux.
    """
    src = _lire(_JOURNAL)
    assert 'data-source-kind="engine"' in src and 'data-source-kind="declared"' in src, (
        'les deux historiques ne sont plus marqués par leur provenance')
    assert 'Aucun chiffre ne passe de l' in src, (
        'la phrase qui interdit le mélange des deux sources a disparu')


def test_l_equite_n_est_pas_dupliquee_dans_le_journal():
    """CONTRE-EXEMPLE du test suivant. `PAGES.md` §7 demande la courbe
    d'équité ici ; l'y ramener créerait une SECONDE courbe d'équité, donc deux
    vérités sur un même capital. La règle « une donnée = un seul domicile »
    prime — et c'est elle qu'on garde, pas la liste.

    Si ce test devient rouge, la bonne question n'est pas « comment le faire
    passer » mais « pourquoi y a-t-il deux domiciles ».
    """
    journal = _lire(_JOURNAL)
    for builder in ('equityCard', 'drawdownCard'):
        assert builder not in journal, (
            '%s est appelé depuis le Journal alors qu\'il est domicilié dans '
            'Portefeuille : deux courbes pour une même donnée.' % builder)
    portefeuille = _lire(_PORTFOLIO)
    # `equityCard` apparaît deux fois dans Portefeuille : la GARDE de
    # disponibilité (`&&VXCharts.equityCard`) et l'APPEL. Chercher le nom
    # laissait passer un appel remplacé tant que la garde subsistait.
    for builder in ('equityCard', 'drawdownCard'):
        assert 'VXCharts.%s(' % builder in portefeuille, (
            'le domicile a disparu de Portefeuille (%s n\'y est plus APPELÉ) : '
            'l\'équité n\'est plus nulle part, et le relais du Journal pointe '
            'vers le vide.' % builder)


def test_le_journal_nomme_le_domicile_de_l_equite():
    """Une donnée déplacée doit laisser une adresse LÀ OÙ ON LA CHERCHE.

    Le Journal nommait déjà le domicile — deux fois, dans `overview` et dans un
    état vide. Il ne le nommait pas dans `progression`, la vue qui pose la
    question. C'est ce trou-là qui est gardé, pas une absence totale que
    j'allais publier à tort.

    Portée : on vérifie le lien DANS la vue `progression`, pas n'importe où
    dans le fichier — cinq vues y cohabitent, et un lien vers Portefeuille
    ailleurs ne dirait rien à qui cherche sa progression.
    """
    src = _lire(_JOURNAL)
    debut = src.index("    'progression': \"\"\"")
    bloc = src[debut:src.index("    'track-record': \"\"\"", debut)]
    # `/portfolio?view=performance` apparaît TROIS fois dans le fichier (deux
    # mentions préexistantes, hors de cette vue) : la présence est donc lue
    # dans le bloc `progression` SEUL, et sur un élément d'action.
    assert re.search(r'<a[^>]+href="/portfolio\?view=performance"', bloc), (
        'la vue Progression ne dit plus où sont l\'équité et le drawdown.')
    assert re.search(r'quit[e&][^<]*drawdown', bloc, re.I), (
        'le relais existe mais ne NOMME plus ce qu\'il va chercher : un lien '
        'sans objet est le « View more » que COPY.md proscrit.')


def test_la_calibration_ne_fabrique_pas_un_score_qu_elle_ne_mesure_pas():
    """Le Brier est déclaré indisponible tant qu'il n'est pas mesurable. C'est
    la règle « donnée absente → mention honnête » appliquée à une métrique, et
    c'est plus difficile à tenir qu'un tiret : il est tentant d'afficher un
    chiffre approché."""
    src = _lire(_JOURNAL)
    assert 'Brier indisponible' in src, (
        'la mention d\'indisponibilité du Brier a disparu : vérifier qu\'un '
        'score n\'a pas été fabriqué à la place.')
