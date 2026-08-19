"""Vertex 1.0 · G5 — lancer TWS doit suffire.

Ce fichier garde la promesse « je lance TWS et ça se connecte », et il la garde
là où elle se cassait vraiment : pas dans la connexion elle-même — qui marchait
— mais dans les **désaccords entre les cinq endroits qui se connectaient**.

Les trois défauts mesurés dans le code, et ce qu'ils produisaient :

1. la lecture du compte cherchait le **papier** en premier, les trois autres
   flux le **réel**. Deux TWS joignables → le cash d'un compte et les cotations
   d'un autre sur le même écran. Chaque chiffre vrai, l'écran faux ;
2. deux sites portaient le **clientId 17**. IBKR refuse la seconde session, et
   le message d'erreur ne parle jamais de collision ;
3. la passerelle n'essayait **qu'un port** (7497). Sur un TWS réel seul, elle ne
   se connectait jamais, en silence.

Aucun de ces trois-là ne se voit dans un test qui ouvre une connexion : ils ne
se voient qu'en comparant les sites entre eux. D'où des tests qui lisent le
code autant qu'ils exécutent le module.
"""
from __future__ import annotations

import pathlib
import re

import pytest

from vertex.data_sources import ibkr_link

RACINE = pathlib.Path(__file__).resolve().parents[1]
TERMINAL = RACINE / 'terminal.py'
PASSERELLE = RACINE / 'vertex/data_sources/ibkr_gateway.py'


@pytest.fixture(autouse=True)
def _memoire_vierge():
    """Le module retient le port qui a marché — un test qui hériterait du
    souvenir d'un autre mesurerait autre chose que ce qu'il croit."""
    ibkr_link.oublier()
    yield
    ibkr_link.oublier()


# ── Les identifiants ──────────────────────────────────────────────────────

def test_chaque_role_a_son_identifiant_et_ils_sont_tous_distincts():
    ids = ibkr_link.CLIENT_IDS
    assert len(set(ids.values())) == len(ids), (
        'deux rôles partagent un clientId : IBKR refusera la seconde session, '
        'et le message d\'erreur ne mentionnera pas la collision. C\'est '
        'exactement le défaut corrigé (compte et passerelle valaient 17).')
    assert {'options', 'compte', 'cotations', 'indices', 'passerelle'} <= set(ids)


def test_un_role_inconnu_est_une_erreur_franche():
    """Rendre un identifiant par défaut recréerait la collision qu'on corrige —
    silencieusement, ce qui est pire."""
    with pytest.raises(KeyError):
        ibkr_link.client_id('inexistant')


def test_plus_aucun_clientid_en_dur_dans_les_sites_de_connexion():
    src = TERMINAL.read_text(encoding='utf-8')
    en_dur = re.findall(r'clientId\s*=\s*(\d+)', src)
    assert not en_dur, (
        'clientId écrit en dur dans terminal.py : %s — le registre unique perd '
        'sa raison d\'être dès qu\'un site s\'en écarte.' % en_dur)


# ── L'ordre des ports ─────────────────────────────────────────────────────

def test_un_seul_ordre_de_ports_pour_tout_le_produit():
    """LE défaut n°1. Il ne se voit qu'en comparant les sites entre eux."""
    for fichier in (TERMINAL, PASSERELLE):
        src = fichier.read_text(encoding='utf-8')
        code = '\n'.join(l for l in src.splitlines()
                         if not l.lstrip().startswith('#'))
        tuples = re.findall(r'\(\s*74\d\d\s*,\s*\d{4}[^)]*\)', code)
        assert not tuples, (
            '%s porte encore sa propre liste de ports : %s. Deux ordres '
            'différents = le cash d\'un compte et les cotations d\'un autre.'
            % (fichier.name, tuples))


def test_le_reel_est_cherche_avant_le_papier():
    ordre = ibkr_link.ports_declares()
    assert ordre.index(7496) < ordre.index(7497)
    assert ordre.index(4001) < ordre.index(4002)


