"""tests/test_hygiene_lot71.py — SKYLER LOT 71 : hygiène des références.

Ouverture du PROGRAMME 100 % (lots 71+, directive utilisateur : « continue
à tout développer et quand t'as tout à 100 tu me dis »). Défaut réel hérité
du lot 68 (divergence documentaire, dite alors) : la docstring de
vertex/data_sources/ibkr_gateway.py citait un gardien inexistant
(tests/test_readonly_gateway.py) — les vrais gardiens sont test_no_orders,
test_ibkr_honesty et test_order_ticket. Corrigé PAR la source.

Gardien PROSPECTIF : tout chemin `tests/test_*.py` cité dans le code
vertex/ (docstrings/commentaires) doit exister sur le disque — sinon la
doc ment sur qui garde quoi. Balayage complet, pas seulement le gateway.
"""
import os
import re

PAT = re.compile(r'tests/test_[A-Za-z0-9_]+\.py')


def _walk_vertex_py():
    for root, dirs, files in os.walk('vertex'):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in files:
            if f.endswith('.py'):
                yield os.path.join(root, f)


def test_gateway_docstring_cites_real_guardians():
    src = open('vertex/data_sources/ibkr_gateway.py', encoding='utf-8').read()
    assert 'test_readonly_gateway' not in src, (
        'la docstring du gateway cite un gardien inexistant')
    assert 'test_no_orders' in src and 'test_ibkr_honesty' in src, (
        'la docstring doit citer les vrais gardiens READONLY')


def test_no_python_file_cites_missing_test_file():
    offenders = []
    for path in _walk_vertex_py():
        src = open(path, encoding='utf-8', errors='ignore').read()
        for ref in sorted(set(PAT.findall(src))):
            if not os.path.exists(ref):
                offenders.append(f'{path} -> {ref}')
    assert not offenders, (
        'références de tests inexistants (la doc ment) : ' + '; '.join(offenders))
