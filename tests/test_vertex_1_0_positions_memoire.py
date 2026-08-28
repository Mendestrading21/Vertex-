"""Lot 2 — la mémoire des positions COURTIER a disparu avec la capacité.

Ce banc gardait la politique de fraîcheur de `_ibkr_positions()` : borne
unique de 15 s, échec jamais mémorisé, limite architecturale avouée dans le
code. Le helper a été SUPPRIMÉ — lire les positions du compte viole la
frontière market-data-only — et sa politique avec lui.

Ce qui reste, et que ce banc garde désormais : le memo des COTATIONS
(`_q_memo`), qui est du marché. Sa propriété centrale est la même qu'avant :
un échec n'est jamais mémorisé — une cote illisible un instant ne doit pas
faire passer le marché pour muet pendant toute la borne.
"""
from __future__ import annotations

import pathlib

SRC = (pathlib.Path(__file__).resolve().parents[1]
       / 'vertex' / 'app' / 'routes' / 'positions_api.py')


def _corps_quotes() -> str:
    src = SRC.read_text(encoding='utf-8')
    deb = src.index('def _quotes(')
    fin = src.index('@bp.route', deb)
    return src[deb:fin]


def test_le_helper_de_positions_courtier_n_existe_plus():
    src = SRC.read_text(encoding='utf-8')
    assert 'def _ibkr_positions' not in src, (
        'le lecteur de positions du compte est revenu dans positions_api.'
    )


def test_les_cotations_gardent_leur_memoire_partagee():
    corps = _corps_quotes()
    assert '_q_memo' in corps, (
        'les cotations ne sont plus mémorisées : chaque carte repaiera '
        'l\'aller-retour worker pour la même page.'
    )


def test_un_echec_de_cotation_n_est_jamais_memorise():
    corps = _corps_quotes()
    assert 'if valeur:' in corps or 'if valeur is not None' in corps, (
        'le memo des cotations doit refuser de retenir un échec — sinon une '
        'cote illisible un instant fait passer le marché pour muet.'
    )
