import json

from vertex.services import persist


def test_cache_path_refuses_directory_escape(monkeypatch, tmp_path):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    try:
        persist.cache_path('../outside.json')
        assert False, 'un chemin sortant de la racine doit être refusé'
    except ValueError as exc:
        assert str(exc) == 'cache_path_invalide'


def test_save_json_replaces_cache_atomically_and_loads_value(monkeypatch, tmp_path):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    persist.save_json('nested/cache.json', {'version': 2, 'ok': True})
    assert persist.load_json('nested/cache.json', {}) == {'version': 2, 'ok': True}
    assert not list(tmp_path.rglob('*.tmp'))


def test_oversized_cache_returns_default_without_parsing(monkeypatch, tmp_path):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    monkeypatch.setattr(persist, 'MAX_CACHE_BYTES', 8)
    (tmp_path / 'large.json').write_text(json.dumps({'long': 'x' * 64}), encoding='utf-8')
    assert persist.load_json('large.json', {'fallback': True}) == {'fallback': True}
    assert persist.health()['load_failures'] >= 1


def test_load_cache_returns_isolated_copy_and_tracks_hit(monkeypatch, tmp_path):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    persist.save_json('cache.json', {'nested': {'value': 1}})
    first = persist.load_json('cache.json', {})
    first['nested']['value'] = 99
    second = persist.load_json('cache.json', {})
    assert second == {'nested': {'value': 1}}
    assert persist.health()['cache_hits'] >= 1
