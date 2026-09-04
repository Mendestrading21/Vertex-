"""tests/test_config_validation.py — SKYLER LOT 111 : validation de config figée.

Trou réel de couverture : vertex/app/config_validation.py (§11 — le
diagnostic de configuration affiché par Système et le rapport de
démarrage) n'avait AUCUN test direct (consommé via startup seulement).
Ses promesses — jamais une valeur de secret exposée, conséquence exacte
pour chaque absence, alias historiques — n'étaient figées nulle part.
Caractérisations nées vertes (dites) — moteur INTACT ; environnement
manipulé exclusivement via monkeypatch.
"""
from vertex.app.config_validation import _SPEC, validate_config


def _clean(monkeypatch):
    for name, *_ in _SPEC:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.delenv('TRADINGVIEW_SECRET', raising=False)


def test_missing_variable_names_its_exact_consequence(monkeypatch):
    _clean(monkeypatch)
    out = validate_config()
    code = out['VERTEX_CODE']
    assert code['status'] == 'MISSING' and code['required'] is False
    assert '127.0.0.1' in code['consequence'], (
        'chaque absence dit sa conséquence — jamais une panne silencieuse')
    assert out['_summary']['missing'] == len(_SPEC)


def test_invalid_value_is_named_not_silently_accepted(monkeypatch):
    _clean(monkeypatch)
    monkeypatch.setenv('VERTEX_CODE', 'abc')            # < 4 caractères
    monkeypatch.setenv('IBKR_PORT', 'pas-un-port')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'mauvais-prefixe')
    out = validate_config()
    for k in ('VERTEX_CODE', 'IBKR_PORT', 'ANTHROPIC_API_KEY'):
        assert out[k]['status'] == 'INVALID', k
    assert out['_summary']['invalid'] == 3


def test_no_secret_value_is_ever_echoed(monkeypatch):
    _clean(monkeypatch)
    monkeypatch.setenv('VERTEX_SECRET', 'super-secret-de-seize-caracteres')
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'sk-vrai-secret-api')
    out = validate_config()
    dump = repr(out)
    assert 'super-secret' not in dump and 'sk-vrai' not in dump, (
        'le rapport ne contient JAMAIS une valeur — statuts seulement')
    assert out['VERTEX_SECRET']['status'] == 'CONFIGURED'
    assert 'consequence' not in out['VERTEX_SECRET'], (
        'configuré : plus de conséquence à annoncer')


def test_tradingview_legacy_alias_is_accepted(monkeypatch):
    _clean(monkeypatch)
    monkeypatch.setenv('TRADINGVIEW_SECRET', 'ancien-alias-12car')
    out = validate_config()
    assert out['TRADINGVIEW_WEBHOOK_SECRET']['status'] == 'CONFIGURED', (
        'compat .env historiques : l\'alias vaut la variable canonique')


def test_whitespace_only_value_is_missing_not_configured(monkeypatch):
    _clean(monkeypatch)
    monkeypatch.setenv('IBKR_HOST', '   ')
    assert validate_config()['IBKR_HOST']['status'] == 'MISSING'


def test_market_data_mode_enum_case_insensitive(monkeypatch):
    _clean(monkeypatch)
    monkeypatch.setenv('IBKR_MARKET_DATA_MODE', 'delayed')
    assert validate_config()['IBKR_MARKET_DATA_MODE']['status'] == 'CONFIGURED'
    monkeypatch.setenv('IBKR_MARKET_DATA_MODE', 'TURBO')
    assert validate_config()['IBKR_MARKET_DATA_MODE']['status'] == 'INVALID'


def test_summary_counts_add_up_and_ignore_private_keys(monkeypatch):
    _clean(monkeypatch)
    monkeypatch.setenv('VERTEX_TIMEZONE', 'Europe/Zurich')
    monkeypatch.setenv('IBKR_PORT', '7496')
    monkeypatch.setenv('VERTEX_CODE', 'ab')             # invalide
    out = validate_config()
    s = out['_summary']
    assert s == {'configured': 2, 'missing': len(_SPEC) - 3, 'invalid': 1}
    assert s['configured'] + s['missing'] + s['invalid'] == len(_SPEC)


def test_no_variable_is_hard_required_readonly_by_design(monkeypatch):
    _clean(monkeypatch)
    out = validate_config()
    assert all(v['required'] is False for k, v in out.items()
               if not k.startswith('_')), (
        'aucune variable obligatoire : l\'app démarre toujours, en mode sûr')
    assert 'READONLY=True en dur' in out['VERTEX_READONLY']['consequence']
