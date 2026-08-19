"""Vertex 1.0 · #779/G1 — `/scan` ET `/api/rescan` SORTENT AVEC LEUR PORTE.

Deux routes de plus quittent `terminal.py`, et avec elles la **porte
anti-rafale** : événement, verrou, fenêtre, délai restant. Le groupe n'avait
aucune dépendance au monolithe — seulement `threading`, `os`, `time` et `math`.

```text
routes LEGACY   7 → 5
```

## Le piège que l'analyse statique ne pouvait pas voir

`terminal.py` fait `from vertex.data.universe import *`. Les six ensembles
d'indices servis par `/scan` — `_DOW30`, `_NDX100`, `_SP500_SET`, `_RUT_SET`,
`_EU_SET`, `_ASIA_SET` — venaient donc du paquet **sans qu'aucune ligne d'import
ne les nomme**. Mon inventaire de dépendances, qui croise les symboles utilisés
avec les symboles déclarés, les avait comptés comme inexistants : ils
n'apparaissaient dans *aucune* des deux listes, donc leur intersection était
vide, et la route paraissait plus simple qu'elle ne l'était.

Un `import *` rend une mesure de dépendances **silencieusement incomplète**.
C'est un `curl /scan` qui l'a révélé, pas l'AST.

## Ce qui casserait en silence si l'événement était recréé

`vertex/services/live_engine.py::configure` transmet `EVENEMENT` à la boucle de
scan, qui attend **cet objet précis**. Le réassigner — au lieu de le muter par
`set()` — laisserait la boucle attendre un objet que plus personne ne réveille :
`/api/rescan` répondrait 200, et rien ne repartirait. Même famille de piège que
`scan_state` (« muter en place, jamais réassigner »).

## Un test qui dépendait de l'ordre des autres

La première version de `test_l_evenement_reste_celui_qu_attend_la_boucle`
affirmait `live_engine._CFG['rescan_event'] is rescan_gate.EVENEMENT`. Elle
passait seule et **échouait dans la suite complète** : `tests/test_live_engine.py`
reconfigure légitimement le moteur avec ses propres états. Un test qui dépend de
l'ordre des autres ne prouve rien ; il vise désormais le **câblage** de
`terminal.py`, qui est stable. (Il vit dans `tests/test_rescan_rate_limit.py`,
avec le reste de la porte.)

## `scan_age` avait deux implémentations identiques

`terminal.py::_scan_age` et une fermeture locale de
`vertex/app/routes/decision_api.py` calculaient exactement la même chose. Deux
copies dérivent au premier ajustement, et l'écran afficherait alors deux âges
différents pour la même donnée. Une seule maison : `vertex.app.state.scan_age`.
"""
import pathlib
import re

import pytest

from vertex.app import factory, rescan_gate
from vertex.app.state import scan_age, scan_state

RACINE = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def application():
    from vertex.runtime import app
    return app


@pytest.fixture(autouse=True)
def porte_ouverte():
    rescan_gate.reinitialiser()
    yield
    rescan_gate.reinitialiser()


def test_les_deux_routes_repondent_et_leur_contrat_tient(application):
    client = application.test_client()
    corps = client.get('/scan').get_json()
    for cle in ('ai_on', 'scan_age', 'rescan_cooldown_remaining', 'idx_sets',
                'data_source'):
        assert cle in corps, '/scan ne sert plus « %s »' % cle
    #  LE PIÈGE DE L'IMPORT ÉTOILÉ : ces six ensembles venaient du paquet sans
    #  qu'aucune ligne d'import ne les nomme. Vides, la page Marchés ne saurait
    #  plus dire à quel indice appartient un titre.
    tailles = {k: len(v) for k, v in corps['idx_sets'].items()}
    assert sorted(tailles) == ['asia', 'dow', 'eu', 'ndx', 'rut', 'sp']
    assert all(n > 0 for n in tailles.values()), (
        'un ensemble d\'indices est vide : %s' % tailles)

    r = client.get('/api/rescan')
    assert r.status_code == 200 and r.get_json()['ok'] is True


def test_les_blueprints_sont_les_proprietaires_declares(application):
    adaptateur = application.url_map.bind('localhost')
    for chemin, point in (('/scan', 'scan_api.scan_ep'),
                          ('/api/rescan', 'scan_api.api_rescan')):
        vu, _ = adaptateur.match(chemin)
        assert vu == point, '%s est servi par « %s »' % (chemin, vu)


def test_le_monolithe_ne_les_definit_plus():
    src = RACINE.joinpath('terminal.py').read_text(encoding='utf-8')
    for vue in ('scan_ep', 'api_rescan', '_scan_age'):
        assert not re.search(r'^def %s\(' % vue, src, re.M), (
            '`terminal.py` redefinit %s : deux domiciles, et rien ne dit '
            'lequel gagne' % vue)
    assert not re.search(r'^_last_rescan_ts\s*=', src, re.M), (
        'le monolithe tient de nouveau son propre horodatage de porte : deux '
        'fenetres independantes, donc aucune')


