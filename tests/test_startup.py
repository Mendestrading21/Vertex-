"""tests/test_startup.py — SKYLER LOT 105 : séquence de démarrage figée.

Trou réel de couverture : vertex/services/startup.py — le test existant
(test_obsidian_theme) vérifie l'APPARTENANCE des 8 étapes, pas leur
ORDRE constitutionnel (§10), ni le contrat d'erreur de _step (jamais
bloquant), ni les statuts honnêtes par étape, ni le fait que
startup_report() rend une copie.
Caractérisations nées vertes (dites) — moteur INTACT ; état module
_REPORT restauré via monkeypatch quand un test le vierge.
"""
from vertex.services import startup as su


def test_steps_run_in_constitutional_order():
    rep = su.run_startup_sequence({})
    assert [s['step'] for s in rep['steps']] == [
        'configuration', 'claude', 'ibkr', 'tradingview',
        'storage', 'engines', 'scheduler', 'live_stream'], (
        'l\'ordre §10 est un contrat, pas un hasard')


def test_step_wrapper_never_raises_and_truncates_detail():
    def boom():
        raise RuntimeError('x' * 500)
    s = su._step('essai', boom)
    assert s['status'] == 'ERROR' and len(s['detail']) == 200
    assert s['step'] == 'essai' and isinstance(s['ms'], int)


def test_ibkr_step_status_matches_config_honestly():
    rep = su.run_startup_sequence({})
    ib = next(s for s in rep['steps'] if s['step'] == 'ibkr')
    if ib['status'] == 'OFFLINE':
        assert 'MODEL_ESTIMATE' in ib['detail'], 'sans IBKR : Greeks modèle, dit'
    else:
        assert ib['status'] == 'CONFIGURED' and 'readonly=True' in ib['detail'], (
            'jamais CONNECTED sans preuve — configuré seulement')


def test_tradingview_missing_secret_is_honest_503(monkeypatch):
    monkeypatch.delenv('TRADINGVIEW_WEBHOOK_SECRET', raising=False)
    monkeypatch.delenv('TRADINGVIEW_SECRET', raising=False)
    rep = su.run_startup_sequence({})
    tv = next(s for s in rep['steps'] if s['step'] == 'tradingview')
    assert tv['status'] == 'MISSING' and '503 honnête' in tv['detail']


def test_tradingview_with_secret_is_configured(monkeypatch):
    monkeypatch.setenv('TRADINGVIEW_WEBHOOK_SECRET', 'secret-de-test')
    rep = su.run_startup_sequence({})
    tv = next(s for s in rep['steps'] if s['step'] == 'tradingview')
    assert tv['status'] == 'CONFIGURED' and 'webhook signé' in tv['detail']


def test_report_asserts_readonly_and_ok_without_errors():
    rep = su.run_startup_sequence({})
    assert rep['ran'] is True and rep['readonly'] is True
    assert rep['order_execution'] == 'disabled-by-design'
    assert rep['ok'] is (not any(s['status'] == 'ERROR' for s in rep['steps']))
    storage = next(s for s in rep['steps'] if s['step'] == 'storage')
    assert storage['status'] == 'CONNECTED'      # répertoire inscriptible en test


def test_startup_report_returns_a_copy_not_the_state():
    su.run_startup_sequence({})
    rep = su.startup_report()
    rep['ran'] = 'falsifié'
    rep['steps'] = []
    assert su.startup_report()['ran'] is True, (
        'muter le rapport rendu ne touche jamais l\'état interne')


def test_before_any_run_report_is_honest_not_ran(monkeypatch):
    monkeypatch.setattr(su, '_REPORT', {'ran': False})
    assert su.startup_report() == {'ran': False}, (
        'avant la séquence : ran False, aucun statut inventé')
