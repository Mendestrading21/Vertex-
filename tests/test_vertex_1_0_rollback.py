"""Vertex 1.0 · G6 — le comparateur de bureaux, et rien de plus.

Ce que ce fichier garde et ce qu'il ne garde PAS, dit franchement :

- **il garde** `comparer_bureaux`, la pièce qui décide si un retour arrière a
  perdu quelque chose. C'est du calcul pur, donc mutable, donc gardable ;
- **il ne garde pas** la mesure opérationnelle elle-même — créer un arbre de
  travail, démarrer un second serveur et interroger son API n'a pas sa place
  dans une suite qui doit rester rapide et hermétique. Cette preuve-là vit dans
  `docs/vertex-1.0/validation/G6-ROLLBACK.md`, avec sa date et son SHA.

Le dire est important : un gardien qui laisserait croire qu'il éprouve le
rollback complet vaudrait moins que pas de gardien du tout, parce qu'il
autoriserait à ne plus refaire la mesure.

Ce que la mesure a trouvé, et qui justifie la distinction faite ici entre
« absentes » et « différentes » : une clé qui disparaît se voit à l'écran (la
liste est vide, l'utilisateur appelle). Une clé dont le CONTENU a changé ne se
voit pas — l'écran affiche quelque chose de plausible. C'est la perte
silencieuse, et c'est la seule qui mérite le mot « danger ».
"""
from __future__ import annotations

import pathlib
import re

from tools.vertex_1_0.mesurer_rollback import comparer_bureaux

RACINE = pathlib.Path(__file__).resolve().parents[1]
OUTIL = RACINE / 'tools/vertex_1_0/mesurer_rollback.py'

BASE = {'data': {'myTrades': '[{"sym":"ACN"}]', 'myFavs': '["ABNB"]',
                 'vxJournal': '{}'}}


def test_deux_bureaux_identiques_ne_declenchent_rien():
    r = comparer_bureaux(BASE, {'data': dict(BASE['data'])})
    assert r['identique']
    assert not r['absentes'] and not r['differentes'] and not r['ajoutees']


def test_une_cle_disparue_est_vue():
    reste = {'data': {k: v for k, v in BASE['data'].items() if k != 'myFavs'}}
    r = comparer_bureaux(BASE, reste)
    assert not r['identique']
    assert r['absentes'] == ['myFavs']


def test_un_contenu_change_est_vu_et_nomme_a_part():
    """La perte SILENCIEUSE. Si elle était rangée avec les disparitions, un
    rapport pourrait dire « aucune clé perdue » alors que le bureau ment."""
    altere = {'data': dict(BASE['data'], myTrades='[]')}
    r = comparer_bureaux(BASE, altere)
    assert not r['identique']
    assert r['differentes'] == ['myTrades']
    assert not r['absentes'], (
        'un contenu modifié n\'est pas une disparition — les confondre ferait '
        'écrire « aucune clé perdue » sur un bureau vidé de sa substance.')


def test_une_cle_inventee_par_l_ancienne_version_est_vue():
    ajout = {'data': dict(BASE['data'], vieilleCle='1')}
    r = comparer_bureaux(BASE, ajout)
    assert not r['identique']
    assert r['ajoutees'] == ['vieilleCle']


def test_un_bureau_vide_face_a_un_bureau_plein_ne_passe_pas_pour_identique():
    """Le cas qui compte vraiment : le rollback démarre et rend un bureau
    vide. Sans cette assertion, « identique » resterait vrai sur deux
    dictionnaires vides et le rapport conclurait à tort."""
    r = comparer_bureaux(BASE, {})
    assert not r['identique']
    assert sorted(r['absentes']) == ['myFavs', 'myTrades', 'vxJournal']
    assert r['cles_apres'] == 0


def test_l_outil_emporte_les_donnees_dans_l_arbre_anterieur():
    """Sans la recopie du bureau, on mesurerait un démarrage à vide — une
    réponse « oui » à une question qu'on n'a pas posée."""
    src = OUTIL.read_text(encoding='utf-8')
    assert 'shutil.copy2(source, arbre / FICHIER_BUREAU)' in src, (
        "l'outil n'emporte plus le bureau dans l'arbre antérieur : il "
        'mesurerait un démarrage à vide.')


def test_l_outil_lit_la_variable_de_port_que_le_produit_lit():
    """Le premier essai passait `VERTEX_PORT`, que rien ne lit : la version
    antérieure s'était liée au port déjà pris et n'avait pas démarré.
    L'instrument accusait le produit d'un défaut qui était le sien."""
    src = OUTIL.read_text(encoding='utf-8')
    assert "PORT=str(PORT_ANCIEN)" in src
    #  On vise l'AFFECTATION, pas le mot : le commentaire qui raconte l'erreur
    #  cite forcément `VERTEX_PORT`, et interdire le mot effacerait la trace de
    #  la leçon en même temps que le défaut.
    assert not re.search(r'VERTEX_PORT\s*=\s*str', src), (
        "l'outil repasse par une variable de port que le produit ne lit pas.")
    produit = (RACINE / 'terminal.py').read_text(encoding='utf-8')
    assert "os.environ.get('PORT'" in produit, (
        'le produit ne lit plus `PORT` — la variable employée par la mesure '
        'doit suivre, sinon le banc teste un port que personne n\'écoute.')
