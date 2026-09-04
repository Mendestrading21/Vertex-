"""Vertex Test 1.0 · #782 — CLASSIFICATION DES 697 BRANCHES, SANS RIEN SUPPRIMER.

`CLEANUP_POLICY.md` interdit toute suppression sans **preuve de non-usage**.
`tools/mesures/mesurer_branches.py` produit cette preuve, branche par
branche. Ce fichier garde l'instrument, pas le dépôt : il vérifie que la
classification reste **discriminante** et que ses témoins mordent.

## Ce que la mesure a établi

```text
697 branches distantes
 31  FUSIONNEE          — tous les commits sont dans main : perte NULLE prouvée
  1  CONTENU_IDENTIQUE  — commits inédits, diff vide
 51  CONTENUE_AILLEURS  — une autre branche la contient entièrement
614  UNIQUE             — contient du travail que main n'a pas
694 arbres distincts sur 697
```

## L'hypothèse que j'avais, et que la mesure a réfutée

Je m'attendais à ce que la série Skyler V2 soit une **chaîne linéaire** —
`lot-120` contenant `lot-119`, etc. Les compteurs de commits inédits le
suggéraient fortement : 274, 275, 276, incrémentés de 1.

Vérifié directement : `git merge-base --is-ancestor lot-100 lot-101` **échoue**.
Les branches ont été refaites, pas empilées. Et le regroupement par arbre le
confirme : **694 contenus distincts sur 697**.

Conséquence pour le nettoyage : il n'y a pas de collapse facile. Les 614
branches portent réellement 614 états différents du dépôt. La décision de les
garder ou non est une **politique**, pas une mesure — et c'est exactement le
partage que `CLEANUP_POLICY.md` prévoit.

## Le témoin qui compte le plus

Une classification qui range l'inconnu du côté rassurant est **plus dangereuse
que pas de classification** : elle autoriserait une suppression sur une preuve
qui n'en est pas une. Le témoin négatif vérifie donc qu'une référence fabriquée
ressort `INACCESSIBLE`, jamais `FUSIONNEE`.
"""
import pathlib
import sys

import pytest

RACINE = pathlib.Path(__file__).resolve().parents[1]
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

from tools.mesures import mesurer_branches as _mes  # noqa: E402


@pytest.fixture(scope='module')
def base():
    """`origin/main` si le dépôt a ses références distantes, sinon on saute :
    un conteneur frais peut ne pas les avoir, et un test qui échoue faute de
    données ne dit rien sur le code."""
    if _mes._git('rev-parse', '--verify', '--quiet', 'origin/main^{commit}') is None:
        pytest.skip('references distantes absentes de ce clone')
    return 'origin/main'


def test_le_temoin_negatif_ne_range_pas_l_inconnu_du_cote_rassurant(base):
    """LE TEST LE PLUS IMPORTANT DU FICHIER.

    Si une référence introuvable ressortait « FUSIONNEE », l'outil autoriserait
    une suppression sur une preuve qui n'existe pas."""
    fantome = _mes.classer(_mes.TEMOIN_ABSENT, base, set())
    assert fantome['classe'] == 'INACCESSIBLE', (
        'une reference inexistante est classee « %s » : l\'outil delivrerait '
        'un permis de supprimer sans preuve' % fantome['classe'])


def test_le_temoin_positif_prouve_que_la_comparaison_compare(base):
    """La base comparée à elle-même doit être fusionnée et sans diff. Sinon,
    « 31 fusionnées » ne veut rien dire."""
    soi = _mes.classer(base, base, _mes._fusionnees(base))
    assert soi['classe'] == 'FUSIONNEE' and soi['diff_vide'] is True


def test_la_classification_est_discriminante(base):
    """Une classification qui range tout dans une seule classe n'informe pas."""
    #  `confinement=False` : la recherche des maillons coute 614 appels git
    #  (~70 s). Un gardien lent finit desactive, et un gardien desactive ne
    #  garde rien. La passe complete reste dans le rapport.
    r = _mes.mesurer(base, confinement=False)
    assert r['total'] > 100, 'trop peu de branches pour conclure'
    #  CE QUE CE TEST A DÛ APPRENDRE SUR LUI-MÊME.
    #
    #  Sa première version exigeait « au moins 3 classes non vides ». Avec
    #  `confinement=False`, CONTENUE_AILLEURS n'est jamais calculée : il ne
    #  restait donc que FUSIONNEE, UNIQUE, et une CONTENU_IDENTIQUE qui tenait
    #  à UNE branche — la seule dont le diff avec `main` fût vide. Un clone qui
    #  ne la porte pas (693 refs au lieu de 697) faisait tomber le compte à 2 et
    #  échouer le test, sans qu'aucun code n'ait changé.
    #
    #  Le seuil reposait donc sur une coïncidence, pas sur une propriété. Ce qui
    #  guide réellement la décision de nettoyage est la SÉPARATION entre « perte
    #  prouvée nulle » et « porte du travail » — et qu'aucune des deux n'avale
    #  tout, car une classification qui range tout d'un côté n'informe pas.
    fusionnees = r['par_classe'].get('FUSIONNEE', 0)
    uniques = r['par_classe'].get('UNIQUE', 0)
    assert fusionnees > 0, (
        'aucune branche fusionnee detectee alors que main a des ancetres : '
        '`git branch -r --merged` ne repond plus')
    assert uniques > 0, (
        'aucune branche ne porte de travail inedit : `git rev-list` ou '
        '`git diff` ne repond plus')
    assert fusionnees + uniques <= r['total'], 'comptage incoherent'
    assert fusionnees < r['total'] and uniques < r['total'], (
        'une seule classe avale les %d branches : la classification ne guide '
        'plus aucune decision' % r['total'])


def test_la_serie_skyler_n_est_PAS_une_chaine_lineaire(base):
    """CONTRE-EXEMPLE MESURÉ, contre une intuition très plausible.

    Les compteurs de commits inédits s'incrémentent de 1 d'un lot au suivant,
    ce qui suggère fortement un empilement. Il n'y en a pas : les branches ont
    été refaites. Le vérifier empêche de « simplifier » le nettoyage sur une
    hypothèse fausse — et de supprimer un maillon en croyant qu'un autre le
    contient."""
    a = 'origin/agent/skyler-v2-lot-100'
    b = 'origin/agent/skyler-v2-lot-101'
    for ref in (a, b):
        if _mes._git('rev-parse', '--verify', '--quiet', ref + '^{commit}') is None:
            pytest.skip('branches Skyler absentes de ce clone')
    import subprocess
    contenu = subprocess.run(['git', 'merge-base', '--is-ancestor', a, b],
                             cwd=RACINE, capture_output=True).returncode == 0
    assert not contenu, (
        'lot-100 est desormais un ancetre de lot-101 : la serie a ete rebasee '
        'en chaine, et le recensement des maillons doit etre refait')


def test_l_outil_ne_supprime_rien():
    """Un outil de nettoyage qui peut supprimer est un outil qui supprimera.
    Celui-ci mesure, et c'est tout."""
    src = pathlib.Path(_mes.__file__).read_text(encoding='utf-8')
    for dangereux in ('push --delete', 'branch -D', 'branch -d', 'update-ref -d',
                      'reflog expire', 'gc --prune'):
        assert dangereux not in src, (
            'l\'instrument de mesure sait desormais supprimer (« %s ») : la '
            'preuve et l\'acte doivent rester separes' % dangereux)
