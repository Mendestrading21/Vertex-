"""vertex/engines/decision_memory.py — MÉMOIRE DÉCISIONNELLE INSTITUTIONNELLE (LOT 10).

Fige chaque décision canonique servie en un record IMMUABLE du ledger
(SCENARIO_CALIBRATION.md §10) : identité, version du SkylerPacket et du moteur,
données/fraîcheur au moment de la décision, score /40 et niveau, confiance
(honnêtement None tant qu'aucun modèle calibré n'existe), thèse, catalyseur,
déclencheur, invalidation, scénarios avec probabilités honnêtes, EV honnête,
objection adverse, opinion minoritaire, inconnues et portefeuille figé.

Règles absolues du lot :
  - une décision historique n'est JAMAIS réécrite (append-only, falsification
    refusée, l'original gagne toujours) ;
  - aucune donnée connue APRÈS la décision n'entre dans le record : la mesure
    ne voit que les séances strictement postérieures, retrouvées par empreinte
    de fin de série (`tail_at_decision`) — série non alignée = non mesurable,
    jamais devinée ;
  - les résultats sont séparés PAR VERSION DE MOTEUR (jamais mélangés, jamais
    recalculés en douce sous une nouvelle version : autre version → autre id) ;
  - horizons de mesure déclarés uniquement : 5/20/60 séances, horizon du
    catalyseur (conversion jours→séances ÉTIQUETÉE estimée), horizon de thèse
    et échéance option honnêtement NON_APPLICABLE tant que le moteur 0.1.0 ne
    les déclare pas ;
  - la classification d'erreur est déterministe avec base explicite, et les
    recommandations restent EN_ATTENTE_VALIDATION_HUMAINE — ce module n'importe
    ni ne modifie jamais la Constitution, les poids ou les seuils.

Fonctions pures (horloge injectée), JSON-sérialisables. Lecture seule, aucun ordre.
"""
from __future__ import annotations

import hashlib
import math

MEMORY_SCHEMA_VERSION = 1
MEMORY_FILE = 'skyler_memory.json'
MAX_DECISIONS = 2000
_TAIL_LEN = 8                    # empreinte de fin de série au moment de la décision
_FREQ_WINDOW_S = 7 * 86400       # fenêtre du biais de fréquence (7 jours)
_FREQ_MAX = 10                   # au-delà : fréquence excessive sur un même titre

ERROR_CLASSES = ('ERREUR_DE_DONNEES', 'ERREUR_DE_MODELE', 'ERREUR_DE_SCENARIO',
                 'ERREUR_DE_TIMING', 'ERREUR_INSTRUMENT', 'ERREUR_DE_SIZING',
                 'ERREUR_DE_DISCIPLINE', 'VARIANCE_NORMALE')

_BULLISH = ('ACHETER', 'RENFORCER')


def _num(x):
    """Nombre FINI ou None — NaN/infini refusés (jamais sérialisés ni mesurés)."""
    if isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x):
        return float(x)
    return None


# ─── Gel d'une décision (ledger immuable) ───────────────────────────────────────

