"""vertex/engines/session_log.py — LOG DE SÉANCES DATÉES (LOT 15).

Accumule UNE clôture par symbole et par jour de scan RÉEL — la date est la
date d'observation effective (horloge réelle du serveur au moment du scan),
jamais inventée ni interpolée. Le log donne aux horizons de la mémoire
décisionnelle (lot 10) un comptage de SÉANCES réel : les clôtures aux dates
strictement postérieures à la date de la décision.

Règles :
  - même date = même séance : la dernière observation du jour raffine la
    clôture (le scan de fin de journée est le plus proche du vrai close) ;
  - dates triées, bornées (MAX_SESSIONS par symbole) ;
  - valeurs non finies et dates malformées refusées ;
  - fonctions PURES (le log est passé/retourné, jamais muté en place) ;
  - persistance runtime `skyler_sessions.json` (gitignorée) — aucun jour sans
    scan n'est comblé : un trou dans le log reste un trou.

Lecture seule, aucun ordre.
"""
from __future__ import annotations

import math

SESSIONS_FILE = 'skyler_sessions.json'
MAX_SESSIONS = 400               # ~19 mois de séances par symbole
SCHEMA = 1


def _valid_date(d):
    if not isinstance(d, str) or len(d) != 10 or d[4] != '-' or d[7] != '-':
        return False
    y, m, dd = d[:4], d[5:7], d[8:10]
    return y.isdigit() and m.isdigit() and dd.isdigit()


def _num(x):
    if isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x):
        return float(x)
    return None


def empty_log():
    return {'schema': SCHEMA, 'symbols': {}}


def record_close(log, sym, date, close):
    """Enregistre la clôture observée d'une séance — dédupliqué par date (la
    dernière observation du jour gagne), trié, borné. Entrée invalide →
    log inchangé, jamais devinée."""
    sym = str(sym or '').upper()
    px = _num(close)
    if not sym or px is None or px <= 0 or not _valid_date(date):
        return log if log is not None else empty_log()
    out = {'schema': (log or {}).get('schema', SCHEMA),
           'symbols': {k: list(v) for k, v in ((log or {}).get('symbols') or {}).items()}}
    rows = [e for e in out['symbols'].get(sym, []) if e.get('date') != date]
    rows.append({'date': date, 'close': px})
    rows.sort(key=lambda e: e['date'])
    out['symbols'][sym] = rows[-MAX_SESSIONS:]
    return out


def closes_after_date(log, sym, date):
    """Clôtures des séances STRICTEMENT postérieures à la date de décision.
    Titre non suivi ou date absente → None (non mesurable, jamais deviné)."""
    if not log or not _valid_date(date):
        return None
    rows = ((log.get('symbols') or {}).get(str(sym or '').upper()))
    if rows is None:
        return None
    return [e['close'] for e in rows if e.get('date') and e['date'] > date]


def merge_log(current, imported):
    """RESTAURATION par rejeu (LOT 46) : n'ajoute que les séances (symbole,
    date) ABSENTES du log local — la clôture LOCALE gagne toujours (le scan
    local est l'observation de référence, jamais remplacée par une archive).
    Entrées invalides (date malformée, clôture non finie ou ≤ 0, non-dict,
    liste manquante) comptées, jamais fatales. Retourne (merged, stats)."""
    cur = current if isinstance(current, dict) else empty_log()
    out = {'schema': cur.get('schema', SCHEMA),
           'symbols': {k: list(v) for k, v in (cur.get('symbols') or {}).items()}}
    stats = {'added_sessions': 0, 'skipped_sessions': 0, 'corrupted_entries': 0}
    imp = imported if isinstance(imported, dict) else {}
    symbols = imp.get('symbols')
    if not isinstance(symbols, dict):
        if symbols not in (None, {}):
            stats['corrupted_entries'] += 1
        return out, stats
    for sym, rows in sorted(symbols.items()):
        s = str(sym or '').upper()
        if not s or not isinstance(rows, list):
            stats['corrupted_entries'] += 1
            continue
        existing = {e.get('date') for e in out['symbols'].get(s, [])
                    if isinstance(e, dict)}
        for e in rows:
            if not isinstance(e, dict):
                stats['corrupted_entries'] += 1
                continue
            date, px = e.get('date'), _num(e.get('close'))
            if not _valid_date(date) or px is None or px <= 0:
                stats['corrupted_entries'] += 1
                continue
            if date in existing:
                stats['skipped_sessions'] += 1
                continue
            out = record_close(out, s, date, px)
            existing.add(date)
            stats['added_sessions'] += 1
    return out, stats


__all__ = ['empty_log', 'record_close', 'closes_after_date', 'merge_log',
           'SESSIONS_FILE', 'MAX_SESSIONS']
