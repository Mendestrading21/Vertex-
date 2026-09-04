"""Vertex Test 1.0 · #779/G1 — LES TROIS DERNIÈRES ROUTES LEGACY.

`/desc/<sym>`, `/options/<sym>` et `/api/ticker/<sym>` quittent `terminal.py`,
avec ce qui les retenait :

- la **table française** des descriptions → `vertex/data/descriptions_fr.py`
  (c'est une donnée, pas un helper) ;
- le **paquet options** et ses deux coerceurs → `vertex/options/pack.py` ;
- le **cache des chaînes d'options** → `vertex/app/caches.py`, neuvième cache.

```text
routes LEGACY   3 → 0
```

## Le défaut que ce lot a introduit, et que la parité a attrapé

En retirant `/api/ticker`, la coupe est allée du décorateur jusqu'au commentaire
de section suivant. **L'enregistrement du blueprint `desk` vivait dans cet
intervalle.** Sept routes du poste personnel — synchronisation, sauvegardes,
restauration, cotation des positions — ont disparu du service.

Rien n'a levé d'erreur : Flask ne se plaint pas d'un blueprint qu'on
n'enregistre pas. Le compte de règles est passé de 194 à **187**, et c'est le
diff avant/après qui l'a montré, pas la suite de tests.

C'est la raison d'être du filet de parité posé au tout premier lot de #779 :
comparer l'**ensemble complet des règles**, pas seulement celles qu'on croit
toucher.

## Ce que `_i` et `_f` protègent, et pourquoi ils déménagent AVEC leurs gardes

Les deux coerceurs transforment un `NaN` de chaîne d'options en `0`. Ce `0`
n'est inoffensif **que parce que** deux garde-fous l'écartent avant tout calcul
servi : `if iv <= 0 or oi <= 0` et `if K < lo or K > hi`. Les trois sont partis
ensemble ; c'est ce déplacement conjoint qui préserve le raisonnement du lot 385,
et les tests de ce lot le vérifient à leur nouvelle adresse.

## Le cache des options est partagé par TROIS parties

Le chargement disque au démarrage, `_opt_loop` (rotation de l'univers) et
`options_pack` (fiche ouverte). Le monolithe le **remplit** (`.update(...)`) au
lieu de le réassigner : une réassignation séparerait la boucle de la route sans
qu'aucune erreur ne soit levée — le même piège que `scan_state`.
"""
import pathlib
import re

import pytest

from vertex.app import caches, factory
from vertex.data.descriptions_fr import DESCRIPTIONS

RACINE = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def application():
    from vertex.runtime import app
    return app


def test_aucune_route_legacy_ne_reste(application):
    """LE BUT DE #779. Une route servie par `terminal.py` est une route dont
    personne ne peut nommer le propriétaire sans lire le monolithe."""
    legacy = [r.rule for r in application.url_map.iter_rules() if '.' not in r.endpoint]
    #  `static` est la route interne de Flask, pas une route du produit.
    legacy = [r for r in legacy if not r.startswith('/static')]
    assert legacy == [], (
        'des routes sont de nouveau servies par le monolithe : %s' % legacy)


def test_la_surface_servie_est_complete(application):
    """LE FILET QUI A ATTRAPÉ LA VRAIE RÉGRESSION DE CE LOT.

    Retirer `/api/ticker` avait emporté l'enregistrement du blueprint `desk` —
    sept routes disparues, aucune erreur levée. Un test qui ne regarde que les
    routes qu'on croit toucher ne l'aurait jamais vu."""
    regles = {r.rule for r in application.url_map.iter_rules()}
    #  Lot 2 : `/api/ibkr/positions` (import du portefeuille du COMPTE) est
    #  retiree par contrat — market-data-only. Elle ne fait plus partie de la
    #  surface due, et sa NON-existence est gardee ailleurs
    #  (test_reconciliation_pnl.py).
    for indispensable in ('/api/desk', '/api/desk/backups', '/api/desk/restore',
                          '/api/pos-quotes', '/api/watchlist-tv',
                          '/api/journal/postmortem'):
        assert indispensable in regles, (
            '%s a disparu du service : le blueprint desk n\'est plus enregistre '
            '(Flask ne se plaint JAMAIS d\'un blueprint oublie)' % indispensable)
    assert len(regles) >= 180, 'la surface servie a fondu : %d regles' % len(regles)


def test_les_trois_routes_ont_leur_proprietaire(application):
    adaptateur = application.url_map.bind('localhost')
    for chemin, point in (('/desc/AAPL', 'descriptions_api.desc_ep'),
                          ('/options/AAPL', 'ticker_api.opt_ep'),
                          ('/api/ticker/AAPL', 'ticker_api.api_ticker')):
        vu, _ = adaptateur.match(chemin)
        assert vu == point, '%s est servi par « %s »' % (chemin, vu)


