"""vertex.strategy.memory.store — stockage versionné de la mémoire (§33).

AUCUNE règle proposée n'est active avant confirmation humaine : le store
refuse de retourner comme « actives » des entrées non CONFIRMED.
"""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path

from .schemas import ACTIVE_STATUS, STATUSES, STORAGE_KEYS, validate_status


class MemoryStore:
    def __init__(self, path: Path | str | None = None) -> None:
        self._path = Path(path) if path else None
        self._data: dict[str, list] = {k: [] for k in STORAGE_KEYS}
        self._lock = threading.Lock()
        self._seq = 0
        if self._path and self._path.exists():
            try:
                loaded = json.loads(self._path.read_text(encoding='utf-8'))
                for k in STORAGE_KEYS:
                    self._data[k] = list(loaded.get(k, []))
                self._seq = int(loaded.get('_seq', 0))
            except (json.JSONDecodeError, OSError):
                pass  # store corrompu → repart proprement, l'ancien fichier reste sur disque

    def _persist(self) -> None:
        if self._path is None:
            return
        payload = dict(self._data)
        payload['_seq'] = self._seq
        tmp = self._path.with_suffix('.tmp')
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding='utf-8')
        tmp.replace(self._path)

    def add(self, key: str, entry: dict, status: str = 'OBSERVED') -> dict:
        if key not in STORAGE_KEYS:
            raise KeyError(f'clé de mémoire inconnue: {key}')
        validate_status(status)
        with self._lock:
            self._seq += 1
            entry = dict(entry)
            entry.setdefault('id', f'{key}-{self._seq}')
            entry['status'] = status
            entry.setdefault('created_at',
                             time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
            self._data[key].append(entry)
            self._persist()
            return entry

    def set_status(self, key: str, entry_id: str, status: str,
                   confirmed_by_human: bool = False) -> dict:
        validate_status(status)
        if status == ACTIVE_STATUS and not confirmed_by_human:
            raise PermissionError('CONFIRMED exige confirmed_by_human=True — '
                                  'aucune activation automatique')
        with self._lock:
            for entry in self._data[key]:
                if entry.get('id') == entry_id:
                    entry['status'] = status
                    if status == ACTIVE_STATUS:
                        entry['confirmed_at'] = time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                                              time.gmtime())
                    self._persist()
                    return entry
        raise KeyError(f'entrée introuvable: {entry_id}')

    def entries(self, key: str, status: str | None = None) -> list[dict]:
        with self._lock:
            items = list(self._data[key])
        if status:
            items = [e for e in items if e.get('status') == status]
        return items

    def active(self, key: str) -> list[dict]:
        """SEULES les entrées CONFIRMED sont actives (invariant produit)."""
        return self.entries(key, status=ACTIVE_STATUS)
