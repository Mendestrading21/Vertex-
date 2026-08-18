"""SIGNAL OS · LOT 63 — QUATRE ÉTIQUETTES DE FRAÎCHEUR ÉTAIENT DES CONSTANTES.

Réserve SIGNAL-OS-62 §6.1, de ma main : *« Options n'a aucun vocabulaire de
fraîcheur. »* **Ce verdict était faux**, et le lot 63 a commencé par le corriger.

Options porte bien une étiquette — dans une **troisième** grammaire que mon
instrument du lot 62 ne connaissait pas — et cette étiquette était exactement la
même constante que celle que je venais de corriger sur Aujourd'hui.

Deux fautes de méthode, pas une :

1. **Mon inventaire des grammaires était incomplet** : trois, pas deux.
2. **Ma granularité était la page.** L'outil du lot 62 rendait « DIT » dès qu'UNE
   étiquette réagissait. Une page portant un badge honnête *et* un badge constant
   était donc déclarée saine. *Un verdict par page masque un défaut par badge.*

## Le résultat, mesuré badge par badge sous vieillissement à +2 h

| page | étiquette | avant |
| --- | --- | --- |
| Analyse | carte-Verdict | `demoState()?'fallback':'delayed'` — constante |
| Opportunités | hero | `m==='fallback'?'fallback':'delayed'` — constante |
| Portefeuille | synthèse | `__pfLive?'live':'delayed'` — « À actualiser » inatteignable |
| Options | carte-Verdict | `d.demo?'demo':'delayed'`, texte « DELAYED » — constante |
| Système | hero | décrit la CONNEXION — texte honnête, **classe** menteuse |

Le motif est net et il désigne la cause : **les cinq puces issues de
`VX.freshness.chip()` réagissaient toutes ; les quatre badges écrits à la main
mentaient tous.** Le défaut ne venait pas des pages, il venait de ce qu'écrire
l'étiquette soi-même était plus court que d'aller chercher un âge. D'où le
correctif : `VX.freshness.domainChip()` rend l'honnêteté plus courte que le
mensonge.

Après correction, l'instrument rend **0 constante sur les huit espaces**.
"""
import pathlib

import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent
CORE = RACINE / 'vertex' / 'static' / 'vertex' / 'js' / 'vx-core.js'
OPTIONS = RACINE / 'vertex' / 'static' / 'vertex' / 'js' / 'pages' / 'options-structure.js'
PAGES = RACINE / 'vertex' / 'ui' / 'pages'
OUTIL = RACINE / 'tools' / 'mesurer_fraicheur_par_badge.py'


def _lire(p):
    return p.read_text(encoding='utf-8')


def _compact(p):
    return _lire(p).replace(' ', '').replace('\n', '')


@pytest.fixture(scope='module')
def outil():
    return _lire(OUTIL)


def test_le_helper_de_domaine_lit_un_age_reel():
    """LA CAUSE, TENUE PAR SA CORRECTION.

    `domainChip` n'a de valeur que s'il lit `age_s` du domaine. Un helper qui
    rendrait une étiquette fixe reproduirait le défaut à l'échelle de toute
    l'application au lieu d'une page."""
    c = _compact(CORE)
    assert 'domainChip(nom){' in c, (
        'le helper canonique de fraicheur par domaine a disparu : chaque page '
        'va reecrire son etiquette a la main, et c\'est exactement ce qui a '
        'produit les quatre constantes du lot 63')
    #  ON VISE L'EXPRESSION, PAS LE NOM — lecon du sixieme gardien creux (lot 62,
    #  ou `VX.freshness.THRESH` apparaissait AUSSI dans mon commentaire).
    assert "st.domains&&st.domains[nom];" in c and "d.age_s==='number')?d.age_s*1000:null" in c, (
        'le helper ne lit plus `domains.<nom>.age_s` : il ne peut donc plus '
        'rendre qu\'une etiquette sans information d\'age')
    assert 'this.chip(this.assess({ageMs:a,' in c, (
        'le helper n\'evalue plus l\'age par `assess` : les seuils vont diverger '
        'de ceux du reste de l\'application')


def test_analyse_et_options_lisent_le_helper_et_non_une_constante():
    """Les deux cartes-Verdict — là où chaque page CONCLUT — affichaient une
    étiquette qui ne bougeait pas à +2 h."""
    an = _compact(PAGES / 'analysis_page.py')
    assert "VX.freshness.domainChip('prices')" in an, (
        'la carte-Verdict d\'Analyse ne lit plus l\'age du domaine `prices` : '
        'son etiquette redevient une constante, sur l\'objet ou la page conclut')
    op = _compact(OPTIONS)
    assert "VX.freshness.domainChip('options')" in op, (
        'la carte-Verdict d\'Options ne lit plus l\'age du domaine `options` — '
        'et une prime, une IV et un spread vieillissent en MINUTES')


