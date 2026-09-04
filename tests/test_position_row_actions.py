"""Lot 35 — les actions d'une POSITION sont accessibles depuis ses lignes.

Trois défauts mesurés au navigateur (E2E, serveur démo) :

1. le bouton ⋯ des lignes de positions portait `data-entity-menu` (menu du
   TITRE : favoris, watchlist, alerte…) — « Modifier / Clôturer / Supprimer
   la position » (`E.openPositionMenu`, par id) n'était déclenchable NULLE
   PART : une saisie erronée était indélébile depuis l'interface ;
2. le bouton « Clôturer » (`data-close-pos`) n'avait AUCUN handler — bouton
   mort ;
3. `openAddModal('', 'position')` (bouton « Déclarer une position ») oubliait
   la destination préréglée après la saisie du ticker : l'étape 2 redemandait
   « Position » à l'utilisateur qui venait de cliquer « Déclarer une
   position ».

Ces bancs épinglent la vérité SERVIE (fichiers réellement servis), pas une
intention.
"""
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PAGE = (RACINE / 'vertex' / 'ui' / 'pages' / 'portfolio_page.py').read_text(encoding='utf-8')
ENTITES = (RACINE / 'vertex' / 'static' / 'vertex' / 'js' / 'vx-entities.js').read_text(encoding='utf-8')


def test_lignes_positions_ouvrent_le_menu_position():
    """Chaque surface listant des positions (cartes équipe, tableau actions,
    tableau options) offre le menu POSITION par id — pas seulement le menu
    du titre."""
    assert PAGE.count('data-position-menu="${t.id}"') >= 3, (
        'les lignes de positions doivent porter data-position-menu="${t.id}" '
        '(menu Modifier/Clôturer/Supprimer) — sinon une saisie erronée est '
        'indélébile depuis l’interface')


def test_bouton_cloturer_a_un_handler():
    """`data-close-pos` est câblé dans la délégation globale de vx-entities.js
    vers E.openClosePosition (clôture déclarative → journal)."""
    assert 'data-close-pos' in ENTITES, (
        'le bouton Clôturer (data-close-pos) doit avoir un handler délégué — '
        'mesuré mort au navigateur (aucun listener)')
    assert 'openClosePosition' in ENTITES.split('data-close-pos', 1)[1][:400], (
        'le handler data-close-pos doit ouvrir E.openClosePosition')


def test_declarer_une_position_saute_le_choix_de_destination():
    """openAddModal('', dest) : après la saisie du ticker, si la destination
    est déjà connue, on va directement à l'étape 3 (détails)."""
    apres = ENTITES.split("getElementById('vx-add-next')", 1)[1][:400]
    assert 'dest ? 3 : 2' in apres, (
        "le handler Continuer doit honorer la destination préréglée : "
        "step = dest ? 3 : 2 — sinon « Déclarer une position » redemande "
        "la destination déjà choisie")
