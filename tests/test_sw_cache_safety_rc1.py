"""tests/test_sw_cache_safety_rc1.py — gardien de sécurité du cache service worker.

Récupéré de la RC1 (commit 28d1e4e, absent de la lignée Neon Glass — voir
docs/skyler/BRANCH_CONVERGENCE_AUDIT.md §3.1/§7.1) et adapté : l'assertion de
version est désormais DYNAMIQUE (la lignée courante est v87+), les invariants
structurels restent identiques :
  · le précache (addAll) ne contient QUE le manifest + l'icône (aucun asset de
    page/graphe ne peut y être épinglé) ;
  · la stratégie est network-first (le frais est toujours préféré) ;
  · l'activation purge tout cache != version courante ;
  · aucun des 6 graphes supprimés en RC1 n'est référencé dans le SW.
"""
import re

import terminal


def _sw():
    c = terminal.app.test_client()
    return c.get('/sw.js').get_data(as_text=True)


def test_sw_has_single_versioned_cache_at_or_after_rc1():
    """Une seule constante de cache td-shell-vN, et N ne régresse jamais sous la RC1 (v51)."""
    sw = _sw()
    versions = sorted(set(re.findall(r"td-shell-v(\d+)", sw)), key=int)
    assert len(versions) == 1, f'plusieurs versions de cache dans le SW : {versions}'
    assert int(versions[0]) >= 51, 'régression de version SW sous la RC1 (v51)'


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
