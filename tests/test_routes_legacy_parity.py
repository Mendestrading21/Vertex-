"""Vertex Test 1.0 · #779/G1 — QUATRE ROUTES QUITTENT LE MONOLITHE, ET UNE PASSERELLE.

`RELEASE_GATES.md` G1 veut que `terminal.py` cesse d'être le centre de nouvelles
responsabilités. L'inventaire comptait **11 routes LEGACY** ; ce lot en déplace
quatre, après avoir mesuré — et non supposé — ce dont chacune dépend vraiment.

## La mesure qui a changé le plan

Le premier arbitrage annonçait « 2 à 5 dépendances chacune, patron
`make_blueprint` requis ». En classant chaque dépendance par son **origine** —
définie dans `terminal.py`, ou seulement importée depuis le paquet — le tableau
s'est révélé bien plus favorable :

```text
api_track_record   0 dépendance LOCALE  (`_track` et `scan_state` sont du paquet)
api_alerts_status  1                    (`_ALERTS_FIRED`)
ibkr_ep            1                    (`_ibkr_snapshot`)
quotes_ep          1                    (`_sync_ibkr_state`) … qui n'en avait aucune
```

`_sync_ibkr_state` a donc pu **partir avec** : ses deux entrées, `_live_meta` et
`scan_state`, avaient déjà un domicile dans le paquet. Elle restait dans le
monolithe par habitude, pas par couplage.

## Pourquoi cette passerelle de quatre lignes compte

C'est le **seul chemin** par lequel l'état réel du socket IBKR atteint la page
Système : `vertex/services/connections.py` lit `scan_state['ibkr_connected']` et
`['ibkr_live']`, que personne d'autre n'écrit. La casser afficherait un état de
*configuration* — « IBKR activé » — au lieu d'un état de *session*, c'est-à-dire
exactement le mensonge que `connections.py` existe pour éviter.

## Le seuil de fraîcheur est EMPRUNTÉ, jamais recopié

`/quotes` et la passerelle partagent `ibkr_state.FENETRE_S`. Deux tables
divergeraient au premier ajustement, et `/quotes` servirait des cours que la page
Système déclare périmés — le défaut mesuré aux lots 62-64 sur les étiquettes de
fraîcheur, transposé au serveur.
"""
import pathlib

import pytest

from vertex.app import factory, ibkr_state
from vertex.app.caches import _live_meta
from vertex.app.state import scan_state

RACINE = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def application():
    from vertex.runtime import app
    return app


@pytest.fixture()
def meta_propre():
    avant = dict(_live_meta)
    yield
    _live_meta.clear()
    _live_meta.update(avant)


def test_les_quatre_routes_repondent_encore(application):
    """La parité, vue du client : mêmes chemins, mêmes formes de réponse."""
    client = application.test_client()
    attendus = {
        '/quotes': ('quotes', 'meta', 'fresh'),
        #  Lot 2 : `/ibkr` rend la preuve de socket — connected/mode/error —
        #  et plus AUCUN champ de compte (positions, net_liq, cash retires).
        '/ibkr': ('connected', 'mode'),
        '/api/alerts/status': ('fired', 'ts'),
        '/api/track-record': ('by_verdict', 'by_grade', 'by_regime'),
    }
    for chemin, cles in attendus.items():
        r = client.get(chemin)
        assert r.status_code == 200, '%s repond %d' % (chemin, r.status_code)
        corps = r.get_json()
        manquantes = [c for c in cles if c not in corps]
        assert not manquantes, (
            '%s ne sert plus %s : le contrat a change en deplaçant la route'
            % (chemin, manquantes))


def test_les_blueprints_sont_les_proprietaires_declares(application):
    """Un chemin qui répond ne dit pas QUI le sert. Si le monolithe en gardait
    une copie, la route répondrait toujours — et l'extraction n'aurait rien
    déplacé."""
    adaptateur = application.url_map.bind('localhost')
    for chemin, point in (('/quotes', 'live_state_api.quotes_ep'),
                          ('/ibkr', 'live_state_api.ibkr_ep'),
                          ('/api/alerts/status', 'live_state_api.api_alerts_status'),
                          ('/api/track-record', 'track_record_api.api_track_record')):
        vu, _ = adaptateur.match(chemin)
        assert vu == point, '%s est servi par « %s », pas par %s' % (chemin, vu, point)


def test_le_monolithe_ne_les_definit_plus():
    """La preuve que l'extraction a RETIRÉ, et pas seulement ajouté."""
    src = RACINE.joinpath('terminal.py').read_text(encoding='utf-8')
    import re
    for vue in ('quotes_ep', 'ibkr_ep', 'api_alerts_status', 'api_track_record'):
        #  ON VISE LA DÉFINITION, pas le nom : les trois vues sont citées dans
        #  les commentaires qui expliquent leur départ.
        assert not re.search(r'^def %s\(' % vue, src, re.M), (
            '`terminal.py` redefinit %s : la route a deux domiciles, et rien '
            'ne dit lequel gagne' % vue)
    assert not re.search(r"^@app\.route\('/quotes'\)", src, re.M)
    assert '_live_state_api.make_blueprint(' in src, (
        'le monolithe n\'enregistre plus les sondes d\'etat : trois routes '
        'disparaissent du service')