def test_un_port_force_passe_devant_sans_masquer_les_autres(monkeypatch):
    """Forcer un port ne doit pas EMPÊCHER de trouver TWS ailleurs : une
    variable oubliée dans un `.env` couperait sinon la connexion sans rien
    dire — précisément le genre de panne qu'on ne diagnostique pas."""
    monkeypatch.setenv('IBKR_PORT', '4002')
    ordre = ibkr_link.ports_declares()
    assert ordre[0] == 4002
    assert set(ordre) >= {7496, 7497, 4001, 4002}, (
        'forcer un port a supprimé les autres : TWS relancé sur un autre port '
        'ne serait plus jamais trouvé.')


def test_le_port_qui_a_marche_passe_en_tete():
    assert ibkr_link.ordre_des_ports()[0] == 7496
    ibkr_link.noter_succes(4001, 'cotations')
    assert ibkr_link.ordre_des_ports()[0] == 4001, (
        'le port trouvé n\'est pas partagé : chaque flux repaie la découverte, '
        'et TWS éteint le worker options attend 4 essais × 6 s par job.')


def test_le_souvenir_est_efface_quand_plus_personne_n_y_arrive():
    """Un souvenir qu'on ne remet jamais en question devient un mensonge le
    jour où l'utilisateur passe du papier au réel."""
    ibkr_link.noter_succes(7497, 'cotations')
    assert ibkr_link.etat()['port'] == 7497
    ibkr_link.noter_echec('cotations', 'TWS ferme')
    assert ibkr_link.etat()['port'] is None
    assert 'API' in ibkr_link.etat()['raison'], (
        "l'état muet ne dit plus quoi faire : « ça ne marche pas » sans geste "
        'à faire n\'aide personne.')


def test_un_role_encore_connecte_conserve_le_souvenir():
    """Le contre-exemple : un flux qui tombe pendant qu'un autre tient ne doit
    pas effacer un port qui marche encore."""
    ibkr_link.noter_succes(7496, 'cotations')
    ibkr_link.noter_echec('indices', 'timeout')
    assert ibkr_link.etat()['port'] == 7496


# ── La sonde ──────────────────────────────────────────────────────────────

def test_la_sonde_trouve_le_premier_port_ouvert():
    r = ibkr_link.sonder(essai=lambda p: p == 7497)
    assert r['retenu'] == 7497
    assert r['mode'] == 'TWS papier'
    assert not r['ambigu']


def test_la_sonde_signale_l_ambiguite_quand_deux_tws_repondent():
    """Deux TWS joignables n'est pas une erreur — mais le taire, si : c'est la
    situation exacte où l'écran peut mélanger deux comptes."""
    r = ibkr_link.sonder(essai=lambda p: p in (7496, 7497))
    assert r['ambigu']
    assert r['retenu'] == 7496, 'le réel doit gagner quand les deux répondent'


def test_la_sonde_ne_ment_pas_quand_rien_ne_repond():
    r = ibkr_link.sonder(essai=lambda p: False)
    assert r['retenu'] is None and r['mode'] is None and not r['ouverts']


def test_la_sonde_n_ouvre_aucune_session_ibkr():
    """Elle parle TCP, pas le protocole IBKR : aucun clientId consommé, aucune
    session vivante perturbée. Une sonde qui se connecterait vraiment pourrait
    faire tomber le flux qu'elle vient vérifier."""
    #  Lecture à l'AST, pas au texte : la docstring de ce module DÉCRIT le
    #  défaut corrigé et cite forcément `clientId` et `ib_async`. Un contrôle
    #  textuel interdirait d'expliquer ce qu'on garde.
    import ast
    src = (RACINE / 'vertex/data_sources/ibkr_link.py').read_text(encoding='utf-8')
    arbre = ast.parse(src)
    for n in ast.walk(arbre):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            noms = [a.name for a in n.names] + [getattr(n, 'module', '') or '']
            assert not any('ib_async' in x or 'ib_insync' in x for x in noms), (
                'ibkr_link importe la bibliothèque du broker : il ouvrirait de '
                'vraies sessions, consommerait des clientId, et pourrait faire '
                'tomber le flux qu\'il vient vérifier.')
        if isinstance(n, ast.Call):
            assert not any(k.arg == 'clientId' for k in n.keywords), (
                'ibkr_link ouvre une session IBKR : sa sonde doit rester au '
                'niveau TCP.')
    assert 'socket.create_connection' in src


