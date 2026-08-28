"""Lot 9 — plus jamais deux propriétaires pour une même route.

L'histoire du dépôt en compte deux : `GET /options/<sym>` (le JSON gagnait —
neuf liens internes déversaient des accolades, corrigé au lot 8 du travail
graphique) et `GET /api/anomalies/<sym>` (deux implémentations aux formes de
réponse DIFFÉRENTES ; celle de strategy_os_api était masquée et son seul
consommateur, la page legacy /strategy-os, est une redirection 301 — code
mort des deux côtés).

Une collision Flask est silencieuse : le premier enregistré gagne, l'autre
existe dans le code, se fait tester, et ne sert jamais. Ce banc rend la
réapparition IMPOSSIBLE : il énumère la carte réelle des routes et échoue si
une règle (chemin + méthode) a deux endpoints.
"""
from __future__ import annotations

import collections
import os

os.environ.setdefault('DEMO', '1')
os.environ.setdefault('NO_IBKR', '1')


def test_aucune_route_n_a_deux_proprietaires():
    import terminal
    vues = collections.defaultdict(set)
    for r in terminal.app.url_map.iter_rules():
        for m in (r.methods or set()) - {'HEAD', 'OPTIONS'}:
            vues[(r.rule, m)].add(r.endpoint)
    doubles = {k: sorted(v) for k, v in vues.items() if len(v) > 1}
    assert not doubles, (
        'routes à deux propriétaires — le premier enregistré gagne et '
        'l\'autre est du code mort qui se croit vivant : %r' % doubles)
