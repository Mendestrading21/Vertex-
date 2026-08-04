"""vertex/engines/market_context.py — MARKETCONTEXT CANONIQUE (SKYLER LOT 3).

Agrège l'état marché DÉJÀ produit par le scan en un contexte typé et traçable :
chaque dimension porte {value, unit, source, as_of, status} (contrat FactValue de
SKYLER_ARCHITECTURE.md). Invariants :

  - absent ≠ 0 : une dimension non disponible est MISSING (valeur None), jamais
    remplie par une approximation non étiquetée ;
  - un contexte n'est jamais plus frais que sa donnée la plus ancienne critique
    (`freshness_floor` = as_of du scan) ;
  - deux sources qui divergent → statut CONFLICTED + entrée `conflicts` (visible,
    jamais résolu en douce) ;
  - régime classé par le moteur déterministe §24 (`vertex.market.regime_engine`),
    transition et « ce qui a changé depuis la dernière session » calculés contre
    le contexte précédent fourni par l'appelant (jamais deviné) ;
  - fonction PURE (l'horloge est injectée), JSON-sérialisable, déterministe.

Aucun calcul financier nouveau, aucun ordre — lecture seule.
"""
from __future__ import annotations

import time

from vertex.market.regime_engine import classify_regime

SCHEMA_VERSION = 1
STALE_AFTER_S = 2100          # aligné sur STALE_SCAN_SEC (constants.py)

# Dimensions du schéma cible non alimentées par une source réelle aujourd'hui —
# déclarées MISSING honnêtement (elles arrivent avec leurs sources, jamais avant).
_UNAVAILABLE = ('rates_curve', 'dollar', 'credit_spreads', 'vol_term_structure',
                'dispersion', 'liquidity', 'cross_asset')

_UNITS_UNAVAILABLE = {'rates_curve': 'bps', 'dollar': 'index', 'credit_spreads': 'bps',
                      'vol_term_structure': 'ratio', 'dispersion': 'ratio',
                      'liquidity': 'score', 'cross_asset': 'composite'}


def _fact(value, unit, source, as_of, status, **extra):
    d = {'value': value, 'unit': unit, 'source': source, 'as_of': as_of, 'status': status}
    if extra:
        d.update(extra)
    return d


