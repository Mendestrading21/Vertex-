"""LOT 621 — hiérarchie décisionnelle d'Aujourd'hui et Marchés.

Ces gardiens vérifient la composition initiale et la divulgation progressive
sans figer des pixels. Les hôtes historiques restent présents pour les moteurs
et les états live/démo/n-d, mais les preuves répétées ne concurrencent plus la
question principale.
"""
from __future__ import annotations

import re

import pytest

import terminal
from vertex.ui.pages import briefing, markets_page


def _details_containing(src: str, needle: str) -> str:
    """Retourne le panneau details qui contient ``needle``."""
    for match in re.finditer(r'<details\b[^>]*>(.*?)</details>', src, re.S):
        if needle in match.group(1):
            return match.group(0)
    raise AssertionError(f'{needle!r} ne se trouve dans aucun disclosure')


def test_today_leads_with_one_decision_and_four_kpis():
    html = briefing._CONTENT
    js = briefing._JS

    for cls in ('vx-page-lead', 'vx-kpi-strip', 'vx-hero-grid',
                'vx-insight-rail', 'vx-toolbar', 'vx-section-stack',
                'vx-disclosure'):
        assert cls in html

    assert 'data-max-kpis="4"' in html
    assert html.index('id="vx-hero"') < html.index('id="vx-regime-body"')
    assert html.index('id="vx-regime-body"') < html.index('id="vx-opp-stocks"')
    assert 'class="vx-today-decision"' in js
    assert ".map(l=>esc(l)).join('<br>')" not in js

    # Quatre emplacements runtime : régime, breadth, VIX et meilleure opportunité.
    for label in ("kpiTile('Régime'", "kpiTile('Breadth'",
                  "kpiTile('VIX'", "kpiTile('Meilleure opp.'"):
        assert label in js


def test_today_keeps_one_regime_visual_and_relegates_deep_context():
    html = briefing._CONTENT
    details = _details_containing(html, 'id="vx-calendar"')

    assert 'id="vx-portfolio"' in details
    assert html.index('id="vx-opp-stocks"') < html.index('<details')
    assert html.index('id="vx-alerts"') < html.index('<details')
    assert briefing._JS.count('VXCharts.regimeAura(') == 1
    assert 'timestamp:r&&(r.as_of||r.timestamp||r.updated)||null' in briefing._JS


def test_today_freshness_and_changelog_are_compact_and_sourced():
    js = briefing._JS

    assert 'Fraîcheur de l’analyse' in js
    assert 'lecture seule' in js
    assert "chip('VIX'" not in js
    assert "chip('Opportunités'" not in js
    assert '.slice(0,3)' in js
    assert 'Source : comparaison locale de cette session' in js
    assert 'MarketContext déterministe' in js


def test_markets_overview_is_four_kpis_one_main_chart_and_leadership():
    """VERTEX 2.0 — même intention, structure canonique.

    Le banc gardait « la comparaison des indices et les mouvements ne
    concurrencent pas le graphique de référence au premier écran ». Ils
    vivaient repliés dans un `<details>` de la Synthèse ; ils ont désormais
    leur sous-vue `indices` (« Indices & cross-asset » du contrat de page).
    La garantie est plus forte, pas plus faible : ils ne sont plus sur le
    premier écran DU TOUT, et leur URL est partageable.
    """
    html = markets_page._VIEW_CONTENT['overview']
    indices = markets_page._VIEW_CONTENT['indices']

    # Le premier écran : régime, risque, graphique de référence, leadership.
    assert html.index('id="vx-mk-spy"') < html.index('id="vx-mk-leader"')
    assert 'id="vx-mk-regime"' in html and 'id="vx-mk-risk"' in html

    # Ce qui a déménagé ne doit être NI perdu, NI resté sur la Synthèse.
    for cible in ('id="vx-mk-strip"', 'id="vx-mk-multi"',
                  'id="vx-mk-top"', 'id="vx-mk-flop"'):
        assert cible not in html, cible + ' est resté sur la Synthèse'
        assert cible in indices, cible + ' a disparu au lieu de déménager'
    assert 'id="vx-mk-spy"' not in indices
    assert 'class="vx-kpi-strip' in indices and 'data-max-kpis="4"' in indices

    # La Synthèse dit OÙ ils sont partis — un déménagement muet est une perte.
    assert '?view=indices' in html

    assert "IDX_MAIN.filter" in markets_page._JS and '.slice(0,4)' in markets_page._JS
    assert 'vx-mk-regime-gauge' not in markets_page._JS


