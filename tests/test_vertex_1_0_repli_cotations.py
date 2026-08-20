"""Vertex 1.0 · G2/G5 — une valeur connue ne doit pas rester invisible.

Défaut reproduit en local, sur la surface qui compte le plus (le P&L du
portefeuille) :

```
POST /api/pos-quotes {"positions":[{"sym":"ACN"}]}
  ->  {"live": false, "results": {}}          # RIEN
```

…pendant que le même serveur portait **ACN à 198,0** en mémoire, établi par le
cycle de scan. Le client exige une cotation par ligne : sans elle il pose
`ok = false` et n'affiche **aucun** P&L. Un seul fournisseur était consulté
(`if todo and ibkr_enabled:`), et son silence vidait l'écran.

C'est le pendant exact du défaut hors séance : là, un prix réel était jeté
faute de clôture ; ici, un prix réel n'était même pas cherché.

## Ce que le repli ne fait PAS

Il ne comble **jamais une option**. Le scan ne cote pas de contrats, et
fabriquer un prix d'option à partir du sous-jacent serait précisément la donnée
inventée que le produit interdit. Une option non cotée reste absente, donc
honnêtement `—`.

Il n'écrit pas dans le cache des cotations : ce cache sert les cotations
broker, et y ranger un cours de scan le ferait servir **à la place** d'une
vraie cotation pendant tout le TTL.
"""
from __future__ import annotations

import pathlib

import pytest

from vertex.app.routes.desk import completer_par_repli

RACINE = pathlib.Path(__file__).resolve().parents[1]
DESK = RACINE / 'vertex/app/routes/desk.py'
TERMINAL = RACINE / 'terminal.py'

PRIX = {'ACN': {'spot': 198.0, 'spot_chg': -0.53},
        'AOS': {'spot': 179.0, 'spot_chg': 0.33}}


def _repli(sym):
    return PRIX.get(sym)


def _action(sym):
    return {'sym': sym, 'key': '%s|||' % sym}


def _option(sym):
    return {'sym': sym, 'exp': '2026-12', 'strike': 200, 'right': 'C',
            'key': '%s|2026-12|200|C' % sym}


# ── Le cas qui vidait l'écran ─────────────────────────────────────────────

def test_une_action_sans_cotation_broker_est_comblee_et_etiquetee():
    out = {}
    n = completer_par_repli([_action('ACN')], out, _repli)
    assert n == 1
    assert out['ACN|||']['spot'] == 198.0
    assert out['ACN|||']['source'] == 'scan', (
        "sans étiquette, un cours de scan se fait passer pour une cotation "
        'broker — le mensonge de provenance le plus facile à commettre.')
    assert out['ACN|||']['type'] == 'STK'


def test_une_option_n_est_JAMAIS_comblee():
    """Le scan ne cote pas de contrats. Dériver un prix d'option du
    sous-jacent serait une donnée fabriquée."""
    out = {}
    assert completer_par_repli([_option('ACN')], out, _repli) == 0
    assert out == {}, (
        'une option a reçu un prix qui n\'existe pas : c\'est exactement '
        'l\'invention que le produit interdit.')


def test_une_cotation_broker_deja_presente_n_est_pas_ecrasee():
    """Le repli est un DERNIER recours. L'écraser inverserait la priorité des
    sources et remplacerait du live par un cours de scan."""
    out = {'ACN|||': {'type': 'STK', 'spot': 199.42}}
    assert completer_par_repli([_action('ACN')], out, _repli) == 0
    assert out['ACN|||']['spot'] == 199.42
    assert 'source' not in out['ACN|||']


def test_un_symbole_inconnu_du_scan_reste_absent():
    out = {}
    assert completer_par_repli([_action('ZZQQ')], out, _repli) == 0
    assert out == {}, 'un prix a été fabriqué pour un symbole que rien ne cote.'


