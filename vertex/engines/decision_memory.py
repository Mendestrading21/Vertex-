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
  - horizons de mesure déclarés uniquement : 5/20/60 séances (comptées en
    séances RÉELLES via le log daté du lot 15, empreinte de série en secours),
    horizon du catalyseur (conversion jours→séances ÉTIQUETÉE estimée),
    horizon de thèse et échéance option honnêtement NON_APPLICABLE tant que le
    moteur courant ne les déclare pas ;
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


def option_dte_bucket(dte):
    """Bucket de DTE stable pour l’observation, jamais une règle de sélection."""
    value = _num(dte)
    if value is None or value < 0:
        return None
    if value < 75:
        return 'UNDER_75'
    if value < 105:
        return '75_104'
    if value < 135:
        return '105_134'
    if value < 165:
        return '135_164'
    if value < 181:
        return '165_180'
    if value <= 210:
        return '181_210'
    return 'OVER_210'


def _option_context(packet):
    """Fige uniquement le contexte options déjà présent dans le packet."""
    ctx = ((packet or {}).get('contexts') or {}).get('options') or {}
    if not ctx.get('available'):
        return {'available': False,
                'reason': ctx.get('reason') or 'contexte options non fourni à la décision'}
    best = ctx.get('best') or {}
    mandate = best.get('mandate') or {}
    bounds = mandate.get('bounds') or {}
    dte = _num(best.get('dte'))
    return {
        'available': bool(best),
        'universe': ctx.get('universe'),
        'dte': dte,
        'dte_bucket': option_dte_bucket(dte),
        'delta': _num(best.get('delta')),
        'iv': _num(best.get('iv')),
        'open_interest': _num(best.get('oi')),
        'volume': _num(best.get('volume')),
        'spread_pct': _num(best.get('spread_pct')),
        'quote_age_seconds': _num(best.get('quote_age_seconds')),
        'mandate_status': ctx.get('mandate_status') or best.get('mandate_status'),
        'holding_plan_sessions': list(bounds.get('holding_plan_sessions') or []),
        'instrument_pnl_available': False,
        'note': 'contexte de sélection figé ; P&L contractuel non mesuré par ce ledger sans quotes de sortie',
    }


# ─── Gel d'une décision (ledger immuable) ───────────────────────────────────────