def test_opportunites_partage_une_seule_fraicheur():
    """Deux étiquettes sur le même écran, une honnête et une décorative : c'est
    le calcul partagé qui empêche la seconde de rementir."""
    src = _compact(PAGES / 'opportunities_page.py')
    #  Le site d'APPEL, pas le nom : `opFreshHtml()` est une sous-chaine de sa
    #  propre definition `function opFreshHtml(){` — troisieme fois que ce piege
    #  se presente dans la serie (lot 57, lot 62, ici).
    assert "+opFreshHtml()+" in src, (
        'le hero d\'Opportunites n\'appelle plus le calcul de fraicheur partage : '
        'son badge redevient une etiquette ecrite a la main')
    assert 'awaitopFresh();' in src, (
        'le manifeste n\'est plus attendu avant le rendu : le hero peindra « — » '
        'la ou l\'age est connaissable une fraction de seconde plus tard')


def test_portefeuille_peut_enfin_dire_a_actualiser():
    """`__pfLive?'live':'delayed'` ne consultait aucun âge : l'état « À
    actualiser » lui était structurellement inatteignable."""
    src = _compact(PAGES / 'portfolio_page.py')
    assert 'VX.freshness.chip(VX.freshness.assess({ageMs:a,live:!!window.__pfLive}))' in src, (
        'le badge du Portefeuille ne lit plus l\'age de session : « A actualiser » '
        'redevient inatteignable, et des marks de trois jours porteront la meme '
        'etiquette que des marks de trois secondes')
    assert 'awaitpfFresh();' in src, (
        'le manifeste n\'est plus attendu avant le rendu de la synthese')


def test_le_badge_systeme_ne_porte_plus_le_vetement_de_la_fraicheur():
    """Son TEXTE était honnête — « Système opérationnel » décrit la connexion.
    C'est sa CLASSE qui mentait, et c'est elle qui a fait qu'un instrument l'a
    pris deux fois de suite pour ce qu'il n'est pas."""
    src = _compact(PAGES / 'system_page.py')
    assert '"vx-badgevx-badge-status"data-status="\'+(_tone==' in src, (
        'le hero de Systeme est reparti dans la grammaire de la fraicheur : un '
        'etat de CONNEXION habille en age de donnee')


def test_l_outil_a_un_temoin_positif_pris_dans_le_produit(outil):
    """UN TÉMOIN PRIS DANS LE PRODUIT VAUT MIEUX QU'UN TÉMOIN FABRIQUÉ.

    Il prouve la chaîne entière — interception, vieillissement, identification,
    comparaison — dans les conditions exactes de la mesure. Sans lui, « aucune
    constante trouvée » et « je ne sais pas voir » rendent le même chiffre."""
    assert '_TEMOIN_ANCRE' in outil and "'vx-hero-fresh'" in outil, (
        'le temoin positif a disparu : l\'outil pourrait rendre « aucune '
        'constante » en etant simplement aveugle')
    assert 'if not any(_TEMOIN_ANCRE in c for c, _, _ in reagissent):' in outil, (
        'l\'outil n\'exige plus de VOIR le temoin bouger : son verdict cesse de '
        'vouloir dire quelque chose')


def test_l_outil_force_la_branche_non_demo_sur_les_deux_visites(outil):
    """LE TÉMOIN M'A REPRIS DÈS LE PREMIER PASSAGE. En mode démonstration les
    pages court-circuitent l'évaluation : tout paraît constant. Et abaisser
    `demo` sur la seule visite vieillie ferait paraître REACTIF ce qui ne fait
    que sortir du mode démo."""
    assert 'def _hors_demo(' in outil, (
        'la neutralisation du mode demonstration a disparu : toutes les '
        'etiquettes reparaitront constantes, pour la mauvaise raison')
    #  On vise l'appel INCONDITIONNEL, avant le `if age is not None` : c'est
    #  cela qui garantit les DEUX visites, et non la simple existence de la
    #  fonction.
    assert '_hors_demo(charge)\n        if age is not None:' in outil, (
        'le mode demo n\'est plus neutralise sur les DEUX visites : le nominal '
        'dirait « Demo » et le vieilli autre chose, et TOUT paraitrait reagir')


def test_l_outil_connait_les_trois_grammaires(outil):
    """Trois, pas deux. En ignorer une a fait rendre « sans vocabulaire » sur
    Options, qui portait justement l'une des constantes."""
    for sel in ("'.vx-fresh-chip[data-state]'",
                "'.vx-freshness[data-live]'",
                "'.vx-freshness[data-state]'"):
        assert sel in outil, (
            'la grammaire %s a disparu de l\'outil : une famille entiere '
            'd\'etiquettes cesse d\'etre mesuree' % sel)


def test_l_outil_mesure_badge_par_badge_et_non_page_par_page(outil):
    """La faute de granularité du lot 62 : un verdict par page masque un défaut
    par badge. L'appariement par chemin DOM est ce qui la répare."""
    assert 'def _comparer(avant, apres):' in outil, (
        'la comparaison badge-par-badge a disparu')
    assert "a = {b['chemin']: b for b in avant}" in outil, (
        'les etiquettes ne sont plus appariees par leur chemin DOM : deux badges '
        'de la meme page redeviennent indiscernables')
