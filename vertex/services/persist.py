"""
vertex/services/persist.py — Persistance JSON sur disque (Ch. II · Ch. III).

Les petits caches disque de VERTEX (fondamentaux, options, macro, desk perso…)
survivent aux redémarrages — vital contre le throttle yfinance et pour ne
jamais repartir de zéro. Un seul module écrit ces fichiers : chargement
tolérant (fichier absent/corrompu → valeur par défaut), écriture sous verrou,
erreurs d'E/S avalées volontairement (un cache est un confort, jamais une
condition de fonctionnement).

Les fichiers vivent à la racine du dépôt (aux côtés de terminal.py), comme
depuis toujours — aucun chemin ne change.
"""

import json
import os
import threading

# Racine du dépôt : vertex/services/persist.py → vertex/services → vertex → racine.
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_LOCK = threading.Lock()


def cache_path(name):
    """Chemin absolu d'un fichier de cache (racine du dépôt)."""
    return os.path.join(_BASE_DIR, name)


def load_json(name, default):
    """Charge un JSON depuis le disque ; `default` si absent ou illisible."""
    try:
        with open(cache_path(name), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


def save_json(name, obj):
    """Écrit un JSON sur disque sous verrou. Échec silencieux (cache best-effort)."""
    try:
        with _LOCK:
            with open(cache_path(name), 'w', encoding='utf-8') as f:
                json.dump(obj, f)
    except Exception:
        pass


__all__ = ['cache_path', 'load_json', 'save_json']
