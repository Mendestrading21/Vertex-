"""tests/test_ai_health.py — SKYLER LOT 112 : santé du runtime IA figée.

Trou réel de couverture : vertex/ai/health.py (§10 — l'état Claude
affiché par Système et le rapport de démarrage) n'avait qu'UN usage
superficiel en test (statut ∈ ensemble). Sa promesse centrale — jamais
« CONNECTED » sans preuve d'appel réel, aucun réseau spontané — n'était
figée nulle part.
Caractérisations nées vertes (dites) — moteur INTACT ; état module
_LAST sauvegardé/restauré, env via monkeypatch.
"""
import pytest

from vertex.ai import health as H


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    saved = dict(H._LAST)
    H._LAST.update({'ok_ts': None, 'err_ts': None, 'error': None})
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
    monkeypatch.delenv('ANTHROPIC_MODEL', raising=False)
    yield
    H._LAST.update(saved)


def test_without_key_missing_with_honest_note():
    h = H.health()
    assert h == {'status': 'MISSING', 'configured': False, 'model': None,
                 'fallback': 'déterministe (moteurs)',
                 'note': 'ANTHROPIC_API_KEY absente — synthèse déterministe servie.'}


def test_with_key_but_no_call_is_configured_never_connected(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'sk-test')
    h = H.health()
    assert h['status'] == 'CONFIGURED', (
        'une clé n\'est pas une preuve — CONNECTED exige un appel réel')
    assert h['last_success'] is None


def test_recorded_success_proves_connected(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'sk-test')
    H.record_success()
    h = H.health()
    assert h['status'] == 'CONNECTED' and h['last_success'] is not None
    assert h['last_error'] is None


def test_failure_after_success_degrades_and_truncates(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'sk-test')
    H.record_success()
    H._LAST['ok_ts'] -= 10                    # le succès date d'avant
    H.record_failure('boom ' + 'x' * 500)
    h = H.health()
    assert h['status'] == 'DEGRADED'
    assert len(h['last_error']) == 200


def test_success_after_failure_reconnects(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'sk-test')
    H.record_failure('panne')
    H._LAST['err_ts'] -= 10
    H.record_success()
    h = H.health()
    assert h['status'] == 'CONNECTED', 'le DERNIER appel réel fait foi'
    assert h['last_error'] is None            # le succès efface l\'erreur


def test_model_default_and_override(monkeypatch):
    assert H.model() == 'claude-sonnet-5'     # défaut documenté
    monkeypatch.setenv('ANTHROPIC_MODEL', '  claude-perso  ')
    assert H.model() == 'claude-perso'        # strip appliqué


def test_whitespace_key_is_not_configured(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', '   ')
    assert H.configured() is False
    assert H.health()['status'] == 'MISSING'


def test_key_value_never_leaks_into_report(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'sk-secret-tres-prive')
    H.record_success()
    assert 'sk-secret' not in repr(H.health()), (
        'le rapport de santé ne contient jamais la clé — statuts seulement')
