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


def test_widget_count_ge_60(client):
    """FINANCE NATIVE P03 exige ≥ 60 widgets réellement implémentés."""
    from vertex.ui.pages import widget_lab
    benches = widget_lab._benches()
    assert len(benches) >= 60, f'seulement {len(benches)} widgets (< 60)'


def test_finance_native_forms_present(html):
    """P03 : objets de marché propriétaires (chandeliers + formes signature)."""
    for w in ('Candlestick Snapshot', 'Support / Resistance Spine', 'Price Ladder',
              'Market Tape', 'Market Correlation Web', 'Relative-Strength Path',
              'Market Breadth Field', 'Volatility Cone', 'Order-Flow Ribbon',
              'Risk / Reward Terrain', 'Position Health Strip', 'Liquidity Depth',
              'Earnings Gap Map', 'Catalyst Runway'):
        assert w in html, f'objet financier signature manquant : {w}'


def test_finance_grammar_present(html):
    """P03 : grammaire boursière native (prix, %, niveaux, conclusion, source)."""
    from vertex.ui.pages import widget_lab
    benches = widget_lab._benches()
    # ≥ 20 widgets clairement financiers (chandeliers + formes marché natives).
    fin_families = {'Marchés', 'Momentum', 'Breadth', 'Volatilité', 'Opportunité',
                    'Analyse', 'Portefeuille', 'Options', 'Catalyseurs', 'Régime'}
    fin = [b for b in benches if b[2] in fin_families]
    assert len(fin) >= 20, f'seulement {len(fin)} widgets financiers'
    # conclusion de décision + pied de source (couple verdict/preuve, honnêteté)
    assert '▸' in html                                   # ligne de conclusion
    assert 'entrée valide' in html or 'invalidation' in html  # grammaire décision
    assert 'objectif' in html and 'stop' in html         # niveaux de trading


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
    # identité : provient de la rampe CANONIQUE (`--vx-violet-*`), pas d'un
    # alias déprécié ni d'un littéral. Le lab nommait `--vx-ember-500` — même
    # couleur, nom périmé : un nuancier qui nomme mal est pire qu'absent.
    assert 'var(--vx-violet-500)' in html
    hexes = set(re.findall(r'#[0-9a-fA-F]{6}', html))

    def bluish(x):
        r, g, b = int(x[1:3], 16), int(x[3:5], 16), int(x[5:7], 16)
        return b > r + 30 and b > g + 30 and b > 90 and r < 110
    blues = [x for x in hexes if bluish(x)]
    assert not blues, f'bleu identitaire dans le lab : {blues}'


def test_no_order_path_readonly(html):
    for bad in ('placeOrder', 'place_order', 'submitOrder'):
        assert bad not in html, f'chemin d’ordre interdit : {bad}'


# ═══ CURATION PASS 04 — chaque widget classé, 15 officiels max, contrats ═══
def test_curation_every_widget_classified():
    """Aucun widget non classé : tout bench a un score/statut."""
    from vertex.ui.pages import widget_lab
    ids = [b[0] for b in widget_lab._benches()]
    for wid in ids:
        assert wid in widget_lab.CURATION, f'widget non classé : {wid}'
    # pas d'entrée orpheline
    for wid in widget_lab.CURATION:
        assert wid in ids, f'curation orpheline : {wid}'


def test_curation_caps_and_distribution():
    """≤ 15 Officiels, ≤ 20 Références ; tout le reste explicitement classé."""
    from collections import Counter
    from vertex.ui.pages import widget_lab
    dist = Counter(widget_lab._status(s)[0] for s, _ in widget_lab.CURATION.values())
    assert dist['official'] <= 15, f'{dist["official"]} officiels (> 15)'
    assert dist['reference'] <= 20, f'{dist["reference"]} références (> 20)'
    # somme = total, aucun non classé
    assert sum(dist.values()) == len(widget_lab._benches())


def test_official_contracts_complete():
    """Chaque officiel a un contrat normalisé complet."""
    from vertex.ui.pages import widget_lab
    officials = [w for w, (s, _) in widget_lab.CURATION.items() if s >= 90]
    assert len(officials) <= 15
    fields = ('usage', 'api', 'pages', 'unit', 'period', 'compact', 'mobile')
    for wid in officials:
        c = widget_lab.CONTRACTS.get(wid)
        assert c, f'officiel sans contrat : {wid}'
        for f in fields:
            assert c.get(f), f'contrat {wid} : champ manquant {f}'


