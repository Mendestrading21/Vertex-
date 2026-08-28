"""tests/test_neon_glass_01.py — HÉRITAGE du prototype Neon Glass (lot 24).

Ce banc gardait le prototype « neon orange / cuivre » d'Aujourd'hui via sa
feuille `neon-glass.css`. Cette direction est ABANDONNÉE (Black Glass —
Signal Light) et la feuille — jamais servie, vérifié au navigateur à
plusieurs reprises (SW v232, lot 14, lot 24) — est SUPPRIMÉE sur décision
humaine explicite (2026-08-28).

Le banc n'est pas écarté : il est réécrit vers ce qui reste VRAI —
1. la feuille morte ne revient pas et rien ne la référence ;
2. ses invariants encore vivants sont tenus par les feuilles SERVIES :
   mouvement réduit respecté, aucun glow permanent sur le point « live »
   (le §26 de vertex-2-0.css refuse le halo/l'animation continue),
   chaque espace servi porte son attribut `data-space` ;
3. READONLY reste affiché.
Les invariants propres au prototype (identité Ember, --ng-*, widgets
vx-op-*/vx-mk-* de la feuille) meurent avec lui — les classes encore
rendues ont été rapatriées AU MÉRITE (§24, §26, §27 de vertex-2-0.css).
"""
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_DIR = os.path.join(ROOT, 'vertex', 'static', 'vertex', 'css')
MORTE = os.path.join(CSS_DIR, 'neon-glass.css')
V2 = os.path.join(CSS_DIR, 'vertex-2-0.css')


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _read(p):
    with open(p, encoding='utf-8') as fh:
        return fh.read()


def test_la_feuille_morte_est_supprimee_et_personne_ne_la_reference(client):
    assert not os.path.isfile(MORTE), 'neon-glass.css ne doit pas revenir'
    html = client.get('/').get_data(as_text=True)
    assert 'neon-glass' not in html
    #  aucune feuille servie ne l'importe
    for f in os.listdir(CSS_DIR):
        if f.endswith('.css'):
            assert '@import' not in _read(os.path.join(CSS_DIR, f)) or \
                   'neon-glass' not in _read(os.path.join(CSS_DIR, f))


def test_mouvement_reduit_respecte_dans_les_feuilles_servies():
    #  l'invariant vivait dans la feuille morte ; il vit dans les feuilles
    #  réellement chargées par la coque.
    couvert = [f for f in ('animations.css', 'glass.css', 'vertex-2-0.css')
               if 'prefers-reduced-motion' in _read(os.path.join(CSS_DIR, f))]
    assert couvert, 'plus aucune feuille servie ne respecte le mouvement réduit'


def test_aucun_glow_permanent_sur_le_point_live():
    flat = _read(V2).replace(' ', '')
    assert '.vx-live-dot{box-shadow:none;animation:none}' in flat, (
        'le refus du halo permanent (§26) a disparu de la couche finale')


def test_les_espaces_servis_portent_leur_attribut(client):
    for path, space in (('/', 'briefing'), ('/opportunities', 'opportunities'),
                        ('/portfolio', 'portfolio'), ('/analysis', 'analysis'),
                        ('/options', 'options'), ('/system', 'system')):
        html = client.get(path).get_data(as_text=True)
        assert f'data-space="{space}"' in html, f'{path} sans attribut d\'espace'


def test_readonly_still_intact(client):
    html = client.get('/system').get_data(as_text=True)
    assert 'READONLY' in html
