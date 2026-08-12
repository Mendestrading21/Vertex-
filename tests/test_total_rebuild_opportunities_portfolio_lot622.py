"""Gardiens LOT 622 — reconstruction Opportunités + Portefeuille.

Ces tests verrouillent la hiérarchie Réponse → Justification → Expertise sans
modifier les contrats de données. Ils ciblent surtout les régressions visuelles
qui peuvent induire une lecture financière erronée : valeur manquante placée au
milieu d'un scatter, tableaux trop larges, KPI répétés et graphiques doublonnés.
"""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPP = (ROOT / 'vertex/ui/pages/opportunities_page.py').read_text(encoding='utf-8')
PF = (ROOT / 'vertex/ui/pages/portfolio_page.py').read_text(encoding='utf-8')


def _segment(source: str, start: str, end: str) -> str:
    left = source.index(start)
    right = source.index(end, left)
    return source[left:right]


def test_new_information_architecture_classes_are_wired_on_both_pages():
    required = ('vx-page-lead', 'vx-kpi-strip', 'vx-hero-grid',
                'vx-insight-rail', 'vx-toolbar', 'vx-disclosure',
                'vx-section-stack')
    for cls in required:
        assert cls in OPP, f'{cls} absent d’Opportunités'
        assert cls in PF, f'{cls} absent du Portefeuille'


def test_radar_fuses_editorial_answer_and_dominant_candidate():
    hero = _segment(OPP, 'function renderHero', '/* ── ACTIONS ── */')
    assert 'id="op-dominant"' in hero
    radar = _segment(OPP, 'async function renderRadar', '/* ── HERO ÉDITORIAL')
    assert '<div class="vx-grid vx-mt4"><div class="vx-col-12" id="op-dominant"' not in radar
    assert 'opRanked(rows).slice(1,4)' in OPP  # trois cartes secondaires maximum


def test_scatter_is_fixed_0_100_and_never_imputes_missing_timing_to_50():
    radar = _segment(OPP, 'async function renderRadar', '/* ── HERO ÉDITORIAL')
    assert radar.count('min:0,max:100') == 2
    assert 'getPixelForValue(55)' in radar
    assert "v===null||v===undefined||v===''?null:Number(v)" in radar
    assert 'v!==null&&Number.isFinite(v)&&v>=0&&v<=100' in radar
    assert 'ok:axisOk(x)&&axisOk(y)' in radar
    assert 'axe qualité ou timing n/d' in radar
    assert '??50' not in radar
    assert 'data:plotted.map' in radar


def test_radar_keeps_one_primary_chart_and_relegates_matrix_and_skyler():
    assert '<details class="vx-disclosure vx-mt4" id="op-compare-disclosure">' in OPP
    assert 'id="op-compare"' in OPP
    assert 'vx-card vx-card--compact' in _segment(
        OPP, 'async function renderFunnel', '/* ── RADAR')
    skyler = _segment(OPP, 'async function loadSkylerRank', 'const RENDER=')
    assert "document.createElement('details')" in skyler
    assert 'Expertise avancée · Classement Skyler /40' in skyler


def test_stocks_show_a_six_column_top_then_full_technical_access():
    stocks = _segment(OPP, 'async function renderStocks', '/* ── OPTIONS')
    assert 'f.slice(0,10).map(essentialRow)' in stocks
    assert ('<th>Titre</th><th>Décision</th><th class="vx-num" data-sortable>Score</th>'
            in stocks)
    assert '<th class="vx-num">Cours</th><th class="vx-num">R:R</th><th>Action</th>' in stocks
    assert 'id="op-stocks-full"' in stocks and 'f.map(technicalRow)' in stocks
    assert 'Décision moteur' not in stocks  # une seule colonne de décision


def test_options_is_a_three_contract_shortlist_and_canonical_relay():
    options = _segment(OPP, 'async function renderOptions', '/* ── ANOMALIES')
    assert ').slice(0,3)' in options
    assert 'Shortlist options — relais vers l’espace Options' in options
    assert 'id="op-options-full"' in options
    assert 'id="op-contract" hidden' in options
    assert '/options">Options Intelligence' in options


