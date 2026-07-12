"""Tests — enrichissement Claude+web & honnêteté de provenance (§28).

Invariants vérifiés :
- une valeur Claude porte TOUJOURS sa source, jamais déguisée en broker réel ;
- un chiffre n'est conservé QUE si une recherche web réelle a eu lieu (citations) ;
- sans clé/provider → statut MISSING, AUCUN chiffre inventé ;
- langage de certitude → la cotation est rejetée (absente) ;
- précédence honnête broker > claude_web > absent.
"""
import pytest

from vertex.ai import enrichment as E
from vertex.ai import provenance as P


# ─────────────────────────────────────────── provenance
def test_wrap_marks_claude_as_estimation_not_broker():
    env = P.wrap(123.45, source=P.SRC_CLAUDE_WEB,
                 citations=[{'title': 'Yahoo', 'url': 'https://finance.yahoo.com/x'}])
    assert env['value'] == 123.45
    assert env['estimation'] is True
    assert env['is_real_broker'] is False
    assert env['source_label'] == 'via Claude · web · différé'
    assert env['citations'][0]['url'].startswith('https://')


def test_broker_is_the_only_real_source():
    assert P.wrap(10, source=P.SRC_BROKER)['is_real_broker'] is True
    assert P.wrap(10, source=P.SRC_CLAUDE_WEB)['is_real_broker'] is False
    assert P.wrap(10, source=P.SRC_CLAUDE)['is_real_broker'] is False


def test_absent_is_none_never_zero():
    a = P.absent('pas de donnée')
    assert a['value'] is None
    assert a['source'] == P.SRC_NONE
    assert a['estimation'] is False


def test_prefer_broker_over_claude_over_absent():
    broker = P.wrap(100, source=P.SRC_BROKER)
    claude = P.wrap(101, source=P.SRC_CLAUDE_WEB)
    assert P.prefer(claude, broker)['source'] == P.SRC_BROKER
    assert P.prefer(P.absent(), claude)['source'] == P.SRC_CLAUDE_WEB
    assert P.prefer(P.absent(), P.absent())['value'] is None


def test_citations_without_url_are_dropped():
    env = P.wrap(1, source=P.SRC_CLAUDE_WEB, citations=[{'title': 'x'}, {'url': 'https://a.b'}])
    assert len(env['citations']) == 1


# ─────────────────────────────────────────── garde-fou : chiffre sans recherche
def test_quote_dropped_when_no_web_search_happened():
    # data a un prix mais aucune citation ET searches=0 → on refuse le chiffre.
    res = {'data': {'price': 200.0}, 'citations': [], 'searches': 0, 'text': '200'}
    env = E.parse_quote(res)
    assert env['value'] is None            # jamais un chiffre non sourcé
    assert env['source'] == P.SRC_NONE


def test_quote_kept_when_search_with_citations():
    res = {'data': {'price': 198.5, 'currency': 'USD', 'change_pct': 1.2, 'note': 'Yahoo différé'},
           'citations': [{'title': 'Yahoo', 'url': 'https://finance.yahoo.com/quote/ACN'}],
           'searches': 1, 'text': 'Le cours est 198.5'}
    env = E.parse_quote(res)
    assert env['value'] == 198.5
    assert env['source'] == P.SRC_CLAUDE_WEB
    assert env['change_pct'] == 1.2
    assert env['citations']


def test_quote_rejected_on_certainty_language():
    res = {'data': {'price': 198.5}, 'citations': [{'url': 'https://x.y'}],
           'searches': 1, 'text': 'gain garanti, cours 198.5'}
    env = E.parse_quote(res)
    assert env['value'] is None            # langage de certitude → rejeté


def test_quote_null_price_is_absent():
    res = {'data': {'price': None}, 'citations': [{'url': 'https://x.y'}], 'searches': 1}
    assert E.parse_quote(res)['value'] is None


