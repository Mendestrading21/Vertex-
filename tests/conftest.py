"""
tests/conftest.py — Environnement de test déterministe.

Force le mode DÉMO (aucun réseau) et DÉSACTIVE le verrou d'accès, afin que la
suite teste la logique de l'application indépendamment de tout .env local
(ex. VERTEX_CODE défini sur la machine du dev). Doit s'exécuter AVANT l'import
de l'application.
"""

import os

os.environ['DEMO'] = '1'
os.environ['NO_IBKR'] = '1'
# Verrou d'accès désactivé pendant les tests (clé présente mais vide → dotenv
# ne l'écrase pas, AUTH_ON reste False).
os.environ['VERTEX_CODE'] = ''
os.environ['ACCESS_CODE'] = ''


# ── Gardes rendues caduques par la refonte Black Glass ──────────────────────
#
#  Cent cinquante-trois bancs de `main` decrivent, jeton par jeton et
#  identifiant par identifiant, une interface qui n'est plus servie. Ils sont
#  ecartes UN PAR UN, nommes, avec leur motif — jamais par une regle large qui
#  en emporterait de nouveaux sans qu'on le voie.
#
#  `tests/_supersede.py` porte la liste et l'explication ; le recensement
#  `test_vertex_1_0_gardes_superseedees.py` verifie qu'elle ne grossit pas,
#  qu'aucune entree n'est morte, et qu'un banc hors liste n'est jamais ecarte.
def pytest_collection_modifyitems(config, items):
    import importlib.util
    import os

    import pytest

    #  Charge par CHEMIN : `tests/` n'est pas un paquet, et en faire un
    #  changerait la resolution des imports de toute la suite.
    chemin = os.path.join(os.path.dirname(__file__), '_supersede.py')
    spec = importlib.util.spec_from_file_location('_vx_supersede', chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    sep = chr(92)
    for item in items:
        motif = mod.REGISTRE.get(item.nodeid.replace(sep, '/'))
        if motif:
            item.add_marker(pytest.mark.skip(reason='SUPERSEDE - ' + motif))
