"""tests/test_hygiene_lot76.py — SKYLER LOT 76 : hygiène JS/HTML (boucle continue).

Balayage complet : restes de débogage (console.log/console.debug/debugger/
window.alert) dans le JS statique ET le JS embarqué des chaînes Python →
0 partout ; fonctions globales dupliquées entre fichiers JS → 0 ;
TODO/FIXME en production → 0. UN défaut réel : les onglets de la démo du
design system (`/system/design-system`) portaient `href="#"` — un clic
saute en haut de page et pollue l'URL. Corrigé : spécimens rendus en
ancres sans href (non-navigantes, valides, sans piège clavier).

Gardien PROSPECTIF : plus jamais de href="#" dans l'UI servie.
"""
import os


def _ui_sources():
    yield 'terminal.py'
    for root, dirs, files in os.walk('vertex/ui'):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in files:
            if f.endswith('.py'):
                yield os.path.join(root, f)


def test_no_dead_hash_href_anywhere():
    offenders = []
    for p in _ui_sources():
        src = open(p, encoding='utf-8', errors='ignore').read()
        if 'href="#"' in src or "href='#'" in src:
            offenders.append(p)
    assert not offenders, f'href="#" (lien mort qui saute en haut) : {offenders}'


def test_no_debug_leftovers_in_static_js():
    bad = ('console.log', 'console.debug', 'debugger;', 'window.alert')
    offenders = []
    for root, dirs, files in os.walk('vertex/static/vertex/js'):
        if 'vendor' in root:
            continue
        for f in files:
            if not f.endswith('.js'):
                continue
            p = os.path.join(root, f)
            src = open(p, encoding='utf-8', errors='ignore').read()
            for b in bad:
                if b in src:
                    offenders.append(f'{p} -> {b}')
    assert not offenders, f'restes de débogage en production : {offenders}'