def build(scan_state, prev=None, now=None, demo=False, stale_after_s=STALE_AFTER_S):
    """Construit le MarketContext depuis l'état partagé du scan (lecture seule).

    `prev` : contexte précédent (dict) pour transition + diff — None = inconnu honnête.
    `now`  : horloge injectée (tests reproductibles) ; time.time() par défaut.
    """
    scan_state = scan_state or {}
    now = time.time() if now is None else now
    market = scan_state.get('market') or {}
    mc = scan_state.get('market_ctx') or {}
    ts = scan_state.get('scan_ts')
    as_of = scan_state.get('scan_ts_h') or scan_state.get('updated')

    has_scan = isinstance(ts, (int, float)) and not isinstance(ts, bool)
    age = (now - ts) if has_scan else None
    if not has_scan:
        base_status = 'MISSING'
    elif demo:
        base_status = 'DEMO'
    elif age is not None and age > stale_after_s:
        base_status = 'STALE'
    else:
        base_status = 'LIVE'

    def dim(value, unit, source, **extra):
        st = 'MISSING' if value is None else base_status
        return _fact(value, unit, source, as_of if value is not None else None, st, **extra)

    # ── Dimensions réellement alimentées par le scan ────────────────────────────
    trend = {'TREND': 'UP', 'CHOP': 'FLAT'}.get(market.get('regime'), market.get('spy_trend'))
    breadth = market.get('breadth') if market.get('breadth') is not None else mc.get('breadth')
    leadership = ('CYCLICAL' if market.get('risk') == 'Risk-On'
                  else 'DEFENSIVE' if market.get('risk') == 'Risk-Off' else None)

    # VIX : deux sources réelles (lens marché + contexte marché) — un désaccord
    # matériel (> 1 pt) est CONFLICTED, jamais moyenné en silence.
    vix_a, vix_b = market.get('vix'), mc.get('vix')
    conflicts = []
    vix_val = vix_b if vix_b is not None else vix_a
    vix_status_override = None
    if vix_a is not None and vix_b is not None and abs(vix_a - vix_b) > 1.0:
        vix_status_override = 'CONFLICTED'
        conflicts.append({'dimension': 'vix',
                          'sources': ['scan.market', 'scan.market_ctx'],
                          'values': [vix_a, vix_b],
                          'note': 'sources VIX en désaccord — non résolu, affiché tel quel'})

    dimensions = {
        'spy_trend': dim(trend, 'trend', 'scan.market'),
        'breadth_ma200_pct': dim(breadth, '%', 'scan.breadth'),
        'vix': dim(vix_val, 'index', 'scan.market_ctx', band=mc.get('vix_band')),
        'leadership': dim(leadership, 'category', 'scan.market'),
        'roro': dim(mc.get('roro'), 'ratio', 'scan.market_ctx'),
    }
    if vix_status_override and dimensions['vix']['value'] is not None:
        dimensions['vix']['status'] = vix_status_override
    for name in _UNAVAILABLE:
        dimensions[name] = _fact(None, _UNITS_UNAVAILABLE[name], None, None, 'MISSING')

    missing = sorted(n for n, d in dimensions.items() if d['status'] == 'MISSING')

    # ── Régime (moteur déterministe §24) + transition ───────────────────────────
    reg = classify_regime({'index_trend': trend, 'breadth_pct': breadth,
                           'vix': vix_val, 'leadership': leadership})
    prev_label = ((prev or {}).get('regime') or {}).get('label')
    transition = {'from': prev_label, 'to': reg.get('regime'),
                  'changed': (None if prev_label is None else prev_label != reg.get('regime'))}
    regime = {'label': reg.get('regime'), 'confidence': reg.get('confidence'),
              'secondary': reg.get('secondary') or [],
              'dimensions_used': reg.get('dimensions_used') or [],
              'notes': reg.get('notes') or [], 'adjustments': reg.get('adjustments'),
              'transition': transition}

    # ── « Ce qui a changé depuis la dernière session » (jamais inventé) ─────────
    changes = []
    pdims = (prev or {}).get('dimensions') or {}

    def pval(name):
        return (pdims.get(name) or {}).get('value')

    if prev:
        if prev_label and prev_label != regime['label']:
            changes.append('Régime : %s → %s' % (prev_label, regime['label']))
        pv = pval('vix')
        if pv is not None and vix_val is not None and abs(vix_val - pv) >= 2.0:
            changes.append('VIX : %.1f → %.1f' % (pv, vix_val))
        pband = (pdims.get('vix') or {}).get('band')
        band = dimensions['vix'].get('band')
        if pband and band and pband != band:
            changes.append('Bande VIX : %s → %s' % (pband, band))
        pb = pval('breadth_ma200_pct')
        if pb is not None and breadth is not None and abs(breadth - pb) >= 5.0:
            changes.append('Largeur (breadth MM200) : %.0f %% → %.0f %%' % (pb, breadth))
        pl = pval('leadership')
        if pl and leadership and pl != leadership:
            changes.append('Leadership : %s → %s' % (pl, leadership))

    return {
        'schema_version': SCHEMA_VERSION,
        'generator': 'deterministic',
        'as_of': as_of if has_scan else None,
        'age_s': (round(age) if age is not None else None),
        'freshness_floor': as_of if has_scan else None,
        'demo': bool(demo),
        'dimensions': dimensions,
        'missing': missing,
        'conflicts': conflicts,
        'regime': regime,
        'changes_since_prev': changes,
        'note': 'Contexte descriptif — pas une prévision ; dimensions absentes = MISSING, jamais estimées.',
    }


__all__ = ['build', 'SCHEMA_VERSION']