def test_news_parsing_normalizes_impact_and_drops_empty():
    res = {'data': {'items': [
        {'headline': 'Résultats en hausse', 'impact': 'bidon', 'why': 'beat', 'date': '2026-07-10'},
        {'headline': '', 'impact': 'HAUSSIER'},
    ]}, 'citations': [{'url': 'https://n.ews/a'}], 'searches': 1}
    env = E.parse_news(res)
    assert env['value'][0]['impact'] == 'NEUTRE'      # 'bidon' normalisé
    assert len(env['value']) == 1                     # entrée vide supprimée
    assert env['source'] == P.SRC_CLAUDE_WEB


def test_news_absent_when_no_items():
    res = {'data': {'items': []}, 'citations': [], 'searches': 1}
    assert E.parse_news(res)['value'] is None


# ─────────────────────────────────────────── sans clé : MISSING, zéro fabrication
class _UnavailableProvider:
    model = 'claude-sonnet-5'

    def available(self):
        return False


def test_run_without_provider_is_missing_and_fabricates_nothing():
    snap = E.run(['ACN', 'ABT'], provider=_UnavailableProvider(), persist_store=False)
    assert snap['status'] == E.STATUS_MISSING
    assert snap['surfaces']['quotes'] == {}
    assert 'ANTHROPIC_API_KEY' in snap['note']


# ─────────────────────────────────────────── run avec provider simulé
class _FakeProvider:
    model = 'claude-sonnet-5-test'

    def available(self):
        return True

    def research_json(self, system, user):
        # Simule une recherche web aboutie avec citation.
        if 'actualité' in user or 'items' in user:
            return {'data': {'items': [{'headline': 'News', 'impact': 'HAUSSIER',
                                        'why': 'catalyseur', 'date': '2026-07-11'}]},
                    'citations': [{'url': 'https://n.ews/x'}], 'searches': 1}
        return {'data': {'price': 150.0, 'currency': 'USD', 'note': 'Yahoo différé'},
                'citations': [{'title': 'Yahoo', 'url': 'https://finance.yahoo.com/q'}],
                'searches': 1, 'text': 'cours 150'}


def test_run_with_fake_provider_produces_sourced_estimates():
    snap = E.run(['ACN'], provider=_FakeProvider(), persist_store=False)
    assert snap['status'] == E.STATUS_OK
    q = snap['surfaces']['quotes']['ACN']
    assert q['value'] == 150.0
    assert q['is_real_broker'] is False and q['estimation'] is True
    assert q['citations'][0]['url'].startswith('https://')
    assert snap['surfaces']['news']['ACN']['value'][0]['impact'] == 'HAUSSIER'


def test_run_caps_symbol_count():
    many = ['S%02d' % i for i in range(100)]
    snap = E.run(many, provider=_UnavailableProvider(), persist_store=False)
    assert len(snap['symbols']) <= E.MAX_SYMBOLS


# ─────────────────────────────────────────── extraction du web_provider
def test_web_provider_extracts_text_and_citations_from_fake_message():
    from vertex.ai.web_provider import ClaudeWebProvider

    class _Cit:
        def __init__(self, url, title):
            self.url = url
            self.title = title

    class _Block:
        def __init__(self, type, text=None, citations=None):
            self.type = type
            self.text = text
            self.citations = citations

    class _Msg:
        model = 'claude-sonnet-5'
        content = [
            _Block('server_tool_use'),
            _Block('web_search_tool_result'),
            _Block('text', text='Cours 150 $. ',
                   citations=[_Cit('https://finance.yahoo.com/q', 'Yahoo')]),
            _Block('text', text='Source fiable.', citations=None),
        ]

    out = ClaudeWebProvider._extract(_Msg())
    assert out['text'] == 'Cours 150 $. Source fiable.'
    assert out['citations'] == [{'title': 'Yahoo', 'url': 'https://finance.yahoo.com/q'}]
    assert out['searches'] == 2


def test_web_provider_unavailable_without_key(monkeypatch):
    from vertex.ai.web_provider import ClaudeWebProvider
    p = ClaudeWebProvider(api_key='')
    assert p.available() is False
