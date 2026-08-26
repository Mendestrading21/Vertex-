"""vertex.ai.response_validator — validation stricte des réponses IA (§28)."""
from __future__ import annotations

from .chiffres import nombres_du_packet, non_sourcees
from .models import ANALYSIS_RESPONSE_SCHEMA

CERTAINTY_PHRASES = ('99 % sûr', '99% sûr', 'garanti', 'certain à 100', 'sans risque',
                     'aucun risque', 'sûr à 100')


def validate_analysis(payload, packet=None) -> tuple[bool, list[str]]:
    """Retourne (valide, erreurs). Une réponse invalide déclenche le fallback.

    Quand `packet` est fourni, tout chiffre du texte **absent du packet** rend
    la réponse invalide. Le prompt interdisait déjà à l'IA de *calculer* ; rien
    n'empêchait le modèle d'**énoncer** un prix, un P/E, une probabilité ou un
    Greek qui n'existe nulle part. Mesuré le 26 août 2026 : cinq chiffres
    inventés, tous acceptés. Une règle que rien n'applique est une intention.

    `packet` reste optionnel : les appelants qui ne l'ont pas gardent le
    comportement d'avant, et le contrôle ne devient pas une panne pour eux.
    """
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
    #  Aucun chiffre qui ne vienne du packet. `CLAUDE.md`, interdit absolu :
    #  « inventer prix/prime/Greek/probabilité/source ».
    if packet is not None:
        connues = nombres_du_packet(packet)
        for cle, valeur in payload.items():
            for texte in _textes(valeur):
                for x in non_sourcees(texte, packet, connues):
                    errors.append(
                        'chiffre absent du packet dans %s : %s (« %s »)'
                        % (cle, x['valeur'], x['extrait']))
    return not errors, errors


def _textes(valeur):
    """Les chaînes d'une valeur de réponse, listes imbriquées comprises.

    `contradictions` et `questions_for_user` sont des listes : ne regarder que
    les chaînes de premier niveau laisserait passer un chiffre inventé dans une
    contradiction — précisément là où le lecteur cherche un fait.
    """
    if isinstance(valeur, str):
        return [valeur]
    if isinstance(valeur, (list, tuple)):
        out = []
        for v in valeur:
            out.extend(_textes(v))
        return out
    if isinstance(valeur, dict):
        out = []
        for v in valeur.values():
            out.extend(_textes(v))
        return out
    return []
