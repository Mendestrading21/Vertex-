"""SIGNAL OS · LOT 65 — LE GUIDE QUI PILOTE CHAQUE SESSION N'ÉTAIT VÉRIFIÉ PAR RIEN.

`CLAUDE.md` est le document à plus fort effet de levier du dépôt : il est lu au
début de **chaque** session et décide de ce qu'on cherche, de ce qu'on croit déjà
mesuré, et de ce qu'on ne revérifie pas. **Rien ne le vérifiait.**

Il avait dérivé, de la façon la plus banale qui soit : il annonçait `terminal.py`
à **7 158 lignes** — le chiffre du lot 323 — alors que le fichier en compte
**7 275**. Personne n'a menti ; le code a bougé, la phrase est restée.

C'est exactement le défaut que cette série traque partout ailleurs, appliqué au
document qui la gouverne. Un guide faux est pire qu'un guide muet : il fait
économiser une vérification qu'il ne mérite pas.

## Ce qui est gardé — et seulement ce qui est vérifiable

1. chaque fichier cité existe (nom nu résolu dans l'arbre) ;
2. le compte de lignes de `terminal.py` annoncé est le vrai ;
3. la liste des modules `vertex/ui/*.py` annoncée « complète, mesurée » l'est ;
4. les cinq reliques annoncées supprimées le sont ;
5. `READONLY = True`.

Les affirmations d'opinion et les récits de lots ne sont **pas** jugés : ils ne
sont pas mécaniquement vérifiables, et prétendre le contraire serait la garantie
creuse que ce dépôt passe son temps à démonter.

## La règle que ce lot inscrit dans le guide, et pourquoi elle compte

Les lots 62 à 64 ont mesuré **neuf** étiquettes de fraîcheur : les cinq issues du
helper canonique réagissaient toutes à l'âge, les quatre écrites à la main
mentaient toutes. Le défaut ne venait pas d'une négligence mais d'une **pente** :
écrire l'étiquette soi-même est plus court que d'aller chercher un âge. Sans
règle écrite dans le guide, une session future la redescendra.
"""
import pathlib

import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent
GUIDE = RACINE / 'CLAUDE.md'


@pytest.fixture(scope='module')
def verif():
    from tools.mesurer_guide_exact import verifier
    mortes, ecarts, n = verifier()
    return {'mortes': mortes, 'ecarts': ecarts, 'n': n}


def test_le_guide_ne_pointe_vers_aucun_fichier_disparu(verif):
    """Un guide qui envoie chercher là où il n'y a rien fait perdre plus de temps
    qu'il n'en fait gagner — et il fait douter du reste, qui est juste."""
    assert verif['mortes'] == [], (
        'CLAUDE.md cite des fichiers qui n\'existent pas : %s' % verif['mortes'])
    assert verif['n'] >= 25, (
        'le releve ne trouve presque plus de fichiers cites (%d) : l\'extraction '
        'est cassee, et « aucune reference morte » ne veut plus rien dire'
        % verif['n'])


def test_les_chiffres_et_listes_du_guide_sont_exacts(verif):
    """LA DÉRIVE RÉELLE, TENUE PAR SA CORRECTION.

    7 158 annoncées contre 7 275 réelles. Rejouée : l'instrument la voit."""
    assert verif['ecarts'] == [], (
        'CLAUDE.md annonce des chiffres ou des listes que le code dement : %s'
        % ['%s : %s -> %s' % e for e in verif['ecarts']])


def test_le_temoin_mord():
    """« Aucune référence morte » et « je ne sais pas voir » rendent le même
    chiffre. Le témoin cite un fichier inexistant sur une copie en mémoire."""
    from tools.mesurer_guide_exact import verifier
    mortes, _, _ = verifier(temoin=True)
    assert 'tools/ce_fichier_nexiste_pas_temoin.py' in mortes, (
        'le temoin ne mord plus : le verdict de l\'outil cesse de valoir')


def test_les_fichiers_cites_comme_supprimes_ne_sont_pas_reproches_au_guide():
    """`vertex/ui/journal.py` est cité POUR DIRE qu'il n'existe plus. Le compter
    comme une référence morte serait reprocher au guide d'être exact."""
    from tools.mesurer_guide_exact import _CITES_COMME_SUPPRIMES
    assert 'vertex/ui/journal.py' in _CITES_COMME_SUPPRIMES
    for ref in _CITES_COMME_SUPPRIMES:
        assert not (RACINE / ref).exists(), (
            '%s existe de nouveau : il doit sortir de la liste des fichiers '
            '« cites comme supprimes », sinon l\'outil cesse de le verifier' % ref)


def test_la_regle_de_fraicheur_est_inscrite_dans_le_guide():
    """LA PENTE QUI A PRODUIT NEUF ÉTIQUETTES, DONT QUATRE MENSONGÈRES.

    Écrire l'étiquette à la main est plus court que d'aller chercher un âge.
    C'est une pente, pas une négligence — et seule une règle écrite dans le
    document lu à chaque session l'empêche d'être redescendue."""
    t = GUIDE.read_text(encoding='utf-8')
    #  On vise les DEUX entrees canoniques, pas le mot « fraicheur » : celui-ci
    #  apparait deja ailleurs dans le guide, et un test qui le chercherait
    #  passerait sans que la regle existe (le gardien creux de la serie).
    assert 'VX.freshness.domainChip(' in t, (
        'la voie canonique par domaine a disparu du guide : une session future '
        'reecrira une etiquette a la main, et le lot 63 a mesure que 4 sur 4 de '
        'celles-la mentaient')
    assert 'VX.freshness.THRESH' in t, (
        'le guide ne dit plus d\'EMPRUNTER les seuils : deux tables vont '
        'diverger, et deux pages diront des choses differentes de la meme donnee')
    assert 'vx-badge-status' in t, (
        'le piege du « mot honnete dans le mauvais vetement » a disparu du '
        'guide : un etat de connexion rehabille en age de donnee')