def test_markets_macro_limits_and_extra_assets_are_details():
    html = markets_page._VIEW_CONTENT['macro']
    details = _details_containing(html, 'Limites des données')

    assert 'data-max-kpis="4"' in html
    assert html.index('id="vx-mk-macro-kpis"') < html.index('id="vx-mk-yield"')
    assert 'id="vx-mk-macro-extra"' in details
    assert 'maturités intermédiaires' in details
    assert 'const primary=known.slice(0,4),extra=known.slice(4);' in markets_page._JS

    match = re.search(r'<div class="([^"]*)" id="vx-mk-macro-regime"', html)
    assert match and 'vx-grid' in match.group(1)


def test_markets_breadth_prioritises_trend_and_relegates_advanced_views():
    html = markets_page._VIEW_CONTENT['breadth']
    details = _details_containing(html, 'id="vx-mk-funnel"')

    assert html.index('id="vx-mk-breadth-trend"') < html.index('<details')
    assert html.index('id="vx-mk-breadth-gauge"') < html.index('<details')
    assert 'vx-insight-rail' in html[:html.index('<details')]
    for host in ('vx-mk-verdicts', 'vx-mk-internals-card', 'vx-mk-dist-card',
                 'vx-mk-health-card'):
        assert f'id="{host}"' in details

    # L'hôte historique demeure, mais il est devenu KPI + rail : aucune jauge dupliquée.
    assert "VXCharts.gauge('vx-mk-breadth-gauge'" not in markets_page._JS
    assert 'Participation non calculée' in markets_page._JS
    assert 'vx-mk-breadth-trend' in markets_page._JS


def test_markets_volatility_has_one_vix_visual_and_text_context():
    html = markets_page._VIEW_CONTENT['volatility']
    details = _details_containing(html, 'id="vx-mk-vol-rail"')
    js = markets_page._JS

    assert 'vx-card vx-card--hero' in html
    #  VERTEX 2.0 : l'en-tête passe par `vx2.page_header`. L'intention —
    #  la page porte un en-tête canonique et sa question métier — tient.
    entete = markets_page._entete()
    assert 'vx2-header' in entete and 'vx2-question' in entete
    assert html.index('id="vx-mk-vix"') < html.index('<details')
    assert 'IV par symbole' in details
    assert "VXCharts.gauge('vx-mk-vix-gauge'" not in js
    assert js.count('vx-rail--stress') == 1
    assert 'Positionnement — Défense ↔ Attaque' not in js
    assert 'VIX non fourni' in js


def test_data_contracts_and_readonly_are_preserved():
    src = briefing._JS + markets_page._JS

    for endpoint in ('/scan', '/api/market/regime', '/api/market/summary',
                     '/api/market/context', '/api/briefing/editorial',
                     '/api/session/digest', '/cal-feed'):
        assert endpoint in src
    for state in ('Démo', 'Périmé', 'Indisponible', 'n/d'):
        assert state in src
    for forbidden in ('placeOrder', 'place_order', 'submitOrder', 'transmit'):
        assert forbidden not in src


@pytest.fixture(scope='module')
def client():
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


@pytest.mark.parametrize('url, marker', [
    ('/', 'vx-today-decision'),
    ('/markets?view=overview', 'vx-markets-overview-details'),
    ('/markets?view=macro', 'vx-markets-macro-details'),
    ('/markets?view=breadth', 'vx-markets-breadth-details'),
    ('/markets?view=volatility', 'vx-markets-volatility-details'),
])
def test_rebuilt_routes_render(client, url: str, marker: str):
    response = client.get(url)
    assert response.status_code == 200
    assert marker in response.get_data(as_text=True)
