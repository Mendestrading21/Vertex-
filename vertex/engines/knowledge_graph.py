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


def _residual_vs_market(rets, mkt):
    """Résidus de la régression OLS des rendements sur ceux du marché
    (r_t − β·m_t) + part de variance expliquée (R²). Variance de marché nulle
    → résidus = rendements bruts, R² = 0 (rien d'expliqué, rien d'inventé)."""
    n = len(rets)
    if n != len(mkt) or n < 2:
        return None, None
    mm = sum(mkt) / n
    var_m = sum((m - mm) ** 2 for m in mkt)
    if var_m <= 0:
        return list(rets), 0.0
    mr = sum(rets) / n
    beta = sum((r - mr) * (m - mm) for r, m in zip(rets, mkt)) / var_m
    resid = [r - beta * m for r, m in zip(rets, mkt)]
    var_r = sum((r - mr) ** 2 for r in rets)
    if var_r <= 0:
        return resid, 0.0
    mres = sum(resid) / n
    var_res = sum((x - mres) ** 2 for x in resid)
    r2 = max(0.0, min(1.0, 1.0 - var_res / var_r))
    return resid, round(r2, 3)


# ─── Construction ───────────────────────────────────────────────────────────────

def build(symbols, sector_map=None, closes_by_sym=None, events_by_sym=None,
          positions=None, quotes=None, as_of=None, demo=False):
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
    # Série SPY disponible → corrélation PARTIELLE sur les résidus de marché
    # (deux titres qui suivent le marché ne co-bougent pas « en propre ») ;
    # sinon corrélation brute, ÉTIQUETÉE — jamais un fallback silencieux.
    with_series = [s for s in symbols
                   if len([c for c in (closes_by_sym.get(s) or []) if _num(c) is not None]) >= MIN_POINTS]
    skipped = [s for s in symbols if closes_by_sym.get(s) and s not in with_series]
    if skipped:
        limits.append('co-mouvement non évalué pour %s : série < %d points — jamais deviné'
                      % (', '.join(skipped), MIN_POINTS))
    spy = closes_by_sym.get('SPY')
    residual_mode = ('SPY' in with_series and spy is not None)
    if residual_mode:
        pair_pool = [s for s in with_series if s != 'SPY']
        limits.append('co-mouvement : méthode residual_vs_SPY (résidus de la régression '
                      'sur SPY) — SPY exclu des paires (son co-mouvement avec le marché est trivial)')
    else:
        pair_pool = with_series
        if with_series:
            limits.append('série SPY absente — corrélation brute étiquetée `raw` '
                          '(peut refléter le marché plutôt qu’un lien propre)')
    for i, a in enumerate(pair_pool):
        for b in pair_pool[i + 1:]:
            ca, cb = closes_by_sym[a], closes_by_sym[b]
            L = min(len(ca), len(cb), len(spy)) if residual_mode else min(len(ca), len(cb))
            ra, rb = _log_returns(ca[-L:]), _log_returns(cb[-L:])
            if ra is None or rb is None:
                continue
            r2 = None
            if residual_mode:
                rm = _log_returns(spy[-L:])
                if rm is None:
                    continue
                ra, r2a = _residual_vs_market(ra, rm)
                rb, r2b = _residual_vs_market(rb, rm)
                if ra is None or rb is None:
                    continue
                r2 = {a: r2a, b: r2b}
            corr = _pearson(ra, rb)
            if corr is None or not math.isfinite(corr) or corr < CORR_STRONG:
                continue
            method = 'residual_vs_SPY' if residual_mode else 'raw'
            edge = {'relation': 'CO_MOVES_WITH',
                    'src': 'company:%s' % a, 'dst': 'company:%s' % b,
                    'source': 'série canonique de clôtures (scan)',
                    'evidence_level': 'F2', 'method': method,
                    'value': round(corr, 3), 'window': L - 1,
                    'basis': ('corrélation des résidus de marché %s/%s = %.2f sur %d points '
                              '(seuil %.2f) — régression sur SPY, part expliquée retirée'
                              % (a, b, corr, L - 1, CORR_STRONG)) if residual_mode else
                             ('corrélation brute (méthode raw) des rendements log %s/%s = %.2f '
                              'sur %d points (seuil %.2f) — SPY absent, marché non contrôlé'
                              % (a, b, corr, L - 1, CORR_STRONG))}
            if r2 is not None:
                edge['r2'] = r2
            edges.append(edge)

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
    graph['hidden_groups'] = _hidden_groups(graph['hidden_dependencies'], sector_map)
    graph['sector_exposure'] = _sector_exposure(positions, sector_map, quotes)
    graph['research_questions'] = _research_questions(symbols, sector_map, events_by_sym)
    return graph