def freeze(decision, packet=None, price=None, closes=None, portfolio_ctx=None, now=None):
    """Construit le record immuable d'une décision canonique — uniquement depuis
    ce qui est connu AU MOMENT de la décision. Champs absents = None, jamais
    inventés."""
    d = decision or {}
    p = packet or {}
    engine_version = p.get('engine_version') or 'unknown'
    sym = d.get('symbol')
    as_of = d.get('as_of')
    # Identité déterministe : une autre version de moteur produit un AUTRE id —
    # une décision historique n'est jamais recalculée en douce sous une nouvelle
    # version, les deux records coexistent, séparés.
    raw = '%s|%s|%s|%s|%s' % (sym, as_of, d.get('decision'), engine_version,
                              bool(p.get('demo')))
    decision_id = hashlib.sha1(raw.encode('utf-8')).hexdigest()[:16]

    sc = d.get('score') or {}
    scen = d.get('scenarios') or {}
    trigger = ((scen.get('base') or {}).get('trigger')
               if scen.get('available') else None)

    contradictions = d.get('contradictions') or []
    minority = (contradictions[1]['detail'] if len(contradictions) > 1
                else (contradictions[0]['detail'] if contradictions and
                      d.get('capped_by_gate') is None else None))

    pf = portfolio_ctx or {}
    portfolio = ({'available': True,
                  'n_positions': pf.get('n_positions'),
                  'total_value': pf.get('total_value'),
                  'hhi': pf.get('hhi'),
                  'top_symbol': pf.get('top_symbol'),
                  'top_weight_pct': pf.get('top_weight_pct')}
                 if pf.get('available') else
                 {'available': False,
                  'reason': pf.get('reason') or 'portefeuille non fourni à la décision'})

    tail = ([_num(c) for c in closes[-_TAIL_LEN:]]
            if closes and all(_num(c) is not None for c in closes[-_TAIL_LEN:])
            else None)

    px = _num(price)
    return {
        'memory_schema': MEMORY_SCHEMA_VERSION,
        'decision_id': decision_id,
        'packet_schema_version': p.get('schema_version'),
        'engine_version': engine_version,
        'profile_version': p.get('profile_version'),
        'symbol': sym, 'as_of': as_of, 'recorded_at': now,
        'demo': bool(p.get('demo')),
        'price_at_decision': px,
        'tail_at_decision': tail,
        'decision': d.get('decision'),
        # figés SEULEMENT si le moteur les produit (0.3.0+) — sinon None honnête
        'operational_state': d.get('operational_state'),
        'operational_state_note': (d.get('operational_state_basis')
                                   if d.get('operational_state') is not None else
                                   'non émis par le moteur %s — jamais inventé' % engine_version),
        'capped_by_gate': d.get('capped_by_gate'),
        'score_total': sc.get('total'), 'score_max': sc.get('max'),
        'score_blocks': sc.get('blocks') or {},
        'level': d.get('level') or sc.get('level'),
        'insufficient_blocks': sc.get('insufficient_blocks') or [],
        'confidence': (d['confidence'].get('value')
                       if isinstance(d.get('confidence'), dict) else None),
        'confidence_factors': (d['confidence'].get('factors')
                               if isinstance(d.get('confidence'), dict) else None),
        'confidence_note': (d['confidence'].get('method')
                            if isinstance(d.get('confidence'), dict) else
                            'aucun modèle de confiance calibré (moteur %s) — jamais inventée'
                            % engine_version),
        'thesis': d.get('main_reason'),
        'catalyst': d.get('catalyst'),
        'trigger': trigger,
        'invalidation': d.get('invalidation'),
        'max_risk_pct': d.get('max_risk_pct'),
        'scenarios': scen,
        'expected_value': None,
        'ev_note': 'aucune probabilité calibrée — EV incalculable, jamais inventée',
        'strongest_objection': d.get('strongest_objection'),
        'minority_opinion': minority,
        'unknowns': d.get('unknowns') or [],
        'contradictions_count': len(contradictions),
        'portfolio': portfolio,
    }


# ─── Mémoire append-only ────────────────────────────────────────────────────────

def empty_memory():
    return {'schema': MEMORY_SCHEMA_VERSION, 'decisions': [], 'outcomes': []}


def append_decision(memory, record):
    """Ajoute un record — append-only, borné. Un decision_id déjà présent n'est
    JAMAIS remplacé, même si le contenu diffère : l'historique original gagne."""
    mem = {'schema': (memory or {}).get('schema', MEMORY_SCHEMA_VERSION),
           'decisions': list((memory or {}).get('decisions') or []),
           'outcomes': list((memory or {}).get('outcomes') or [])}
    r = record or {}
    if not r.get('decision_id') or not r.get('symbol'):
        return mem
    if any(e.get('decision_id') == r['decision_id'] for e in mem['decisions']):
        return mem
    mem['decisions'].append(r)
    mem['decisions'] = mem['decisions'][-MAX_DECISIONS:]
    return mem


