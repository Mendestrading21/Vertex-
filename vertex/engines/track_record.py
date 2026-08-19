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


def _fwd(closes, dates, jour_iso, horizon):
    """Rendement % entre la séance `jour_iso` (AAAA-MM-JJ) et +horizon séances.

    Rend `(None, i)` si l'horizon **n'est pas encore échu** : c'est la garde
    anti-look-ahead. Une entrée dont les +20 séances n'ont pas eu lieu ne doit
    pas être notée, sinon la fiabilité affichée serait celle des seuls verdicts
    assez vieux pour avoir eu raison.

    ── LE DÉFAUT CORRIGÉ ICI (#783/G3) ────────────────────────────────────────
    Cette fonction cherchait un libellé `'%m-%d'` dans `series['dates']`, qui
    contient des dates **ISO** (`'2026-05-15'`). `'05-15' in ['2026-05-15', …]`
    est toujours faux : `.index()` levait `ValueError` sur CHAQUE entrée, et
    `evaluate()` rendait `resolved: 0` quoi qu'il arrive. Le moteur ne se notait
    pas — et l'écran attribuait ce vide à un manque d'historique.

    Mesuré : 8 entrées dont +1, +5 et +20 étaient tous échus → **0 résolue**.

    La comparaison se fait désormais en ISO, ce qui supprime au passage
    l'ambiguïté d'année que l'ancienne recherche de « dernière occurrence »
    tentait de contourner : `series['date_labels']` existe précisément parce que
    `analysis.py` sépare les deux formats « afin de ne jamais réinterpréter les
    années ». Le registre porte un horodatage complet ; l'année est connue.
    """
    try:
        i = dates.index(jour_iso)
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
    #  ── POURQUOI UNE ENTRÉE N'EST PAS NOTÉE ───────────────────────────────
    #  Sans ce détail, `resolved: 0` se lit « pas encore assez d'historique »
    #  alors que la cause peut être toute autre — c'est exactement ce qui est
    #  arrivé : une jointure de dates cassée rendait 0 quoi qu'il arrive, et
    #  l'écran invitait l'utilisateur à patienter pour une condition qui ne
    #  pouvait jamais se résoudre.
    ignores = {'sans_serie': 0, 'date_absente': 0, 'horizon_non_echu': 0}

    def bucket(key):
        return groups.setdefault(key, {'n': 0, 'f1': [], 'f5': [], 'f20': [], 'tp': [0, 0]})

    days = set()
    for e in entries:
        sym = e.get('ticker')
        d = detail.get(sym) or {}
        s = d.get('series') or {}
        closes, dates = s.get('close') or [], s.get('dates') or []
        if not closes or not dates:
            #  Le titre n'est plus dans le scan du jour : aucune série pour le
            #  noter. Voir la note servie — la fiabilité ne porte que sur les
            #  titres encore suivis.
            ignores['sans_serie'] += 1
            continue
        jour = datetime.fromtimestamp(e.get('ts', 0)).strftime('%Y-%m-%d')
        days.add(jour)
        f1, i = _fwd(closes, dates, jour, 1)
        f5, _ = _fwd(closes, dates, jour, 5)
        f20, _ = _fwd(closes, dates, jour, 20)
        if f1 is None and f5 is None and f20 is None:
            #  `i is None` = la séance de la décision est introuvable dans la
            #  série ; sinon, aucun horizon n'est encore échu — refus délibéré
            #  de noter, c'est la garde anti-look-ahead.
            ignores['date_absente' if i is None else 'horizon_non_echu'] += 1
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
           'ignores': ignores,
           'note': ('rendements sur CLÔTURES quotidiennes (pas d\'intraday) · '
                    'TP1-avant-stop approximé sur clôtures · fenêtre séries '
                    '~120 séances · ne note QUE les titres encore suivis par le '
                    'scan du jour : un verdict sur un titre sorti de l\'univers '
                    'n\'est jamais compté, la fiabilité porte donc sur les '
                    'survivants'),
           'by_verdict': {k[1]: agg(b) for k, b in groups.items() if k[0] == 'verdict' and b['n'] >= 5},
           'by_grade': {k[1]: agg(b) for k, b in groups.items() if k[0] == 'grade' and b['n'] >= 5},
           'by_regime': {k[1]: agg(b) for k, b in groups.items() if k[0] == 'regime' and b['n'] >= 5},
           'as_of': datetime.now().strftime('%H:%M %d/%m')}
    _MEMO['ts'] = now
    _MEMO['data'] = out
    return out


__all__ = ['record', 'evaluate', 'LEDGER']
