"""tests/test_sector_exposure.py — SKYLER LOT 24 : exposition sectorielle.

Le knowledge graph agrège l'exposition du PORTEFEUILLE par secteur déclaré :
`sector_exposure` (par secteur : titres détenus, nombre de positions, poids en
% si les cotes le permettent — sinon None avec raison, jamais estimé). Un
groupe caché entièrement dans un même secteur est étiqueté
`sector_concentration`. Affiché sur Portefeuille → Risque ; SW v98 → v99.
"""
import pytest

from vertex.engines import knowledge_graph as KG


def _closes(base, n=60, phase=0):
    out, x = [], float(base)
    for i in range(n):
        x = x * (1 + 0.001 + (0.01 if (i + phase) % 2 else -0.01))
        out.append(round(x, 6))
    return out


SECMAP = {'AAA': 'Semiconducteurs', 'BBB': 'Semiconducteurs', 'CCC': 'Energie',
          'GGA': 'Tech', 'GGB': 'Tech', 'GGC': 'Tech'}


def _build(positions, quotes=None, symbols=None, closes=None):
    return KG.build(symbols or ['AAA', 'BBB', 'CCC', 'ZZZ'], sector_map=SECMAP,
                    closes_by_sym=closes or {}, events_by_sym={},
                    positions=positions, quotes=quotes, as_of='t', demo=False)


# ─── Exposition sectorielle du portefeuille ─────────────────────────────────────

def test_sector_exposure_with_quotes_weights():
    pos = [{'symbol': 'AAA', 'quantity': 10}, {'symbol': 'BBB', 'quantity': 20},
           {'symbol': 'CCC', 'quantity': 5}]
    quotes = {'AAA': 100.0, 'BBB': 50.0, 'CCC': 200.0}      # 1000 + 1000 + 1000
    g = _build(pos, quotes=quotes)
    se = g['sector_exposure']
    semi = se['Semiconducteurs']
    assert semi['symbols'] == ['AAA', 'BBB'] and semi['n_positions'] == 2
    assert semi['weight_pct'] == pytest.approx(66.67, abs=0.1)
    assert se['Energie']['weight_pct'] == pytest.approx(33.33, abs=0.1)


def test_sector_exposure_without_quotes_honest_counts():
    pos = [{'symbol': 'AAA', 'quantity': 10}, {'symbol': 'CCC', 'quantity': 5}]
    g = _build(pos, quotes=None)
    se = g['sector_exposure']
    assert se['Semiconducteurs']['n_positions'] == 1
    assert se['Semiconducteurs']['weight_pct'] is None      # jamais estimé
    assert 'cote' in se['Semiconducteurs']['basis'] or 'poids' in se['Semiconducteurs']['basis']


def test_unmapped_held_position_labelled():
    pos = [{'symbol': 'ZZZ', 'quantity': 3}]
    g = _build(pos)
    se = g['sector_exposure']
    assert 'HORS_WATCHLIST' in se
    assert se['HORS_WATCHLIST']['symbols'] == ['ZZZ']


def test_no_positions_empty_exposure():
    g = _build(None)
    assert g['sector_exposure'] == {}


def test_sector_exposure_deterministic():
    pos = [{'symbol': 'AAA', 'quantity': 10}]
    assert _build(pos, quotes={'AAA': 100.0}) == _build(pos, quotes={'AAA': 100.0})


# ─── Concentration sectorielle des groupes cachés ───────────────────────────────

def _group_closes(same_sector=True):
    closes = {'GGA': _closes(100), 'GGB': _closes(50), 'GGC': _closes(80)}
    secmap = dict(SECMAP)
    if not same_sector:
        secmap['GGC'] = 'Energie'
    return closes, secmap


def test_mono_sector_group_flagged():
    closes, secmap = _group_closes(same_sector=True)
    g = KG.build(['GGA', 'GGB', 'GGC'], sector_map=secmap, closes_by_sym=closes,
                 events_by_sym={}, as_of='t')
    assert g['hidden_groups']
    grp = g['hidden_groups'][0]
    assert grp['sector_concentration'] is True
    assert grp['sector'] == 'Tech'
    assert 'CONCENTRATION' in grp['basis'].upper() or 'secteur' in grp['basis']


def test_mixed_sector_group_not_flagged():
    """Groupe multi-secteurs (co-mouvement + même catalyseur daté partagés) :
    reste un groupe, mais JAMAIS étiqueté concentration sectorielle."""
    closes, secmap = _group_closes(same_sector=False)
    ev = {s: [{'label': 'CPI', 'dte': 10, 'source': 'calendar.macro'}]
          for s in ('GGA', 'GGB', 'GGC')}
    g = KG.build(['GGA', 'GGB', 'GGC'], sector_map=secmap, closes_by_sym=closes,
                 events_by_sym=ev, as_of='t')
    assert g['hidden_groups']
    grp = g['hidden_groups'][0]
    assert grp['sector_concentration'] is False
    assert grp['sector'] is None


# ─── Surfaçage ──────────────────────────────────────────────────────────────────

def test_graph_route_serves_sector_exposure():
    import terminal
    d = terminal.app.test_client().get('/api/skyler/graph').get_json()
    assert 'sector_exposure' in d


def test_portfolio_risk_view_renders_sector_exposure():
    import terminal
    body = terminal.app.test_client().get('/portfolio?view=risk',
                                          follow_redirects=True).get_data(as_text=True)
    assert 'sector_exposure' in body
    assert 'Exposition sectorielle' in body


def test_service_worker_bumped_to_at_least_v99():
    import re
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 99
    assert 'td-shell-v98' not in body
