"""SKYLER LOT 619 — gardiens de la fiche Analyse « décision d'abord ».

Le lot reste strictement présentationnel : les routes et les hôtes historiques
demeurent, mais une seule Carte-Verdict est ouverte. Les moteurs secondaires,
les anomalies détaillées et les outils de préparation vivent derrière une
divulgation progressive. Le graphique ne transforme jamais une donnée absente
en zéro et un catalyseur futur n'est jamais posé sur la dernière bougie passée.
"""
from __future__ import annotations

from html.parser import HTMLParser
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'vertex/ui/pages/analysis_page.py'
THEME = ROOT / 'vertex/static/vertex/css/neon-glass.css'
CHART_CORE = ROOT / 'vertex/static/vertex/js/charts/chart-core.js'
ANOMALY_CHART = ROOT / 'vertex/static/vertex/js/charts/anomaly-scan.js'
LWC_CHART = ROOT / 'vertex/static/vertex/js/charts/candlestick-lwc.js'


def _read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


@pytest.fixture(scope='module')
def analysis_html() -> str:
    import terminal

    response = terminal.app.test_client().get('/analysis/AAPL')
    assert response.status_code == 200
    return response.get_data(as_text=True)


class _DOM(HTMLParser):
    """Parse seulement le DOM initial ; le HTML écrit dans <script> reste du texte."""

    _VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
             'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, html: str):
        super().__init__(convert_charrefs=True)
        self.nodes: list[dict] = []
        self.stack: list[dict] = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attrs': dict(attrs),
                'ancestors': tuple(self.stack), 'order': len(self.nodes)}
        self.nodes.append(node)
        if tag not in self._VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self._VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                return

    def by_id(self, node_id: str) -> list[dict]:
        return [n for n in self.nodes if n['attrs'].get('id') == node_id]


def _classes(node: dict) -> set[str]:
    return set((node['attrs'].get('class') or '').split())


def _inside(node: dict, class_name: str) -> bool:
    return any(class_name in _classes(parent) for parent in node['ancestors'])


