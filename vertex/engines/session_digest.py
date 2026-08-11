"""
vertex/engines/session_digest.py — SESSION D'ANALYSE (digest de commandement).

Assemble un instantané compact de la « session d'analyse ouverte » à partir de
l'état DÉJÀ calculé par le scan de fond (`scan_state`) et le calendrier
(`cal_state`). AUCUN nouveau calcul financier, AUCUN verdict recalculé : ce module
ne fait que LIRE et agréger ce que les moteurs ont produit — régime, opportunités
actionnables, catalyseurs imminents, pouls marché, confiance des données.

Invariants :
- Lecture seule, aucun ordre (comme tout le métier VERTEX).
- Donnée absente → valeur honnête `None` / `n/d` (jamais inventée).
- Fonction pure (pas de Flask) → testable et réutilisable.

État de session :
  'analyzing' — le scan tourne, rien encore de publié (démarrage à froid).
  'ready'     — analyse disponible et fraîche.
  'restored'  — servi depuis l'instantané disque (posé par la route) le temps que
                le scan republie ; l'UI l'indique honnêtement.
"""
from __future__ import annotations

import time

try:
    from vertex.engines import market_lens
except Exception:                                    # pragma: no cover - garde-fou import
    market_lens = None


def _market_score(mc):
    """Score marché /100 via l'unique source market_lens.climate — jamais réinventé."""
    if not mc or market_lens is None:
        return None
    try:
        cl = market_lens.climate(mc)
        return cl['score'] if cl else None
    except Exception:
        return None


def _regime(mc, has_data):
    """Régime lisible dérivé du market_ctx (mêmes règles que /api/command)."""
    roro = mc.get('roro')
    spy = mc.get('spy_regime')
    if roro == 'RISK-OFF':
        label, tone = 'RISK-OFF', 'risk'
    elif roro == 'RISK-ON' and spy != 'CHOP':
        label, tone = 'RISK-ON', 'go'
    elif has_data:
        label, tone = 'NEUTRE', 'wait'
    else:
        label, tone = None, 'idle'
    return {'label': label, 'tone': tone, 'roro': roro, 'spy_regime': spy,
            'score': _market_score(mc)}


def build(scan_state, cal_state=None, demo=False):
    """Construit le digest de la session d'analyse depuis l'état partagé.

    N'exécute aucun moteur : lit `scan_state` (régime, comité, rows, detail) et
    `cal_state` (catalyseurs) tels qu'ils ont été remplis par la boucle de fond.
    """
    scan_state = scan_state or {}
    mc = scan_state.get('market_ctx') or {}
    cm = scan_state.get('committee') or {}
    rows = scan_state.get('rows') or []
    detail = scan_state.get('detail') or {}
    ts = scan_state.get('scan_ts')
    as_of = scan_state.get('scan_ts_h') or scan_state.get('updated')

    has_data = bool(rows) or bool(mc)

    # Opportunités actionnables : MÊME critère que le Command Center (verdict comité).
    decisions = cm.get('decisions') or []
    actionable = [d.get('symbol') for d in decisions
                  if isinstance(d, dict) and d.get('verdict') in ('ACHETER', 'RENFORCER') and d.get('symbol')]

    # Catalyseurs imminents : depuis le calendrier moteur (dte croissant), jamais inventés.
    # dte NON numérique ignoré (un seul dte texte ne doit PAS masquer tous les catalyseurs).
    items = ((cal_state or {}).get('items')) or []
    dated = [c for c in items if isinstance(c, dict) and isinstance(c.get('dte'), (int, float))
             and not isinstance(c.get('dte'), bool)]
    dated.sort(key=lambda c: c['dte'])
    nxt = dated[0] if dated else None

    # Confiance données : couverture réelle (titres scannés ayant un détail moteur).
    covered = sum(1 for r in rows if isinstance(r, dict) and r.get('symbol') in detail) if rows else 0
    confidence = round(100 * covered / len(rows)) if rows else None

    return {
        'state': 'ready' if has_data else 'analyzing',
        'as_of': as_of,
        'age_s': (round(time.time() - ts) if isinstance(ts, (int, float)) and not isinstance(ts, bool) else None),
        'demo': bool(demo),
        'generator': 'deterministic',
        'regime': _regime(mc, has_data),
        'opportunities': {
            'actionable': len(actionable),
            'universe': len(rows),
            'top': actionable[:3],
        },
        'catalysts': {
            'count': len(dated),
            'next': ({'label': nxt.get('label'), 'dte': nxt.get('dte')} if nxt else None),
        },
        'market': {
            'vix': mc.get('vix'),
            'vix_band': mc.get('vix_band'),
            'breadth': mc.get('breadth'),
        },
        'confidence': confidence,
    }


__all__ = ['build']
