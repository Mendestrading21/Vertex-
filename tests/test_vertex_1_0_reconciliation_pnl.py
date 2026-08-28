"""Lot 2 — la réconciliation du P&L contre le COMPTE courtier est retirée.

Ce fichier gardait vingt-et-un bancs sur `vertex.data_sources.ibkr_compte` :
le résumé de compte sans ligne BASE, l'écart réel de 95,46 USD entre
`accountSummary` et `reqPnL` mesuré le 24 août 2026, la réconciliation qui ne
désigne aucun gagnant. Leur intention était juste — ne jamais choisir une
source de P&L en silence — mais leur MATIÈRE était la lecture du compte :
`managedAccounts`, `accountSummary`, `portfolio`, `reqPnL`.

La frontière market-data-only l'interdit désormais, readonly ou pas :
`readonly=True` empêche l'ordre, il ne protège pas la confidentialité du
compte. Le module a été SUPPRIMÉ, sa route avec lui.

Ce que ce fichier garde maintenant, c'est la vérité inverse — et elle doit
être aussi solide que l'ancienne :

1. la capacité n'existe plus nulle part (module, route, worker, UI) ;
2. son remplaçant dit « courtier non lu » au lieu d'un faux accord ;
3. l'intention « aucune source ne gagne en silence » survit là où elle a
   encore un objet : le P&L de Vertex est calculé sur les positions
   DÉCLARÉES, cotées par symbole — une seule source, nommée à l'écran.
"""
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _lit(*chemin) -> str:
    return (ROOT.joinpath(*chemin)).read_text(encoding='utf-8')


def test_le_module_de_compte_n_existe_plus():
    assert not (ROOT / 'vertex' / 'data_sources' / 'ibkr_compte.py').exists(), (
        'ibkr_compte.py est revenu : lire le résumé de compte, le portefeuille '
        'ou reqPnL viole la frontière market-data-only.'
    )
    assert not (ROOT / 'vertex' / 'data_sources' / 'ibkr_positions.py').exists(), (
        'ibkr_positions.py est revenu : les positions du compte ne se lisent plus.'
    )


def test_la_route_de_reconciliation_n_est_plus_servie():
    src = _lit('vertex', 'app', 'routes', 'positions_api.py')
    assert "@bp.route('/api/positions/pnl-reconciliation')" not in src
    assert 'ibkr_compte' not in src


def test_la_route_d_import_des_positions_n_est_plus_servie():
    src = _lit('vertex', 'app', 'routes', 'desk.py')
    assert "@bp.route('/api/ibkr/positions')" not in src


def test_le_worker_ne_repond_plus_au_job_positions():
    src = _lit('terminal.py')
    assert "elif kind == 'positions':" not in src, (
        'le worker sert à nouveau les positions du compte via opt_job.'
    )


def test_le_snapshot_ibkr_ne_porte_plus_un_seul_champ_de_compte():
    """`/ibkr` rend la preuve de socket — connected/mode/error — rien d'autre."""
    src = _lit('terminal.py')
    debut = src.index('def _ibkr_snapshot():')
    fin = src.index('\ndef ', debut + 10)
    corps = src[debut:fin]
    for champ in ("'account'", "'net_liq'", "'cash'", "'buying_power'",
                  "'upnl'", "'positions'"):
        assert champ not in corps, (
            'le snapshot /ibkr porte à nouveau %s — un champ de compte.' % champ
        )


def test_l_ui_ne_consomme_plus_les_routes_de_compte():
    pf = _lit('vertex', 'ui', 'pages', 'portfolio_page.py')
    assert '/api/ibkr/positions' not in pf
    assert 'pnl-reconciliation' not in pf


def test_le_remplacant_avoue_courtier_non_lu():
    """`/api/positions/reconcile` rend un état honnête, jamais un faux accord."""
    from vertex.positions.reconciler import reconcile
    r = reconcile([{'symbol': 'AAPL', 'source': 'MANUAL'}], [],
                  ibkr_online=False)
    # L'API exacte importe moins que la propriété : hors ligne ne conclut pas.
    texte = str(r).upper()
    assert 'DATA_REPAIR' in texte or 'OFFLINE' in texte or 'UNKNOWN' in texte \
        or r.get('ibkr_online') is False, (
            'la réconciliation hors ligne doit dire qu\'elle n\'a pas lu le '
            'courtier, pas rendre un accord vide : %r' % (r,)
        )
