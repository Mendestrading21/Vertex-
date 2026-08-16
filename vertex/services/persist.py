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
import tempfile
import threading
import copy
import hashlib

# Racine du dépôt : vertex/services/persist.py → vertex/services → vertex → racine.
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_LOCK = threading.Lock()
MAX_CACHE_BYTES = 32 * 1024 * 1024
MAX_MEMORY_ENTRIES = 64
_READ_CACHE = {}
_STATS = {'loads': 0, 'load_failures': 0, 'saves': 0, 'save_failures': 0,
          'cache_hits': 0, 'cache_misses': 0, 'last_error': None}


def cache_path(name):
    """Chemin de cache validé, toujours contenu dans la racine du dépôt."""
    root = os.path.abspath(_BASE_DIR)
    path = os.path.abspath(os.path.join(root, str(name or '')))
    if not path.startswith(root + os.sep):
        raise ValueError('cache_path_invalide')
    return path


def _signature(path, stat=None):
    """Empreinte de contenu : les mtime trop proches ne masquent jamais une écriture externe."""
    stat = stat or os.stat(path)
    digest = hashlib.blake2b(digest_size=16)
    with open(path, 'rb') as raw:
        for chunk in iter(lambda: raw.read(128 * 1024), b''):
            digest.update(chunk)
    return (stat.st_mtime_ns, stat.st_ctime_ns, stat.st_size, digest.digest())


def load_json(name, default):
    """Charge un JSON depuis le disque ; `default` si absent ou illisible."""
    try:
        path = cache_path(name)
        with _LOCK:
            stat = os.stat(path)
            if stat.st_size > MAX_CACHE_BYTES:
                raise ValueError('cache_too_large')
            signature = _signature(path, stat)
            cached = _READ_CACHE.get(path)
            if cached and cached['signature'] == signature:
                _STATS['cache_hits'] += 1
                return copy.deepcopy(cached['data'])
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            _STATS['loads'] += 1
            _STATS['cache_misses'] += 1
            if len(_READ_CACHE) >= MAX_MEMORY_ENTRIES and path not in _READ_CACHE:
                _READ_CACHE.pop(next(iter(_READ_CACHE)))
            _READ_CACHE[path] = {'signature': signature, 'data': data}
            return copy.deepcopy(data)
    except Exception as exc:
        _STATS['load_failures'] += 1
        _STATS['last_error'] = type(exc).__name__
        return default


def save_json(name, obj):
    """Écrit un JSON atomiquement sous verrou.

    Une écriture partielle ne remplace jamais le cache existant. Les échecs restent
    non bloquants pour l’analyse, mais sont comptabilisés pour l’observabilité.
    """
    tmp_path = None
    try:
        with _LOCK:
            path = cache_path(name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            fd, tmp_path = tempfile.mkstemp(prefix='.vertex-', suffix='.tmp',
                                            dir=os.path.dirname(path))
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(obj, f)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, path)
            tmp_path = None
            _STATS['saves'] += 1
            stat = os.stat(path)
            _READ_CACHE[path] = {'signature': _signature(path, stat),
                                 'data': copy.deepcopy(obj)}
    except Exception as exc:
        _STATS['save_failures'] += 1
        _STATS['last_error'] = type(exc).__name__
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


def health():
    """État non sensible de la persistance : compteurs, jamais de chemins ou données."""
    return {**_STATS, 'memory_entries': len(_READ_CACHE),
            'max_memory_entries': MAX_MEMORY_ENTRIES, 'max_cache_bytes': MAX_CACHE_BYTES}


__all__ = ['cache_path', 'load_json', 'save_json', 'health', 'MAX_CACHE_BYTES']
