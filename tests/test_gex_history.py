"""tests/test_gex_history.py — journal quotidien du GEX : réel seulement, borné."""
import os
import tempfile

import pytest

from vertex.options import gex, gex_history
from vertex.services import persist


@pytest.fixture(autouse=True)
def _isolated_storage(monkeypatch, tmp_path):
    """Stockage isolé : ne touche jamais aux fichiers runtime réels."""
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    yield


def _profile():
    return gex.compute([
        {'type': 'CALL', 'strike': 105, 'gamma': 0.05, 'oi': 1000, 'spot': 100},
    ], symbol='TEST')


def test_record_and_series_roundtrip():
    assert gex_history.record(_profile()) is True
    s = gex_history.series('TEST')
    assert len(s) == 1
    assert s[0]['net_gex'] == 500000
    assert s[0]['spot'] == 100
    assert s[0]['date']


def test_same_day_last_writer_wins():
    gex_history.record(_profile())
    gex_history.record(_profile())
    assert len(gex_history.series('TEST')) == 1     # une entrée par jour


def test_empty_profile_never_recorded():
    assert gex_history.record(gex.compute([])) is False
    assert gex_history.series(None) == []


def test_series_unknown_symbol_empty():
    assert gex_history.series('NOPE') == []
