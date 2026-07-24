"""tests/test_sw_cache_safety_rc1.py — RC1 (gardien service worker).

Prouve que le service worker ne peut PAS servir un asset obsolète de façon
durable après la suppression des 6 graphes morts :
  · le précache (addAll) ne contient QUE le manifest + l'icône (aucun asset de
    page/graphe ne peut y être épinglé) ;
  · la stratégie est network-first (le frais est toujours préféré) ;
  · l'activation purge tout cache != version courante (v50 → v51) ;
  · aucun des 6 fichiers supprimés n'est référencé dans le SW ;
  · la version est bien v51.
"""
import re

import terminal


def _sw():
    c = terminal.app.test_client()
    return c.get('/sw.js').get_data(as_text=True)


def test_sw_version_is_v51():
    sw = _sw()
    assert "td-shell-v51" in sw
    assert "td-shell-v50" not in sw


def test_sw_precache_only_manifest_and_icon():
    """addAll ne doit épingler que des assets stables — jamais une page ou un graphe."""
    sw = _sw()
    m = re.search(r"addAll\(\[([^\]]*)\]\)", sw)
    assert m, 'précache addAll introuvable'
    precache = m.group(1)
    assert '/manifest.webmanifest' in precache
    assert '/static/icon-180.png' in precache
    # aucun asset de page/graphe épinglé (sinon un obsolète pourrait survivre)
    for bad in ('.js', 'markets', 'options', 'chart'):
        assert bad not in precache, f'asset épinglé interdit dans le précache : {bad}'


def test_sw_is_network_first_and_purges_old_caches():
    sw = _sw()
    # network-first : fetch avant le repli cache
    assert 'network-first' in sw or 'fetch(req)' in sw
    assert sw.index('fetch(req)') < sw.index('cache.match(req)')
    # activation : suppression des caches != version courante
    assert 'caches.keys()' in sw and 'caches.delete' in sw and 'k!==CACHE' in sw
    assert 'clients.claim' in sw


def test_sw_does_not_reference_deleted_charts():
    sw = _sw()
    for dead in ('correlation-matrix', 'factor-chart', 'geographic-exposure',
                 'vol-surface', 'breadth-chart', 'sector-chart'):
        assert dead not in sw, f'le SW référence un graphe supprimé : {dead}'