def freeze(decision, packet=None, price=None, closes=None, portfolio_ctx=None,
           now=None, session_date=None):
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
    option = _option_context(p)
    contexts = p.get('contexts') or {}
    quality_ctx = contexts.get('data_quality') or {}
    reconciliation_ctx = contexts.get('reconciliation') or {}
    data_evidence = {
        'quality_available': quality_ctx.get('available'),
        'quality_overall': quality_ctx.get('overall'),
        'quality_actionable': quality_ctx.get('actionable_allowed'),
        'spot_freshness': (quality_ctx.get('freshness') or {}).get('spot'),
        'options_freshness': (quality_ctx.get('freshness') or {}).get('options'),
        'reconciliation_available': reconciliation_ctx.get('available'),
        'reconciliation_actionable': reconciliation_ctx.get('actionable_allowed'),
        'reconciliation_blocking': reconciliation_ctx.get('blocking'),
    }

    px = _num(price)
    return {
        'memory_schema': MEMORY_SCHEMA_VERSION,
        'decision_id': decision_id,
        'packet_schema_version': p.get('schema_version'),
        'engine_version': engine_version,
        'profile_version': p.get('profile_version'),
        'symbol': sym, 'as_of': as_of, 'recorded_at': now,
        'session_date': session_date,   # date d'observation réelle — None si inconnue
        # régime de marché AU MOMENT de la décision (label du packet) — None honnête
        'regime': (((p.get('contexts') or {}).get('market') or {}).get('regime') or {}).get('label'),
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
        # kind EXPLICITE émis par le moteur (0.9.0+) — jamais re-parsé du label
        'catalyst_kind': d.get('catalyst_kind'),
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
        'option': option,
        # Preuves de données AU MOMENT de la décision. Elles nourrissent une
        # surveillance descriptive de dérive, sans réécrire les anciens records.
        'data_evidence': data_evidence,
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
    """Mesure le sous-jacent aux horizons déclarés uniquement.

    Les horizons 5/10/15 séances suivent le mandat Swing 3–6M. Les horizons 20/60
    restent disponibles pour l’analyse de thèse. Le P&L du contrat reste explicitement
    non applicable tant qu’aucune quote de sortie de contrat n’est enregistrée.
    """
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

    horizons = {
        'H5': measured(5),
        'H10': measured(10),
        'H15': measured(15),
        'H20': measured(20),
        'H60': measured(60),
    }

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
    option = r.get('option') or {}
    if option.get('available'):
        horizons['OPTION'] = _horizon(
            'NON_APPLICABLE',
            basis='contrat %s / DTE %s figé, mais quote de sortie absente : P&L contractuel non mesuré'
                  % (option.get('universe') or 'inconnu', option.get('dte') or 'inconnu'))
    else:
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
        if not isinstance(o, dict):        # magasin corrompu → entrée ignorée
            continue
        if o.get('decision_id') == r.get('decision_id'):
            for h in ('H60', 'H20', 'H15', 'H10', 'H5'):
                hz = (o.get('horizons') or {}).get(h) or {}
                if hz.get('status') == 'MESURE':
                    return classify_error(r, hz.get('return_pct'), h)['class']
    return None


def detect_patterns(memory):
    """Détecte les 10 comportements récurrents du lot — calculés uniquement
    depuis la mémoire figée ; un biais inobservable sans trades réels est
    honnêtement INSUFFISANT, jamais deviné."""
    mem = memory or empty_memory()
    # magasin corrompu → entrées non-dict ignorées (refus honnête, jamais 500)
    decs = [r for r in (mem.get('decisions') or []) if isinstance(r, dict)]
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
        if not isinstance(o, dict):        # magasin corrompu → entrée ignorée
            continue
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
        if not isinstance(r, dict):        # magasin corrompu → entrée ignorée
            continue
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


# ─── Post-mortem par décision (LOT 20) ──────────────────────────────────────────

def find_decision(memory, decision_id):
    for r in (memory or {}).get('decisions') or []:
        if isinstance(r, dict) and r.get('decision_id') == decision_id:
            return r
    return None


def find_outcome(memory, decision_id):
    for o in (memory or {}).get('outcomes') or []:
        if isinstance(o, dict) and o.get('decision_id') == decision_id:
            return o
    return None


def post_mortem(record, outcome):
    """Revue POST-MORTEM déterministe (mode Post-Mortem du comité) — décision
    vs résultat observé, scénario ayant CONTENU le résultat, classification par
    horizon mesuré. Uniquement depuis les données figées ; rien de mesuré →
    honnêtement indisponible. L'erreur de discipline reste inobservable sans
    trades réels — dit, jamais deviné."""
    r = record or {}
    measured = []
    for h in ('H5', 'H20', 'H60', 'CATALYSEUR'):
        hz = ((outcome or {}).get('horizons') or {}).get(h) or {}
        if hz.get('status') == 'MESURE' and _num(hz.get('return_pct')) is not None:
            measured.append((h, float(hz['return_pct'])))
    if not measured:
        return {'available': False,
                'reason': 'aucun horizon mesuré pour cette décision — post-mortem '
                          'impossible, rien d’inventé'}

    horizons = [{'horizon': h, 'return_pct': ret,
                 'classification': classify_error(r, ret, h)}
                for h, ret in measured]
    longest, ret = measured[-1]

    scen = r.get('scenarios') or {}
    containing, scen_note = None, None
    if scen.get('available'):
        bear_r = _num((scen.get('bear') or {}).get('return_pct'))
        base_r = _num((scen.get('base') or {}).get('return_pct'))
        bull_r = _num((scen.get('bull') or {}).get('return_pct'))
        if None not in (bear_r, base_r, bull_r):
            if ret < bear_r:
                containing = 'HORS_FOURCHETTE_BASSE'
            elif ret < base_r:
                containing = 'PESSIMISTE'
            elif ret < bull_r:
                containing = 'PROBABLE'
            else:
                containing = 'EXCEPTIONNEL_ATTEINT'
        else:
            scen_note = 'scénarios figés incomplets — containment non évaluable'
    else:
        scen_note = 'aucun scénario figé à la décision — containment non évaluable'

    return {'available': True,
            'longest_horizon': longest, 'return_pct': ret,
            'horizons': horizons,
            'scenario_containing': containing,
            'scenario_note': scen_note,
            'mfe_pct': (outcome or {}).get('mfe_pct'),
            'mae_pct': (outcome or {}).get('mae_pct'),
            'discipline_note': 'erreur de discipline inobservable sans trades réels '
                               'liés à la décision — jamais devinée',
            'summary': 'Décision %s (%s, moteur %s) — rendement observé %+.1f %% à %s, '
                       'classé %s.' % (r.get('decision'), r.get('symbol'),
                                       r.get('engine_version'), ret, longest,
                                       horizons[-1]['classification']['class'])}


# ─── Facteur de calibration réel (LOT 19) ───────────────────────────────────────

MIN_CALIBRATION_SAMPLE = 20


def _hit_factor(hit_rate):
    """Formule UNIQUE du facteur de calibration : 0,50 + 0,40 × hit rate —
    borné [0,50, 0,90] par construction, jamais 1,0."""
    return round(0.5 + 0.4 * hit_rate, 3)


def calibration_factor(memory, engine_version):
    """Facteur `calibration` de la confiance depuis les résultats MESURÉS de la
    mémoire — pour CETTE version de moteur UNIQUEMENT (jamais mélangées).
    scenario hit rate = part des décisions mesurées dont le résultat était
    contenu par les scénarios (DECISION_CORRECTE ou VARIANCE_NORMALE) au plus
    long horizon mesuré. Facteur = `_hit_factor` — jamais 1,0. Échantillon <
    MIN_CALIBRATION_SAMPLE → 0,50 avec raison « échantillon insuffisant » :
    un facteur ne s'invente pas sur 3 mesures."""
    rows = _measured_hits(memory, engine_version)
    n = len(rows)
    if n < MIN_CALIBRATION_SAMPLE:
        return {'value': 0.5, 'n_measured': n, 'hit_rate': None,
                'engine_version': engine_version,
                'basis': 'échantillon insuffisant (%d/%d mesure(s) pour le moteur %s) — '
                         'facteur plafonné à 0,50, jamais inventé'
                         % (n, MIN_CALIBRATION_SAMPLE, engine_version)}
    hits = sum(1 for *_, h in rows if h)
    hit_rate = hits / n
    return {'value': _hit_factor(hit_rate),
            'n_measured': n, 'hit_rate': round(hit_rate, 3),
            'engine_version': engine_version,
            'basis': 'scenario hit rate %d/%d = %.0f %% pour le moteur %s — '
                     'facteur 0,50 + 0,40 × hit rate, borné [0,50, 0,90]'
                     % (hits, n, hit_rate * 100, engine_version)}


# ─── Calibration par contexte (LOT 22 — SCENARIO_CALIBRATION §13) ───────────────

def _measured_records(memory, engine_version):
    """[(record, hit)] pour chaque décision MESURÉE de cette version — jamais
    de mélange de versions ; entrées non-dict (magasin corrompu) ignorées."""
    mem = memory if isinstance(memory, dict) else empty_memory()
    out = []
    for r in mem.get('decisions') or []:
        if not isinstance(r, dict):        # magasin corrompu → entrée ignorée
            continue
        if r.get('engine_version') != engine_version:
            continue
        cls = _measured_class(mem, r)
        if cls is None:
            continue
        out.append((r, cls in ('DECISION_CORRECTE', 'VARIANCE_NORMALE')))
    return out


def _measured_hits(memory, engine_version):
    """(niveau, décision, régime, catalyseur?, kind, hit) pour chaque décision
    MESURÉE de cette version — régime et kind sont ceux FIGÉS au moment de la
    décision (None honnête pour les anciens records)."""
    return [(r.get('level'), r.get('decision'), r.get('regime'),
             bool(r.get('catalyst')), r.get('catalyst_kind'), hit)
            for r, hit in _measured_records(memory, engine_version)]


CONTEXT_GROUPS = ('by_level', 'by_decision', 'by_regime',
                  'by_catalyst', 'by_catalyst_type',
                  'by_option_universe', 'by_option_dte_bucket', 'by_holding_plan')


def _cell_key(group, r):
    """Clé de cellule d'un record pour un groupe de contexte — None si le
    record n'appartient à aucune cellule du groupe. SOURCE UNIQUE de la règle
    d'appartenance, consommée par `calibration_by_context` ET
    `cell_decisions` (anti-divergence) ; contexte non-chaîne (magasin
    corrompu) ≠ cellule, kind absent/non-chaîne → `inconnu`."""
    if group == 'by_level':
        v = r.get('level')
        return v if isinstance(v, str) and v else None
    if group == 'by_decision':
        v = r.get('decision')
        return v if isinstance(v, str) and v else None
    if group == 'by_regime':
        v = r.get('regime')
        return v if isinstance(v, str) and v else None
    if group == 'by_catalyst':
        return 'avec_catalyseur' if r.get('catalyst') else 'sans_catalyseur'
    if group == 'by_catalyst_type':
        if not r.get('catalyst'):
            return None
        k = r.get('catalyst_kind')
        return k if isinstance(k, str) and k else 'inconnu'
    option = r.get('option') or {}
    if group == 'by_option_universe':
        v = option.get('universe')
        return v if option.get('available') and isinstance(v, str) and v else None
    if group == 'by_option_dte_bucket':
        v = option.get('dte_bucket')
        return v if option.get('available') and isinstance(v, str) and v else None
    if group == 'by_holding_plan':
        values = option.get('holding_plan_sessions') or []
        return '_'.join(str(int(v)) for v in values if _num(v) is not None) or None
    return None


def _context_cell(rows, label):
    n = len(rows)
    if n < MIN_CALIBRATION_SAMPLE:
        return {'status': 'INSUFFISANT', 'n_measured': n, 'hit_rate': None,
                'value': None,
                'basis': 'cellule %s : %d/%d mesure(s) — hit rate non calculé, '
                         'jamais inventé' % (label, n, MIN_CALIBRATION_SAMPLE)}
    hits = sum(1 for h in rows if h)
    hr = hits / n
    return {'status': 'MESURE', 'n_measured': n, 'hit_rate': round(hr, 3),
            'value': _hit_factor(hr),
            'basis': 'cellule %s : hit rate %d/%d = %.0f %% — facteur borné [0,50, 0,90]'
                     % (label, hits, n, hr * 100)}


def calibration_by_context(memory, engine_version):
    """Découpe la calibration par NIVEAU et par DÉCISION — chaque cellule a son
    propre hit rate SEULEMENT si son échantillon suffit ; sinon INSUFFISANT
    dit. Jamais de mélange de versions."""
    rows = _measured_records(memory, engine_version)
    # règle d'appartenance UNIQUE : `_cell_key` (partagée avec cell_decisions)
    groups = {g: {} for g in CONTEXT_GROUPS}
    for r, hit in rows:
        for g in CONTEXT_GROUPS:
            key = _cell_key(g, r)
            if key is not None:
                groups[g].setdefault(key, []).append(hit)
    labels = {'by_level': 'niveau', 'by_decision': 'décision',
              'by_regime': 'régime', 'by_catalyst': 'catalyseur',
              'by_catalyst_type': 'type_catalyseur',
              'by_option_universe': 'univers_option',
              'by_option_dte_bucket': 'bucket_dte_option',
              'by_holding_plan': 'plan_detention_sessions'}
    out = {'engine_version': engine_version, 'n_measured_total': len(rows)}
    # Les segments catalyseurs et options sont des découpes d’OBSERVATION :
    # ils décrivent à ce stade le résultat directionnel du sous-jacent, jamais
    # une calibration du P&L du contrat tant que les quotes de sortie manquent.
    for g in CONTEXT_GROUPS:
        out[g] = {k: _context_cell(v, '%s=%s' % (labels[g], k))
                  for k, v in sorted(groups[g].items())}
    out['note'] = ('calibration par contexte — une cellule sous-échantillonnée '
                   'reste INSUFFISANTE et l’agrégat global est le secours ; les '
                   'segments catalyseurs/options sont des découpes d’observation '
                   'et non une calibration de P&L contractuel')
    return out


def cell_decisions(memory, engine_version, group, key):
    """DRILL-DOWN d'une cellule de calibration : les décisions MESURÉES qui la
    composent (id, titre, séance, contextes figés, hit/miss) — MÊME règle
    d'appartenance que `calibration_by_context` (`_cell_key`, source unique).
    Groupe inconnu ou clé dégénérée → None (l'appelant dit le 404). Jamais
    de mélange de versions ; lecture seule."""
    if group not in CONTEXT_GROUPS or not isinstance(key, str) or not key:
        return None
    decisions = []
    for r, hit in _measured_records(memory, engine_version):
        if _cell_key(group, r) != key:
            continue
        decisions.append({'decision_id': r.get('decision_id'),
                          'symbol': r.get('symbol'),
                          'session_date': r.get('session_date'),
                          'level': r.get('level'), 'decision': r.get('decision'),
                          'regime': r.get('regime'),
                          'catalyst': r.get('catalyst'),
                          'catalyst_kind': r.get('catalyst_kind'),
                          'hit': hit})
    return {'group': group, 'key': key, 'engine_version': engine_version,
            'n_measured': len(decisions),
            'hits': sum(1 for x in decisions if x['hit']),
            'decisions': decisions,
            'note': 'décisions MESURÉES de la cellule — même règle '
                    'd’appartenance que calibration_by_context (source '
                    'unique), records immuables, lecture seule'}


def calibration_factor_for(memory, engine_version, level=None, regime=None):
    """Facteur de calibration à SERVIR au moteur — priorité DOCUMENTÉE :
    cellule du NIVEAU courant si mesurée → cellule du RÉGIME courant si
    mesurée → agrégat global → 0,50. Portée (`scope`) explicite. Simple par
    choix : pas de croisement niveau×régime (échantillons trop exigeants)."""
    ctx = None
    if level or regime:
        ctx = calibration_by_context(memory, engine_version)
    for key, val, kind in (('by_level', level, 'level'),
                           ('by_regime', regime, 'regime')):
        # contexte non-chaîne (entrée dégénérée) → jamais une clé de cellule
        if not val or not isinstance(val, str) or ctx is None:
            continue
        cell = (ctx.get(key) or {}).get(val)
        if cell and cell['status'] == 'MESURE':
            return {'value': cell['value'], 'hit_rate': cell['hit_rate'],
                    'n_measured': cell['n_measured'],
                    'engine_version': engine_version,
                    'scope': 'context:%s=%s' % (kind, val),
                    'basis': cell['basis'] + ' (moteur %s)' % engine_version}
    g = calibration_factor(memory, engine_version)
    g['scope'] = 'global'
    return g


def option_calibration_summary(memory, engine_version, options_context):
    """État de maturité des segments options pour une décision.

    Les cellules décrivent à ce stade des résultats directionnels du sous-jacent,
    pas un rendement de contrat. Elles ne sont donc jamais converties en
    probabilité, ni consommées par le facteur de confiance du moteur.
    """
    context = options_context or {}
    best = context.get('best') or {}
    universe = context.get('universe')
    bucket = option_dte_bucket(best.get('dte'))
    if not context.get('available') or not universe or not bucket:
        return {'available': False,
                'reason': 'contexte options ou DTE absent — calibration segmentée non évaluable',
                'scope': 'DIRECTIONAL_PROXY_ONLY'}
    cells = calibration_by_context(memory, engine_version)
    u_cell = ((cells.get('by_option_universe') or {}).get(universe) or
              {'status': 'INSUFFISANT', 'n_measured': 0})
    d_cell = ((cells.get('by_option_dte_bucket') or {}).get(bucket) or
              {'status': 'INSUFFISANT', 'n_measured': 0})
    mature = u_cell.get('status') == 'MESURE' and d_cell.get('status') == 'MESURE'
    return {
        'available': True,
        'scope': 'DIRECTIONAL_PROXY_ONLY',
        'universe': universe,
        'dte_bucket': bucket,
        'mature': mature,
        'universe_cell': u_cell,
        'dte_bucket_cell': d_cell,
        'note': ('segments observés sur le résultat directionnel du sous-jacent ; '
                 'P&L de contrat, spread de sortie et slippage non mesurés'),
    }


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


# ─── Restauration souveraine (LOT 45) ───────────────────────────────────────────

def merge_memory(current, imported):
    """RESTAURATION par REJEU APPEND-ONLY d'un ledger importé dans le ledger
    courant : chaque décision repasse par `append_decision` (un decision_id
    existant n'est JAMAIS remplacé — l'historique local gagne), chaque outcome
    par `append_outcome` (monotone : seule une mesure couvrant strictement
    plus de séances remplace). Entrées non-dict comptées, jamais fatales ;
    import dégénéré → rien d'ajouté. Retourne (merged, stats)."""
    merged = {'schema': (current or {}).get('schema', MEMORY_SCHEMA_VERSION),
              'decisions': list((current or {}).get('decisions') or []),
              'outcomes': list((current or {}).get('outcomes') or [])}
    stats = {'added_decisions': 0, 'skipped_decisions': 0,
             'added_outcomes': 0, 'skipped_outcomes': 0,
             'corrupted_entries': 0}
    imp = imported if isinstance(imported, dict) else {}
    decs = imp.get('decisions')
    outs = imp.get('outcomes')
    for r in (decs if isinstance(decs, list) else []):
        if not isinstance(r, dict):
            stats['corrupted_entries'] += 1
            continue
        before = len(merged['decisions'])
        merged = append_decision(merged, r)
        if len(merged['decisions']) > before:
            stats['added_decisions'] += 1
        else:
            stats['skipped_decisions'] += 1
    for o in (outs if isinstance(outs, list) else []):
        if not isinstance(o, dict):
            stats['corrupted_entries'] += 1
            continue
        before = merged['outcomes']
        merged = append_outcome(merged, o)
        if merged['outcomes'] != before:
            stats['added_outcomes'] += 1
        else:
            stats['skipped_outcomes'] += 1
    if not isinstance(decs, list):
        stats['corrupted_entries'] += 1 if decs not in (None, []) else 0
    if not isinstance(outs, list):
        stats['corrupted_entries'] += 1 if outs not in (None, []) else 0
    return merged, stats


# ─── Santé du ledger (LOT 35) ───────────────────────────────────────────────────

def ledger_health(memory):
    """CONTRÔLE DE COHÉRENCE du ledger multi-versions — le contrôle DIT les
    anomalies, il ne répare JAMAIS rien en silence (l'historique original
    gagne toujours) : doublons de decision_id, outcomes orphelins (sans
    décision), outcomes mesurés sous une AUTRE version que leur décision
    (mélange interdit), entrées corrompues (non-dict). Déterministe."""
    mem = memory if isinstance(memory, dict) else {}
    decs_raw = mem.get('decisions') or []
    outs_raw = mem.get('outcomes') or []
    if not isinstance(decs_raw, list):
        decs_raw = []
    if not isinstance(outs_raw, list):
        outs_raw = []
    decs = [r for r in decs_raw if isinstance(r, dict)]
    outs = [o for o in outs_raw if isinstance(o, dict)]
    corrupted = (len(decs_raw) - len(decs)) + (len(outs_raw) - len(outs))

    seen, dupes = set(), 0
    version_by_id = {}
    for r in decs:
        rid = r.get('decision_id')
        if rid in seen:
            dupes += 1
        elif rid is not None:
            seen.add(rid)
            version_by_id[rid] = r.get('engine_version')

    orphans, mismatches = 0, 0
    for o in outs:
        oid = o.get('decision_id')
        if oid not in version_by_id:
            orphans += 1
        elif o.get('engine_version') != version_by_id[oid]:
            mismatches += 1

    anomalies = dupes + orphans + mismatches + corrupted
    status = 'SAIN' if anomalies == 0 else 'ANOMALIES'
    return {'status': status,
            'duplicate_decision_ids': dupes,
            'orphan_outcomes': orphans,
            'version_mismatches': mismatches,
            'corrupted_entries': corrupted,
            'n_decisions': len(decs), 'n_outcomes': len(outs),
            'basis': ('ledger cohérent : %d décision(s), %d résultat(s), '
                      '0 anomalie' % (len(decs), len(outs))) if status == 'SAIN'
                     else ('%d anomalie(s) : %d doublon(s) d’id, %d résultat(s) '
                           'orphelin(s), %d mélange(s) de versions, %d entrée(s) '
                           'corrompue(s) — rien n’est réparé en silence, '
                           'l’historique original gagne'
                           % (anomalies, dupes, orphans, mismatches, corrupted))}


__all__ = ['freeze', 'empty_memory', 'append_decision', 'append_outcome',
           'sessions_after', 'measure', 'classify_error', 'detect_patterns',
           'aggregates', 'recommendations', 'calibration_factor',
           'calibration_by_context', 'calibration_factor_for',
           'find_decision', 'find_outcome', 'post_mortem', 'ledger_health',
           'cell_decisions', 'CONTEXT_GROUPS', 'merge_memory',
           'ERROR_CLASSES', 'MEMORY_FILE', 'MAX_DECISIONS',
           'MEMORY_SCHEMA_VERSION', 'MIN_CALIBRATION_SAMPLE']
