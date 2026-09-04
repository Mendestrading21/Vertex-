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


# ── Import deterministe du monolithe ───────────────────────────────────────
#
#  `terminal.app` est un singleton construit au premier import, avec la
#  constitution active A CET INSTANT. Tant que l'import venait du premier banc
#  collecte, la configuration de l'application dependait de l'ordre
#  alphabetique des noms de fichiers. On l'importe donc ici, avant toute
#  collecte, sur la constitution par defaut.
import terminal as _terminal  # noqa: E402,F401

#  Etat VIERGE de la constitution, fige AVANT la collecte. Un module de test
#  qui importe `vertex.runtime` active V4 des l'import, donc avant toute
#  fixture : un instantane pris au premier test capturerait deja la pollution.
from vertex.strategy import constitution as _c_mod  # noqa: E402
from vertex.strategy import release as _r_mod  # noqa: E402

_CONSTITUTION_VIERGE = (_c_mod.PROFILES_DIR, _c_mod.load_profile,
                        _c_mod.list_versions, _c_mod.propose_new_version,
                        _r_mod._ACTIVATED)


# ── Gardes rendues caduques par la refonte Black Glass ──────────────────────
#
#  Cent cinquante-trois bancs de `main` decrivent, jeton par jeton et
#  identifiant par identifiant, une interface qui n'est plus servie. Ils sont
#  ecartes UN PAR UN, nommes, avec leur motif — jamais par une regle large qui
#  en emporterait de nouveaux sans qu'on le voie.
#
#  `tests/_supersede.py` porte la liste et l'explication ; le recensement
#  `test_gardes_superseedees.py` verifie qu'elle ne grossit pas,
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


# ── Isolation de la constitution active ────────────────────────────────────
#
#  `vertex.strategy.release.activate_release_profile()` remplace en place
#  `PROFILES_DIR`, `load_profile`, `list_versions` et `propose_new_version` du
#  module `constitution`, et se garde d'un drapeau `_ACTIVATED` sans inverse.
#  Le premier test qui l'appelle imposait donc V4 a TOUS les suivants : la
#  suite ne passait que grace a l'ordre alphabetique des anciens noms de
#  fichiers. Un test ne doit pas dependre du nom de son voisin.
import pytest as _pytest


def _restaurer_constitution():
    (_c_mod.PROFILES_DIR, _c_mod.load_profile, _c_mod.list_versions,
     _c_mod.propose_new_version, _r_mod._ACTIVATED) = _CONSTITUTION_VIERGE


@_pytest.fixture(autouse=True)
def _constitution_isolee():
    _restaurer_constitution()
    yield
    _restaurer_constitution()