def append_outcome(memory, outcome):
    """Enregistre un résultat mesuré. Un résultat existant n'est remplacé que
    par une mesure couvrant STRICTEMENT PLUS de séances (monotone) — la mesure
    s'enrichit avec le temps, elle ne régresse jamais."""
    mem = {'schema': (memory or {}).get('schema', MEMORY_SCHEMA_VERSION),
           'decisions': list((memory or {}).get('decisions') or []),
           'outcomes': list((memory or {}).get('outcomes') or [])}
    o = outcome or {}
    if not o.get('decision_id'):
        return mem
    for i, e in enumerate(mem['outcomes']):
        if e.get('decision_id') == o['decision_id']:
            if (o.get('sessions_observed') or 0) > (e.get('sessions_observed') or 0):
                mem['outcomes'][i] = o
            return mem
    mem['outcomes'].append(o)
    mem['outcomes'] = mem['outcomes'][-MAX_DECISIONS:]
    return mem


# ─── Anti-look-ahead : séances strictement postérieures ─────────────────────────

def sessions_after(closes, tail):
    """Retrouve l'empreinte de fin de série figée à la décision dans la série
    actuelle et renvoie UNIQUEMENT les clôtures postérieures. Série non
    alignée (fenêtre roulée, données révisées) → None : non mesurable, jamais
    deviné."""
    if not tail or not closes or len(closes) < len(tail):
        return None
    n = len(tail)
    for i in range(len(closes) - n, -1, -1):          # dernière occurrence
        if all(_num(closes[i + k]) == tail[k] for k in range(n)):
            return [_num(c) for c in closes[i + n:]]
    return None


# ─── Mesure aux horizons déclarés ───────────────────────────────────────────────

def _horizon(status, sessions=None, return_pct=None, basis='', estimated=None):
    h = {'status': status, 'sessions': sessions, 'return_pct': return_pct,
         'basis': basis}
    if estimated is not None:
        h['estimated'] = estimated
    return h


def measure(record, closes_after):
    """Mesure le résultat d'un record aux horizons déclarés UNIQUEMENT —
    5/20/60 séances, horizon du catalyseur (jours→séances étiqueté estimé),
    horizon de thèse et échéance option (NON_APPLICABLE tant que le moteur ne
    les déclare pas). Horizon non atteint = EN_ATTENTE, jamais inventé."""
    r = record or {}
    after = [c for c in (closes_after or []) if _num(c) is not None]
    px = _num(r.get('price_at_decision'))
    n = len(after)

    def measured(sessions, estimated=None):
        if px is None or px <= 0:
            return _horizon('NON_MESURABLE', sessions,
                            basis='prix à la décision absent — rendement incalculable',
                            estimated=estimated)
        if n < sessions:
            return _horizon('EN_ATTENTE', sessions,
                            basis='%d/%d séance(s) postérieure(s) observée(s)' % (n, sessions),
                            estimated=estimated)
        return _horizon('MESURE', sessions,
                        round((after[sessions - 1] / px - 1) * 100, 2),
                        basis='clôture séance +%d vs prix à la décision' % sessions,
                        estimated=estimated)

    horizons = {'H5': measured(5), 'H20': measured(20), 'H60': measured(60)}

    # Horizon du catalyseur : le record fige « Libellé (J-N) » en jours
    # calendaires ; conversion en séances ÉTIQUETÉE estimée (× 5/7).
    dte = None
    cat = r.get('catalyst') or ''
    if '(J-' in cat:
        try:
            dte = int(cat.split('(J-')[1].split(')')[0])
        except Exception:
            dte = None
    if dte is None:
        horizons['CATALYSEUR'] = _horizon('NON_APPLICABLE',
                                          basis='aucun catalyseur daté figé à la décision')
    else:
        s = max(1, round(dte * 5 / 7))
        h = measured(s, estimated=True)
        h['basis'] += ' — J-%d calendaires ≈ %d séances (× 5/7, estimation étiquetée)' % (dte, s)
        horizons['CATALYSEUR'] = h

    horizons['THESE'] = _horizon('NON_APPLICABLE',
                                 basis='horizon de thèse non déclaré par le moteur %s — jamais supposé'
                                       % r.get('engine_version'))
    horizons['OPTION'] = _horizon('NON_APPLICABLE',
                                  basis='aucun instrument option choisi par le moteur %s'
                                        % r.get('engine_version'))

    mfe = mae = None
    if px and px > 0 and after:
        mfe = round((max(after) / px - 1) * 100, 2)
        mae = round((min(after) / px - 1) * 100, 2)

    return {'decision_id': r.get('decision_id'),
            'engine_version': r.get('engine_version'),
            'symbol': r.get('symbol'),
            'sessions_observed': n,
            'horizons': horizons,
            'mfe_pct': mfe, 'mae_pct': mae,
            'note': 'séances strictement postérieures à la décision uniquement — aucun look-ahead'}


