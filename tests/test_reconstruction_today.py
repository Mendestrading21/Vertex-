"""tests/test_reconstruction_today.py — RECONSTRUCTION 01 : Aujourd'hui.

Gardiens de la reconstruction de « Aujourd'hui » (route `/`) avec les widgets
VALIDÉS du Widget Lab, réalisés en live (Neon Glass Orange) : Regime Aura (W01)
et Catalyst Runway (W-CR). On vérifie que la page utilise ces objets validés,
câblés aux vraies APIs, sans réintroduire les widgets bannis, et que les deux
builders live existent et sont sourcés/honnêtes.
"""
import pathlib

import pytest

import terminal

_ROOT = pathlib.Path(__file__).resolve().parents[1]
_BRIEF = (_ROOT / 'vertex/ui/pages/briefing.py').read_text(encoding='utf-8')
_AURA = (_ROOT / 'vertex/static/vertex/js/charts/regime-aura.js').read_text(encoding='utf-8')
_RUNWAY = (_ROOT / 'vertex/static/vertex/js/charts/catalyst-runway.js').read_text(encoding='utf-8')


@pytest.fixture(scope='module')
def client():
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def test_today_uses_validated_objects():
    """Aujourd'hui réalise Regime Aura + Catalyst Runway (widgets validés)."""
    assert 'VXCharts.regimeAura' in _BRIEF, 'régime doit utiliser l’objet validé Regime Aura'
    assert 'VXCharts.catalystRunway' in _BRIEF, 'catalyseurs doivent utiliser Catalyst Runway'
    # les deux builders live sont inclus
    assert '/static/vertex/js/charts/regime-aura.js' in _BRIEF
    assert '/static/vertex/js/charts/catalyst-runway.js' in _BRIEF


def test_today_drops_non_validated_widgets():
    """Aucun widget non validé / duplication Marchés réintroduit."""
    for bad in ('VXCharts.gauge', 'timelineCard', 'vx-regime-gauge',
                'loadPulse', 'vx-market-chart', 'VXCharts.breadthCard', 'loadRotation'):
        assert bad not in _BRIEF, f'widget non validé réintroduit : {bad}'


def test_today_summary_invariants_preserved():
    """Les invariants « résumé, pas copie de Marchés » restent tenus."""
    for keep in ('vx-hero', 'async function loadSummary', 'vx-diff', 'kpiTile',
                 'Aucun historique de comparaison disponible', 'vx-demo-banner',
                 "kpiTile('VIX',vixHtml,''"):
        assert keep in _BRIEF, f'invariant perdu : {keep}'


def test_validated_builders_are_honest_and_sourced():
    """Les builders live portent états honnêtes + source (aucune donnée inventée)."""
    # Regime Aura : état vide/erreur honnête + source moteur
    assert 'VX.states.empty' in _AURA and 'VX.states.error' in _AURA
    assert 'Moteur de régimes' in _AURA
    # Catalyst Runway : état vide honnête + source calendrier + pas de *Card sans source
    assert 'VX.states.empty' in _RUNWAY
    assert 'calendrier moteur' in _RUNWAY
    # objets sémantiques : couleurs via tokens --vx-*, aucun bleu identitaire
    for js in (_AURA, _RUNWAY):
        assert '--vx-' in js
        assert '#45D6E8' not in js  # cyan technique n'est pas réintroduit en dur


def test_today_no_order_path():
    """READONLY : aucun verbe d'ordre dans la page reconstruite ni les builders."""
    for bad in ('placeOrder', 'place_order', 'submitOrder', 'transmit'):
        assert bad not in _BRIEF and bad not in _AURA and bad not in _RUNWAY


def test_root_route_still_200_with_shell(client):
    """La route `/` répond 200 et garde le shell (space briefing, neon-glass, SW v55)."""
    body = client.get('/').get_data(as_text=True)
    assert 'data-space="briefing"' in body
    assert '/static/vertex/css/neon-glass.css' in body
    assert 'vx-skeleton' in body               # squelette de chargement conservé
    sw = client.get('/sw.js').get_data(as_text=True)
    assert 'td-shell-v122' in sw
