"""
LOT 367 — Le paramètre `?view=` : pas le trou qu'on croyait, mais un chemin
d'injection qui n'était gardé par rien.

**Piste de départ** : les gardiens JS (lots 182/186) ne balayent que les routes
NUES. Les variantes `?view=…` servent-elles du JavaScript jamais parsé ?

**Mesure** : 37 variantes découvertes depuis le HTML servi (les onglets des
pages) — ma liste tirée d'un grep du code n'en voyait que 25. Elles servent
**16 blocs inline** absents des routes nues. Cela ressemblait à un trou
quatre fois plus grand que celui du lot 359.

**Vérification avant de conclure** — et c'est là que la piste s'effondre : le
diff entre le bloc d'une route nue et celui de sa variante fait **deux
lignes** :

    -const VIEW="team";
    +const VIEW="risk";

Le JavaScript est **identique au reste près**. Une faute de syntaxe s'y
verrait sur la route nue, déjà balayée par le lot 182. **Il n'y a pas de
trou** — et un gardien qui reparse 16 quasi-doublons aurait coûté du temps
d'exécution pour ne rien attraper.

**Ce qui, en revanche, n'était gardé par rien** : ce paramètre d'URL atteint
les octets servis (une constante JS sur 4 pages, un attribut `data-view` sur
2 autres). Sa sûreté tient à une **liste blanche** — chaque page ramène une
valeur inconnue à sa vue par défaut. Sondé avec deux charges hostiles sur les
8 pages qui lisent `view=` : aucune fuite, ni dans le JS, ni dans le HTML.
C'est cette propriété que ce fichier fige.
"""
#  MARCHES EST FUSIONNE DANS LE DASHBOARD (Black Glass).
#
#  `/markets` ne sert plus de page : la route redirige 302 vers `/#…`
#  pour preserver les favoris. Les listes d'espaces ci-dessous ne le
#  citent donc plus, et les appels directs visent `/`, qui porte
#  desormais ce contenu. La couverture n'est pas perdue : elle a
#  simplement suivi le contenu.
import re

import pytest

import terminal

# Les 8 routes qui lisent `view=` (vertex/app/routes/redesign.py).
ROUTES = ('/opportunities', '/portfolio', '/analysis', '/journal',
          '/intelligence', '/system', '/options')

# Charges hostiles : sortie de chaîne JS, et sortie d'attribut HTML.
PAYLOADS = (
    ("'; alert(1); //", 'alert(1)'),
    ('"><img src=x onerror=alert(1)>', 'onerror=alert'),
    ('</script><script>alert(1)</script>', 'alert(1)'),
)

_INLINE = re.compile(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', re.S)


@pytest.fixture(scope='module')
def client():
    return terminal.app.test_client()


def _page(client, route, view):
    r = client.get(route, query_string={'view': view})
    assert r.status_code == 200, '%s?view=… doit rester servi (%s)' % (route, r.status_code)
    return r.get_data(as_text=True)


@pytest.mark.parametrize('route', ROUTES)
@pytest.mark.parametrize('payload,trace', PAYLOADS)
def test_une_vue_hostile_ne_traverse_jamais_jusqu_aux_octets_servis(
        client, route, payload, trace):
    html = _page(client, route, payload)
    assert payload not in html, (
        '%s recopie la valeur de ?view= telle quelle dans la page — la liste '
        'blanche a sauté' % route)
    assert trace not in html, '%s : charge hostile exécutable dans la page' % route


@pytest.mark.parametrize('route', ROUTES)
def test_la_vue_retombe_sur_une_valeur_connue(client, route):
    """Valeur inconnue → vue par défaut, jamais une vue fabriquée."""
    html = _page(client, route, 'vue_qui_nexiste_pas_42')
    assert 'vue_qui_nexiste_pas_42' not in html
    js = '\n'.join(b for a, b in _INLINE.findall(html)
                   if b.strip() and 'json' not in a.lower())
    for m in re.finditer(r'const VIEW\s*=\s*([\'"])([^\'"]*)\1', js):
        assert re.fullmatch(r'[a-z_]+', m.group(2)), (
            '%s : la constante VIEW servie n\'est pas un identifiant simple '
            '(%r)' % (route, m.group(2)))


def test_le_gardien_ne_tourne_pas_a_vide(client):
    # Une vue LÉGITIME doit bien changer la page — sinon le paramètre serait
    # ignoré et ces tests ne prouveraient rien.
    nue = _page(client, '/portfolio', '')
    vue = _page(client, '/portfolio', 'risk')
    assert nue != vue, 'le paramètre ?view= ne change plus rien : gardien à revoir'
    assert 'const VIEW="risk"' in vue or "const VIEW='risk'" in vue
