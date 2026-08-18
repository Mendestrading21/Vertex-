"""SIGNAL OS · LOT 34 — READONLY TENU PAR UNE LISTE BLANCHE MESURÉE.

Réserve ouverte du lot 31, écrite en toutes lettres : le garde-fou READONLY
« reste une liste de NOMS ; un chemin d'exécution nommé dynamiquement
passerait ». Le lot 33 a montré ce que valent les listes de noms tenues à la
main — c'est par là qu'une quatrième sortie de news est passée.

On inverse l'instrument. Au lieu d'interdire `placeOrder`, `submit_order`,
`transmit`… (et d'espérer avoir tout nommé), on **énumère les capacités
réellement employées** sur l'objet `IB` et on les confronte à une liste blanche
classée une à une. Une capacité nouvelle sort du lot **quel que soit son nom**.

Ce que la mesure dit aujourd'hui : 22 capacités distinctes, toutes en lecture,
aucun accès à nom calculé. `placeOrder` n'est pas « interdit » — il est
**absent**, et sa réapparition serait vue sans qu'on ait eu à le prévoir.

Les deux garde-fous d'un tel test — il ne suffit pas qu'il passe :
  · un TÉMOIN prouve que le scanner voit vraiment un ordre (sinon un scanner
    aveugle passerait toujours) ;
  · un PLANCHER interdit qu'il ne trouve presque plus rien.
"""
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import mesurer_surface_ibkr as surface        # noqa: E402


def test_toute_la_surface_ibkr_employee_est_classee_en_lecture():
    """LA propriété. Elle ne nomme aucun interdit : elle énumère l'employé."""
    vue, _, _, _ = surface.mesurer()
    hors = sorted(set(vue) - surface.LISTE_BLANCHE)
    assert not hors, (
        'capacite(s) IBKR employees hors liste blanche : %s\n'
        'A CLASSER PAR UN HUMAIN — lecture seule, ou execution ? Si lecture, '
        'ajouter a LISTE_BLANCHE avec le commentaire qui le justifie ; si '
        'execution, c\'est une violation de l\'invariant produit.'
        % ', '.join('%s (%s)' % (n, ', '.join(sorted(set(vue[n])))) for n in hors))


def test_aucun_acces_a_nom_calcule_sur_l_objet_ibkr():
    """Un nom calculé échappe par construction à toute liste, blanche comme
    noire. On n'en interdit pas l'idée — on constate qu'il n'y en a pas, et on
    le saura le jour où il y en aura un."""
    _, dynamiques, _, _ = surface.mesurer()
    assert not dynamiques, (
        'acces IBKR a nom calcule : %s — aucune liste ne peut le classer'
        % dynamiques)


def test_la_liste_blanche_elle_meme_ne_contient_aucun_verbe_d_execution():
    """Sinon il suffirait d'ajouter `placeOrder` à la liste blanche pour que le
    gardien se taise. La liste est gardée par ce qu'elle NE PEUT PAS contenir."""
    coupables = [c for c in surface.LISTE_BLANCHE
                 if any(v in c.lower() for v in surface.VERBES_D_ORDRE)]
    assert not coupables, 'verbe d\'execution dans la liste blanche : %s' % coupables


def test_le_scanner_voit_un_ordre_quand_il_y_en_a_un(tmp_path):
    """LE TÉMOIN — sans lui, un scanner aveugle passerait tous les autres tests.

    Trois formes, dont deux que ma première version ratait : l'ALIAS
    (`self._ib = ib`, seul chemin par lequel la passerelle appelle IBKR) et le
    SECOND NIVEAU (`ib.client.…`)."""
    (tmp_path / 'faux.py').write_text(textwrap.dedent('''
        from ib_insync import IB
        def executer(contrat, ordre):
            ib = IB()
            ib.placeOrder(contrat, ordre)          # direct
            self._ib = ib
            self._ib.cancelOrder(ordre)            # par alias
            ib.client.placeOrderAsync(ordre)       # second niveau
    '''), encoding='utf-8')
    vue, _, porteurs, lus = surface.mesurer(str(tmp_path), ignorer_tests=False)
    assert lus == 1 and porteurs == {'ib', '_ib'}
    for capacite in ('placeOrder', 'cancelOrder', 'client.placeOrderAsync'):
        assert capacite in vue, '%s invisible pour le scanner' % capacite
    assert sorted(set(vue) - surface.LISTE_BLANCHE) == [
        'cancelOrder', 'client.placeOrderAsync', 'placeOrder']


def test_le_scanner_voit_un_nom_calcule_quand_il_y_en_a_un(tmp_path):
    """Second témoin : le nom calculé doit être RELEVÉ, et le nom littéral doit
    au contraire rejoindre la surface (sinon on le perdrait des deux côtés)."""
    (tmp_path / 'faux.py').write_text(textwrap.dedent('''
        from ib_insync import IB
        def ruse(verbe):
            ib = IB()
            getattr(ib, verbe)()                   # nom CALCULE
            getattr(ib, 'reqTickers')()            # nom litteral
    '''), encoding='utf-8')
    vue, dynamiques, _, _ = surface.mesurer(str(tmp_path), ignorer_tests=False)
    assert len(dynamiques) == 1 and dynamiques[0][0] == 'faux.py'
    assert 'reqTickers' in vue, 'un nom litteral doit rejoindre la surface'


def test_la_mesure_couvre_reellement_le_depot():
    """Le plancher. Un scanner qui ne lit plus rien passerait tout le reste."""
    vue, _, porteurs, lus = surface.mesurer()
    assert lus >= 250, 'le scanner ne lit plus que %d fichiers' % lus
    assert porteurs >= {'ib', '_ib'}, (
        'objets IB derives : %s — l\'alias `self._ib` n\'est plus suivi, et la '
        'passerelle n\'appelle IBKR QUE par lui' % sorted(porteurs))
    assert len(vue) >= 20, 'surface tombee a %d capacites' % len(vue)
