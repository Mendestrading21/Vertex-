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

    # `vx-disclosure` a été RETIRÉ de cette liste au lot Signal OS · Aujourd'hui.
    # Il n'y a plus de repli sur cette page : voir
    # `test_today_keeps_one_regime_visual_and_shows_catalysts` ci-dessous.
    for cls in ('vx-page-lead', 'vx-kpi-strip', 'vx-hero-grid',
                'vx-insight-rail', 'vx-toolbar', 'vx-section-stack'):
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


def test_today_keeps_one_regime_visual_and_shows_catalysts():
    """RENVERSEMENT ASSUMÉ DU LOT 621 — les catalyseurs sortent du repli.

    Le 621 avait mis calendrier et portefeuille dans un `<details>` fermé, sous
    le résumé « Catalyseurs et portefeuille », pour qu'ils ne concurrencent pas
    la décision principale.

    `PAGES.md` les classe **4ᵉ et 5ᵉ** des six rangs d'Aujourd'hui — entre les
    opportunités et le brief éditorial. Ce sont des éléments de premier plan.
    Et un catalyseur à J-2 qu'il faut déplier pour voir ne remplit pas son
    office : il existe précisément pour prévenir **avant**.

    Ce qui est CONSERVÉ du 621, et qui était sa vraie trouvaille : une seule
    visualisation de régime sur la page, et l'ordre décision → régime →
    opportunités → surveillance.
    """
    html = briefing._CONTENT
    # Les commentaires HTML ne sont pas du balisage. Le commentaire qui EXPLIQUE
    # le retrait du repli cite `<details>` — chercher la sous-chaîne dans la
    # source brute le comptait comme un repli réel (même famille que 616-B :
    # chercher une sous-chaîne n'est pas lire du balisage).
    balisage = re.sub(r'<!--.*?-->', '', html, flags=re.S)

    assert '<details' not in balisage, (
        'un repli est réapparu sur Aujourd\'hui. Vérifier ce qu\'il cache : si '
        'c\'est un des six rangs de PAGES.md, il ne doit pas être replié.')
    assert 'id="vx-calendar"' in balisage and 'id="vx-portfolio"' in balisage
    # L'ordre de la page suit celui de la hiérarchie cible.
    for avant, apres in (('id="vx-hero"', 'id="vx-regime-body"'),
                         ('id="vx-regime-body"', 'id="vx-opp-stocks"'),
                         ('id="vx-opp-stocks"', 'id="vx-alerts"'),
                         ('id="vx-alerts"', 'id="vx-calendar"'),
                         ('id="vx-calendar"', 'id="vx-portfolio"')):
        assert balisage.index(avant) < balisage.index(apres), (
            'ordre rompu : %s devrait précéder %s' % (avant, apres))
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
    html = markets_page._VIEW_CONTENT['overview']
    details = _details_containing(html, 'id="vx-mk-multi"')

    assert 'class="vx-kpi-strip' in html
    assert 'data-max-kpis="4"' in html
    assert html.index('id="vx-mk-strip"') < html.index('id="vx-mk-spy"')
    assert html.index('id="vx-mk-spy"') < html.index('id="vx-mk-leader"')
    assert 'id="vx-mk-top"' in details and 'id="vx-mk-flop"' in details
    assert 'id="vx-mk-spy"' not in details
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
    assert 'vx-page-lead' in markets_page._HEADER
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
