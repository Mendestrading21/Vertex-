"""tests/test_pages_opportunities_analysis_04.py — PR n°4 (gardiens de refonte).

Opportunités : Hero éditorial + scatter renommé (op-radar → op-scatter).
Analyse : Carte-Verdict + Carte-Scénario + raisonnement du comité intégré,
DATA_INSUFFICIENT honnête, domicile unique des scénarios.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as fh:
        return fh.read()


# ── Opportunités ──────────────────────────────────────────────────────
def test_opportunities_scatter_renamed():
    src = _read('vertex/ui/pages/opportunities_page.py')
    assert 'op-scatter' in src, 'le scatter doit s\'appeler op-scatter'
    assert 'op-radar' not in src, 'op-radar (nom trompeur) doit avoir disparu'
    assert 'Scatter d' in src and 'asym' in src.lower()


def test_opportunities_hero_editorial_honest():
    src = _read('vertex/ui/pages/opportunities_page.py')
    assert 'function renderHero' in src and 'op-hero' in src
    # message honnête quand aucune asymétrie
    assert 'Attendre est une décision valide' in src


def test_opportunities_scatter_has_shell_contract():
    src = _read('vertex/ui/pages/opportunities_page.py')
    # le scatter passe par C.card avec conclusion + unité + résumé accessible
    assert "conclusion:" in src and "unit:'score 0-100'" in src and 'summary:' in src


# ── Analyse ───────────────────────────────────────────────────────────
def test_analysis_verdict_card_present():
    src = _read('vertex/ui/pages/analysis_page.py')
    assert 'an-verdict' in src and 'vx-verdict-card' in src
    assert 'loadDecisionStack' in src
    assert "/api/decision/" in src  # decision stack (scénarios, comité, confiance)


def test_analysis_scenario_card_single_home():
    src = _read('vertex/ui/pages/analysis_page.py')
    assert 'vx-scenario-grid' in src
    assert 'Pessimiste' in src and 'Probable' in src and 'Exceptionnel' in src
    # un SEUL domicile des scénarios : plus de « Bull / Base / Bear » concurrent
    assert 'Bull / Base / Bear' not in src


def test_analysis_committee_integrated():
    src = _read('vertex/ui/pages/analysis_page.py')
    assert 'an-committee' in src and 'Raisonnement du comité' in src
    assert 'devils_advocate' in src  # avocat du diable


def test_analysis_data_insufficient_honest():
    src = _read('vertex/ui/pages/analysis_page.py')
    assert "final_decision==='DATA_INSUFFICIENT'" in src
    assert 'vx-insufficient' in src and 'Vertex ne tranche pas' in src
    assert 'aucune probabilité inventée' in src.lower()


def test_analysis_no_invented_probability():
    """Les scénarios ne fabriquent pas de probabilité chiffrée."""
    src = _read('vertex/ui/pages/analysis_page.py')
    assert 'aucune probabilité inventée' in src.lower()
