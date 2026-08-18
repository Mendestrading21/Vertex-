"""SIGNAL OS · LOT 64 — UNE PORTÉE N'EST PAS UNE SORTIE.

Réserve SIGNAL-OS-63 §6.4, de ma main : *« `opts.freshness` n'est passé par aucun
appelant de `VXCharts.card`. Le badge de fraîcheur canonique du Chart Shell est
donc du code mort. »* Je l'avais lu au `grep` — ce n'est pas une mesure.

Ce lot mesure les **deux côtés du contrat** du Chart Shell, et il y a deux façons
de le rompre :

| direction | ce que ça veut dire |
| --- | --- |
| **passée, jamais lue** | une page **croit dire quelque chose** et le composant l'ignore |
| **lue, jamais passée** | une capacité que personne ne demande — du code mort |

La première est la plus grave, et le résultat est rassurant : **aucune**. Aucune
page ne croit nommer une source, une conclusion ou une limite que le shell
jetterait en silence.

## Ce que la seconde a trouvé, et la conclusion qu'elle renverse

`SKYLER-LOT-581` avait conclu, de `freshnessBadge` : *« un seul site d'appel,
mais il est dans `C.card` — **chaque carte-graphique du produit rend donc ce
badge** »*.

**C'est exactement l'inverse**, et c'est mesurable des deux côtés :

- statiquement, `opts.freshness` n'était passé par **aucun** appelant, et la
  fonction rend `''` sans valeur ;
- au navigateur, **4 cartes-graphiques peintes, 0 badge de fraîcheur**.

Le lot 581 avait justement corrigé « un compte d'appels n'est pas une surface
d'écran ». Il a commis aussitôt le défaut symétrique : **une portée n'est pas une
sortie.** Un raisonnement juste sur la portée d'un site d'appel, appliqué à un
appel qui ne produit rien.

Retiré plutôt que câblé : l'âge a **déjà** un domicile sur la carte — la
provenance en pied, peinte sur les 4 cartes mesurées. Câbler l'en-tête aurait
créé un second domicile pour la même donnée, le défaut même corrigé au lot 63.

## Trois artefacts de mon propre découpage, arrêtés avant publication

Mon premier passage accusait `false` et `true` d'être des options (valeurs par
défaut d'une déstructuration prises pour des clés), `height` d'être ignorée
(lue via `chartHeightStyle(opts)`, un saut que je ne suivais pas), et `coup`
d'être une clé — venue de « se lit d'un coup d'œil », un **commentaire** dont les
apostrophes ASCII désynchronisaient mon suivi des chaînes.

*Publier ces trois-là aurait été accuser le produit de mes fautes.*
"""
import pathlib

import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent
CORE = RACINE / 'vertex' / 'static' / 'vertex' / 'js' / 'charts' / 'chart-core.js'
HEAT = RACINE / 'vertex' / 'static' / 'vertex' / 'js' / 'charts' / 'heatmap.js'


@pytest.fixture(scope='module')
def mesure():
    from tools.mesurer_contrat_chart_shell import mesurer
    ignorees, mortes, opaques, lues, passees = mesurer()
    return {'ignorees': ignorees, 'mortes': mortes, 'opaques': opaques,
            'lues': lues, 'passees': passees}


def test_aucune_option_passee_n_est_ignoree_par_le_shell(mesure):
    """LA DIRECTION QUI COMPTE VRAIMENT.

    Une page qui passe `source:` en pensant nommer sa source, et rien ne
    s'affiche : c'est un défaut d'honnêteté, invisible à la lecture des deux
    fichiers séparément. Ce test le rendrait visible le jour où il apparaît."""
    assert mesure['ignorees'] == [], (
        'des options sont passees a un builder qui ne les lit pas : la page '
        'croit dire quelque chose que le composant jette en silence — %s'
        % mesure['ignorees'][:8])


def test_le_badge_de_fraicheur_mort_du_chart_shell_reste_retire(mesure):
    """`opts.freshness` n'a jamais rien peint. Le remettre sans appelant
    recréerait un second domicile pour un âge déjà affiché en pied de carte."""
    assert 'freshness' not in mesure['lues'].get('card', set()), (
        'le Chart Shell relit `opts.freshness` : si aucun appelant ne le passe, '
        'c\'est du code mort qui rend un badge vide ; s\'il en existe un, l\'age '
        'a desormais DEUX domiciles sur la meme carte (avec la provenance)')
    src = CORE.read_text(encoding='utf-8')
    #  On vise la DEFINITION, pas le nom : le nom survit dans le commentaire qui
    #  explique le retrait — un test cherchant « freshnessBadge » serait creux
    #  par construction (le piege des lots 57, 62 et 63).
    assert 'C.freshnessBadge = function' not in src, (
        'le badge de fraicheur du Chart Shell est revenu : il faut alors un '
        'appelant qui le nourrisse, sinon il rend une chaine vide sur chaque carte')
    assert 'C.freshnessBadge' not in HEAT.read_text(encoding='utf-8'), (
        'heatmap.js rappelle une fonction retiree : la carte leverait une erreur')


