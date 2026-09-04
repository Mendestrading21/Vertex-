"""Gardiens lot 624 — hiérarchie Journal et cockpit Système.

Ces tests verrouillent la progressive disclosure sans supprimer les hôtes,
routes ou endpoints historiques qui portent les données réelles.
"""

import pytest

from vertex.ui.pages import performance_page, system_page


def _between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def test_discipline_leads_with_response_four_kpis_hypotheses_and_next_axis():
    view = performance_page._VIEW_CONTENT['overview']
    #  VERTEX 2.0 : le hero de discipline portait un SQUELETTE PERPÉTUEL.
    #  `loadDiscipline()` avait été retirée — elle était appelée et définie nulle
    #  part, et faisait échouer toute la vue — mais ses deux conteneurs sont
    #  restés. Le bloc promettait donc une donnée qui n'arrivait jamais.
    #  Il porte désormais un état honnête sur la surface canonique 2.0
    #  (`vx2-surface`) : « calcul non disponible dans Vertex », avec sa cause.
    assert 'id="vx-pf-hero"' in view and 'vx2-surface' in view
    assert 'calcul non disponible dans Vertex' in view
    assert 'vx-skeleton' not in view.split('id="vx-pf-hero"', 1)[1][:600], \
        'le hero ne doit plus porter un squelette qui ne se résout jamais'
    assert 'id="vx-pf-kpis" data-max-kpis="4"' in view
    #  Les mesures de discipline ont leur propre conteneur : elles ecrasaient
    #  la bande des resultats declares, melangeant deux populations dans un
    #  meme emplacement.
    assert 'id="vx-pf-discipline"' in view
    assert 'id="vx-pf-hypo"' in view
    assert 'id="vx-pf-next-axis"' in view and 'vx-insight-rail' in view

    js = performance_page._JS
    for label in ('Respect de la méthode', 'Qualité des entrées',
                  'Qualité des sorties', 'Respect des invalidations'):
        assert label in js
    assert "cell('" in js and 'Prochain axe' in js


def test_declared_results_and_engine_history_are_progressively_disclosed():
    view = performance_page._VIEW_CONTENT['overview']
    declared = _between(view, 'id="vx-pf-results-disclosure"',
                        'id="vx-pf-history-disclosure"')
    assert 'vx-disclosure' in view
    assert 'vx-pf-postmortem' in declared and 'vx-pf-dist' in declared
    assert 'P&amp;L, r&eacute;ussite et profit factor' in declared
    assert '/portfolio?view=performance' in declared

    advanced = view.split('id="vx-pf-history-disclosure"', 1)[1]
    assert 'vx-pf-calibration' in advanced and 'vx-pf-memory' in advanced
    assert '?view=track-record' in advanced


def test_chronology_has_a_clean_toolbar_and_historical_sources_stay_separate():
    labels = dict(performance_page._VIEWS)
    #  VERTEX 2.0 : les onglets prennent les libelles canoniques de
    #  `navigation-and-pages.md` §10. La sous-vue est la meme, son URL aussi.
    assert labels['journal'] == 'Journal'
    assert labels['track-record'] == 'Signaux théoriques'
    assert labels['real'] == 'Trades réels'

    chronology = performance_page._VIEW_CONTENT['journal']
    assert 'Chronologie des d&eacute;cisions' in chronology
    assert 'vx-toolbar' in chronology
    assert chronology.index('vx-pf-filter') < chronology.index('vx-pf-journal')
    assert 'Timeline' not in chronology

    #  VERTEX 2.0 — la garantie est PLUS FORTE qu'avant, pas plus faible.
    #
    #  Les deux populations cohabitaient dans une seule vue, séparées par une
    #  phrase (« Aucun chiffre ne passe de l'une à l'autre »). Une phrase
    #  demande au lecteur de se méfier ; deux vues le dispensent de le faire.
    #  Le contrat les réclame séparées, et deux vues ne se mélangent pas.
    moteur = performance_page._VIEW_CONTENT['track-record']
    declare = performance_page._VIEW_CONTENT['real']

    #  Chacune ne porte QUE sa population.
    assert 'data-source-kind="engine"' in moteur
    assert 'data-source-kind="declared"' not in moteur
    assert 'data-source-kind="declared"' in declare
    assert 'data-source-kind="engine"' not in declare

    #  Chacune NOMME sa population, plutôt que de laisser deviner.
    assert 'verdicts rendus par les moteurs' in moteur
    assert 'trades que vous avez d&eacute;clar&eacute;s' in declare

    #  Et chacune renvoie à l'autre : séparer sans dire où est l'autre moitié
    #  ferait croire que la page ne mesure qu'une chose.
    assert '?view=real' in moteur
    assert '?view=track-record' in declare