def test_la_passerelle_ibkr_est_bien_celle_qui_sert():
    """`terminal._sync_ibkr_state` doit ÊTRE la fonction du paquet, pas une
    copie qui lui ressemble. Deux implémentations divergeraient en silence."""
    import terminal
    assert terminal._sync_ibkr_state is ibkr_state.sync, (
        'le monolithe a repris sa propre passerelle : `connections.py` lirait '
        'un etat ecrit par un autre code que celui qui est teste ici')
    src = RACINE.joinpath('terminal.py').read_text(encoding='utf-8')
    import re
    assert not re.search(r'^def _sync_ibkr_state\(', src, re.M)


def test_la_passerelle_ecrit_bien_dans_letat_partage(meta_propre):
    """L'EFFET, pas la présence. C'est le seul chemin par lequel l'état du
    socket atteint la page Système."""
    import time
    _live_meta.update({'connected': True, 'rt': True, 'ts': time.time()})
    assert ibkr_state.sync() is True
    assert scan_state['ibkr_connected'] is True
    assert scan_state['ibkr_live'] is True

    #  Un worker figé garde `connected: True` : le socket n'est pas fermé, il ne
    #  répond plus. Sans borne d'âge, l'ecran annoncerait « live » sur des ticks
    #  vieux de plusieurs heures.
    _live_meta['ts'] = time.time() - (ibkr_state.FENETRE_S + 5)
    assert ibkr_state.sync() is False
    assert scan_state['ibkr_connected'] is False, (
        'une session dont les ticks sont perimes est encore declaree '
        'connectee : le garde-fou de fraicheur ne mord plus')


def test_quotes_refuse_de_servir_des_cours_perimes(application, meta_propre):
    """LE POINT DE LA ROUTE. Servir une table ancienne en la présentant comme du
    direct serait une valeur inventée au sens de la règle n°4 ; rendre `{}` est
    l'aveu honnête."""
    import time
    from vertex.app.caches import _live_quotes
    _live_quotes['TEST'] = {'last': 1.0}
    try:
        _live_meta.update({'connected': True, 'rt': True, 'ts': time.time()})
        corps = application.test_client().get('/quotes').get_json()
        assert corps['fresh'] is True and 'TEST' in corps['quotes']

        _live_meta['ts'] = time.time() - (ibkr_state.FENETRE_S + 5)
        corps = application.test_client().get('/quotes').get_json()
        assert corps['fresh'] is False, 'la fraicheur annoncee ne suit plus l\'age'
        assert corps['quotes'] == {}, (
            'des cours perimes sont servis comme du direct : %s' % corps['quotes'])
    finally:
        _live_quotes.pop('TEST', None)


def test_le_seuil_de_fraicheur_est_emprunte_et_non_recopie():
    """Deux tables de seuils divergeraient au premier ajustement, et `/quotes`
    servirait des cours que la page Système déclare périmés — le défaut mesuré
    aux lots 62-64 sur les étiquettes, transposé au serveur."""
    src = RACINE.joinpath('vertex/app/routes/live_state_api.py').read_text(
        encoding='utf-8')
    assert 'ibkr_state.frais()' in src, (
        'la route calcule sa propre fraicheur au lieu d\'emprunter celle de '
        'la passerelle')
    import re
    assert not re.search(r'\b75\b', src), (
        'un seuil numerique est de nouveau ecrit en dur dans la route')


def test_les_alertes_sont_partagees_par_reference():
    """La boucle d'alertes mute `_ALERTS_FIRED` en place. Si la fabrique en
    prenait une COPIE, la route servirait l'état du démarrage pour toujours —
    et rien ne planterait."""
    import terminal
    from vertex.app.routes import live_state_api

    partage = {}
    bp = live_state_api.make_blueprint(ibkr_snapshot=lambda: {}, alerts_fired=partage)
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(bp)
    partage['ACN'] = {'niveau': 100}
    assert app.test_client().get('/api/alerts/status').get_json()['fired'] == {
        'ACN': {'niveau': 100}}, (
        'la fabrique a copie le dictionnaire : les alertes declenchees apres le '
        'demarrage ne seraient jamais servies')

    src = RACINE.joinpath('terminal.py').read_text(encoding='utf-8')
    assert 'alerts_fired=_ALERTS_FIRED' in src, (
        'le monolithe ne passe plus son dictionnaire d\'alertes')


def test_le_registre_declare_les_nouveaux_proprietaires():
    """Une liste déclarative qui diverge du réel fait croire à un inventaire."""
    assert ('vertex.app.routes.track_record_api', 'bp') in factory.BLUEPRINTS
    assert 'live_state_api' in factory.A_INJECTION
    assert len(factory.A_INJECTION['live_state_api']) > 20, (
        'la raison de l\'injection ne dit plus POURQUOI elle est necessaire')


def test_aucun_chemin_d_ordre_dans_les_nouveaux_modules():
    """Invariant produit absolu : Vertex n'exécute jamais un ordre."""
    for module in ('vertex/app/routes/live_state_api.py',
                   'vertex/app/routes/track_record_api.py',
                   'vertex/app/ibkr_state.py'):
        src = RACINE.joinpath(module).read_text(encoding='utf-8')
        for verbe in ('placeOrder', 'place_order', 'submit_order', 'transmit',
                      'bracketOrder', 'MarketOrder', 'LimitOrder'):
            assert verbe not in src, '%s contient %s' % (module, verbe)