def test_official_domain_coverage():
    """Les officiels couvrent les 15 domaines exigés (par famille/usage)."""
    from vertex.ui.pages import widget_lab
    benches = {b[0]: b for b in widget_lab._benches()}
    officials = [w for w, (s, _) in widget_lab.CURATION.items() if s >= 90]
    fams = {benches[w][2] for w in officials}
    # domaines structurants présents parmi les officiels
    for fam in ('Régime', 'Momentum', 'Breadth', 'Rotation', 'Opportunité',
                'Analyse', 'Portefeuille', 'Options', 'Volatilité', 'Catalyseurs'):
        assert fam in fams, f'domaine officiel non couvert : {fam}'


def test_curation_ui_present(html):
    """Statuts, récap et panneau contrat rendus dans le lab."""
    assert 'wl-summary' in html and 'Officiels' in html
    for st in ('official', 'reference', 'rework', 'rejected'):
        assert f'wl-status--{st}' in html, f'statut UI manquant : {st}'
    assert 'Contrat officiel' in html          # panneau contrat
    assert 'API données' in html


def test_reworked_widgets_renamed(html):
    """Les 3 widgets faibles sont retravaillés (nouveaux noms, plus les anciens)."""
    for new in ('Investment Pipeline', 'Bias Cost Ledger', 'Discipline Curve'):
        assert new in html, f'widget retravaillé manquant : {new}'
    for old in ('>Selection Funnel<', '>Bias Heatmap<', '>Progress Ladder<'):
        assert old not in html, f'ancien nom persistant : {old}'
    # honnêteté : pipeline sait dire zéro actionnable
    assert 'Aucun dossier actionnable' in html


def test_export_enriched(html):
    """Export : statuts + notes + version + note libre par widget."""
    assert 'vxWidgetLabNotes' in html          # persistance des notes
    assert 'data-note' in html                 # bouton note par tuile
    assert 'P04-curation' in html              # version du lab injectée


# ═══ GALERIE PASS 05 — matière · lumière · palette · 10 objets ═══
def test_gallery_present(html):
    """La galerie musée existe : hero + plaques + divider."""
    assert 'gx-gallery' in html and 'gx-plate' in html
    assert 'gx-hero' in html and 'gx-h1' in html
    assert '✦ Galerie' in html                 # entrée de nav
    assert 'gx-divider' in html                # transition vers la bibliothèque


def test_gallery_ten_objects():
    """Exactement 10 objets galerie, chacun rendu en SVG."""
    from vertex.ui.pages import widget_lab
    assert len(widget_lab._GALLERY) == 10
    for entry in widget_lab._GALLERY:
        svg = entry[6]()                       # le lambda générateur
        assert svg.strip().startswith('<svg'), f'objet non-SVG : {entry[1]}'


def test_material_library_11(html):
    """Bibliothèque de 11 matières réelles (pas des rectangles gris)."""
    for mat in ('matte', 'smoked', 'frosted', 'obsidian', 'carbon', 'ceramic',
                'anodized', 'polished', 'brushed', 'soft-glass', 'metal'):
        assert f'gx-mat--{mat}' in html, f'matière manquante : {mat}'


def test_warm_palette_and_ramps(html):
    """20 gris chauds + gammes orange/vert/rouge définies (scopé .wl)."""
    assert '--g0:' in html and '--g19:' in html          # rampe de 20 gris
    for tok in ('--o-ember', '--o-copper', '--o-glow', '--o-light', '--o-burn'):
        assert tok in html, f'orange manquant : {tok}'
    for tok in ('--gr-trading', '--gr-institution', '--gr-live'):
        assert tok in html, f'vert manquant : {tok}'
    for tok in ('--r-risk', '--r-loss', '--r-bear'):
        assert tok in html, f'rouge manquant : {tok}'


def test_gallery_light_and_type(html):
    """Système de lumière (scène + glow local) et typographie de galerie."""
    assert 'gx-stage' in html                  # scène éclairée
    assert 'gx-panel' in html                  # panneau matière
    assert 'Neue Montreal' in html             # référence typographique
    assert 'Dix objets' in html                # manifeste éditorial