# ─── Exposition sectorielle du portefeuille (LOT 24) ────────────────────────────

def _sector_exposure(positions, sector_map, quotes):
    """Agrège les positions RÉELLES par secteur déclaré. Poids en % seulement
    si TOUTES les positions ont une cote (sinon None avec raison — un poids
    partiel serait un mensonge). Titre hors watchlist → HORS_WATCHLIST."""
    sector_map = sector_map or {}
    quotes = quotes or {}
    held = {}
    for p in (positions or []):
        s = str(p.get('symbol') or '').upper()
        qty = p.get('quantity')
        if not s or not isinstance(qty, (int, float)) or isinstance(qty, bool) or not qty:
            continue
        held[s] = held.get(s, 0.0) + float(qty)
    if not held:
        return {}
    values, all_quoted = {}, True
    for s, qty in held.items():
        px = _num(quotes.get(s))
        if px is None or px <= 0:
            all_quoted = False
            values[s] = None
        else:
            values[s] = qty * px
    total = sum(v for v in values.values() if v is not None) if all_quoted else None
    out = {}
    for s in sorted(held):
        sec = sector_map.get(s) or 'HORS_WATCHLIST'
        cell = out.setdefault(sec, {'symbols': [], 'n_positions': 0,
                                    'weight_pct': None, 'basis': ''})
        cell['symbols'].append(s)
        cell['n_positions'] += 1
    for sec, cell in out.items():
        if total and total > 0:
            w = sum(values[s] for s in cell['symbols']) / total * 100
            cell['weight_pct'] = round(w, 2)
            cell['basis'] = ('%d position(s) — %.1f %% du portefeuille valorisé aux '
                             'cotes réelles' % (cell['n_positions'], w))
        else:
            cell['basis'] = ('%d position(s) — poids n/d : cote absente pour au moins '
                             'une position, jamais estimé' % cell['n_positions'])
    return out


def _hidden_groups(deps, sector_map=None):
    """Composantes connexes des paires de dépendances cachées — un GROUPE de
    3 titres ou plus partage une exposition commune plus large qu'une paire.
    Groupe entièrement dans un même secteur déclaré → CONCENTRATION SECTORIELLE."""
    sector_map = sector_map or {}
    adj = {}
    for d in deps or []:
        a, b = d['symbols']
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    seen, groups = set(), []
    for s in sorted(adj):
        if s in seen:
            continue
        comp, stack = [], [s]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            comp.append(x)
            stack.extend(adj[x] - seen)
        if len(comp) >= 3:
            comp = sorted(comp)
            n_links = sum(len(d['links']) for d in deps
                          if set(d['symbols']) <= set(comp))
            secs = {sector_map.get(s) for s in comp}
            mono = len(secs) == 1 and None not in secs
            groups.append({'symbols': comp, 'n_links': n_links,
                           'sector_concentration': mono,
                           'sector': (next(iter(secs)) if mono else None),
                           'basis': ('%d titres inter-reliés par %d lien(s) indépendant(s) — '
                                     'exposition de groupe non évidente au premier regard'
                                     % (len(comp), n_links))
                                    + (' — CONCENTRATION SECTORIELLE : tout le groupe est '
                                       'dans le secteur déclaré %s' % next(iter(secs))
                                       if mono else '')})
    return groups


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

MAX_PATHS = 200                  # garde de volume dure de la propagation


def propagate(graph, node_id, max_hops=2, max_paths=None):
    """Chemins simples depuis un nœud (≤ max_hops), chaque saut expliqué par la
    relation et la base de l'arête traversée. Nœud inconnu → liste vide.
    GARDE DE VOLUME : jamais plus de `max_paths` chemins (MAX_PATHS par
    défaut) — troncature DÉTERMINISTE (parcours trié) ; l'appelant compare
    len(résultat) à la garde pour DIRE la troncature, jamais silencieuse."""
    g = graph or {}
    ids = {n['id'] for n in (g.get('nodes') or [])}
    if node_id not in ids:
        return []
    limit = MAX_PATHS if max_paths is None else max(1, int(max_paths))
    adj = {}
    for e in (g.get('edges') or []):
        adj.setdefault(e['src'], []).append((e['dst'], e))
        adj.setdefault(e['dst'], []).append((e['src'], e))
    paths = []

    def walk(path, hops):
        if len(paths) >= limit:
            return
        cur = path[-1]
        for nxt, e in sorted(adj.get(cur, []), key=lambda t: (t[0], t[1]['relation'])):
            if len(paths) >= limit:
                return
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
           'GRAPH_ENGINE_VERSION', 'MIN_POINTS', 'CORR_STRONG', 'MAX_DTE',
           'MAX_PATHS']
