"""tests/test_services_lot90.py — SKYLER LOT 90 : persist + connections figés.

Caractérisations nées vertes (dites) des deux services critiques :
`persist` (la persistance JSON dont dépendent desk_data et la mémoire
souveraine) et `connections` (l'état honnête des intégrations — jamais
plus favorable que la réalité). Les tests redirigent persist vers un
répertoire temporaire : AUCUN fichier runtime touché.
"""
import os

import pytest

from vertex.services import connections as cx
from vertex.services import persist


@pytest.fixture()
def tmp_persist(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    return tmp_path


def test_load_absent_file_returns_default(tmp_persist):
    assert persist.load_json('inexistant.json', {'d': 1}) == {'d': 1}
    assert persist.load_json('inexistant.json', None) is None


def test_load_corrupted_json_returns_default_never_crashes(tmp_persist):
    (tmp_persist / 'corrompu.json').write_text('{pas du json', encoding='utf-8')
    assert persist.load_json('corrompu.json', 'defaut') == 'defaut'


def test_save_load_roundtrip_faithful(tmp_persist):
    obj = {'trades': [{'sym': 'ACN', 'qty': 10}], 'accents': 'été — n/d'}
    persist.save_json('rt.json', obj)
    assert persist.load_json('rt.json', None) == obj


def test_save_failure_is_silent_by_contract(tmp_persist, monkeypatch):
    monkeypatch.setattr(persist, 'cache_path',
                        lambda n: os.path.join(str(tmp_persist), 'dossier/absent', n))
    persist.save_json('x.json', {'a': 1})   # ne doit JAMAIS lever (cache best-effort)


def test_cache_path_joins_repo_base(tmp_persist):
    p = persist.cache_path('desk_data.json')
    assert p == os.path.join(str(tmp_persist), 'desk_data.json')


def test_ibkr_disabled_is_offline_with_action():
    snap = cx.snapshot({}, ibkr_enabled=False)
    ibkr = next(c for c in snap['connections'] if c['name'] == 'IBKR')
    assert ibkr['status'] == cx.OFFLINE and ibkr['configured'] is False
    assert 'TWS' in ibkr['action']


def test_ibkr_enabled_without_session_never_claims_live():
    snap = cx.snapshot({}, ibkr_enabled=True)
    ibkr = next(c for c in snap['connections'] if c['name'] == 'IBKR')
    assert ibkr['status'] == cx.OFFLINE, 'configuré ≠ connecté — jamais LIVE sans preuve'
    assert 'jamais présenté comme connecté' in ibkr['detail']


def test_ibkr_connected_delayed_and_live_states():
    delayed = next(c for c in cx.snapshot({'ibkr_connected': True},
                                          ibkr_enabled=True)['connections']
                   if c['name'] == 'IBKR')
    live = next(c for c in cx.snapshot({'ibkr_live': True},
                                       ibkr_enabled=True)['connections']
                if c['name'] == 'IBKR')
    assert delayed['status'] == cx.DELAYED
    assert live['status'] == cx.LIVE
    assert 'lecture seule' in live['detail'], 'le READONLY reste dit même en LIVE'


def test_all_statuses_canonical_and_readonly_always_true():
    snap = cx.snapshot({}, ibkr_enabled=False)
    for c in snap['connections']:
        assert c['status'] in cx.CANONICAL_STATUSES, c['name']
    assert snap['readonly'] is True


def test_demo_mode_labels_every_connection():
    snap = cx.snapshot({}, ibkr_enabled=False, demo_mode=True)
    assert snap['demo'] is True
    assert all(c.get('demo') is True for c in snap['connections'])