def test_le_monolithe_ne_les_definit_plus():
    src = RACINE.joinpath('terminal.py').read_text(encoding='utf-8')
    for vue in ('desc_ep', 'opt_ep', 'api_ticker', 'options_pack', '_i', '_f'):
        assert not re.search(r'^def %s\(' % vue, src, re.M), (
            '`terminal.py` redefinit %s' % vue)
    assert not re.search(r'^_FR_DESC\s*=', src, re.M)
    #  Le cache est IMPORTÉ puis REMPLI, jamais redéfini.
    assert not re.search(r'^_OPTALL_CACHE\s*=', src, re.M), (
        'le monolithe redefinit le cache des chaines d\'options : la boucle et '
        'la route cesseraient de voir le meme objet, en silence')
    assert '_OPTALL_CACHE.update(' in src


def test_le_cache_des_options_est_partage_par_les_trois_parties():
    import terminal
    from vertex.options import pack
    assert terminal._OPTALL_CACHE is caches._OPTALL_CACHE is pack._OPTALL_CACHE, (
        'les trois parties ne voient plus le meme cache : la rotation de fond '
        'et la fiche ouverte travailleraient chacune dans leur coin')
    assert '_OPTALL_CACHE' in caches.POLITIQUE, (
        'le neuvieme cache n\'a ni proprietaire ni politique de fraicheur')


def test_les_coerceurs_ont_demenage_AVEC_leurs_garde_fous():
    """Le `0` de `_i`/`_f` n'est inoffensif QUE parce que deux garde-fous
    l'écartent avant tout calcul servi. Les séparer ferait entrer un repli dans
    la médiane d'IV ATM et dans le GEX rendus à l'utilisateur."""
    src = RACINE.joinpath('vertex/options/pack.py').read_text(encoding='utf-8')
    assert 'def _i(' in src and 'def _f(' in src
    for garde in ('if iv <= 0 or oi <= 0:', 'if K < lo or K > hi:'):
        assert garde in src, (
            'le garde-fou « %s » n\'a pas suivi les coercitions : leur 0 '
            'entrerait dans un calcul SERVI' % garde)


def test_la_table_francaise_est_une_donnee_et_reste_complete():
    """Elle sert en démonstration et en secours de throttle. Vide, une fiche
    ouverte un jour de limitation yfinance n'afficherait rien du tout."""
    assert len(DESCRIPTIONS) >= 20, (
        'la table de descriptions a fondu : %d titres' % len(DESCRIPTIONS))
    for sym, valeur in DESCRIPTIONS.items():
        assert len(valeur) == 3, '%s : forme attendue (resume, secteur, pays)' % sym
        assert all(isinstance(x, str) and x.strip() for x in valeur), (
            '%s porte un champ vide' % sym)
    #  Aucun chiffre de marche dans une table de descriptions.
    src = RACINE.joinpath('vertex/data/descriptions_fr.py').read_text(encoding='utf-8')
    for interdit in ('price', 'strike', 'delta', 'implied'):
        assert interdit not in src.lower(), (
            'la table de descriptions contient « %s » : ce n\'est plus une '
            'donnee statique' % interdit)


def test_desc_ne_cache_jamais_un_echec(application):
    """Mémoriser un `info` vide figerait une fiche muette pour toujours, alors
    qu'un réessai plus tard aboutirait."""
    from vertex.app.routes import descriptions_api as _desc
    src = pathlib.Path(_desc.__file__).read_text(encoding='utf-8')
    assert "if out['summary']:" in src, (
        'la condition qui reserve le cache aux fetch REUSSIS a disparu')
    corps = application.test_client().get('/desc/ZZZZINEXISTANT').get_json()
    assert corps['summary'] == '' and corps['employees'] is None
    assert 'ZZZZINEXISTANT' not in _desc._cache, (
        'un echec a ete memorise : la fiche resterait vide meme apres retour '
        'du reseau')


def test_le_registre_declare_les_deux_derniers_proprietaires():
    for chemin in ('vertex.app.routes.descriptions_api', 'vertex.app.routes.ticker_api'):
        assert (chemin, 'bp') in factory.BLUEPRINTS, '%s absent du registre' % chemin


def test_aucun_chemin_d_ordre_dans_les_nouveaux_modules():
    for module in ('vertex/options/pack.py', 'vertex/app/routes/ticker_api.py',
                   'vertex/app/routes/descriptions_api.py',
                   'vertex/data/descriptions_fr.py'):
        src = RACINE.joinpath(module).read_text(encoding='utf-8')
        for verbe in ('placeOrder', 'place_order', 'submit_order', 'transmit',
                      'bracketOrder', 'MarketOrder', 'LimitOrder'):
            assert verbe not in src, '%s contient %s' % (module, verbe)
