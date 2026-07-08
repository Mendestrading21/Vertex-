"""
tests/test_real_data.py — Connexions données réelles (macro, news+, trimestres, IBKR).

Calendrier macro daté (FOMC publiés, NFP calculés, CPI indicatif), repli
RSS + sentiment lexical, historique trimestriel robuste, et l'import
positions IBKR avec ses erreurs honnêtes hors connexion.
"""

from datetime import date

from vertex.data import macro_calendar
from vertex.services import news_plus


# ─── Macro réel ───

def test_fomc_dates_are_published_2026_calendar():
    assert date(2026, 7, 29) in macro_calendar.FOMC_2026
    assert len(macro_calendar.FOMC_2026) == 8


def test_macro_events_sorted_dated_flagged():
    evs = macro_calendar.events(horizon_days=90, today=date(2026, 7, 8))
    assert evs and all(e['dte'] >= 0 for e in evs)
    assert [e['date'] for e in evs] == sorted(e['date'] for e in evs)
    kinds = {e['kind'] for e in evs}
    assert kinds == {'FOMC', 'NFP', 'CPI'}
    # NFP : premier vendredi (août 2026 → le 7)
    nfp = [e for e in evs if e['kind'] == 'NFP']
    assert any(e['date'] == '2026-08-07' for e in nfp)
    # CPI honnête : marqué indicatif ; FOMC : exact
    assert all(e['approx'] for e in evs if e['kind'] == 'CPI')
    assert all(not e['approx'] for e in evs if e['kind'] == 'FOMC')
    # FOMC du 29 juillet visible à J-21
    assert any(e['date'] == '2026-07-29' and e['dte'] == 21 for e in evs)


def test_cal_feed_carries_macro():
    import terminal
    j = terminal.app.test_client().get('/cal-feed').get_json()
    assert 'macro' in j and isinstance(j['macro'], list)


# ─── News multi-sources + sentiment ───

def test_sentiment_lexical():
    assert news_plus.sentiment('Nvidia beats estimates, shares surge') == 1
    assert news_plus.sentiment('Apple faces lawsuit as shares plunge') == -1
    assert news_plus.sentiment('Company holds annual meeting') == 0
    assert news_plus.sentiment('Le titre bondit après des résultats record') == 1


def test_parse_rss_sample():
    xml = """<?xml version="1.0"?><rss><channel>
      <item><title>NVDA hits record high - Reuters</title>
        <link>https://x/1</link><pubDate>Tue, 07 Jul 2026 12:00:00 GMT</pubDate>
        <source url="https://reuters.com">Reuters</source></item>
      <item><title>Chip demand surges - Bloomberg</title><link>https://x/2</link>
        <pubDate>Tue, 07 Jul 2026 11:00:00 GMT</pubDate></item>
    </channel></rss>"""
    items = news_plus.parse_rss(xml)
    assert len(items) == 2
    assert items[0]['publisher'] == 'Reuters' and items[0]['title'].startswith('NVDA')
    assert items[1]['publisher'] == 'Bloomberg'      # extrait du suffixe du titre
    assert news_plus.parse_rss('pas du xml') == []


def test_aggregate_by_ticker():
    ag = news_plus.aggregate([{'sym': 'NVDA', 'senti': 1}, {'sym': 'NVDA', 'senti': 1},
                              {'sym': 'AAPL', 'senti': -1}])
    assert ag['NVDA'] == {'score': 1.0, 'n': 2}
    assert ag['AAPL']['score'] == -1.0


def test_news_feed_exposes_sentiment():
    import terminal
    from vertex.app.state import news_state
    saved = dict(news_state)
    try:
        news_state['items'] = [{'sym': 'NVDA', 'title': 'record surge', 'senti': 1}]
        j = terminal.app.test_client().get('/news-feed').get_json()
        assert j['sentiment']['NVDA']['score'] == 1.0
    finally:
        news_state.clear()
        news_state.update(saved)


def test_news_loop_has_rss_fallback_and_sentiment():
    src = open('terminal.py', encoding='utf-8').read()
    assert '_news_plus.rss_news(sym' in src
    assert "_news_plus.sentiment(" in src


# ─── Trimestres ───

def test_quarters_survives_bad_ticker():
    from vertex.data import company

    class Boom:
        @property
        def quarterly_income_stmt(self):
            raise RuntimeError('réseau coupé')
    assert company._quarters(Boom()) == []

    import pandas as pd

    class Fake:
        quarterly_income_stmt = pd.DataFrame(
            {'2026-03-31': [1000.0, 100.0], '2025-12-31': [900.0, 90.0]},
            index=['Total Revenue', 'Net Income'])
    q = company._quarters(Fake())
    assert len(q) == 2 and q[0]['q'] == '2025-12-31'          # chronologique
    assert q[-1]['rev'] == 1000 and q[-1]['ni'] == 100


# ─── Import positions IBKR ───

def test_ibkr_positions_offline_is_honest_503():
    import terminal
    r = terminal.app.test_client().get('/api/ibkr/positions')
    assert r.status_code == 503
    j = r.get_json()
    assert j['ok'] is False and 'IBKR' in j['err'] and j['positions'] == []


def test_worker_and_desk_button_wired():
    src = open('terminal.py', encoding='utf-8').read()
    assert "elif kind == 'positions':" in src                 # worker lecture seule
    assert 'dkImportIBKR' in src                              # bouton Desk
    assert 'importé TWS (réel)' in src                        # note sur les positions importées
    assert 'long only' in src                                 # les shorts sont ignorés, pas déformés
