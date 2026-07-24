"""tests/test_journal_system_07.py — PR n°7 (gardiens Journal + Système).

Journal (« Suis-je en train de devenir un meilleur investisseur ? ») : discipline
UNIQUEMENT — Hero éditorial honnête, stats comportementales, hypothèses,
progression. Aucune performance de portefeuille (elle vit dans Portefeuille).
Système (« Puis-je faire confiance à Vertex aujourd'hui ? ») : Hero technique
cockpit. READONLY absolu.
"""
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as fh:
        return fh.read()


JR = 'vertex/ui/pages/performance_page.py'
SY = 'vertex/ui/pages/system_page.py'


# ── Journal = discipline uniquement ──────────────────────────────────────
def test_journal_is_discipline_not_portfolio_performance():
    src = _read(JR)
    # aucune courbe de performance de portefeuille au Journal
    assert 'equityCard' not in src and 'drawdownCard' not in src and 'heatmapCard' not in src
    # discipline / comportement
    assert 'Discipline' in src and 'function behavioral' in src
    assert 'respectMethod' in src and 'invalRespect' in src
    # renvoi vers le domicile de la performance
    assert '/portfolio?view=performance' in src


def test_journal_hero_is_honest_no_fabricated_percent():
    src = _read(JR)
    assert 'vx-pf-hero' in src and 'function loadDiscipline' in src
    # honnêteté explicite : rien n'est inventé
    assert 'inventé' in src
    # pas de pourcentage codé en dur type « 92 % » dans le Hero
    assert '92 %' not in src and '92%' not in src


def test_journal_new_views_present():
    src = _read(JR)
    for v in ('overview', 'journal', 'learnings', 'progression', 'track-record'):
        assert f"('{v}'," in src
    assert 'function loadHypotheses' in src and 'function loadProgression' in src
    # biais comportementaux
    assert 'vx-pf-biais' in src


def test_journal_routes_200(client):
    for v in ('overview', 'journal', 'learnings', 'progression', 'track-record'):
        r = client.get('/journal?view=' + v)
        assert r.status_code == 200, v
    r = client.get('/journal')
    assert r.status_code == 200 and '<h1>Journal</h1>' in r.get_data(as_text=True)


# ── Système = Hero technique cockpit ─────────────────────────────────────
def test_system_hero_technique_present():
    src = _read(SY)
    assert 'vx-sys-hero' in src
    assert 'Confiance données' in src
    assert 'Système opérationnel' in src and 'Système partiellement dégradé' in src
    # confiance = IBKR + fraîcheur + erreurs + readonly
    assert 'IBKR' in src and 'lecture seule confirmée' in src


def test_system_route_200_and_readonly(client):
    r = client.get('/system')
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert '<h1>Système</h1>' in html
    assert 'READONLY' in html  # invariant affiché
