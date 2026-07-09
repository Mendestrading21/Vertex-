"""
vertex/engines/track_record.py — LE MOTEUR SE NOTE LUI-MÊME (Ch. auto-évaluation).

Vertex émet des verdicts chaque jour ; ce module mesure s'ils sont BONS.
1. `record(state)`  — snapshot quotidien de chaque verdict scanné → verdict
   ledger (JSONL, append-only). Reprend le format historique d'edge_ledger.jsonl
   (723 entrées existantes = graine d'historique).
2. `evaluate(state)` — relit le ledger, joint chaque entrée aux SÉRIES DE PRIX
   RÉELLES du scan (series.close/dates) et calcule les rendements à +5/+20
   séances, le taux de réussite et le hit TP1-avant-stop (approximation sur
   clôtures — honnêtement étiquetée), agrégés par verdict / grade / régime.

Aucune promesse, que du mesuré. Analyse only.
"""

import json
import os
import time
from datetime import datetime

from vertex.services import persist

LEDGER = 'edge_ledger.jsonl'
META = 'track_meta.json'
_MEMO = {'ts': 0.0, 'data': None}


def _ledger_path():
    return persist.cache_path(LEDGER)


def record(state):
    """Ajoute le snapshot du jour (1×/jour calendaire) : un verdict par titre scanné.
    Idempotent — re-appeler dans la journée ne double rien."""
    rows = state.get('rows') or []
    detail = state.get('detail') or {}
    if not rows:
        return 0
    today = datetime.now().strftime('%Y-%m-%d')
    meta = persist.load_json(META, {}) or {}
    if meta.get('last_day') == today:
        return 0
    mctx = state.get('market_ctx') or {}
    n = 0
    try:
        with open(_ledger_path(), 'a', encoding='utf-8') as f:
            for r in rows:
                sym = r.get('symbol')
                d = detail.get(sym) or {}
                if not sym or d.get('price') is None:
                    continue
                plan = d.get('plan') or {}
                rec = {'ts': time.time(), 'ticker': sym, 'price': d.get('price'),
                       'decision': d.get('verdict'), 'score': d.get('score'),
                       'entry': plan.get('entry'), 'stop': plan.get('stop'),
                       'targets': {'tp1': plan.get('tp1'), 'tp2': plan.get('tp2')},
                       'market_regime': mctx.get('spy_regime'), 'sector_regime': mctx.get('roro'),
                       'features': {'grade': d.get('grade'), 'rs': d.get('rs'),
                                    'setup_quality': d.get('setup_quality')},
                       'outcome': None}
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                n += 1
    except Exception:
        return 0
    persist.save_json(META, {'last_day': today, 'last_n': n})
    return n


def _load_ledger(max_lines=20000):
    out = []
    try:
        with open(_ledger_path(), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except Exception:
                        continue
    except Exception:
        pass
    return out[-max_lines:]


def _fwd(closes, dates, day, horizon):
    """Rendement % entre la séance `day` (MM-DD) et +horizon séances. None si trop récent."""
    try:
        i = len(dates) - 1 - dates[::-1].index(day)   # dernière occurrence (bord d'année)
    except ValueError:
        return None, None
    j = i + horizon
    if j >= len(closes) or not closes[i]:
        return None, i
    return (closes[j] / closes[i] - 1) * 100, i


def _hit_tp1(closes, i, entry, tp1, stop, max_h=20):
    """TP1 touché avant le stop dans les `max_h` séances (sur CLÔTURES — approximation)."""
    if not (entry and tp1 and stop) or i is None:
        return None
    for c in closes[i + 1:i + 1 + max_h]:
        if c >= tp1:
            return True
        if c <= stop:
            return False
    return None                                       # ni l'un ni l'autre → non résolu


def evaluate(state, max_age=1800):
    """Statistiques de fiabilité du moteur, agrégées et honnêtes. Mémoïsé 30 min."""
    now = time.time()
    if _MEMO['data'] is not None and now - _MEMO['ts'] < max_age:
        return _MEMO['data']
    detail = state.get('detail') or {}
    entries = _load_ledger()

    resolved, groups = 0, {}

    def bucket(key):
        return groups.setdefault(key, {'n': 0, 'f1': [], 'f5': [], 'f20': [], 'tp': [0, 0]})

    days = set()
    for e in entries:
        sym = e.get('ticker')
        d = detail.get(sym) or {}
        s = d.get('series') or {}
        closes, dates = s.get('close') or [], s.get('dates') or []
        if not closes or not dates:
            continue
        day = datetime.fromtimestamp(e.get('ts', 0)).strftime('%m-%d')
        days.add(day)
        f1, i = _fwd(closes, dates, day, 1)
        f5, _ = _fwd(closes, dates, day, 5)
        f20, _ = _fwd(closes, dates, day, 20)
        if f1 is None and f5 is None and f20 is None:
            continue
        resolved += 1
        tp = _hit_tp1(closes, i, e.get('entry'),
                      (e.get('targets') or {}).get('tp1'), e.get('stop'))
        gr = (e.get('features') or {}).get('grade') or '—'
        for key in (('verdict', str(e.get('decision') or '—')),
                    ('grade', str(gr)),
                    ('regime', str(e.get('market_regime') or '—'))):
            b = bucket(key)
            b['n'] += 1
            if f1 is not None:
                b['f1'].append(f1)
            if f5 is not None:
                b['f5'].append(f5)
            if f20 is not None:
                b['f20'].append(f20)
            if tp is True:
                b['tp'][0] += 1
                b['tp'][1] += 1
            elif tp is False:
                b['tp'][1] += 1

    def agg(b):
        def avg(a):
            return round(sum(a) / len(a), 2) if a else None

        def win(a):
            return round(100 * sum(1 for x in a if x > 0) / len(a)) if a else None
        return {'n': b['n'], 'avg_1j': avg(b['f1']), 'avg_5j': avg(b['f5']), 'avg_20j': avg(b['f20']),
                'win_1j': win(b['f1']), 'win_5j': win(b['f5']), 'win_20j': win(b['f20']),
                'tp1_rate': (round(100 * b['tp'][0] / b['tp'][1]) if b['tp'][1] else None),
                'tp1_resolved': b['tp'][1]}

    out = {'entries': len(entries), 'resolved': resolved, 'days': len(days),
           'note': ('rendements sur CLÔTURES quotidiennes (pas d\'intraday) · '
                    'TP1-avant-stop approximé sur clôtures · fenêtre séries ~120 séances'),
           'by_verdict': {k[1]: agg(b) for k, b in groups.items() if k[0] == 'verdict' and b['n'] >= 5},
           'by_grade': {k[1]: agg(b) for k, b in groups.items() if k[0] == 'grade' and b['n'] >= 5},
           'by_regime': {k[1]: agg(b) for k, b in groups.items() if k[0] == 'regime' and b['n'] >= 5},
           'as_of': datetime.now().strftime('%H:%M %d/%m')}
    _MEMO['ts'] = now
    _MEMO['data'] = out
    return out


__all__ = ['record', 'evaluate', 'LEDGER']
