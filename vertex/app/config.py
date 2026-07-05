"""
vertex/app/config.py — Configuration centrale de VERTEX (dérivée de l'environnement).

Un seul endroit lit os.environ. Le reste du code importe des valeurs déjà
résolues et documentées. Toute la configuration de sûreté (lecture seule,
verrou d'accès) est centralisée et explicite ici.
"""

import os
import hashlib

# ─── SÛRETÉ : VERTEX est un terminal d'ANALYSE, en LECTURE SEULE. ───
# Cette constante est structurelle et ne doit jamais passer à False.
# Elle documente et affirme l'invariant produit : aucun ordre n'est jamais passé.
READONLY = True
ANALYSIS_ONLY = True

# ─── IBKR : activé seulement hors cloud (là où TWS/Gateway tourne). ───
# Toute connexion IBKR se fait en readonly=True (verrou côté courtier) — voir ib_reader.py.
IBKR_ENABLED = os.environ.get('NO_IBKR') != '1'

# ─── MODE DÉMO : chiffres synthétiques réalistes mais FICTIFS (cloud / vitrine). ───
# Activé par défaut sur le cloud (NO_IBKR=1). Forcer DEMO=1 / désactiver DEMO=0.
DEMO_MODE = os.environ.get('DEMO', '1' if os.environ.get('NO_IBKR') == '1' else '0') == '1'

# ─── VERROU D'ACCÈS (code d'entrée) — optionnel, activé par variable d'env. ───
# VERTEX_CODE défini → toute l'app est protégée par un code. Sinon aucun verrou.
VERTEX_CODE = (os.environ.get('VERTEX_CODE') or os.environ.get('ACCESS_CODE') or '').strip()
AUTH_ON = bool(VERTEX_CODE)

# Clé de signature des sessions : VERTEX_SECRET, sinon dérivée déterministe du code.
SECRET_KEY = (os.environ.get('VERTEX_SECRET')
              or hashlib.sha256(('vertex-secret::' + (VERTEX_CODE or 'demo')).encode()).hexdigest())

# Démarrage immédiat du scan à l'import (utile derrière gunicorn --preload / Render).
START_ON_IMPORT = os.environ.get('START_ON_IMPORT') == '1'

__all__ = ['READONLY', 'ANALYSIS_ONLY', 'IBKR_ENABLED', 'DEMO_MODE',
           'VERTEX_CODE', 'AUTH_ON', 'SECRET_KEY', 'START_ON_IMPORT']
