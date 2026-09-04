"""tests/test_partial_corr.py — SKYLER LOT 17 : corrélation partielle + groupes.

Le co-mouvement du knowledge graph ne doit plus confondre « les deux titres
suivent le marché » avec « les deux titres partagent une exposition propre » :
quand la série SPY est disponible, la corrélation se calcule sur les RÉSIDUS
de marché (régression des rendements log sur SPY — méthode et R² étiquetés) ;
sans SPY, la corrélation brute reste, ÉTIQUETÉE `raw` (jamais silencieuse).
Les dépendances cachées gagnent la synthèse des GROUPES ≥ 3 titres
(composantes connexes), exposée dans l'API et affichée sur Portefeuille/Risque.
"""
import pytest

from vertex.engines import knowledge_graph as KG


def _mk(base, rets):
    """Série de clôtures depuis une liste de rendements simples."""
    out, x = [], float(base)
    for r in rets:
        x = x * (1 + r)
        out.append(round(x, 6))
    return out


def _market(n=61):
    return [0.01 if i % 2 else -0.01 for i in range(n)]     # marché alternant ±1 %


def _idio(period, n=61, amp=0.005):
    return [amp if i % period == 0 else -amp / (period - 1) for i in range(n)]


def _closes_spurious():
    """A et B suivent tous deux SPY mais leurs composantes propres sont
    indépendantes : corrélation BRUTE élevée, corrélation RÉSIDUELLE faible."""
    m = _market()
    a = [mi + ei for mi, ei in zip(m, _idio(3))]
    b = [mi + ei for mi, ei in zip(m, _idio(4))]
    return {'SPY': _mk(500, m), 'AAA': _mk(100, a), 'BBB': _mk(50, b)}


def _closes_genuine():
    """C et D partagent la MÊME composante propre au-delà du marché."""
    m = _market()
    e = _idio(3)
    c = [mi + ei for mi, ei in zip(m, e)]
    d = [mi + ei for mi, ei in zip(m, e)]
    return {'SPY': _mk(500, m), 'CCC': _mk(100, c), 'DDD': _mk(50, d)}


def _build(closes, sector_map=None):
    return KG.build(list(closes), sector_map=sector_map or {},
                    closes_by_sym=closes, events_by_sym={}, positions=None,
                    as_of='t', demo=False)


# ─── Résidus de marché : le faux co-mouvement disparaît ─────────────────────────

def test_spurious_market_comovement_filtered_by_residuals():
    g = _build(_closes_spurious())
    co = [e for e in g['edges'] if e['relation'] == 'CO_MOVES_WITH']
    assert not [e for e in co if {'company:AAA', 'company:BBB'} == {e['src'], e['dst']}], \
        'corrélation portée par le marché seul — ne doit PAS devenir une arête'


def test_genuine_shared_exposure_survives_residuals():
    g = _build(_closes_genuine())
    co = [e for e in g['edges'] if e['relation'] == 'CO_MOVES_WITH']
    pair = [e for e in co if {'company:CCC', 'company:DDD'} == {e['src'], e['dst']}]
    assert pair, 'exposition propre partagée — doit rester une arête'
    e = pair[0]
    assert e['method'] == 'residual_vs_SPY'
    assert e['evidence_level'] == 'F2'
    assert 'r2' in e and 0.0 <= e['r2']['AAA' if 'AAA' in e['r2'] else list(e['r2'])[0]] <= 1.0
    assert 'résidu' in e['basis'] or 'residual' in e['basis']


def test_raw_correlation_falls_back_labelled_without_spy():
    closes = _closes_genuine()
    closes.pop('SPY')
    g = _build(closes)
    co = [e for e in g['edges'] if e['relation'] == 'CO_MOVES_WITH']
    assert co and all(e['method'] == 'raw' for e in co)
    assert any('SPY absente' in l or 'brute' in l for l in g['limits'])


def test_spy_itself_excluded_from_residual_pairs():
    g = _build(_closes_genuine())
    co = [e for e in g['edges'] if e['relation'] == 'CO_MOVES_WITH']
    assert not [e for e in co if 'company:SPY' in (e['src'], e['dst'])]
    assert any('SPY' in l for l in g['limits'])


def test_method_always_labelled():
    for closes in (_closes_genuine(), {k: v for k, v in _closes_genuine().items() if k != 'SPY'}):
        g = _build(closes)
        for e in g['edges']:
            if e['relation'] == 'CO_MOVES_WITH':
                assert e['method'] in ('residual_vs_SPY', 'raw')


def test_residual_build_deterministic():
    assert _build(_closes_spurious()) == _build(_closes_spurious())


# ─── Groupes ≥ 3 : composantes connexes des dépendances cachées ────────────────

def _closes_group_of_three():
    m = _market()
    e = _idio(3)
    return {'SPY': _mk(500, m),
            'GGA': _mk(100, [mi + ei for mi, ei in zip(m, e)]),
            'GGB': _mk(50, [mi + ei for mi, ei in zip(m, e)]),
            'GGC': _mk(80, [mi + ei for mi, ei in zip(m, e)])}


def test_hidden_group_of_three_synthesized():
    closes = _closes_group_of_three()
    secmap = {'GGA': 'Tech', 'GGB': 'Tech', 'GGC': 'Tech'}
    g = _build(closes, sector_map=secmap)
    assert g['hidden_groups'], 'trois titres inter-reliés → un groupe attendu'
    grp = g['hidden_groups'][0]
    assert grp['symbols'] == ['GGA', 'GGB', 'GGC']
    assert grp['n_links'] >= 6                       # 3 paires × ≥2 liens
    assert grp['basis']


def test_no_group_below_three():
    g = _build(_closes_genuine(), sector_map={'CCC': 'Tech', 'DDD': 'Tech'})
    assert g['hidden_dependencies']                  # la paire existe
    assert g['hidden_groups'] == []                  # mais pas de groupe ≥ 3


def test_empty_graph_has_empty_groups():
    g = KG.build([], sector_map={}, closes_by_sym={}, events_by_sym={})
    assert g['hidden_groups'] == []


# ─── Surfaçage : groupes affichés sur Portefeuille/Risque, SW bumpé ─────────────

def test_portfolio_risk_view_renders_hidden_groups():
    import terminal
    body = terminal.app.test_client().get('/portfolio?view=risk',
                                          follow_redirects=True).get_data(as_text=True)
    assert 'hidden_groups' in body
    assert 'Groupes exposés' in body or 'Groupes expos&eacute;s' in body


def test_service_worker_bumped_to_at_least_v96():
    import re
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 96
    assert 'td-shell-v95' not in body
