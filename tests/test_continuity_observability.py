"""CONTINUITY LOT 6 — observabilité (§18).

Métriques de cache exposées par le core, panneau « Continuité » dans Système
(navigation / cache / session / connexion / prix). Contrats statiques.
"""
import os
from pathlib import Path

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('DEMO', '1')

import pytest

import terminal

ROOT = Path(__file__).resolve().parents[1]
CORE = (ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'vx-core.js').read_text(encoding='utf-8')
SYS = (ROOT / 'vertex' / 'ui' / 'pages' / 'system_page.py').read_text(encoding='utf-8')


@pytest.fixture(scope='module')
def client():
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def test_cache_stats_exposed():
    assert 'VX.fetch.stats' in CORE
    for k in ('hits', 'misses', 'dedup', 'hit_rate', 'entries'):
        assert k in CORE, k


def test_continuity_panel_in_system_page():
    assert 'loadContinuity' in SYS
    assert 'vx-continuity' in SYS
    for label in ('Shell persistant', 'Taux de hits', 'Tickers suivis'):
        assert label in SYS, label


def test_continuity_panel_registered_in_data_view():
    assert "loadContinuity()" in SYS
    assert "'continuity'" in SYS       # tâche de rafraîchissement de page


def test_system_data_view_renders(client):
    """La vue Données rend le conteneur du panneau Continuité."""
    html = client.get('/system?view=data').get_data(as_text=True)
    assert 'vx-continuity' in html
    assert 'Continuit' in html