def test_les_deux_temoins_mordent():
    """Un détecteur qui trouve zéro dans les deux sens et qui est simplement
    aveugle rend le même résultat qu'un produit parfait. Deux témoins, un par
    direction, sur une copie en mémoire — jamais sur le disque."""
    from tools.mesurer_contrat_chart_shell import mesurer
    _, mortes, _, _, _ = mesurer(mut_lu=True)
    assert any(c == '__temoin_jamais_passe' for _, c in mortes), (
        'le temoin « lue jamais passee » ne mord plus : « aucun code mort » '
        'cesse de vouloir dire quelque chose')
    ignorees, _, _, _, _ = mesurer(mut_passe=True)
    assert any(c == '__temoin_jamais_lu' for _, c in ignorees), (
        'le temoin « passee jamais lue » ne mord plus — et c\'est la direction '
        'la plus grave des deux')


def test_les_commentaires_ne_fabriquent_plus_de_cles():
    """L'ARTEFACT QUI M'A FAIT INVENTER UNE OPTION.

    « se lit d'un coup d'œil » : deux apostrophes ASCII dans un commentaire
    désynchronisaient le suivi des chaînes, après quoi n'importe quel mot suivi
    de `:` devenait une clé. `coup` a bien failli être publié comme trouvaille."""
    from tools.mesurer_contrat_chart_shell import _masque
    t = "/* d'un coup d'oeil */ f({vrai:1});"
    m = _masque(t)
    assert len(m) == len(t), 'le masque doit conserver les longueurs'
    assert 'coup' not in m, 'le contenu du commentaire n\'est plus masque'
    assert 'vrai:1' in m, 'le masque a mange du code reel — il masque trop'


def test_les_interpolations_de_gabarit_sont_analysees_comme_du_code():
    """LA FAUTE QU'UNE MUTATION A RÉVÉLÉE, ET QUE RIEN NE COUVRAIT.

    Ma première version masquait tout ce qui se trouve entre deux accents
    graves. Or `${…}` contient du **code réel** — et c'est là que `C.card`
    compose son en-tête entier. Remettre `opts.freshness` dans la condition
    laissait donc le gardien vert : la lecture était invisible à l'instrument.
    Un masque trop large rend un détecteur silencieux, ce qui ressemble à s'y
    méprendre à un produit sain."""
    from tools.mesurer_contrat_chart_shell import _masque
    t = 'const h = `<b>texte affiche</b>${opts.freshness ? 1 : 0}`;'
    m = _masque(t)
    assert len(m) == len(t), 'le masque doit conserver les longueurs'
    assert 'texte affiche' not in m, (
        'le TEXTE du gabarit n\'est plus masque : des mots de l\'interface '
        'seront pris pour des cles')
    assert 'opts.freshness' in m, (
        'le CODE des interpolations `${…}` est masque : toutes les lectures '
        'd\'options faites dans un gabarit deviennent invisibles, et l\'outil '
        'declarera « ignorees » des cles parfaitement lues')


def test_les_valeurs_par_defaut_ne_sont_pas_prises_pour_des_cles():
    """`horizontal = false, fill = true` : ma première version ramassait
    `false` et `true` comme des options du composant."""
    from tools.mesurer_contrat_chart_shell import _cles_destructurees
    cles = _cles_destructurees(' horizontal = false, fill = true, yFmt ')
    assert cles == {'horizontal', 'fill', 'yFmt'}, (
        'les valeurs par defaut redeviennent des cles : `false` et `true` '
        'seraient publies comme des options mortes du composant — %s' % sorted(cles))


def test_le_saut_par_une_fonction_aide_est_suivi(mesure):
    """`C.card` ne lit pas `opts.height` : il appelle `chartHeightStyle(opts)`.
    Sans suivre ce saut, l'outil accusait la page de passer une clé que le
    composant lit parfaitement."""
    assert 'height' in mesure['lues'].get('card', set()), (
        'le saut par une fonction aide n\'est plus suivi : des cles parfaitement '
        'lues seront de nouveau declarees ignorees, et le produit accuse a tort')


def test_les_sites_non_analysables_sont_annonces(mesure):
    """AUCUNE LIMITE TUE. Un site dont l'objet est construit ailleurs échappe à
    l'outil ; le taire transformerait son silence en garantie."""
    assert isinstance(mesure['opaques'], list)
    assert mesure['opaques'], (
        'plus aucun site n\'est declare non analysable : soit l\'outil a gagne '
        'en puissance, soit il a cesse de compter ce qu\'il ne sait pas lire — '
        'verifier laquelle des deux avant de retirer ce test')
