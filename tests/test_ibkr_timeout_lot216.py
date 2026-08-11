# -*- coding: utf-8 -*-
"""LOT 216 — gardien de l'invariant CLAUDE.md « IBKR : worker unique avec
RequestTimeout=45 (ne pas retirer — anti-blocage) ».

Lacune mesurée au lot 216 : readonly=True était gardé par 3 tests
(test_no_orders, test_strategy_os_final_guards, test_data_sources) mais
AUCUN test n'épinglait le timeout anti-blocage — on pouvait retirer
`ib.RequestTimeout = REQUEST_TIMEOUT_S` ou changer 45 sans rien casser,
alors qu'un worker IBKR bloqué gèle l'app (règle critique CLAUDE.md).
"""
import pathlib

from vertex.data_sources import ibkr_gateway, ibkr_scheduler

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATEWAY_SRC = (ROOT / 'vertex' / 'data_sources' / 'ibkr_gateway.py').read_text(encoding='utf-8')


def test_le_timeout_anti_blocage_vaut_45_secondes():
    assert ibkr_gateway.REQUEST_TIMEOUT_S == 45


def test_la_connexion_applique_le_timeout_et_reste_readonly():
    # Les DEUX bornes : RequestTimeout côté session ET timeout du connect,
    # dans la même façade readonly=True (source inspectée, pas de TWS requis).
    assert 'ib.RequestTimeout = REQUEST_TIMEOUT_S' in GATEWAY_SRC
    assert 'readonly=True, timeout=REQUEST_TIMEOUT_S' in GATEWAY_SRC
    assert ibkr_gateway.IbkrGateway.READONLY is True


def test_le_scheduler_reste_aligne_sur_le_timeout_gateway():
    # ibkr_scheduler documente « aligné sur le RequestTimeout IBKR existant » —
    # si l'un bouge sans l'autre, ce test casse au lieu de laisser dériver.
    assert ibkr_scheduler.DEFAULT_TIMEOUT_S == ibkr_gateway.REQUEST_TIMEOUT_S
