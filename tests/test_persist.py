"""
tests/test_persist.py — Persistance JSON sur disque (Ch. II).

Aller-retour fidèle, tolérance aux fichiers absents/corrompus, chemins à la
racine du dépôt (là où terminal.py a toujours écrit ses caches).
"""

import os

from vertex.services import persist


def test_cache_path_points_to_repo_root():
    p = persist.cache_path('fund_cache.json')
    root = os.path.dirname(p)
    assert os.path.isfile(os.path.join(root, 'terminal.py'))


def test_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    obj = {'ts': 123, 'data': {'a': [1, 2, 3], 'b': 'été'}}
    persist.save_json('t.json', obj)
    assert persist.load_json('t.json', None) == obj


def test_missing_file_returns_default(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    assert persist.load_json('absent.json', {'d': 1}) == {'d': 1}


def test_corrupt_file_returns_default(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    (tmp_path / 'bad.json').write_text('{pas du json', encoding='utf-8')
    assert persist.load_json('bad.json', []) == []


def test_save_failure_is_silent(monkeypatch):
    monkeypatch.setattr(persist, '_BASE_DIR', '/chemin/inexistant/xyz')
    persist.save_json('t.json', {'x': 1})   # ne doit PAS lever


def test_terminal_uses_the_service():
    import terminal
    from vertex.services import persist as p
    assert terminal._load_json is p.load_json and terminal._save_json is p.save_json
