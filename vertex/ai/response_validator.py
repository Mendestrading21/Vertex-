"""vertex.ai.response_validator — validation stricte des réponses IA (§28)."""
from __future__ import annotations

from .models import ANALYSIS_RESPONSE_SCHEMA

CERTAINTY_PHRASES = ('99 % sûr', '99% sûr', 'garanti', 'certain à 100', 'sans risque',
                     'aucun risque', 'sûr à 100')


def validate_analysis(payload) -> tuple[bool, list[str]]:
    """Retourne (valide, erreurs). Une réponse invalide déclenche le fallback."""
    errors: list[str] = []
    if not isinstance(payload, dict):
        return False, ['réponse non structurée (dict attendu)']
    schema = ANALYSIS_RESPONSE_SCHEMA
    for key, typ in schema['required'].items():
        if key not in payload:
            errors.append(f'clé requise absente: {key}')
        elif not isinstance(payload[key], typ):
            errors.append(f'{key}: type {type(payload[key]).__name__} ≠ {typ.__name__}')
    for key, typ in schema['optional'].items():
        if key in payload and not isinstance(payload[key], typ):
            errors.append(f'{key}: type invalide')
    for key in schema['forbidden_keys']:
        if key in payload:
            errors.append(f'clé interdite présente: {key}')
    unknown = set(payload) - set(schema['required']) - set(schema['optional'])
    if unknown:
        errors.append(f'clés inconnues: {sorted(unknown)}')
    text = ' '.join(str(v) for v in payload.values())
    for phrase in CERTAINTY_PHRASES:
        if phrase.lower() in text.lower():
            errors.append(f'langage de certitude interdit: {phrase!r}')
    # Claude ne calcule pas : une réponse qui prétend recalculer un score final est rejetée
    lowered = text.lower()
    if 'je recalcule le score' in lowered or 'nouveau score final' in lowered:
        errors.append('la réponse tente de recalculer un score final — interdit')
    return not errors, errors
