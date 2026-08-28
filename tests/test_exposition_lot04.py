"""Lot 4 — un démarrage privé non-loopback sans code ÉCHOUE ; la démo exposée
n'écrit pas.

Avant ce lot, `VERTEX_LAN=1` ou `PORT` sans code démarrait sur `0.0.0.0` avec
une phrase d'avertissement — honnête, mais le portefeuille restait lisible par
tout le réseau. Le contrat du skill exige l'échec du démarrage, pas l'aveu.

La démo est la voie publique légitime — et pour cela elle ne doit rien
persister quand elle est exposée : un desk public en écriture est un tableau
blanc mondial. La démo LOCALE (loopback), elle, continue d'écrire : c'est le
mode de travail quotidien.
"""
from __future__ import annotations

from vertex.app.exposition import exposition


def test_lan_sans_code_refuse_le_demarrage():
    e = exposition(False, env={'VERTEX_LAN': '1'})
    assert e['demarrage_refuse'], (
        'VERTEX_LAN=1 sans code doit REFUSER le démarrage, pas avertir : '
        'le desk serait lisible par tout le réseau.'
    )
    assert 'VERTEX_CODE' in e['raison'] and 'DEMO' in e['raison'], (
        'le refus doit nommer les issues (code, démo, loopback).'
    )


def test_hebergeur_sans_code_ni_demo_refuse():
    e = exposition(False, env={'PORT': '10000'})
    assert e['demarrage_refuse'], (
        'un hébergeur (PORT) sans code ni démo expose un desk privé au monde.'
    )


def test_hebergeur_en_demo_demarre_mais_expose_sans_code_reste_nomme():
    e = exposition(False, env={'PORT': '10000', 'DEMO': '1'})
    assert not e['demarrage_refuse'], (
        'la démo est la voie publique légitime : elle démarre.'
    )
    assert e['expose_sans_code'], 'l\'état dangereux reste nommé, pas masqué.'


def test_le_verrou_demarre_partout():
    for env in ({'VERTEX_LAN': '1'}, {'PORT': '10000'}, {}):
        e = exposition(True, env=env)
        assert not e['demarrage_refuse']


def test_loopback_sans_code_demarre():
    e = exposition(False, env={})
    assert not e['demarrage_refuse'] and e['hote'] == '127.0.0.1'


def test_la_demo_exposee_n_ecrit_pas_le_desk():
    from vertex.app.routes import desk as desk_routes
    src = open(desk_routes.__file__, encoding='utf-8').read()
    assert 'demo_exposee' in src or 'demo_publique' in src, (
        'la garde de non-persistance de la démo exposée a disparu de desk.py.'
    )


def test_le_demarrage_lit_le_refus():
    src = open('terminal.py', encoding='utf-8').read()
    assert 'demarrage_refuse' in src, (
        '_start_app ne lit plus le refus : un démarrage dangereux redevient '
        'un simple avertissement.'
    )
