"""tests/test_labels.py — SKYLER LOT 78 : cohérence des libellés FR.

Balayage du texte AFFICHÉ (innerText des 8 pages, Playwright) + des
sources UI : 0 mot anglais d'interface (Loading/Error/Failed/Submit…),
0 faute d'accent fréquente (deja/etat/resume/marche…), ponctuation
conforme — l'unique signalement de ma sonde (« espace avant ; ») est la
NORME typographique française, faux positif dit. SAIN — lot documentaire.

Gardien PROSPECTIF (né vert, dit) : aucun mot anglais d'interface ne doit
apparaître dans le texte visible des sources UI (les termes de trading
assumés — spread, put, call, breadth… — restent hors périmètre).
"""
import os
import re

# Mots d'interface anglais interdits, cherchés UNIQUEMENT en position de
# texte visible (juste après '>' ou en début de chaîne littérale).
_FORBIDDEN = ('Loading', 'Error:', 'Failed', 'Submit', 'Cancel', 'Retry',
              'Please wait', 'Warning:', 'Success!')


def _ui_sources():
    yield 'terminal.py'
    for root, dirs, files in os.walk('vertex/ui'):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in files:
            if f.endswith('.py'):
                yield os.path.join(root, f)


def test_no_english_ui_words_in_visible_text():
    offenders = []
    for p in _ui_sources():
        src = open(p, encoding='utf-8', errors='ignore').read()
        for w in _FORBIDDEN:
            for pat in (f'>{w}', f">'{w}'", f'"{w}"'):
                if pat in src:
                    offenders.append(f'{p} -> {pat}')
    assert not offenders, f'anglais résiduel dans l\'UI FR : {offenders}'


def test_no_common_missing_accents_in_visible_text():
    pat = re.compile(r'>(deja|etat|resume|periode|scenario|derniere|liquidite|volatilite)\b')
    offenders = []
    for p in _ui_sources():
        src = open(p, encoding='utf-8', errors='ignore').read()
        for m in pat.finditer(src):
            offenders.append(f'{p} -> {m.group(0)}')
    assert not offenders, f'accents manquants dans le texte visible : {offenders}'
