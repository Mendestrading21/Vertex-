"""vertex/engines/knowledge_graph.py — KNOWLEDGE GRAPH INSTITUTIONNEL (LOT 11).

Relie sociétés, secteurs, catalyseurs et portefeuille UNIQUEMENT depuis des
sources réelles tracées :

  - appartenance sectorielle : watchlist statique du code
    (`vertex/market/sectors.py`) — fait déclaré F1, source citée ;
  - co-mouvement : corrélation des rendements log sur les séries canoniques
    (≥ MIN_POINTS points partagés) — métrique dérivée F2, fenêtre affichée ;
  - exposition catalyseur : événements DATÉS du calendrier réel (≤ 90 j) — F1 ;
  - détention : positions réelles du desk — F1.

Les relations sans source branchée (fournisseurs, clients, concurrents) ne
sont JAMAIS inventées : elles deviennent des questions de recherche typées
(`status: NON_DOCUMENTE`). La propagation d'impact est explicable arête par
arête (chaque saut porte sa relation et sa base). Une dépendance cachée exige
au moins DEUX liens indépendants (secteur partagé, co-mouvement, même
catalyseur) — jamais un seul indice.

Fonctions pures, déterministes, JSON-sérialisables. Lecture seule, aucun ordre.
"""
from __future__ import annotations

import math

SCHEMA_VERSION = 1
GRAPH_ENGINE_VERSION = '0.1.0'
MIN_POINTS = 40                  # points partagés minimum pour une corrélation
CORR_STRONG = 0.75               # seuil de co-mouvement
MAX_DTE = 90                     # horizon des catalyseurs datés

RELATIONS = ('MEMBER_OF_SECTOR', 'CO_MOVES_WITH', 'EXPOSED_TO_CATALYST',
             'HELD_IN_PORTFOLIO')


def _num(x):
    return float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def _log_returns(closes):
    out = []
    for a, b in zip(closes, closes[1:]):
        fa, fb = _num(a), _num(b)
        if fa is None or fb is None or fa <= 0 or fb <= 0:
            return None
        out.append(math.log(fb / fa))
    return out


def _pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0 or syy <= 0:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sxx * syy)


# ─── Construction ───────────────────────────────────────────────────────────────

