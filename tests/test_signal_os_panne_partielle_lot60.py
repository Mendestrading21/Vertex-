"""SIGNAL OS · LOT 60 — LA PANNE PARTIELLE, ET UNE MATRICE QUI DISAIT « OK » SANS RIEN PROUVER.

Réserve SIGNAL-OS-59 §5.2, de ma main : *« Coupure totale seulement. Une panne
partielle — une source sur cinq en échec — reste le cas le plus fréquent en
vrai, et n'est pas mesurée. »*

Une coupure totale est presque confortable : tout échoue, tout le monde le voit.
La panne partielle est plus traître — la page reçoit quatre réponses sur cinq,
elle a de quoi remplir la plupart de ses cases, et rien ne la force à signaler
celle qui manque.

## Trois fautes, et la deuxième rendait la mesure entièrement creuse

**1. La coupure sortait du périmètre des données.** `**/*market*` attrapait
aussi l'URL de la page `/markets` : le document recevait un 500, rien ne se
chargeait, et le témoin rendait « AVEUGLE ». Il avait raison — je mesurais un
navigateur privé de page, pas un produit qui dégrade. La coupure partielle
réutilise désormais le périmètre éprouvé du mode total et ne coupe, à
l'intérieur, que ce qui porte le nom de la famille.

**2. Trois familles sur six ne coupaient RIEN — et rendaient « 8/8 OK ».**
`portfolio`, `tracking`, `news` : aucune requête interceptée sur aucun des huit
espaces. Quarante-huit cellules vertes dont vingt-quatre ne prouvaient
strictement rien. Un satisfecit vide, et exactement ce que l'en-tête de l'outil
prétendait éviter en disant que les familles sont « tirées des routes réellement
servies ». Elles ne l'étaient pas : je les avais passées à la main. `--familles`
les **relève** maintenant du trafic réel.

**3. « Hors portée » n'existait pas.** Une page qui n'appelle simplement pas une
famille n'est ni saine ni aveugle. Les confondre trompe dans les deux sens : un
« OK » qui ne prouve rien, ou une alarme sur une page qui n'a rien à voir. Trois
verdicts, donc, et « hors portée » n'empoisonne pas le verdict d'ensemble.

## Ce que ce mode ne peut PAS voir — à dire, sinon le vert ment

L'outil détecte les hôtes qui **n'aboutissent pas**. Il ne sait pas reconnaître
un hôte qui aboutit avec une valeur **inventée** ou **périmée** à la place de la
donnée manquante. Un chiffre plausible affiché sans source lui paraîtra sain.
C'est une limite de méthode, pas un réglage — et c'est précisément le défaut que
la panne partielle rend le plus probable.
"""
import pathlib

import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent
OUTIL = RACINE / 'tools' / 'mesurer_hotes_resolus.py'


@pytest.fixture(scope='module')
def source():
    return OUTIL.read_text(encoding='utf-8')


def test_la_coupure_partielle_reste_dans_le_perimetre_des_donnees(source):
    """LA FAUTE LA PLUS COÛTEUSE, TENUE PAR SA CORRECTION.

    Un motif large (`**/*famille*`) attrape l'URL de la page elle-même. Le
    document reçoit alors un 500, rien ne se charge, et l'outil mesure un
    navigateur en panne au lieu d'un produit qui dégrade — verdict flatteur ou
    alarmant, jamais juste."""
    compact = source.replace(' ', '').replace('\n', '')
    assert "page.route('**/{api,scan,cal-feed,news-feed}**',_partielle)" in compact, (
        'la coupure partielle ne passe plus par le perimetre de donnees eprouve : '
        'si elle attrape l\'URL du document, l\'outil mesure un navigateur prive '
        'de page et non un produit qui degrade')
    assert 'famille in route.request.url.split' in source, (
        'la coupure partielle ne filtre plus par nom de famille a l\'interieur '
        'du perimetre')


def test_le_mode_partiel_exige_d_avoir_reellement_coupe(source):
    """ANTI-VACUITÉ. Trois familles sur six ne coupaient rien et rendaient
    « 8/8 OK » : quarante-huit cellules vertes dont la moitié ne prouvait rien."""
    assert 'if famille and not coupees:' in source, (
        'le temoin du mode partiel a disparu : une famille qui n\'intercepte '
        'aucune requete rendrait « tout aboutit » sans avoir rien coupe')
    assert 'HORS PORTEE' in source, (
        'le verdict « hors portee » a disparu — une page qui n\'appelle pas la '
        'famille serait comptee saine ou aveugle, et les deux seraient faux')


def test_les_trois_verdicts_restent_distincts(source):
    """OK / DÉFAUT / AVEUGLE / hors portée. Quatre mots, quatre significations."""
    compact = source.replace(' ', '').replace('\n', '')
    assert "{0:'OK',1:'DEFAUT',2:'AVEUGLE',3:'horsportee'}" in compact, (
        'la table des verdicts a change : verifier que « hors portee » reste '
        'distinct de « OK » et de « AVEUGLE »')
    assert 'pire = max(pire, 0 if code == 3 else code)' in source, (
        '« hors portee » empoisonne de nouveau le verdict d\'ensemble, ou bien '
        'un vrai defaut ne le remonte plus')


def test_les_familles_sont_relevees_et_non_supposees(source):
    """L'en-tête promettait des familles « tirées des routes réellement
    servies ». Elle mentait : je les passais à la main. `--familles` les relève
    du trafic réel des huit espaces."""
    assert 'def relever_familles(' in source, (
        'le releve des familles a disparu : elles redeviendraient des noms '
        'supposes, et trois des six premiers ne coupaient rien')
    assert "'--familles' in argv" in source, 'le mode --familles n\'est plus offert'


def test_la_limite_de_methode_est_ecrite_dans_l_outil(source):
    """UN VERT QUI NE DIT PAS CE QU'IL IGNORE EST UN MENSONGE POLI.

    L'outil voit les hôtes qui n'aboutissent pas. Il ne voit pas un hôte qui
    aboutit avec un chiffre inventé — le défaut que la panne partielle rend
    justement le plus probable. Cette limite doit rester écrite là où on lit le
    résultat."""
    assert 'Ce que ce mode ne peut PAS voir' in source, (
        'la limite de methode a ete retiree de l\'en-tete : un « 8/8 OK » se '
        'lirait comme une garantie qu\'il n\'est pas')
    assert 'inventée' in source or 'inventee' in source, (
        'la mention de la valeur inventee a disparu de la limite')