# ─── Classification déterministe des erreurs ────────────────────────────────────

def classify_error(record, return_pct, horizon_label):
    """Classe un résultat mesuré selon la taxonomie du lot — règles ordonnées,
    base explicite. Les erreurs d'exécution (instrument, sizing, discipline)
    exigent des trades réels absents ici : jamais devinées."""
    r = record or {}
    ret = _num(return_pct)
    if ret is None:
        return {'class': 'NON_CLASSIFIABLE', 'horizon': horizon_label,
                'basis': 'résultat non observé à cet horizon — rien à juger, rien d’inventé'}
    scen = r.get('scenarios') or {}
    bear_r = _num((scen.get('bear') or {}).get('return_pct')) if scen.get('available') else None
    base_r = _num((scen.get('base') or {}).get('return_pct')) if scen.get('available') else None
    decision = r.get('decision')

    if decision in _BULLISH:
        if ret >= 0:
            return {'class': 'DECISION_CORRECTE', 'horizon': horizon_label,
                    'basis': 'rendement %+.1f %% dans le sens de la décision %s' % (ret, decision)}
        if bear_r is None:
            return {'class': 'ERREUR_DE_DONNEES', 'horizon': horizon_label,
                    'basis': 'perte %+.1f %% sans scénarios disponibles à la décision '
                             '(plan incomplet) — le dossier manquait de données' % ret}
        if ret >= bear_r:
            return {'class': 'VARIANCE_NORMALE', 'horizon': horizon_label,
                    'basis': 'perte %+.1f %% dans la fourchette du scénario pessimiste '
                             '(%+.1f %%) envisagé à la décision' % (ret, bear_r)}
        if r.get('insufficient_blocks'):
            return {'class': 'ERREUR_DE_DONNEES', 'horizon': horizon_label,
                    'basis': 'perte %+.1f %% sous le scénario pessimiste avec blocs '
                             'insuffisants (%s) à la décision'
                             % (ret, ', '.join(r['insufficient_blocks']))}
        if (r.get('score_total') or 0) >= 28:
            return {'class': 'ERREUR_DE_MODELE', 'horizon': horizon_label,
                    'basis': 'perte %+.1f %% sous le scénario pessimiste (%+.1f %%) '
                             'malgré un dossier complet noté %s/40'
                             % (ret, bear_r, r.get('score_total'))}
        return {'class': 'ERREUR_DE_SCENARIO', 'horizon': horizon_label,
                'basis': 'perte %+.1f %% hors de la fourchette pessimiste (%+.1f %%) — '
                         'les scénarios n’ont pas contenu le résultat' % (ret, bear_r)}

    # Décisions non haussières : l'erreur mesurable est le mouvement manqué.
    if base_r is not None and base_r > 0 and ret >= base_r:
        return {'class': 'ERREUR_DE_TIMING', 'horizon': horizon_label,
                'basis': 'rendement %+.1f %% ≥ scénario probable (%+.1f %%) réalisé '
                         'sans position — occasion manquée' % (ret, base_r)}
    return {'class': 'DECISION_CORRECTE', 'horizon': horizon_label,
            'basis': 'décision %s : aucun mouvement au-delà du scénario probable manqué '
                     '(%+.1f %%)' % (decision, ret)}


# ─── Biais récurrents (10 comportements) ────────────────────────────────────────

def _measured_class(mem, r):
    """Classe d'erreur du record au plus long horizon séance mesuré, ou None."""
    for o in mem.get('outcomes') or []:
        if o.get('decision_id') == r.get('decision_id'):
            for h in ('H60', 'H20', 'H5'):
                hz = (o.get('horizons') or {}).get(h) or {}
                if hz.get('status') == 'MESURE':
                    return classify_error(r, hz.get('return_pct'), h)['class']
    return None