def test_anomaly_categories_do_not_claim_an_unprovided_feed():
    anomalies = _segment(OPP, 'async function renderAnomalies', '/* ── CALENDRIER')
    assert "Options:'non agrégé ici'" in anomalies
    assert 'Aucun flux agrégé « ${group} » n’est fourni à cette vue.' in anomalies
    assert 'Aucun résultat n’est déduit ou inventé.' in anomalies


def test_portfolio_hero_is_action_first_and_kpis_are_not_repeated_inside_it():
    synth = _segment(PF, 'async function renderSynthese', '/* Diff « depuis')
    hero = synth[:synth.index('/* 4 KPI canoniques')]
    assert 'Prochaine décision analytique' in hero
    assert 'act.label' in hero and 'Risque dominant' in hero
    assert 'de valeur nette' not in hero and 'plLine' not in hero
    for label in ('Valeur nette', 'P&L latent total', 'Concentration', 'Exposition'):
        assert label in synth


def test_positions_have_one_six_column_decision_table_and_technical_disclosure():
    positions = _segment(PF, 'async function renderPositions', '/* ═══ PERFORMANCE')
    expected = ('<th>Position</th><th class="vx-num">Valeur</th><th class="vx-num">P&L</th>'
                '\n        <th class="vx-num">Poids</th><th>Thèse</th><th>Action analytique</th>')
    assert expected in positions
    assert 'id="pf-position-details"' in positions
    for field in ('Prix moyen', 'Prix actuel', 'Valeur marché', 'Conviction',
                  'Invalidation', 'Catalyseur', 'Prochaine action'):
        assert field in positions


def test_contribution_has_one_chart_home_and_performance_uses_8_plus_4_hero():
    assert "VXCharts.card('pf-contrib-host'" not in PF
    assert "VXCharts.card('pf-perf-contrib'" in PF
    assert '<div id="pf-contrib-host" hidden aria-hidden="true"></div>' in PF
    performance = _segment(PF, 'async function renderPerformance', '/* ═══ OPTIONS')
    assert '<div class="vx-col-8" id="pf-perf-equity"></div>' in performance
    assert '<aside class="vx-col-4 vx-insight-rail" id="pf-perf-drawdown"></aside>' in performance


def test_risk_has_one_verdict_four_kpis_one_stress_visual_and_no_hhi_gauge():
    risk = _segment(PF, 'async function renderRisk', '/* Dépendances cachées')
    assert 'aria-label="Verdict de risque"' in risk
    assert 'id="pf-risk-kpis"' in risk
    assert risk.count("${_rk('") == 4
    assert 'aria-label="Visualisation unique des stress tests"' in risk
    assert "VXCharts.gauge('pf-risk-gauge'" not in risk
    assert "kv('HHI'" not in risk
    discipline = _segment(PF, 'async function renderDiscipline', 'const RENDER=')
    assert 'VX.fmt.num(d.hhi' not in discipline
    assert 'Le HHI canonique reste dans les 4 KPI Risque' in discipline


def test_watchlist_explains_the_three_distinct_tracking_types():
    watch = _segment(PF, 'async function renderWatchlist', '/* Discipline V2')
    assert 'Watchlist = idée documentée' in watch
    assert 'Suivi actif = plan entrée/stop/objectif' in watch
    assert 'Favori = raccourci sans thèse' in watch
    assert 'Un favori n’implique ni thèse, ni alerte, ni position.' in watch


def test_all_opportunities_and_portfolio_views_still_render_200():
    import terminal

    client = terminal.app.test_client()
    for view in ('radar', 'stocks', 'options', 'anomalies', 'calendar'):
        assert client.get('/opportunities?view=' + view).status_code == 200, view
    for view in ('team', 'positions', 'performance', 'risk', 'options', 'watchlist'):
        assert client.get('/portfolio?view=' + view).status_code == 200, view
