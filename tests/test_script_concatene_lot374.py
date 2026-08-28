"""LOT 374 (révisé au lot 36) — le contexte JS concaténé des pages servies.

Ce gardien protégeait la surface `<script>` concaténée de `_vpage`
(terminal.py) : sept pages héritées assemblées par `'<script>' + js +
'</script>'`, sûres uniquement parce qu'inaccessibles (301). Le lot 36 a
retiré TOUTE cette couche — le danger qu'il surveillait n'a plus de support.

Ce qui reste vrai et mesurable, et que ce banc continue de figer :
1. les pages réellement servies gardent des balises <script> équilibrées ;
2. les routes héritées redirigent toujours (si l'une redevenait servie sans
   gabarit, ce serait un 404/500 visible ici) ;
3. terminal.py ne réintroduit pas d'assemblage `'<script>' + … + '</script>'`.
"""
import re

import pytest

import terminal

PAGES = ['/', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system']

HERITEES = ['/bordel', '/review', '/research', '/heatmap', '/equipe',
            '/settings', '/health']

_OUVRE = re.compile(r'<script\b[^>]*>', re.I)
_FERME = re.compile(r'</script\s*>', re.I)


@pytest.fixture(scope='module')
def client():
    return terminal.app.test_client()


# ── 1. L'assemblage reste équilibré sur les octets servis ───────────────────

@pytest.mark.parametrize('page', PAGES)
def test_les_balises_script_sont_equilibrees_sur_les_pages_servies(client, page):
    html = client.get(page).get_data(as_text=True)
    o, f = len(_OUVRE.findall(html)), len(_FERME.findall(html))
    assert o == f, '%s : %d <script> ouverts pour %d fermés' % (page, o, f)
    assert o >= 8, (
        '%s : seulement %d bloc(s) <script> — page incomplète, le test '
        'précédent ne prouverait rien' % (page, o))


# ── 2. Les routes héritées restent des redirections ─────────────────────────

@pytest.mark.parametrize('route', HERITEES)
def test_les_routes_heritees_redirigent_toujours(client, route):
    r = client.get(route)
    assert r.status_code in (301, 302, 308), (
        '%s ne redirige plus (HTTP %s) — aucune page héritée n\'a de gabarit '
        'depuis le lot 36' % (route, r.status_code))
    cible = r.headers.get('Location') or ''
    assert cible.startswith('/'), (
        '%s redirige hors du site (%r) — redirection ouverte' % (route, cible))


# ── 3. L'assemblage dangereux ne revient pas dans terminal.py ───────────────

def test_terminal_ne_reintroduit_pas_l_assemblage_script_concatene():
    src = open('terminal.py', encoding='utf-8').read()
    assert not hasattr(terminal, '_vpage'), (
        '`_vpage` est revenu — réauditer son contexte JS concaténé (lot 374)')
    assert "'<script>' + js + '</script>'" not in src, (
        'un assemblage `<script> + js` brut est revenu dans terminal.py — '
        'sérialiser via vertex.ui.shell.json_for_script ou prouver la sûreté')