def detect_patterns(memory):
    """Détecte les 10 comportements récurrents du lot — calculés uniquement
    depuis la mémoire figée ; un biais inobservable sans trades réels est
    honnêtement INSUFFISANT, jamais deviné."""
    mem = memory or empty_memory()
    decs = mem.get('decisions') or []
    out = []

    def pat(name, status, basis):
        out.append({'pattern': name, 'status': status, 'basis': basis})

    no_trades = 'aucun trade réel lié à la mémoire décisionnelle — inobservable, jamais deviné'
    pat('poursuite_du_prix', 'INSUFFISANT', no_trades)
    pat('sortie_prematuree', 'INSUFFISANT', no_trades)
    pat('options_trop_courtes', 'INSUFFISANT',
        'aucun instrument option choisi par le moteur — ' + no_trades)
    pat('spreads_trop_larges', 'INSUFFISANT',
        'aucun instrument option choisi par le moteur — ' + no_trades)

    blocked_loser = sum(1 for r in decs if r.get('capped_by_gate') == 'LOSER_REINFORCEMENT')
    pat('renforcement_perdant',
        'DETECTE' if blocked_loser else 'ABSENT',
        '%d tentative(s) bloquée(s) par la gate LOSER_REINFORCEMENT' % blocked_loser
        if blocked_loser else 'aucune tentative de renforcement perdant enregistrée')

    blocked_conc = sum(1 for r in decs if r.get('capped_by_gate') == 'CONCENTRATION_EXCESSIVE')
    pat('risque_portefeuille_ignore',
        'DETECTE' if blocked_conc else 'ABSENT',
        '%d décision(s) plafonnée(s) par la gate CONCENTRATION_EXCESSIVE' % blocked_conc
        if blocked_conc else 'aucune décision plafonnée par la concentration portefeuille')

    # Surconfiance : niveau S/S+ dont le résultat mesuré est une erreur.
    high = [r for r in decs if r.get('level') in ('S_PLUS', 'S')]
    high_meas = [(r, _measured_class(mem, r)) for r in high]
    high_meas = [(r, c) for r, c in high_meas if c is not None]
    if not high_meas:
        pat('surconfiance', 'INSUFFISANT',
            'aucune décision S/S+ avec résultat mesuré — rien à juger')
    else:
        bad = sum(1 for _, c in high_meas if c.startswith('ERREUR'))
        pat('surconfiance', 'DETECTE' if bad else 'ABSENT',
            '%d/%d décision(s) S/S+ mesurée(s) classée(s) en erreur' % (bad, len(high_meas)))

    # Fréquence excessive : > _FREQ_MAX décisions distinctes sur un même titre en 7 jours.
    freq = None
    by_sym = {}
    for r in decs:
        if _num(r.get('recorded_at')) is not None:
            by_sym.setdefault(r.get('symbol'), []).append(float(r['recorded_at']))
    for s, ts in by_sym.items():
        ts.sort()
        for i in range(len(ts)):
            j = i
            while j < len(ts) and ts[j] - ts[i] <= _FREQ_WINDOW_S:
                j += 1
            if j - i > _FREQ_MAX:
                freq = (s, j - i)
                break
        if freq:
            break
    pat('frequence_excessive',
        'DETECTE' if freq else 'ABSENT',
        '%s : %d décisions en 7 jours (seuil %d)' % (freq[0], freq[1], _FREQ_MAX)
        if freq else 'aucun titre au-delà de %d décisions sur 7 jours' % _FREQ_MAX)

    # Dépendance à une hypothèse unique : un seul bloc de score porte tous les points.
    single = 0
    for r in decs:
        blocks = r.get('score_blocks') or {}
        pos = [b for b in blocks.values() if (b.get('points') or 0) > 0]
        if len(blocks) >= 2 and len(pos) == 1:
            single += 1
    pat('dependance_hypothese_unique',
        'DETECTE' if single else ('ABSENT' if decs else 'INSUFFISANT'),
        '%d décision(s) dont un seul bloc de score porte tous les points' % single
        if single else ('tous les dossiers reposent sur plusieurs blocs'
                        if decs else 'aucune décision en mémoire'))

    # Catalyseur mal évalué : horizon CATALYSEUR mesuré classé en erreur.
    cat_meas, cat_bad = 0, 0
    for o in mem.get('outcomes') or []:
        hz = (o.get('horizons') or {}).get('CATALYSEUR') or {}
        if hz.get('status') != 'MESURE':
            continue
        r = next((x for x in decs if x.get('decision_id') == o.get('decision_id')), None)
        if r is None:
            continue
        cat_meas += 1
        if classify_error(r, hz.get('return_pct'), 'CATALYSEUR')['class'].startswith('ERREUR'):
            cat_bad += 1
    if not cat_meas:
        pat('catalyseur_mal_evalue', 'INSUFFISANT',
            'aucun horizon de catalyseur mesuré — rien à juger')
    else:
        pat('catalyseur_mal_evalue', 'DETECTE' if cat_bad else 'ABSENT',
            '%d/%d horizon(s) de catalyseur mesurés classés en erreur' % (cat_bad, cat_meas))

    return out


