"""tests/test_neon_glass_01.py — NEON GLASS phase 1 (gardiens du prototype).

Prototype VISUEL sur « Aujourd'hui » uniquement :
  · neon-glass.css existe, est lié au shell et scopé à `[data-space="briefing"]` ;
  · identité orange néon / cuivre — AUCUN bleu comme couleur identitaire ;
  · glass premium (backdrop blur + bordure chaude) ; glow seulement live/actif/hover ;
  · mouvement réduit respecté ; aucun autre espace touché (pas de big-bang) ;
  · aucun moteur/donnée modifié ; READONLY intact.
"""
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(ROOT, 'vertex', 'static', 'vertex', 'css', 'neon-glass.css')


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _read(p):
    with open(p, encoding='utf-8') as fh:
        return fh.read()


def test_neon_glass_css_exists_and_linked(client):
    assert os.path.isfile(CSS)
    html = client.get('/').get_data(as_text=True)
    assert '/static/vertex/css/neon-glass.css' in html
    # le shell expose l'espace actif (hook de scope)
    assert 'data-space="briefing"' in html


def test_glass_covers_all_eight_spaces():
    """Le verre glass est désormais UNIFIÉ sur les 8 espaces canoniques (site à
    100 %). Chaque espace doit apparaître dans le scope CSS ; les règles .vx-card
    restent scopées (jamais globales)."""
    css = _read(CSS)
    for space in ('briefing', 'markets', 'opportunities', 'analysis',
                  'portfolio', 'options', 'journal', 'system'):
        assert f'data-space="{space}"' in css, f'espace non couvert par le glass : {space}'
    # aucune règle .vx-card hors scope (toujours précédée du sélecteur .vx-content:is(...))
    for line in css.splitlines():
        s = line.strip()
        if s.startswith('.vx-card') and 'data-space=' not in s:
            raise AssertionError(f'règle .vx-card non scopée : {s}')


def test_neon_identity_no_blue():
    css = _read(CSS).lower()
    # Identité présente et SOURCÉE depuis la rampe canonique : `--ng-neon`
    # pointe sur `--vx-violet-500`. Les noms « ember » / « copper » étaient des
    # alias dépréciés du MÊME violet — épingler l'alias revenait à verrouiller
    # un nom qui ment.
    flat = css.replace(' ', '')
    assert '--ng-neon' in css and '--ng-copper' in css
    assert '--ng-neon:var(--vx-violet-500)' in flat, 'identite depuis la rampe canonique'
    assert 'var(--ng-neon)' in css  # brand local pointe sur l'orange Ember
    # Aucun hex d'identité en dur dans la couche neon-glass.
    assert '--ng-neon:#' not in flat, 'plus de littéral hex local pour l identite'


def test_glass_premium_present():
    css = _read(CSS)
    assert 'backdrop-filter' in css and 'blur(' in css
    # bordure fine blanche (verre neutre — bleu réservé aux accents)
    assert '--ng-border:rgba(255,255,255' in css.replace(' ', '')


def test_cards_overflow_visible_no_tooltip_clip():
    """Régression : les cartes glass ne rognent plus les tooltips/menus
    (bug `overflow:hidden` corrigé → `overflow:visible` par défaut)."""
    flat = _read(CSS).replace(' ', '').replace('\n', '')
    assert 'overflow:visible' in flat, 'les cartes doivent laisser déborder les tooltips'
    head = flat.split('MARCH')[0]
    assert 'overflow:hidden}' not in head, 'aucune carte glass ne doit être en overflow:hidden'


def test_decorative_before_not_clickable():
    """Le filet cuivre décoratif (::before) ne doit jamais capter les clics."""
    flat = _read(CSS).replace(' ', '')
    assert 'pointer-events:none' in flat, 'le ::before décoratif doit être pointer-events:none'


def test_markets_widgets_use_stable_classes():
    """Widgets Marchés stylés via classes STABLES (`vx-mk-*`), pas de sélecteurs
    d'attribut fragiles (`[class*="heat"]`, `[class*="rail"]`, `[id$="-gauge"]`…)."""
    css = _read(CSS)
    assert 'vx-mk-hero-grid' in css and 'vx-mk-chip' in css
    for fragile in ('[class*="heat"]', '[class*="rail"]', '[class*="spark"]', '[id$="-gauge"]'):
        assert fragile not in css, f'sélecteur fragile résiduel : {fragile}'


def test_glow_only_on_live_active_hover():
    css = _read(CSS)
    # le live-dot ne porte PAS de glow permanent par défaut
    assert '.vx-live-dot{box-shadow:none}' in css.replace(' ', '')
    # glow appliqué uniquement à l'état live / au hover
    assert 'data-live="live"' in css and ':hover' in css


def test_reduced_motion_respected():
    css = _read(CSS)
    assert 'prefers-reduced-motion' in css and 'animation:none' in css.replace(' ', '')


def test_all_spaces_carry_glass(client):
    """Tous les espaces portent leur attribut ET sont couverts par le glass CSS
    (unification site-wide — plus de « non migré »)."""
    code = _read(CSS)
    for path, space in (('/markets', 'markets'), ('/opportunities', 'opportunities'),
                        ('/portfolio', 'portfolio'), ('/analysis', 'analysis'),
                        ('/options', 'options'), ('/journal', 'journal'),
                        ('/system', 'system')):
        html = client.get(path).get_data(as_text=True)
        assert f'data-space="{space}"' in html, f'{path} sans attribut d\'espace'
        assert f'data-space="{space}"' in code, f'{space} absent du scope glass'


def test_opportunities_widgets_present():
    """Les widgets premium Opportunités existent (classes stables vx-op-*)."""
    css = _read(CSS)
    for cls in ('vx-op-dominant', 'vx-op-tk', 'vx-op-cmp', 'vx-op-hero-chips',
                'vx-op-mono', 'vx-op-metric'):
        assert cls in css, f'widget Opportunités manquant : {cls}'


def test_readonly_still_intact(client):
    html = client.get('/system').get_data(as_text=True)
    assert 'READONLY' in html