def test_system_readonly_is_compact_and_connections_matrix_precedes_details():
    header = system_page._header('connections')
    #  VERTEX 2.0 : l'en-tete passe par `vx2.page_header` + `vx2.context_bar`.
    #  L'intention — un en-tete canonique, compact, avant la matrice — tient.
    assert 'vx2-header' in header
    assert 'vx-readonly-shield' in header and '<b>READONLY</b>' in header
    assert 'vx-insight vx-mb3' not in header

    view = system_page._VIEW_CONTENT['connections']
    assert view.index('vx-conn-summary') < view.index('vx-sys-gauge')
    assert view.index('vx-conn-summary') < view.index('vx-conn-details')
    assert 'Matrice consolid&eacute;e des connexions' in view
    assert 'id="vx-sys-kpis" data-max-kpis="4"' in view
    details = view.split('id="vx-conn-details"', 1)[1]
    for host in ('vx-conn-ibkr', 'vx-conn-tv', 'vx-conn-ai', 'vx-brain-body',
                 'vx-conn-sync', 'vx-conn-store', 'vx-conn-engines'):
        assert host in details


def test_system_data_is_targeted_and_diagnostics_are_advanced():
    view = system_page._VIEW_CONTENT['data']
    assert 'Donn&eacute;es exploitables' in view
    assert 'vx-toolbar' in view and 'vx-data-refresh' in view
    assert 'vx-data-quality-chart' in view and 'vx-data-fresh' in view
    advanced = view.split('id="vx-data-diagnostics"', 1)[1]
    assert 'vx-data-scan' in advanced and 'vx-continuity' in advanced
    assert 'Diagnostics avanc&eacute;s' in view


def test_system_connections_stay_readable_on_mobile_and_charts_wait_for_theme():
    js = system_page._JS
    assert 'class="vx-connection-row"' in js
    assert "CONFIGURATION_MISSING:'À configurer'" in js
    assert "NOT_IMPLEMENTED:'Non disponible'" in js
    assert js.index('whenChartsReady(()=>{', js.index('async function loadData')) \
        < js.index('const colors=VXCharts.colors;', js.index('async function loadData'))


def test_automations_and_settings_use_user_facing_progressive_labels():
    automations = system_page._VIEW_CONTENT['automations']
    assert 'T&acirc;ches en arri&egrave;re-plan' in automations
    assert 'D&eacute;marrage' in automations and 'Configuration' in automations
    assert '§24' not in automations and '§10' not in automations
    assert 'vx-auto-configuration' in automations and 'vx-disclosure' in automations

    settings = system_page._VIEW_CONTENT['settings']
    advanced = settings.split('id="vx-settings-advanced"', 1)[1]
    for contract in ('vx-desk-export', 'vx-desk-import-file', 'vx-app-update',
                     '/design-system'):
        assert contract in advanced
    assert '/design-system' not in system_page._tabs('settings')


def test_lot624_keeps_data_endpoints_and_all_routes_live():
    for endpoint in ('/api/track-record', '/api/journal/postmortem',
                     '/api/skyler/calibration', '/api/skyler/memory'):
        assert endpoint in performance_page._JS
    for endpoint in ('/api/system/connections', '/api/system-status',
                     '/api/data-quality', '/api/system/diagnostics',
                     '/api/system/automations', '/api/system/startup-report',
                     '/api/system/config'):
        assert endpoint in system_page._JS

    import terminal
    client = terminal.app.test_client()
    for view, _ in performance_page._VIEWS:
        assert client.get('/journal?view=' + view).status_code == 200
    for view, _ in system_page.VIEWS:
        assert client.get('/system?view=' + view).status_code == 200


@pytest.mark.parametrize('module', (performance_page, system_page))
def test_shared_total_rebuild_primitives_are_used(module):
    source = (module._HEADER + ''.join(module._VIEW_CONTENT.values())) \
        if module is performance_page else ''.join(module._VIEW_CONTENT.values())
    for primitive in ('vx-page-lead', 'vx-kpi-strip', 'vx-hero-grid',
                      'vx-insight-rail', 'vx-toolbar', 'vx-disclosure',
                      'vx-section-stack'):
        assert primitive in source, primitive