# ─── Agrégats par version de moteur ─────────────────────────────────────────────

def aggregates(memory):
    """Agrège la mémoire STRICTEMENT par version de moteur — les résultats de
    versions différentes ne sont jamais mélangés ni comparés implicitement."""
    mem = memory or empty_memory()
    by_v = {}
    for r in mem.get('decisions') or []:
        v = r.get('engine_version') or 'unknown'
        b = by_v.setdefault(v, {'n_decisions': 0, 'by_decision': {}, 'by_level': {},
                                'measured': 0, 'error_classes': {}})
        b['n_decisions'] += 1
        b['by_decision'][r.get('decision')] = b['by_decision'].get(r.get('decision'), 0) + 1
        if r.get('level'):
            b['by_level'][r['level']] = b['by_level'].get(r['level'], 0) + 1
        cls = _measured_class(mem, r)
        if cls is not None:
            b['measured'] += 1
            b['error_classes'][cls] = b['error_classes'].get(cls, 0) + 1
    return {'by_engine_version': by_v,
            'note': 'résultats séparés par version de moteur — jamais fusionnés'}


# ─── Recommandations (jamais auto-appliquées) ───────────────────────────────────

def recommendations(patterns, aggs):
    """Propositions d'amélioration DOCUMENTÉES depuis les biais détectés —
    toujours EN_ATTENTE_VALIDATION_HUMAINE. Ce module ne modifie jamais les
    poids, seuils ou la Constitution."""
    props = {
        'renforcement_perdant': 'revoir la discipline d’ajout : la gate a dû bloquer des renforcements perdants',
        'risque_portefeuille_ignore': 'revoir le dimensionnement : des dossiers ont été plafonnés par la concentration',
        'surconfiance': 'plafonner la confiance des niveaux S/S+ dans ce régime jusqu’à recalibration validée',
        'frequence_excessive': 'espacer les décisions sur un même titre (fenêtre de refroidissement)',
        'dependance_hypothese_unique': 'exiger un second bloc de preuve avant tout niveau supérieur à B',
        'catalyseur_mal_evalue': 'réviser l’évaluation des catalyseurs datés (nouveauté/pricing) avant de les noter',
    }
    out = []
    for p in patterns or []:
        if p.get('status') == 'DETECTE' and p.get('pattern') in props:
            out.append({'pattern': p['pattern'],
                        'proposal': props[p['pattern']],
                        'basis': p.get('basis'),
                        'status': 'EN_ATTENTE_VALIDATION_HUMAINE'})
    return out


__all__ = ['freeze', 'empty_memory', 'append_decision', 'append_outcome',
           'sessions_after', 'measure', 'classify_error', 'detect_patterns',
           'aggregates', 'recommendations',
           'ERROR_CLASSES', 'MEMORY_FILE', 'MAX_DECISIONS', 'MEMORY_SCHEMA_VERSION']
