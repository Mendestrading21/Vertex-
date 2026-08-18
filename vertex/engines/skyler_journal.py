"""vertex/engines/skyler_journal.py — JOURNAL & CALIBRATION DES DÉCISIONS SKYLER (LOT 9).

Enregistre chaque décision canonique servie (symbole, décision, score, niveau,
prix au moment de la décision, horodatage) pour permettre la calibration EX POST :

  - résultats : rendement RÉEL depuis le prix enregistré (cote actuelle) —
    une entrée sans prix ou sans cote reste NON MESURÉE (dit, jamais estimé) ;
  - Brier : machinerie implémentée et prouvée sur données synthétiques, mais
    `available: false` tant qu'aucune PROBABILITÉ CALIBRÉE n'a été émise —
    les scénarios Skyler n'affichent volontairement aucune probabilité (lot 5),
    donc il n'y a rien à noter : l'indisponibilité est la seule réponse honnête.

Journal borné (MAX_ENTRIES), dédupliqué par (symbole, as_of, décision) — un
rechargement de page ne crée pas d'entrée. Persistance runtime via
`vertex.services.persist` (fichier gitignoré). Fonctions pures (horloge et
journal injectés). Lecture seule, aucun ordre.
"""
from __future__ import annotations

MAX_ENTRIES = 2000
JOURNAL_FILE = 'skyler_decisions.json'


def record(journal, decision, price=None, now=None):
    """Ajoute une décision au journal (liste) — dédupliqué, borné. Renvoie la liste."""
    journal = list(journal or [])
    d = decision or {}
    sym = d.get('symbol')
    as_of = d.get('as_of')
    label = d.get('decision')
    if not sym or not label:
        return journal
    for e in reversed(journal):
        if e.get('symbol') == sym:
            if e.get('as_of') == as_of and e.get('decision') == label:
                return journal              # même scan, même décision : pas de doublon
            break
    sc = d.get('score') or {}
    journal.append({
        'symbol': sym, 'decision': label, 'as_of': as_of,
        'score_total': sc.get('total'), 'level': d.get('level') or sc.get('level'),
        'capped_by_gate': d.get('capped_by_gate'),
        'price': (float(price) if isinstance(price, (int, float)) and not isinstance(price, bool) else None),
        'recorded_at': now,
    })
    return journal[-MAX_ENTRIES:]


def merge_journal(current, imported):
    """RESTAURATION par rejeu (LOT 46) : n'ajoute que les entrées ABSENTES du
    journal local, identifiées par le MÊME triple de dédup que `record` —
    (symbol, as_of, decision) — l'entrée LOCALE gagne toujours. Entrées
    non-dict ou sans symbol/decision comptées, jamais fatales. Borné
    MAX_ENTRIES. Retourne (merged, stats)."""
    cur = list(current) if isinstance(current, list) else []
    stats = {'added_entries': 0, 'skipped_entries': 0, 'corrupted_entries': 0}
    if not isinstance(imported, list):
        if imported not in (None, []):
            stats['corrupted_entries'] += 1
        return cur, stats
    seen = {(e.get('symbol'), e.get('as_of'), e.get('decision'))
            for e in cur if isinstance(e, dict)}
    out = cur
    for e in imported:
        if not isinstance(e, dict) or not e.get('symbol') or not e.get('decision'):
            stats['corrupted_entries'] += 1
            continue
        key = (e.get('symbol'), e.get('as_of'), e.get('decision'))
        if key in seen:
            stats['skipped_entries'] += 1
            continue
        out = out + [e]
        seen.add(key)
        stats['added_entries'] += 1
    return out[-MAX_ENTRIES:], stats


def brier(probs, outcomes):
    """Score de Brier = moyenne des (p − résultat)². Entrées invalides refusées."""
    if not probs or len(probs) != len(outcomes):
        raise ValueError('probabilités et résultats de longueurs différentes ou vides')
    for p in probs:
        if not isinstance(p, (int, float)) or isinstance(p, bool) or not (0.0 <= p <= 1.0):
            raise ValueError('probabilité hors [0,1] : %r' % (p,))
    for o in outcomes:
        if o not in (0, 1, True, False):
            raise ValueError('résultat binaire attendu : %r' % (o,))
    return sum((float(p) - (1.0 if o else 0.0)) ** 2 for p, o in zip(probs, outcomes)) / len(probs)


def calibration(journal, quotes=None):
    """État de calibration : comptages exacts + résultats ex post RÉELS.
    Brier indisponible tant qu'aucune probabilité calibrée n'existe."""
    journal = journal or []
    quotes = quotes or {}
    by_decision, by_level = {}, {}
    rows, unmeasured = [], 0
    outcome_coverage_by_decision = {}
    for e in journal:
        decision = e.get('decision')
        by_decision[decision] = by_decision.get(decision, 0) + 1
        coverage = outcome_coverage_by_decision.setdefault(decision, {'total': 0, 'measured': 0})
        coverage['total'] += 1
        lv = e.get('level')
        if lv:
            by_level[lv] = by_level.get(lv, 0) + 1
        px0 = e.get('price')
        px1 = quotes.get(e.get('symbol'))
        if px0 and isinstance(px1, (int, float)) and not isinstance(px1, bool) and px0 > 0:
            coverage['measured'] += 1
            rows.append({'symbol': e['symbol'], 'decision': e.get('decision'),
                         'as_of': e.get('as_of'), 'entry_price': px0,
                         'current_price': float(px1),
                         'return_pct': round((float(px1) / px0 - 1) * 100, 2)})
        else:
            unmeasured += 1
    for coverage in outcome_coverage_by_decision.values():
        coverage['unmeasured'] = coverage['total'] - coverage['measured']
        coverage['coverage_pct'] = round(100 * coverage['measured'] / coverage['total'], 1) if coverage['total'] else 0.0
    return {
        'generator': 'deterministic',
        'n_decisions': len(journal),
        'by_decision': by_decision, 'by_level': by_level,
        'outcomes': ({'available': True, 'measured': len(rows),
                      'unmeasured': unmeasured,
                      'coverage_pct': round(100 * len(rows) / len(journal), 1) if journal else 0.0,
                      'by_decision': outcome_coverage_by_decision,
                      'rows': rows,
                      'note': 'rendements réels depuis le prix enregistré à la décision — descriptif, pas un backtest'}
                     if rows else
                      {'available': False, 'measured': 0, 'unmeasured': unmeasured,
                      'coverage_pct': 0.0,
                      'by_decision': outcome_coverage_by_decision,
                      'reason': 'aucune paire prix enregistré + cote actuelle — rien de mesurable, rien d’inventé'}),
        'brier': {'available': False,
                  'reason': 'aucune probabilité calibrée émise (les scénarios n’en affichent pas — lot 5) ; '
                            'la machinerie brier() est prête et testée pour le jour où un modèle calibré existera'},
        'note': 'Calibration ex post — s’enrichit à mesure que les décisions vieillissent ; jamais un chiffre inventé.',
    }


__all__ = ['record', 'brier', 'calibration', 'MAX_ENTRIES', 'JOURNAL_FILE']
