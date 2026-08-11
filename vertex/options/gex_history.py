"""vertex/options/gex_history.py — HISTORIQUE QUOTIDIEN DU GEX (par sous-jacent).

Journalise, jour après jour, le profil GEX calculé (net/call/put GEX, spot,
zero-gamma) pour tracer le « Daily Gamma Exposure » — le gamma s'empile-t-il ?
Une entrée par jour et par symbole (last-writer-wins sur la même date), bornée
à 120 jours. Stockage runtime `gex_history_cache.json` (gitignoré via *_cache.json).

HONNÊTETÉ : on n'enregistre QUE des profils réels non vides (jamais de point
inventé) ; un jour sans donnée = pas de point (trou honnête dans la série).
Lecture seule, aucun ordre.
"""
from __future__ import annotations

import time

from vertex.services import persist

_FILE = 'gex_history_cache.json'
_MAX_DAYS = 120
_MAX_SYMBOLS = 80          # borne anti-croissance (les plus récents gagnent)


def _today():
    return time.strftime('%Y-%m-%d', time.gmtime())


def record(profile):
    """Journalise le profil GEX du jour (sortie de gex.compute). Best-effort :
    n'enregistre rien si le profil est vide/incomplet. Retourne True si écrit."""
    if not isinstance(profile, dict) or profile.get('empty') or not profile.get('symbol'):
        return False
    net = profile.get('net_gex_total')
    if not isinstance(net, (int, float)) or isinstance(net, bool):
        return False
    sym = str(profile['symbol']).upper()
    entry = {
        'date': _today(),
        'net_gex': round(net),
        'call_gex': round(profile.get('call_gex_total') or 0),
        'put_gex': round(profile.get('put_gex_total') or 0),
        'spot': profile.get('spot'),
        'zero_gamma': profile.get('zero_gamma'),
    }
    data = persist.load_json(_FILE, {})
    if not isinstance(data, dict):
        data = {}
    series = [e for e in (data.get(sym) or []) if isinstance(e, dict)
              and e.get('date') != entry['date']]           # last-writer-wins sur le jour
    series.append(entry)
    series.sort(key=lambda e: e.get('date') or '')
    data[sym] = series[-_MAX_DAYS:]
    if len(data) > _MAX_SYMBOLS:                            # évince les symboles les plus anciens
        keyed = sorted(data.items(), key=lambda kv: (kv[1][-1].get('date') if kv[1] else ''))
        for k, _ in keyed[:len(data) - _MAX_SYMBOLS]:
            data.pop(k, None)
    persist.save_json(_FILE, data)
    return True


def series(symbol):
    """Série quotidienne d'un symbole : [{date, net_gex, call_gex, put_gex, spot, zero_gamma}]."""
    sym = str(symbol or '').upper()
    data = persist.load_json(_FILE, {})
    out = (data.get(sym) or []) if isinstance(data, dict) else []
    return [e for e in out if isinstance(e, dict) and e.get('date')]


__all__ = ['record', 'series']
