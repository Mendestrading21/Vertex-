"""Tests du thème VERTEX OBSIDIAN COPPER DEEP (§30/§36/§53).

Le bleu n'est plus une identité : aucun lien, bouton ou série principale
bleue. Les hard gates stratégiques (§7/§9) sont verrouillés ici aussi.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VXCSS = os.path.join(ROOT, 'vertex', 'static', 'vertex', 'css')
VXJS = os.path.join(ROOT, 'vertex', 'static', 'vertex', 'js')


def _read(*p):
    return open(os.path.join(*p), encoding='utf-8').read()


def _is_blueish(hexval: str) -> bool:
    h = hexval.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    # dominante bleue NETTE : b > r et > g, b élevé, ET rouge faible (le bleu vrai
    # a peu de rouge ; le violet des options en a beaucoup → non bleu)
    return b > r + 30 and b > g + 30 and b > 90 and r < 110


def test_no_blue_primary_theme():
    tokens = _read(VXCSS, 'tokens.css')
    for m in re.finditer(r'--vx-[a-z0-9-]+:\s*(#[0-9a-fA-F]{6})', tokens):
        assert not _is_blueish(m.group(1)), f'token bleu interdit : {m.group(0)}'


def test_no_blue_primary_buttons():
    css = _read(VXCSS, 'buttons.css')
    for m in re.finditer(r'#[0-9a-fA-F]{6}', css):
        assert not _is_blueish(m.group(0)), f'bouton bleu interdit : {m.group(0)}'
    assert 'var(--vx-brand-gradient)' in css   # CTA = orange/cuivre


def test_no_blue_in_ui_pages():
    """Zéro bleu jusque dans les pages bespoke (§36) — accents info/violet compris."""
    import glob
    offenders = []
    for path in glob.glob(os.path.join(ROOT, 'vertex', 'ui', '**', '*.py'), recursive=True):
        src = open(path, encoding='utf-8').read()
        for m in re.finditer(r'#[0-9a-fA-F]{6}', src):
            if _is_blueish(m.group(0)):
                offenders.append(f'{os.path.relpath(path, ROOT)}: {m.group(0)}')
    assert not offenders, 'couleurs bleues interdites dans l\'UI : ' + ', '.join(offenders)


def test_no_blue_main_series():
    theme = _read(VXJS, 'charts', 'chart-theme-obsidian-copper.js')
    series = re.search(r'series:\s*\[(.*?)\]', theme, re.S).group(1)
    for m in re.finditer(r'#[0-9a-fA-F]{6}', series):
        assert not _is_blueish(m.group(0)), f'série bleue interdite : {m.group(0)}'
    core = _read(VXJS, 'charts', 'chart-core.js')
    fallback = re.search(r'series:\s*\[(.*?)\]', core, re.S).group(1)
    for m in re.finditer(r'#[0-9a-fA-F]{6}', fallback):
        assert not _is_blueish(m.group(0)), f'repli série bleue : {m.group(0)}'


def test_rr_gate_is_two():
    """R:R < 2 → jamais ACHETER/RENFORCER (§7) — moteur ET contrats."""
    from vertex.strategy import executive_engine as ee
    from vertex.options import contract_scorer
    assert contract_scorer.MIN_REWARD_RISK == 2.0
    packet = {'symbol': 'TEST',
              'fundamental': {'score': 90}, 'catalysts': {'score': 90},
              'technical': {'score': 90, 'reward_risk': 1.9, 'timing_score': 90},
              'sentiment': {'score': 90},
              'data_quality': {'overall': 'FRESH', 'actionable_allowed': True},
              'reconciliation': {'actionable_allowed': True},
              'guard': {'blocking_rules': [], 'mandatory_reviews': []}}
    out = ee.decide(packet)
    assert out['final_decision'] not in ('ACHETER', 'RENFORCER')
    assert 'RR_BELOW_MINIMUM' in out['blocking_rules']
    packet['technical']['reward_risk'] = 2.5
    out2 = ee.decide(packet)
    assert 'RR_BELOW_MINIMUM' not in out2['blocking_rules']


def test_unknown_regime_blocks_risk():
    """Régime UNKNOWN (confiance 0, 0 dimension) → risque neuf BLOQUÉ (§9)."""
    from vertex.market.regime_engine import classify_regime
    from vertex.strategy import executive_engine as ee
    reg = classify_regime({})
    assert reg['regime'] == 'UNKNOWN'
    adj = reg['adjustments']
    assert adj['new_risk_allowed'] is False
    assert adj['setup_priority'] == 'ATTENDRE'
    packet = {'symbol': 'TEST',
              'fundamental': {'score': 95}, 'catalysts': {'score': 95},
              'technical': {'score': 95, 'reward_risk': 3.0, 'timing_score': 95},
              'sentiment': {'score': 95},
              'data_quality': {'overall': 'FRESH', 'actionable_allowed': True},
              'reconciliation': {'actionable_allowed': True},
              'guard': {'blocking_rules': [], 'mandatory_reviews': []},
              'market_regime': reg}
    out = ee.decide(packet)
    assert out['final_decision'] == 'ATTENDRE'
    assert 'REGIME_BLOCKS_NEW_RISK' in out['blocking_rules']


def test_brief_has_sources():
    from vertex.market.daily_brief import build_daily_brief
    b = build_daily_brief({'source': 'demo'}, {'items': []}, [])
    assert isinstance(b['sources'], list) and b['sources']
    assert b['generator'] == 'deterministic'


def test_brief_has_timestamp():
    from vertex.market.daily_brief import build_daily_brief
    assert build_daily_brief({'source': 'demo'}, {'items': []}, [])['as_of']


def test_brief_does_not_invent_news():
    """Flux vide → la section actualité DIT que le flux est vide."""
    from vertex.market.daily_brief import build_daily_brief
    b = build_daily_brief({'source': 'demo'}, {'items': []}, [])
    dom = next(s for s in b['sections'] if s['label'] == 'Actualité dominante')
    assert 'hors ligne' in dom['text'] or 'aucun événement' in dom['text'].lower()
    assert b['what_changed'] == []


def test_news_is_deduplicated():
    from vertex.market.news_dedup import deduplicate
    evs = [{'title': 'Fed raises rates by 25bp', 'source': 'A', 'time': '1'},
           {'title': 'FED RAISES rates by 25bp', 'source': 'B', 'time': '2'}]
    out = deduplicate(evs)
    assert len(out) == 1 and out[0]['corroborations'] == 2


def test_startup_checks_connections():
    from vertex.services.startup import run_startup_sequence
    rep = run_startup_sequence({})
    steps = [s['step'] for s in rep['steps']]
    for expected in ('configuration', 'claude', 'ibkr', 'tradingview',
                     'storage', 'engines', 'scheduler', 'live_stream'):
        assert expected in steps
    assert rep['order_execution'] == 'disabled-by-design'


def test_claude_outage_uses_fallback():
    from vertex.ai import health
    h = health.health()
    assert h['status'] in ('MISSING', 'CONFIGURED', 'CONNECTED', 'DEGRADED')
    assert 'déterministe' in h['fallback']


def test_company_twin_never_invents():
    from vertex.companies import company_twin
    t = company_twin('ZZZZ', {})
    assert t['fundamentals'] is None and t['scan'] is None
    assert 'scan' in t['missing'] and 'fondamentaux' in t['missing']


def test_change_detector_triggers_recalc():
    from vertex.companies.change_detector import detect_changes
    before = {'scan': {'score': 80, 'verdict': 'BUY'}, 'fundamentals': {'pe': 30}}
    after = {'scan': {'score': 80, 'verdict': 'AVOID'}, 'fundamentals': {'pe': 30}}
    r = detect_changes(before, after)
    assert r['changed'] and r['recalc_required']
    assert any(c['kind'] == 'DECISION_CHANGED' for c in r['changes'])
    same = detect_changes(before, before)
    assert not same['changed'] and not same['recalc_required']
