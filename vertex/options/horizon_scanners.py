"""vertex/options/horizon_scanners.py — SCANNERS PAR UNIVERS (SKYLER LOT 6).

Sépare STRICTEMENT les horizons du mandat V2 :

  TACTICAL [20, 60) · SWING [60, 180) · LEAPS [180, 540]

Jamais une échéance ~35 DTE pour une requête LEAPS (OPTIONS_CORRECTNESS).
Analyse les CALLS et PUTS LONGS uniquement (le profil V1/V2 interdit la vente).
Le mandat LEAPS (delta 0,70-0,90, OI ≥ min, spread ≤ max) est évalué par
candidat et AFFICHÉ (`mandate`, `hors_mandat`) — jamais filtré en silence :
un contrat hors mandat reste visible, étiqueté, jamais recommandé en amont.

Fonctions pures, données du board réel uniquement. Lecture seule, aucun ordre.
"""
from __future__ import annotations

from vertex.options import iv_units

_FALLBACK_UNIVERSES = {'TACTICAL': [20, 60], 'SWING': [60, 180], 'LEAPS': [180, 540]}


def _universes(profile=None):
    try:
        if profile is None:
            from vertex.strategy.constitution import load_profile
            profile = load_profile()
        u = (profile.options_profile or {}).get('universes') or {}
        return {k: list(v) for k, v in u.items() if isinstance(v, (list, tuple)) and len(v) == 2}, profile
    except Exception:
        return dict(_FALLBACK_UNIVERSES), None


def _in_window(dte, universe, win):
    lo, hi = win
    if universe == 'LEAPS':
        return lo <= dte <= hi          # borne haute incluse (mandat 180-540)
    return lo <= dte < hi               # [lo, hi) — la borne haute appartient à l'univers suivant


def scan(board, universe, sym=None, profile=None):
    """Candidats LONGS d'un univers d'horizon. Refus structuré si univers inconnu ;
    vide honnête si aucun contrat dans la fenêtre."""
    universes, prof = _universes(profile)
    universe = (universe or '').upper()
    if universe not in universes:
        return {'available': False, 'universe': universe, 'candidates': [],
                'reason': 'univers inconnu : %r (attendu %s)' % (universe, sorted(universes))}
    win = universes[universe]

    leaps_cat = {}
    if prof is not None:
        try:
            leaps_cat = prof.category('LEAPS') or {}
        except Exception:
            leaps_cat = {}
    d_min = leaps_cat.get('delta_min', 0.70)
    d_max = leaps_cat.get('delta_max', 0.90)
    oi_min = leaps_cat.get('open_interest_min', 500)
    spread_max = leaps_cat.get('spread_pct_max', 5.0)

    out = []
    for c in (board or []):
        if not isinstance(c, dict):
            continue
        if sym and str(c.get('sym', '')).upper() != str(sym).upper():
            continue
        typ = str(c.get('type', '')).upper()
        if typ not in ('CALL', 'PUT'):
            continue
        dte = c.get('dte')
        if not isinstance(dte, (int, float)) or not _in_window(dte, universe, win):
            continue
        iv_dec, iv_unit, iv_warn = iv_units.from_legacy_board(c.get('iv'))
        delta = c.get('delta')
        cand = {
            'sym': c.get('sym'), 'type': typ, 'strike': c.get('strike'),
            'exp': c.get('exp'), 'dte': dte, 'delta': delta,
            'iv': iv_dec, 'iv_unit': ('DECIMAL' if iv_dec is not None else None),
            'oi': c.get('oi'), 'spread_pct': c.get('spread_pct'),
            'cost': c.get('cost'), 'spot': c.get('spot'),
            'quality': c.get('quality'), 'warnings': [w for w in [iv_warn] if w],
        }
        if universe == 'LEAPS':
            delta_ok = (None if delta is None else bool(d_min <= abs(delta) <= d_max))
            oi_ok = (None if c.get('oi') is None else bool(c['oi'] >= oi_min))
            spread_ok = (None if c.get('spread_pct') is None
                         else bool(c['spread_pct'] <= spread_max))
            cand['mandate'] = {'delta_ok': delta_ok, 'oi_ok': oi_ok, 'spread_ok': spread_ok,
                               'bounds': {'delta': [d_min, d_max], 'oi_min': oi_min,
                                          'spread_pct_max': spread_max}}
            cand['hors_mandat'] = any(v is False for v in
                                      (delta_ok, oi_ok, spread_ok))
        else:
            cand['mandate'] = None
            cand['hors_mandat'] = False
        out.append(cand)

    # Conformes au mandat d'abord, puis qualité décroissante — tri stable/déterministe.
    out.sort(key=lambda x: (x['hors_mandat'], -(x.get('quality') or 0)))
    return {
        'available': bool(out), 'universe': universe, 'window': win,
        'n': len(out), 'candidates': out, 'generator': 'deterministic',
        'note': 'Univers strictement séparés — jamais une échéance courte pour une requête LEAPS ; '
                'hors-mandat étiqueté, jamais filtré en silence.',
        'reason': None if out else 'aucun contrat %s dans la fenêtre %s pour ce filtre' % (universe, win),
    }


def options_context(scan_result):
    """OptionsContext minimal pour le SkylerPacket : disponible + meilleur candidat
    + drapeaux de mandat. Jamais construit sans scan réel."""
    if not scan_result or not scan_result.get('available'):
        return {'available': False,
                'reason': (scan_result or {}).get('reason') or 'scan options indisponible'}
    best = scan_result['candidates'][0]
    return {'available': True, 'universe': scan_result['universe'],
            'window': scan_result['window'], 'n': scan_result['n'],
            'best': best, 'best_in_mandate': not best['hors_mandat'],
            'generator': 'deterministic'}


__all__ = ['scan', 'options_context']
