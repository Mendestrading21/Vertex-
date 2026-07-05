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