def _matching_brace(text: str, opening: int) -> int:
    depth = 0
    for i in range(opening, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return i
    raise AssertionError('bloc CSS non fermé')


def _media_ranges(css: str) -> list[tuple[int, int, str]]:
    ranges = []
    for match in re.finditer(r'@media\s*([^\{]+)\{', css):
        opening = match.end() - 1
        ranges.append((opening, _matching_brace(css, opening), match.group(1)))
    return ranges


def _rail_rules(css: str) -> list[tuple[str, list[str]]]:
    """Retourne (déclarations, contextes @media) pour .an-rail-stack."""
    media = _media_ranges(css)
    rules = []
    for match in re.finditer(r'([^{}]*\.an-rail-stack[^{}]*)\{([^{}]*)\}', css):
        contexts = [cond for start, end, cond in media if start < match.start() < end]
        rules.append((match.group(2), contexts))
    return rules


def test_analysis_dom_is_decision_first_then_chart_then_advanced_evidence(analysis_html):
    dom = _DOM(analysis_html)
    ids = ('an-hero', 'an-verdict', 'an-chart', 'an-skyler', 'an-anomaly',
           'an-anomalies', 'an-evidence', 'an-rail-decision')
    nodes = {}
    for node_id in ids:
        found = dom.by_id(node_id)
        assert len(found) == 1, f'{node_id}: attendu exactement une fois dans le DOM initial'
        nodes[node_id] = found[0]

    assert nodes['an-hero']['order'] < nodes['an-verdict']['order'] < nodes['an-chart']['order']
    for advanced in ('an-skyler', 'an-anomaly', 'an-anomalies',
                     'an-evidence', 'an-rail-decision'):
        assert nodes['an-chart']['order'] < nodes[advanced]['order'], advanced


def test_historical_analysis_hosts_are_preserved_once(analysis_html):
    dom = _DOM(analysis_html)
    historical = ('an-skyler', 'an-anomaly', 'an-anomalies', 'an-evidence',
                  'an-rail-decision', 'an-pretrade')
    for node_id in historical:
        assert len(dom.by_id(node_id)) == 1, node_id


def test_only_primary_verdict_is_open(analysis_html):
    dom = _DOM(analysis_html)
    verdict = dom.by_id('an-verdict')[0]
    assert not _inside(verdict, 'an-disclosure')

    # Les deux autres producteurs de lecture décisionnelle restent consultables,
    # mais ne concurrencent plus la Carte-Verdict au premier niveau.
    for secondary in ('an-skyler', 'an-rail-decision'):
        assert _inside(dom.by_id(secondary)[0], 'an-disclosure'), secondary


def test_advanced_evidence_is_progressive(analysis_html):
    dom = _DOM(analysis_html)
    for node_id in ('an-anomaly', 'an-anomalies', 'an-evidence'):
        assert _inside(dom.by_id(node_id)[0], 'an-disclosure'), node_id


def test_readonly_dimensioning_labels_cannot_be_mistaken_for_execution(analysis_html):
    for old in ('Préparer l’ordre (copier IBKR)',
                'Préparation d’ordre — READONLY',
                'Copier le ticket'):
        assert old not in analysis_html

    assert 'Calculer le dimensionnement' in analysis_html
    assert 'Copier l’analyse' in analysis_html
    assert 'aucune exécution' in analysis_html.lower()


def test_radar_keeps_missing_scores_missing():
    src = _read(PAGE)
    core = _read(CHART_CORE)
    compact = re.sub(r'\s+', '', src)
    assert 'Marge risque' in src
    assert 'Radar non tracé' in src
    assert 'value:a[1]||0' not in compact
    assert 'Number.isFinite(value)' in core
    assert 'Radar non tracé — axes n/d' in core
    assert 'Math.round(a.value || 0)' not in core


def test_analysis_freshness_comes_from_the_scan_not_the_http_cache():
    src = _read(PAGE)
    assert 'priceDomain.age_s' in src and 'priceDomain.ts' in src
    assert "VX.fetch.peek('/api/ticker/'" not in src
    assert "timestamp:(t&&t.detail&&t.detail.updated)||Date.now()" not in src


def test_future_catalyst_is_not_backdated_on_last_historical_candle(analysis_html):
    src = _read(PAGE)
    assert not re.search(
        r'events\.push\s*\(\s*\{\s*index\s*:\s*cut\.length\s*-\s*1', src)
    assert 'id="an-catalyst-strip"' in analysis_html
    assert src.count('an-catalyst-strip') >= 2, 'le strip doit avoir un hôte et un peintre'


def test_anomaly_chart_is_calm_and_names_its_scale_and_source():
    src = _read(ANOMALY_CHART)
    assert '<animate ' not in src
    assert "const line = 'var(--vx-brand" in src
    for label in ('clôtures du scan', 'Min ', 'Max ', 'Dernier ', 'Source '):
        assert label in src


def test_candlestick_locale_is_stable_on_linux_browsers():
    src = _read(LWC_CHART)
    assert "localization: { locale: 'fr-FR' }" in src


def test_async_copilot_and_predecision_outputs_are_announced(analysis_html):
    dom = _DOM(analysis_html)
    for node_id in ('an-cp-out', 'an-pt-out'):
        node = dom.by_id(node_id)
        assert len(node) == 1, node_id
        assert node[0]['attrs'].get('aria-live') == 'polite', node_id


def test_late_ticker_data_updates_the_primary_verdict_price():
    src = _read(PAGE)
    assert "'an-verdict-price'" in src
    assert "if(verdictPrice)verdictPrice.textContent" in src


def test_analysis_rail_is_sticky_only_on_desktop_and_static_at_1024(analysis_html):
    dom = _DOM(analysis_html)
    stacks = [n for n in dom.nodes if 'an-rail-stack' in _classes(n)]
    assert len(stacks) == 1
    assert 'position:sticky' not in analysis_html.replace(' ', '')

    css = re.sub(r'/\*.*?\*/', '', _read(THEME), flags=re.S)
    rules = _rail_rules(css)
    assert rules, 'règle CSS .an-rail-stack absente'

    sticky = [(body, ctx) for body, ctx in rules
              if re.search(r'position\s*:\s*sticky', body)]
    assert sticky, 'le rail doit rester sticky sur grand écran'
    assert all(any(re.search(r'min-width\s*:\s*1025px', cond) for cond in ctx)
               for _, ctx in sticky), 'sticky interdit hors media desktop >=1025px'

    static = [(body, ctx) for body, ctx in rules
              if re.search(r'position\s*:\s*static', body)]
    assert any(any(re.search(r'max-width\s*:\s*1024px', cond) for cond in ctx)
               for _, ctx in static), 'position:static requise à <=1024px'
