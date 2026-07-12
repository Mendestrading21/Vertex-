"""vertex.data_sources.tradingview_webhooks — webhook TradingView sécurisé (§32).

POST /api/tradingview/webhook :
  { "secret": "...", "symbol": "NVDA", "signal": "BREAKOUT_CONFIRMED",
    "timestamp": 1699999999, "price": 495.2, ... }

Garanties : secret obligatoire (comparaison constante), symbole/signal/timestamp
validés, anti-replay, dédup, stockage, réponse immédiate, déclenche une
RÉÉVALUATION — ne génère JAMAIS directement un achat.
"""
from __future__ import annotations

import hmac
import os
from typing import Callable

from flask import Blueprint, jsonify, request

from .tradingview_signal_store import SIGNAL_STORE, TradingViewSignalStore


def _resolve_secret() -> str:
    """Résout le secret webhook en acceptant les DEUX noms documentés.

    La doc/.env/rapports utilisent TRADINGVIEW_WEBHOOK_SECRET ; le code lisait
    historiquement TRADINGVIEW_SECRET. On accepte les deux (WEBHOOK d'abord) —
    sinon un utilisateur qui suit la doc croit son webhook actif alors qu'il
    répond 503 (statut menteur). Cf. config_validation._ALIASES."""
    return (os.environ.get('TRADINGVIEW_WEBHOOK_SECRET', '').strip()
            or os.environ.get('TRADINGVIEW_SECRET', '').strip())


def make_blueprint(store: TradingViewSignalStore = SIGNAL_STORE,
                   secret: str | None = None,
                   on_signal: Callable[[dict], None] | None = None) -> Blueprint:
    bp = Blueprint('tradingview', __name__)
    configured_secret = secret if secret is not None else _resolve_secret()
    # L'UI doit pouvoir distinguer « webhook désactivé » de « en attente ».
    store.set_configured(bool(configured_secret))

    @bp.route('/api/tradingview/webhook', methods=['POST'])
    def tradingview_webhook():
        if not configured_secret:
            return jsonify({'ok': False, 'error': 'webhook désactivé '
                            '(TRADINGVIEW_WEBHOOK_SECRET absent)'}), 503
        body = request.get_json(silent=True) or {}
        provided = str(body.get('secret') or '')
        if not hmac.compare_digest(provided, configured_secret):
            return jsonify({'ok': False, 'error': 'secret invalide'}), 403
        result = store.add(symbol=body.get('symbol'), signal=body.get('signal'),
                           event_ts=body.get('timestamp'),
                           payload={k: v for k, v in body.items()
                                    if k not in ('secret',)})
        if not result['accepted']:
            return jsonify({'ok': False, 'error': result['reason']}), 400
        # Réévaluation asynchrone — l'entrée stockée porte action=REEVALUATE ;
        # aucun chemin d'achat n'existe en aval.
        if on_signal is not None:
            try:
                on_signal(result['entry'])
            except Exception:
                pass  # le webhook répond immédiatement même si la réévaluation échoue
        return jsonify({'ok': True, 'action': 'REEVALUATE'}), 200

    @bp.route('/api/tradingview/signals')
    def tradingview_signals():
        sym = request.args.get('symbol')
        return jsonify({'signals': store.recent(symbol=sym), 'status': store.status()})

    return bp