def build(symbols, sector_map=None, closes_by_sym=None, events_by_sym=None,
          positions=None, as_of=None, demo=False):
    """Construit le graphe depuis les sources réelles fournies — chaque arête
    porte provenance, niveau de preuve et base ; rien n'est inventé."""
    symbols = sorted({str(s).upper() for s in (symbols or []) if s})
    sector_map = sector_map or {}
    closes_by_sym = closes_by_sym or {}
    events_by_sym = events_by_sym or {}
    held = sorted({str(p.get('symbol') or '').upper()
                   for p in (positions or []) if p.get('symbol')} & set(symbols))

    nodes, edges, limits = [], [], []
    node_ids = set()

    def node(nid, ntype, label):
        if nid not in node_ids:
            node_ids.add(nid)
            nodes.append({'id': nid, 'type': ntype, 'label': label})

    for s in symbols:
        node('company:%s' % s, 'COMPANY', s)

    # Secteurs — watchlist statique du code (fait déclaré, source citée).
    for s in symbols:
        sec = sector_map.get(s)
        if not sec:
            continue
        node('sector:%s' % sec, 'SECTOR', sec)
        edges.append({'relation': 'MEMBER_OF_SECTOR',
                      'src': 'company:%s' % s, 'dst': 'sector:%s' % sec,
                      'source': 'vertex/market/sectors.py (watchlist statique)',
                      'evidence_level': 'F1',
                      'basis': '%s déclaré dans le secteur %s par la watchlist du code' % (s, sec)})

    # Co-mouvement — corrélation des rendements log sur séries canoniques.
    with_series = [s for s in symbols
                   if len([c for c in (closes_by_sym.get(s) or []) if _num(c) is not None]) >= MIN_POINTS]
    skipped = [s for s in symbols if closes_by_sym.get(s) and s not in with_series]
    if skipped:
        limits.append('co-mouvement non évalué pour %s : série < %d points — jamais deviné'
                      % (', '.join(skipped), MIN_POINTS))
    for i, a in enumerate(with_series):
        for b in with_series[i + 1:]:
            ca, cb = closes_by_sym[a], closes_by_sym[b]
            L = min(len(ca), len(cb))
            ra, rb = _log_returns(ca[-L:]), _log_returns(cb[-L:])
            if ra is None or rb is None:
                continue
            corr = _pearson(ra, rb)
            if corr is None or not math.isfinite(corr) or corr < CORR_STRONG:
                continue
            edges.append({'relation': 'CO_MOVES_WITH',
                          'src': 'company:%s' % a, 'dst': 'company:%s' % b,
                          'source': 'série canonique de clôtures (scan)',
                          'evidence_level': 'F2',
                          'value': round(corr, 3), 'window': L - 1,
                          'basis': 'corrélation des rendements log %s/%s = %.2f sur %d points (seuil %.2f)'
                                   % (a, b, corr, L - 1, CORR_STRONG)})

    # Catalyseurs — uniquement les événements DATÉS du calendrier réel (≤ 90 j).
    for s in symbols:
        for e in (events_by_sym.get(s) or []):
            dte = e.get('dte')
            label = e.get('label')
            if label is None or dte is None or dte > MAX_DTE:
                continue
            cid = 'catalyst:%s' % label
            node(cid, 'CATALYST', label)
            edges.append({'relation': 'EXPOSED_TO_CATALYST',
                          'src': 'company:%s' % s, 'dst': cid,
                          'source': e.get('source') or 'calendrier',
                          'evidence_level': 'F1', 'dte': dte,
                          'basis': '%s exposé à « %s » (J-%d) — date déclarée du calendrier'
                                   % (s, label, dte)})

    # Détention — positions réelles du desk.
    if held:
        node('portfolio:desk', 'PORTFOLIO', 'Portefeuille desk')
        for s in held:
            edges.append({'relation': 'HELD_IN_PORTFOLIO',
                          'src': 'company:%s' % s, 'dst': 'portfolio:desk',
                          'source': 'positions desk (desk_data.json)',
                          'evidence_level': 'F1',
                          'basis': 'position réelle déclarée sur %s' % s})

    limits.append('aucune source fournisseurs/clients/concurrents branchée — '
                  'relations jamais inventées, questions de recherche générées')
    if not symbols:
        limits.append('aucun symbole fourni — graphe vide, rien d’inventé')

    graph = {'schema_version': SCHEMA_VERSION,
             'engine_version': GRAPH_ENGINE_VERSION,
             'generator': 'deterministic',
             'as_of': as_of, 'demo': bool(demo),
             'nodes': nodes, 'edges': edges,
             'limits': limits}
    graph['hidden_dependencies'] = _hidden_dependencies(graph, symbols, held)
    graph['research_questions'] = _research_questions(symbols, sector_map, events_by_sym)
    return graph


# ─── Dépendances cachées (≥ 2 liens indépendants) ───────────────────────────────

def _links_between(edges, a, b):
    """Liens INDÉPENDANTS entre deux sociétés : secteur partagé, co-mouvement,
    même catalyseur — chaque lien cite sa base."""
    na, nb = 'company:%s' % a, 'company:%s' % b
    links = []
    sec_a = {e['dst'] for e in edges if e['relation'] == 'MEMBER_OF_SECTOR' and e['src'] == na}
    sec_b = {e['dst'] for e in edges if e['relation'] == 'MEMBER_OF_SECTOR' and e['src'] == nb}
    for sec in sorted(sec_a & sec_b):
        links.append({'relation': 'MEMBER_OF_SECTOR',
                      'basis': 'même secteur déclaré : %s' % sec.split(':', 1)[1]})
    for e in edges:
        if e['relation'] == 'CO_MOVES_WITH' and {e['src'], e['dst']} == {na, nb}:
            links.append({'relation': 'CO_MOVES_WITH', 'basis': e['basis']})
    cat_a = {e['dst'] for e in edges if e['relation'] == 'EXPOSED_TO_CATALYST' and e['src'] == na}
    cat_b = {e['dst'] for e in edges if e['relation'] == 'EXPOSED_TO_CATALYST' and e['src'] == nb}
    for c in sorted(cat_a & cat_b):
        links.append({'relation': 'EXPOSED_TO_CATALYST',
                      'basis': 'même catalyseur daté : %s' % c.split(':', 1)[1]})
    return links