def test_la_porte_tient_sous_deux_demandes(application):
    """LE CŒUR DE LA PORTE. Le verrou couvre la LECTURE du délai et l'écriture
    de l'horodatage : sans lui, deux demandes simultanées verraient toutes deux
    la porte ouverte, et deux scans d'univers partiraient."""
    client = application.test_client()
    assert client.post('/api/rescan').status_code == 200
    r = client.post('/api/rescan')
    assert r.status_code == 429, 'la porte ne se referme plus'
    corps = r.get_json()
    assert corps['retry_after'] == rescan_gate.COOLDOWN_S
    assert r.headers['Retry-After'] == str(rescan_gate.COOLDOWN_S), (
        'le refus n\'est plus date : le client ne sait pas quand reessayer')


def test_le_refus_ne_trahit_jamais_qui_a_demande(application):
    """La fenêtre est **globale** et le reste : aucune identité n'est retenue,
    donc aucune ne peut fuir dans la réponse."""
    client = application.test_client()
    client.post('/api/rescan')
    corps = str(client.post('/api/rescan').get_json()).lower()
    for interdit in ('ip', 'address', 'client', 'requester', 'identity', 'token'):
        assert interdit not in corps, 'le refus expose « %s »' % interdit


def test_le_delai_servi_par_scan_suit_la_porte(application):
    """`/scan` et `/api/rescan` doivent parler du **même** délai. Deux sources
    divergeraient, et l'écran annoncerait un compte à rebours que le serveur
    n'applique pas."""
    client = application.test_client()
    assert client.get('/scan').get_json()['rescan_cooldown_remaining'] == 0
    client.post('/api/rescan')
    reste = client.get('/scan').get_json()['rescan_cooldown_remaining']
    assert reste == rescan_gate.COOLDOWN_S, (
        '/scan annonce %s s alors que la porte en applique %s'
        % (reste, rescan_gate.COOLDOWN_S))


def test_l_horloge_de_la_porte_ne_recule_jamais():
    """`time.monotonic()`, pas `time.time()`. Une horloge murale peut reculer —
    NTP, changement d'heure, sortie de veille — et un recul rendrait le délai
    restant négatif, donc la porte ouverte, au moment précis où elle doit tenir."""
    #  ON VISE LE CODE, PAS LE FICHIER. `time.time()` vit aussi dans le
    #  docstring qui EXPLIQUE pourquoi il est banni — le chercher tel quel
    #  faisait echouer ce test sur un module parfaitement correct. Dixieme
    #  occurrence de ce piege dans la serie.
    import ast as _ast
    arbre = _ast.parse(
        RACINE.joinpath('vertex/app/rescan_gate.py').read_text(encoding='utf-8'))
    appels = {_ast.unparse(n.func) for n in _ast.walk(arbre)
              if isinstance(n, _ast.Call)}
    assert 'time.monotonic' in appels, (
        'la porte n\'appelle plus l\'horloge monotone')
    assert 'time.time' not in appels, (
        'la porte est repassee a l\'horloge murale : un recul d\'horloge '
        'l\'ouvrirait')


def test_scan_age_n_a_plus_qu_une_maison():
    """Deux copies d'un même calcul dérivent au premier ajustement, et l'écran
    afficherait deux âges différents pour la même donnée."""
    src = RACINE.joinpath('vertex/app/routes/decision_api.py').read_text(
        encoding='utf-8')
    assert not re.search(r'^\s+def _scan_age\(', src, re.M), (
        'decision_api redefinit son propre calcul d\'age de scan')
    assert 'from vertex.app.state import scan_age' in src

    #  L'absence est un aveu, pas un zero : un scan qui n'a jamais eu lieu n'a
    #  pas « zero seconde » d'age.
    memoire = scan_state.pop('scan_ts', None)
    try:
        assert scan_age() is None, (
            'un scan absent rend une valeur numerique : une absence passerait '
            'pour de la fraicheur parfaite')
    finally:
        if memoire is not None:
            scan_state['scan_ts'] = memoire


def test_le_registre_declare_le_nouveau_proprietaire():
    assert ('vertex.app.routes.scan_api', 'bp') in factory.BLUEPRINTS


def test_aucun_chemin_d_ordre_dans_les_nouveaux_modules():
    for module in ('vertex/app/rescan_gate.py', 'vertex/app/routes/scan_api.py'):
        src = RACINE.joinpath(module).read_text(encoding='utf-8')
        for verbe in ('placeOrder', 'place_order', 'submit_order', 'transmit',
                      'bracketOrder', 'MarketOrder', 'LimitOrder'):
            assert verbe not in src, '%s contient %s' % (module, verbe)
