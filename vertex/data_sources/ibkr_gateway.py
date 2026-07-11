"""vertex.data_sources.ibkr_gateway — connexion IBKR STRICTEMENT lecture seule.

Invariant produit : `readonly=True` est codé en dur et non paramétrable.
Aucune méthode d'ordre n'existe dans cette façade ; les tests de sécurité
(tests/test_no_orders.py, tests/test_readonly_gateway.py) inspectent ce module.
"""
from __future__ import annotations

import os
import threading

# Timeout anti-blocage : ne pas retirer (un worker IBKR bloqué gèle l'app).
REQUEST_TIMEOUT_S = 45

_DEFAULT_HOST = os.environ.get('IBKR_HOST', '127.0.0.1')
_DEFAULT_PORT = int(os.environ.get('IBKR_PORT', '7497'))
_DEFAULT_CLIENT_ID = int(os.environ.get('IBKR_CLIENT_ID', '17'))


class IbkrGateway:
    """Façade de connexion. Un seul worker à la fois (lock), lecture seule à vie."""

    READONLY = True  # non négociable — inspecté par les tests de sécurité

    def __init__(self, host: str = _DEFAULT_HOST, port: int = _DEFAULT_PORT,
                 client_id: int = _DEFAULT_CLIENT_ID) -> None:
        self.host, self.port, self.client_id = host, port, client_id
        self._ib = None
        self._lock = threading.Lock()

    # ── cycle de vie ─────────────────────────────────────────────────
    def connect(self):
        """Connexion lecture seule. Import paresseux : l'app doit démarrer sans TWS."""
        from ib_async import IB  # import ici pour le mode dégradé sans dépendance
        with self._lock:
            if self._ib is not None and self._ib.isConnected():
                return self._ib
            ib = IB()
            ib.RequestTimeout = REQUEST_TIMEOUT_S
            # readonly=True EN DUR : cette façade ne peut PAS ouvrir une session
            # capable de transmettre des ordres, quels que soient les arguments.
            ib.connect(self.host, self.port, clientId=self.client_id,
                       readonly=True, timeout=REQUEST_TIMEOUT_S)
            self._ib = ib
            return ib

    def disconnect(self) -> None:
        with self._lock:
            if self._ib is not None:
                try:
                    self._ib.disconnect()
                finally:
                    self._ib = None

    @property
    def connected(self) -> bool:
        return self._ib is not None and self._ib.isConnected()

    def status(self) -> dict:
        return {'connected': self.connected, 'host': self.host, 'port': self.port,
                'client_id': self.client_id, 'readonly': True,
                'order_execution': 'disabled-by-design'}