def _hidden_dependencies(graph, symbols, held):
    """Paires partageant ≥ 2 liens indépendants — priorité aux paires détenues
    (le risque caché du portefeuille), sinon univers scanné."""
    edges = graph['edges']
    scope = held if len(held) >= 2 else symbols
    deps = []
    for i, a in enumerate(scope):
        for b in scope[i + 1:]:
            links = _links_between(edges, a, b)
            if len(links) >= 2:
                deps.append({'symbols': sorted([a, b]), 'links': links,
                             'held': a in held and b in held,
                             'basis': '%s et %s partagent %d lien(s) indépendant(s) — '
                                      'exposition commune non évidente au premier regard'
                                      % (a, b, len(links))})
    return deps


# ─── Questions de recherche (jamais une relation inventée) ──────────────────────

def _research_questions(symbols, sector_map, events_by_sym):
    qs = []
    for s in symbols:
        qs.append({'symbol': s, 'kind': 'value_chain', 'status': 'NON_DOCUMENTE',
                   'question': 'Quels sont les fournisseurs, clients et concurrents '
                               'critiques de %s ? Aucune source branchée — relation '
                               'jamais inventée.' % s})
        if not sector_map.get(s):
            qs.append({'symbol': s, 'kind': 'sector', 'status': 'NON_DOCUMENTE',
                       'question': '%s est hors watchlist sectorielle — quel est son '
                                   'secteur réel ?' % s})
        dated = [e for e in (events_by_sym.get(s) or [])
                 if e.get('dte') is not None and e.get('dte') <= MAX_DTE]
        if not dated:
            qs.append({'symbol': s, 'kind': 'catalyst', 'status': 'NON_DOCUMENTE',
                       'question': 'Aucun catalyseur daté ≤ %d j connu pour %s — '
                                   'lequel manque au calendrier ?' % (MAX_DTE, s)})
    return qs


# ─── Propagation d'impact explicable ────────────────────────────────────────────

def propagate(graph, node_id, max_hops=2):
    """Chemins simples depuis un nœud (≤ max_hops), chaque saut expliqué par la
    relation et la base de l'arête traversée. Nœud inconnu → liste vide."""
    g = graph or {}
    ids = {n['id'] for n in (g.get('nodes') or [])}
    if node_id not in ids:
        return []
    adj = {}
    for e in (g.get('edges') or []):
        adj.setdefault(e['src'], []).append((e['dst'], e))
        adj.setdefault(e['dst'], []).append((e['src'], e))
    paths = []

    def walk(path, hops):
        cur = path[-1]
        for nxt, e in sorted(adj.get(cur, []), key=lambda t: (t[0], t[1]['relation'])):
            if nxt in path:
                continue
            hop = {'relation': e['relation'], 'basis': e['basis'],
                   'evidence_level': e['evidence_level']}
            paths.append({'path': path + [nxt], 'hops': hops + [hop]})
            if len(path) <= max_hops - 1:
                walk(path + [nxt], hops + [hop])

    walk([node_id], [])
    return paths


__all__ = ['build', 'propagate', 'RELATIONS', 'SCHEMA_VERSION',
           'GRAPH_ENGINE_VERSION', 'MIN_POINTS', 'CORR_STRONG', 'MAX_DTE']
