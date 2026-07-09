"""
vertex/app/config.py — Configuration centrale de VERTEX (dérivée de l'environnement).

Un seul endroit lit os.environ. Le reste du code importe des valeurs déjà
résolues et documentées. Toute la configuration de sûreté (lecture seule,
verrou d'accès) est centralisée et explicite ici.
"""

import os
import secrets


def _load_dotenv():
    """Charge .env (racine du projet) dans os.environ — sans dépendance externe.
    Les variables déjà présentes dans l'environnement GARDENT la priorité.
    Rend le verrou d'accès activable en copiant .env.example → .env."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(root, '.env')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, _, v = line.partition('=')
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
    except FileNotFoundError:
        pass
    except Exception:
        pass


_load_dotenv()

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

# Clé de signature des sessions : VERTEX_SECRET, sinon un secret ALÉATOIRE persistant.
# ⚠️ Sécurité : la clé n'est JAMAIS dérivée du code d'accès (sinon un code court
# permettrait de forger un cookie de session hors-ligne). À défaut de VERTEX_SECRET,
# on génère 32 octets aléatoires une fois et on les conserve localement
# (.vertex_secret, hors git) pour que les sessions survivent aux redémarrages.


def _local_secret():
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(root, '.vertex_secret')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read().strip()
        if len(s) >= 32:
            return s
    except Exception:
        pass
    s = secrets.token_hex(32)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(s)
    except Exception:
        pass   # disque en lecture seule → secret par-process (sessions reset au reboot)
    return s


SECRET_KEY = os.environ.get('VERTEX_SECRET') or _local_secret()

# Démarrage immédiat du scan à l'import (utile derrière gunicorn --preload / Render).
START_ON_IMPORT = os.environ.get('START_ON_IMPORT') == '1'

__all__ = ['READONLY', 'ANALYSIS_ONLY', 'IBKR_ENABLED', 'DEMO_MODE',
           'VERTEX_CODE', 'AUTH_ON', 'SECRET_KEY', 'START_ON_IMPORT']
