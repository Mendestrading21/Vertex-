"""vertex.tracking.repository — persistance des suivis (§14-16).

Stockage JSON (`tracking.json`) via le service persist. CRUD + abonnement,
snapshots, arrêt (gèle le résultat final, conserve l'historique), réactivation
(nouvel identifiant, ne modifie pas l'ancien). Lecture seule côté marché ;
aucun ordre. Tous les identifiants/horodatages sont fournis par l'appelant
(déterminisme + testabilité — pas d'horloge cachée).
"""
from __future__ import annotations

from vertex.services import persist
from . import models
from .reference_price import pick_stock_reference, pick_option_reference

_STORE = 'tracking.json'


def _load():
    blob = persist.load_json(_STORE, {'trackings': []}) or {'trackings': []}
    if 'trackings' not in blob:
        blob['trackings'] = []
    return blob


def _save(blob):
    persist.save_json(_STORE, blob)


def list_all(*, status=None):
    items = _load()['trackings']
    if status:
        items = [t for t in items if t.get('status') == status]
    return items


def get(tracking_id):
    return next((t for t in _load()['trackings']
                 if t.get('tracking_id') == tracking_id), None)


def create(*, tracking_id, entity_type, symbol, quote, started_at,
           market_open=True, benchmark_quote=None, decision='', score=None,
           contract_id=None, thesis_snapshot_id=None):
    """Crée un suivi horodaté avec un prix de référence honnête.

    Récupère la meilleure référence disponible ; si aucune → statut
    DATA_REQUIRED (jamais un prix inventé). N'écrase jamais un suivi existant."""
    is_opt = entity_type == 'OPTION'
    if is_opt:
        price, rtype, rsrc, status, warns = pick_option_reference(quote)
    else:
        price, rtype, rsrc, status, warns = pick_stock_reference(quote, market_open=market_open)
    bench_ref = None
    if benchmark_quote is not None:
        bp, _, _, _, _ = pick_stock_reference(benchmark_quote, market_open=market_open)
        bench_ref = bp
    t = models.new_tracking(
        tracking_id, entity_type=entity_type, symbol=symbol, started_at=started_at,
        reference_price=price, reference_price_type=rtype,
        reference_price_source=rsrc, reference_price_timestamp=started_at,
        contract_id=contract_id, strategy_decision_at_start=decision,
        strategy_score_at_start=score, thesis_snapshot_id=thesis_snapshot_id,
        data_quality={'warnings': warns}, status=status)
    t['benchmark_reference_price'] = bench_ref
    blob = _load()
    blob['trackings'].append(t)
    _save(blob)
    return t


def add_snapshot(tracking_id, *, price, at, benchmark_price=None):
    """Ajoute un snapshot horodaté et met à jour high/low. No-op si arrêté."""
    blob = _load()
    t = next((x for x in blob['trackings'] if x.get('tracking_id') == tracking_id), None)
    if not t or t.get('status') != models.ST_ACTIVE:
        return t
    if price is not None:
        t['snapshots'].append({'price': price, 'at': at, 'benchmark_price': benchmark_price})
        hi, lo = t.get('high_since'), t.get('low_since')
        t['high_since'] = price if hi is None else max(hi, price)
        t['low_since'] = price if lo is None else min(lo, price)
    _save(blob)
    return t


def patch(tracking_id, **fields):
    blob = _load()
    t = next((x for x in blob['trackings'] if x.get('tracking_id') == tracking_id), None)
    if not t:
        return None
    allowed = {'strategy_decision_at_start', 'strategy_score_at_start',
               'thesis_snapshot_id', 'benchmark'}
    for k, v in fields.items():
        if k in allowed:
            t[k] = v
    _save(blob)
    return t


def stop(tracking_id, *, at, final_price=None, final_decision=None, reason=''):
    """Arrête un suivi : gèle le résultat final, CONSERVE l'historique."""
    blob = _load()
    t = next((x for x in blob['trackings'] if x.get('tracking_id') == tracking_id), None)
    if not t:
        return None
    from . import returns as R
    values = [t.get('reference_price')] + [s.get('price') for s in t.get('snapshots', [])]
    if final_price is not None:
        values.append(final_price)
    mm = R.mae_mfe(t.get('reference_price'), values)
    t['status'] = models.ST_STOPPED
    t['stopped_at'] = at
    t['final'] = {
        'final_price': final_price,
        'return_pct': R.simple_return(t.get('reference_price'), final_price),
        'mfe_pct': mm['mfe_pct'], 'mae_pct': mm['mae_pct'],
        'final_decision': final_decision, 'reason': reason,
        'is_hypothetical': True,
    }
    _save(blob)
    return t


def restart(tracking_id, *, new_tracking_id, quote, started_at, market_open=True,
            benchmark_quote=None, decision='', score=None):
    """Réactive comme NOUVEAU suivi (nouvel id) — ne modifie pas l'ancien."""
    old = get(tracking_id)
    if not old:
        return None
    return create(tracking_id=new_tracking_id, entity_type=old['entity_type'],
                  symbol=old['symbol'], quote=quote, started_at=started_at,
                  market_open=market_open, benchmark_quote=benchmark_quote,
                  decision=decision, score=score, contract_id=old.get('contract_id'))


def summary():
    items = _load()['trackings']
    active = [t for t in items if t.get('status') == models.ST_ACTIVE]
    return {
        'total': len(items),
        'active': len(active),
        'stopped': sum(1 for t in items if t.get('status') == models.ST_STOPPED),
        'data_required': sum(1 for t in items if t.get('status') == models.ST_DATA_REQUIRED),
        'stocks': sum(1 for t in active if t.get('entity_type') != 'OPTION'),
        'options': sum(1 for t in active if t.get('entity_type') == 'OPTION'),
    }


__all__ = ['list_all', 'get', 'create', 'add_snapshot', 'patch', 'stop',
           'restart', 'summary']
