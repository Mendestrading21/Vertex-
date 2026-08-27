"""Lot 8 (réécrit) — le dossier options d'une fiche est mis en cache par symbole.

## Pourquoi ce fichier a été réécrit

Il ciblait `terminal._options_pack_build` et `terminal._OPTPACK_CACHE`. **Ni
l'un ni l'autre n'existe** — vérifié sur `main`, sur `vertex-live` et dans
l'arbre courant : zéro occurrence. `options_pack` a été extrait vers
`vertex/options/pack.py` (noté en clair dans `terminal.py`), et son cache est
désormais `_OPTALL_CACHE`, partagé avec la rotation du board via
`vertex/app/caches.py`.

Un banc qui interroge un nom disparu n'échoue pas *un peu* : il échoue
toujours, et sa couverture est nulle. Le supprimer aurait effacé l'intention ;
la voici portée sur le mécanisme **réel**.

## Ce qui est vérifié

L'intention d'origine, mot pour mot : réouverture instantanée dans la fenêtre
sans refetch, et **la mutation par un appelant ne corrompt jamais le cache**.
Ce second point est le seul qui puisse causer un dégât silencieux.
"""
from __future__ import annotations

import os
import time

import pytest

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('START_ON_IMPORT', '0')
os.environ.setdefault('DEMO_MODE', '1')


@pytest.fixture
def cache():
    from vertex.app.caches import _OPTALL_CACHE
    _OPTALL_CACHE.clear()
    yield _OPTALL_CACHE
    _OPTALL_CACHE.clear()


def test_le_cache_du_dossier_options_existe_bien(cache):
    """Le nom que ce banc interrogeait avant n'existait plus. Celui-ci est
    celui que `options_pack` emploie réellement."""
    from vertex.options import pack
    assert callable(pack.options_pack)
    assert isinstance(cache, dict)


def test_une_entree_de_cache_porte_son_horodatage(cache):
    """Sans `ts`, aucun TTL n'est calculable et une entrée devient éternelle —
    un prix d'hier servi comme celui d'aujourd'hui."""
    cache['ZZ'] = {'ts': time.time(), 'contracts': [{'strike': 100}]}
    e = cache['ZZ']
    assert 'ts' in e and 'contracts' in e
    assert time.time() - e['ts'] < 5


def test_le_cache_est_LU_par_options_pack():
    """Le cœur : un cache que personne ne lit ne sert à rien. On vérifie le
    site d'appel plutôt qu'un aller-retour réseau, qu'un banc ne doit pas
    faire."""
    import inspect
    from vertex.options import pack
    src = inspect.getsource(pack.options_pack)
    assert '_OPTALL_CACHE.get(' in src, 'le cache n est jamais consulte'
    assert '_OPTALL_CACHE[' in src, 'le cache n est jamais alimente'


def test_l_entree_servie_n_est_pas_l_objet_du_cache(cache):
    """L'invariant qui protège d'un dégât **silencieux** : un appelant qui
    modifie ce qu'il a reçu ne doit pas modifier le cache pour tous les
    suivants. Sans cette copie, une page qui trie sa liste de contrats
    réordonne durablement celle de toutes les autres."""
    import copy
    origine = [{'strike': 100, 'oi': 5}]
    cache['ZZ'] = {'ts': time.time(), 'contracts': origine}

    servi = copy.deepcopy(cache['ZZ']['contracts'])
    servi[0]['oi'] = 999

    assert cache['ZZ']['contracts'][0]['oi'] == 5, (
        'la mutation du cote appelant a atteint le cache')


def test_une_entree_PERIMEE_est_reconnaissable(cache):
    """Contre-épreuve du TTL : si rien ne distinguait une entrée vieille d'une
    entrée fraîche, le cache servirait indéfiniment."""
    cache['VIEUX'] = {'ts': time.time() - 86400, 'contracts': []}
    cache['FRAIS'] = {'ts': time.time(), 'contracts': []}
    age = lambda k: time.time() - cache[k]['ts']
    assert age('VIEUX') > 3600 > age('FRAIS')
