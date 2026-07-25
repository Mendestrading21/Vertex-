"""tests/test_widget_lab.py — LABORATOIRE du Design System (/widget-lab).

Route autonome hors produit : aucune donnée réelle, aucun moteur. Sert à voir /
comparer / choisir les widgets (V1…Vn + états). Gardiens : la route répond, les
benches/variantes/états/verdicts sont présents, l'identité orange Ember tient
sans bleu, l'échantillon est clairement étiqueté, aucun chemin d'ordre.
"""
import re

import pytest

import terminal


@pytest.fixture(scope='module')
def client():
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


@pytest.fixture(scope='module')
def html(client):
    r = client.get('/widget-lab')
    assert r.status_code == 200
    return r.get_data(as_text=True)


def test_route_ok_and_standalone(html):
    # page autonome : son propre <head>, PAS le shell produit
    assert '<title>Vertex · Widget Lab' in html
    assert '/static/vertex/css/tokens.css' in html
    # ne fait pas partie de la nav produit (pas de sidebar 8 espaces)
    assert 'vx-sidebar' not in html


def test_benches_and_families_present(html):
    assert 'wl-bench' in html and 'wl-variants' in html
    # 13 familles produit + Primitives (dont les 5 ajoutées en AD-02)
    for fam in ('Régime', 'Momentum', 'Breadth', 'Rotation', 'Opportunité',
                'Volatilité', 'Marchés', 'Catalyseurs', 'Analyse', 'Portefeuille',
                'Options', 'Journal', 'Système', 'Primitives'):
        assert f'data-fam="{fam}"' in html or f'>{fam}<' in html, f'famille manquante : {fam}'
    # widgets signature attendus (existants + AD-02)
    for w in ('Regime Aura', 'Momentum Comb', 'Breadth Tide', 'Stress Thermocline',
              'Health Reactor', 'Asymmetry Ledge', 'Opportunity Dominant Slab',
              'Sector Rotation Orbit', 'Verdict Slab', 'Scenario Triad', 'Payoff Terrain',
              'Greek Vector Field', 'Data Integrity Reactor', 'READONLY Seal',
              'Volatility Rift', 'Momentum Ribs', 'Catalyst Countdown Ring'):
        assert w in html, f'widget signature manquant : {w}'


def test_material_tiers_present(html):
    """AD-02 : plusieurs matières distinctes (pas des rectangles uniformes)."""
    for mat in ('matte', 'smoked', 'polished', 'deepblack', 'metal', 'frosted'):
        assert f'wl-surf--{mat}' in html, f'matière manquante : {mat}'
    assert '--wl-noise' in html          # micro-texture
    assert 'wl-mobile' in html           # aperçu mobile
    assert 'wl-tip' in html              # tooltip micro-interaction


def test_widget_count_ge_40(client):
    """AD-02 exige ≥ 40 widgets réellement implémentés."""
    from vertex.ui.pages import widget_lab
    benches = widget_lab._benches()
    assert len(benches) >= 40, f'seulement {len(benches)} widgets (< 40)'


def test_variants_and_states(html):
    # variantes V1…Vn comparables
    assert 'V1' in html and 'V2' in html and 'V3' in html and 'V4' in html
    # bande d'états honnête
    for st in ('loading', 'empty', 'insufficient', 'stale', 'demo', 'live'):
        assert f'wl-state--{st}' in html, f'état manquant : {st}'


def test_verdict_controls_and_export(html):
    # choix par variante : Officiel / Référence / Rejeté, persistés localStorage
    for v in ('official', 'reference', 'rejected'):
        assert f'data-v="{v}"' in html, f'verdict manquant : {v}'
    assert 'vxWidgetLabVerdicts' in html      # persistance
    assert 'wl-export' in html                # export des choix


def test_sample_data_clearly_labeled(html):
    # laboratoire : valeurs = échantillons, jamais présentées comme réelles
    assert 'échantillons' in html or 'échantillon' in html
    assert 'aucune donnée réelle' in html


def test_identity_orange_no_blue(html):
    # identité : provient des tokens Ember ; aucun littéral bleu identitaire
    assert 'var(--vx-ember-500)' in html
    hexes = set(re.findall(r'#[0-9a-fA-F]{6}', html))

    def bluish(x):
        r, g, b = int(x[1:3], 16), int(x[3:5], 16), int(x[5:7], 16)
        return b > r + 30 and b > g + 30 and b > 90 and r < 110
    blues = [x for x in hexes if bluish(x)]
    assert not blues, f'bleu identitaire dans le lab : {blues}'


def test_no_order_path_readonly(html):
    for bad in ('placeOrder', 'place_order', 'submitOrder'):
        assert bad not in html, f'chemin d’ordre interdit : {bad}'