def test_un_prix_absent_n_est_pas_remplace_par_zero():
    out = {}
    assert completer_par_repli([_action('X')], out, lambda s: {'spot': None}) == 0
    assert out == {}


def test_un_repli_qui_leve_ne_casse_pas_la_cotation():
    """Le repli est le dernier recours : s'il échoue, on rend ce qu'on a, on ne
    fait pas tomber la requête entière."""
    def _casse(sym):
        raise RuntimeError('source indisponible')

    out = {'AOS|||': {'type': 'STK', 'spot': 179.0}}
    assert completer_par_repli([_action('ACN'), _action('AOS')], out, _casse) == 0
    assert out['AOS|||']['spot'] == 179.0


def test_sans_repli_injecte_rien_ne_change():
    out = {}
    assert completer_par_repli([_action('ACN')], out, None) == 0
    assert out == {}


def test_plusieurs_actions_sont_comblees_en_une_passe():
    out = {}
    n = completer_par_repli([_action('ACN'), _action('AOS'), _option('ACN')],
                            out, _repli)
    assert n == 2
    assert set(out) == {'ACN|||', 'AOS|||'}


# ── Le câblage ────────────────────────────────────────────────────────────

def test_la_route_appelle_le_repli_apres_le_passage_broker():
    """L'ordre compte : appelé avant, le repli servirait de préférence à une
    cotation broker disponible."""
    src = DESK.read_text(encoding='utf-8')
    i_ibkr = src.index("opt_job('posq'")
    i_repli = src.index('completer_par_repli(todo, out, cotation_repli)')
    assert i_ibkr < i_repli, (
        'le repli est consulté AVANT le broker : il servirait un cours de scan '
        'alors qu\'une vraie cotation était disponible.')


def test_le_repli_n_est_pas_mis_en_cache():
    """Le cache sert les cotations broker. Y ranger un cours de scan le ferait
    servir À LA PLACE d'une vraie cotation pendant tout le TTL."""
    src = DESK.read_text(encoding='utf-8')
    corps = src[src.index('def completer_par_repli'):src.index('def make_blueprint')]
    assert 'posq_cache' not in corps


def test_le_produit_injecte_reellement_une_source_de_repli():
    """Une fonction jamais branchée ne corrige rien — `fallback_market_data.py`
    en est la démonstration : le module existait, avec zéro appelant, et le
    P&L restait vide."""
    src = TERMINAL.read_text(encoding='utf-8')
    assert 'cotation_repli=_cotation_repli' in src, (
        'le repli n\'est plus injecté : la route retombera sur `results: {}`.')
    assert 'def _cotation_repli(' in src


def test_le_repli_n_ouvre_aucune_requete_reseau():
    """Il lit une valeur DÉJÀ en mémoire. Y glisser un appel réseau le rendrait
    lent, faillible, et soumis aux limites de débit du fournisseur — au moment
    précis où tout le reste est déjà en panne."""
    import ast
    src = TERMINAL.read_text(encoding='utf-8')
    arbre = ast.parse(src)
    corps = next(ast.get_source_segment(src, n) for n in ast.walk(arbre)
                 if isinstance(n, ast.FunctionDef) and n.name == '_cotation_repli')
    for interdit in ('requests', 'urlopen', 'yf.', 'download', 'opt_job'):
        assert interdit not in corps, (
            '`_cotation_repli` appelle %s : ce n\'est plus un dernier recours '
            'instantané.' % interdit)


@pytest.mark.parametrize('droit', ['C', 'P', 'c', 'p'])
def test_toutes_les_formes_de_droit_d_option_sont_exclues(droit):
    """`right` peut arriver en minuscules du client : ne comparer qu'aux
    majuscules laisserait passer une option."""
    out = {}
    p = {'sym': 'ACN', 'right': droit, 'key': 'ACN|x|1|%s' % droit}
    assert completer_par_repli([p], out, _repli) == 0
    assert out == {}
