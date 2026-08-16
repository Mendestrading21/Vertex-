"""Résolution canonique d'une quote de contrat depuis l'options board.

Ce module ne contacte aucune source et ne passe aucun ordre. Il relie un suivi
hypothétique à un contrat réellement publié dans ``options_board``. L'absence
de quote exploitable reste explicite ; le champ historique ``cost`` n'est jamais
converti automatiquement en mark car son unité/provenance dépend du producteur.
"""
from __future__ import annotations

import math


def _positive(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) and number > 0 else None


def contract_id(contract):
    """Identité stable ``SYM|EXP|STRIKE|C/P`` partagée par le suivi et les positions."""
    c = contract or {}
    sym = str(c.get('sym') or c.get('symbol') or '').upper()
    exp = str(c.get('exp') or c.get('expiry') or '')
    strike = c.get('strike')
    right = str(c.get('type') or c.get('right') or '').upper()
    side = 'P' if right in ('PUT', 'P') else ('C' if right in ('CALL', 'C') else '')
    if not sym or not exp or strike is None or not side:
        return None
    return '%s|%s|%s|%s' % (sym, exp, strike, side)


def _quote(contract, source):
    """Extrait uniquement des prix explicitement portés par le contrat."""
    c = contract or {}
    quote = {'source': source or c.get('source') or 'options_board'}
    for name in ('bid', 'ask', 'mid', 'mark', 'last', 'iv'):
        value = _positive(c.get(name))
        if value is not None:
            quote[name] = value
    # Une quote est exploitable seulement si le référentiel options sait en tirer
    # un MID, MARK ou LAST. Le coût historique par contrat est intentionnellement
    # exclu : il ne constitue pas une quote actuelle prouvée.
    price_kind = None
    bid, ask = quote.get('bid'), quote.get('ask')
    if bid is not None and ask is not None and ask >= bid:
        price_kind = 'BID_ASK_MID'
    elif quote.get('mid') is not None:
        price_kind = 'DIRECT_MID'
    elif quote.get('mark') is not None:
        price_kind = 'DIRECT_MARK'
    elif quote.get('last') is not None:
        price_kind = 'LAST_WITH_WARNING'
    return quote, price_kind


def resolve(board, *, contract_id_value=None, symbol=None, as_of=None, source=None):
    """Résout une quote de board par identité exacte, sans approximation.

    Un symbole seul est insuffisant : une même chaîne contient de nombreux
    strikes/échéances. L'appelant reçoit toujours un objet sérialisable avec une
    raison si le contrat n'est pas prouvé dans le board courant.
    """
    wanted = str(contract_id_value or '')
    symbol = str(symbol or '').upper()
    if not wanted:
        return {'available': False, 'quote': {}, 'reason': 'contract_id requis — symbole seul ambigu',
                'as_of': as_of, 'source': source or 'options_board'}
    matches = [c for c in (board or []) if isinstance(c, dict) and contract_id(c) == wanted]
    if symbol:
        matches = [c for c in matches if str(c.get('sym') or c.get('symbol') or '').upper() == symbol]
    if len(matches) != 1:
        return {'available': False, 'quote': {},
                'reason': ('contrat absent du board courant' if not matches
                           else 'identité contractuelle dupliquée dans le board'),
                'contract_id': wanted, 'as_of': as_of, 'source': source or 'options_board'}
    contract = matches[0]
    quote, price_kind = _quote(contract, source)
    identity = contract_id(contract)
    evidence = {
        'contract_id': identity,
        'symbol': str(contract.get('sym') or contract.get('symbol') or '').upper(),
        'as_of': as_of,
        'source': quote.get('source'),
        'price_kind': price_kind,
        'board_fields': sorted(k for k in ('bid', 'ask', 'mid', 'mark', 'last', 'iv') if k in quote),
        'cost_used_as_quote': False,
    }
    if price_kind is None:
        return {'available': False, 'quote': quote,
                'reason': 'contrat trouvé mais aucune quote bid/ask, mid, mark ou last exploitable',
                'contract_id': identity, 'as_of': as_of, 'source': quote.get('source'),
                'evidence': evidence}
    return {'available': True, 'quote': quote, 'contract_id': identity,
            'as_of': as_of, 'source': quote.get('source'), 'evidence': evidence}


__all__ = ['contract_id', 'resolve']
