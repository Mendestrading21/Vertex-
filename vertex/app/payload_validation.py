"""Validation structurelle bornée des payloads analytiques Vertex."""
from __future__ import annotations

import math

from vertex.app import input_validation


class PayloadError(ValueError):
    pass


def object_body(raw, max_keys=24):
    if not isinstance(raw, dict):
        raise PayloadError('payload_json_objet_requis')
    if len(raw) > max_keys:
        raise PayloadError('payload_trop_de_champs')
    return raw


def required_symbol(body, key='symbol'):
    symbol = input_validation.symbol(body.get(key))
    if not symbol:
        raise PayloadError('symbole_invalide')
    return symbol


def optional_number(body, key, maximum=1_000_000_000):
    value = body.get(key)
    if value is None or value == '':
        return None
    if isinstance(value, bool):
        raise PayloadError('%s_invalide' % key)
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise PayloadError('%s_invalide' % key) from None
    if not math.isfinite(number) or abs(number) > maximum:
        raise PayloadError('%s_hors_borne' % key)
    return number


def object_list(body, key, maximum, minimum=0):
    value = body.get(key)
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        raise PayloadError('%s_taille_invalide' % key)
    if not all(isinstance(item, dict) for item in value):
        raise PayloadError('%s_objets_requis' % key)
    return value


__all__ = ['PayloadError', 'object_body', 'required_symbol', 'optional_number', 'object_list']