# ── La passerelle ─────────────────────────────────────────────────────────

def test_la_passerelle_cherche_le_port_au_lieu_d_en_supposer_un():
    src = PASSERELLE.read_text(encoding='utf-8')
    assert '_DEFAULT_PORT = None' in src, (
        'la passerelle refige un port : elle ne se connectait JAMAIS sur un '
        'TWS réel seul, en silence.')
    assert 'ibkr_link.ordre_des_ports()' in src


def test_la_passerelle_ne_partage_plus_l_identifiant_du_compte():
    from vertex.data_sources.ibkr_gateway import IbkrGateway
    gw = IbkrGateway()
    assert gw.client_id != ibkr_link.client_id('compte')
    assert gw.client_id == ibkr_link.client_id('passerelle')


def test_la_passerelle_avoue_l_echec_au_lieu_de_rendre_un_objet_vide():
    """Un appelant qui recevrait None irait chercher des cotations sur un objet
    absent, et l'erreur parlerait d'attribut manquant au lieu de TWS."""
    from vertex.data_sources.ibkr_gateway import IbkrGateway
    gw = IbkrGateway(host='127.0.0.1')
    with pytest.raises((ConnectionError, Exception)) as exc:
        gw.connect()
    assert 'TWS' in str(exc.value) or 'ports' in str(exc.value).lower()


def test_le_verrou_lecture_seule_reste_ecrit_sur_chaque_site():
    """Le déplacer dans `ibkr_link` le rendrait invisible aux garde-fous qui le
    cherchent à côté de `clientId=` — la protection existerait encore mais plus
    rien ne la tiendrait."""
    for fichier in (TERMINAL, PASSERELLE):
        src = fichier.read_text(encoding='utf-8')
        for m in re.finditer(r'\.connect\s*\(', src):
            seg = src[m.start():m.start() + 260]
            if 'clientId' not in seg:
                continue
            assert re.search(r'readonly\s*=\s*True', seg), (
                '%s : connexion IBKR sans readonly=True' % fichier.name)


def test_la_sonde_trouve_un_VRAI_socket_ouvert():
    """Les autres tests injectent `essai` — utile pour éprouver la logique, mais
    cela ne prouve pas que la sonde TCP fonctionne. On ouvre donc un vrai
    écouteur sur un port standard : c'est la moitié de la promesse « je lance
    TWS et ça se connecte » qui est vérifiable sans TWS.

    Ce que cela NE prouve pas : la poignée de main IBKR elle-même. Le socket
    répond, le protocole n'est pas parlé — et il vaut mieux le dire que de
    laisser croire que G5 est couvert.
    """
    import socket as _socket
    srv = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
    srv.setsockopt(_socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1)
    try:
        srv.bind(('127.0.0.1', 4002))
    except OSError:
        pytest.skip('port 4002 déjà pris — la mesure porterait sur autre chose')
    srv.listen(1)
    try:
        r = ibkr_link.sonder(ports=(7496, 4002), hote_='127.0.0.1', delai=0.5)
        assert r['ouverts'] == [4002], (
            'la sonde TCP ne voit pas un écouteur réel : la découverte '
            'automatique ne fonctionnerait pas non plus avec TWS.')
        assert r['mode'] == 'IB Gateway papier'
    finally:
        srv.close()
