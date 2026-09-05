"""UN ENFANT DE `.vx-grid` SANS PORTÉE OCCUPE UNE COLONNE SUR DOUZE.

## Le défaut mesuré

`.vx-grid` est la grille douze colonnes du produit
(`layout.css` : `grid-template-columns:repeat(12,minmax(0,1fr))`). La portée
d'un enfant vient d'une classe explicite — `vx-col-8`, `vx-span-4`… Sans elle,
CSS Grid place l'enfant sur **une seule** piste.

La carte « Ce qui a changé » d'Aujourd'hui était dans ce cas depuis sa
création. Mesuré au navigateur, `aside.vx-insight-rail` :

    1600 px →  w=95    (une colonne sur douze)
     390 px →  w=20    pour 34 px de contenu

À 390 px la carte n'était pas seulement étroite : son contenu était coupé.
Et rien ne le signalait — pas d'erreur, pas de débordement horizontal de page,
`overflow-x:clip` avalant le reste. Une carte servie, jamais lisible.

## Ce que ce banc garde

Tout enfant direct d'une `.vx-grid` **servie** porte une portée : classe
`vx-col-*` / `vx-span-*`, ou `grid-column` en style inline.

## Portée et limites

Le balayage lit les **octets réellement servis** par les routes, via le client
de test — pas le source Python. Il ne voit donc pas les enfants injectés par
JavaScript après le rendu ; ceux-là restent hors de portée de ce gardien, et
c'est dit ici plutôt que sous-entendu.

Les grilles à gabarit **inline** (`style="grid-template-columns:…"`, employées
par la démo du design system pour montrer des grilles à 2 ou 4 pistes) sont
écartées : une piste par enfant y est le comportement voulu, pas un défaut.
"""
from __future__ import annotations

import re
from html.parser import HTMLParser

import pytest

#: Routes servies dont on inspecte le balisage. Ce sont les pages de
#: navigation ; `/design-system` est incluse — sa démo est justement le cas
#: limite qui vérifie que l'exception « gabarit inline » discrimine.
_ROUTES = ('/', '/calendar', '/markets', '/opportunities', '/analysis',
           '/options', '/simulator', '/portfolio', '/follow-up',
           '/performance', '/intelligence', '/system', '/design-system')

_PORTEE = re.compile(r'\bvx-(?:col|span)-\d+\b')


class _Grilles(HTMLParser):
    """Relève les enfants DIRECTS de chaque `.vx-grid` à gabarit non inline."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.pile: list[tuple[str, bool]] = []      # (tag, est_une_grille)
        self.grilles = 0
        self.enfants = 0
        self.orphelins: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = a.get('class') or ''
        style = a.get('style') or ''
        #  `vx-grid` EXACTEMENT : `vx-grid-4`, `vx-grid-auto`… sont d'autres
        #  grilles, à deux ou quatre pistes, où une piste par enfant est juste.
        grille = 'vx-grid' in classes.split() and 'grid-template-columns' not in style

        if self.pile and self.pile[-1][1]:           # enfant direct d'une grille
            self.enfants += 1
            if not (_PORTEE.search(classes) or 'grid-column' in style):
                self.orphelins.append('<%s class=%r>' % (tag, classes[:70]))

        if grille:
            self.grilles += 1
        if tag not in ('br', 'hr', 'img', 'input', 'meta', 'link', 'source'):
            self.pile.append((tag, grille))

    def handle_endtag(self, tag):
        for i in range(len(self.pile) - 1, -1, -1):
            if self.pile[i][0] == tag:
                del self.pile[i:]
                return


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _analyse(html: str) -> _Grilles:
    p = _Grilles()
    p.feed(html)
    return p


# ── 1. Anti-vide : le détecteur mord-il ? ───────────────────────────────────

def test_le_detecteur_voit_un_orphelin_fabrique():
    """Sans cette contre-épreuve, « zéro orphelin » pourrait ne prouver que
    l'incapacité du parseur à en reconnaître un."""
    p = _analyse('<div class="vx-grid"><aside class="vx-insight-rail">x</aside></div>')
    assert p.grilles == 1, 'la grille elle-même n’est pas reconnue'
    assert p.enfants == 1
    assert len(p.orphelins) == 1, p.orphelins


def test_le_detecteur_se_tait_sur_un_balisage_sain():
    """Trois formes licites : classe `vx-col-*`, alias `vx-span-*`, et
    `grid-column` inline. Crier sur l'une d'elles rendrait le banc inutilisable."""
    sain = ('<div class="vx-grid">'
            '<section class="vx-card vx-col-8">a</section>'
            '<section class="vx-span-4">b</section>'
            '<aside style="grid-column:span 12">c</aside>'
            '</div>')
    p = _analyse(sain)
    assert p.enfants == 3
    assert p.orphelins == [], p.orphelins


def test_le_detecteur_ignore_les_grilles_a_gabarit_INLINE():
    """`vx-grid-4`, `vx-grid-2` et les gabarits inline ne sont pas la grille
    douze colonnes : une piste par enfant y est le comportement voulu."""
    for balisage in ('<div class="vx-grid-4"><div class="vx-kpi">a</div></div>',
                     '<div class="vx-grid" style="grid-template-columns:repeat(2,1fr)">'
                     '<div>a</div></div>'):
        p = _analyse(balisage)
        assert p.orphelins == [], balisage

    #  Contre-épreuve du découpage de classes : « vx-grid-4 » ne doit pas
    #  compter comme « vx-grid », sinon l'exception ci-dessus serait fortuite.
    assert _analyse('<div class="vx-grid-4"><div>a</div></div>').grilles == 0


def test_le_detecteur_ne_confond_pas_petit_enfant_et_enfant_direct():
    """Un petit-enfant n'a pas à porter de portée : il n'est pas dans la
    grille. Les compter aurait produit un banc rouge en permanence."""
    p = _analyse('<div class="vx-grid"><section class="vx-col-12">'
                 '<div class="vx-card">x</div></section></div>')
    assert p.enfants == 1, 'le petit-enfant est compté comme enfant direct'
    assert p.orphelins == []


# ── 2. Dénominateur : les pages contiennent bien des grilles ────────────────

def test_les_routes_servent_vraiment_des_grilles_douze_colonnes(client):
    """Si aucune page n'employait `.vx-grid`, l'absence d'orphelin ci-dessous
    serait vraie pour rien."""
    grilles = enfants = 0
    for route in _ROUTES:
        r = client.get(route)
        if r.status_code != 200:
            continue
        p = _analyse(r.get_data(as_text=True))
        grilles += p.grilles
        enfants += p.enfants
    assert grilles >= 20, 'seulement %d grilles servies' % grilles
    assert enfants >= 40, 'seulement %d enfants de grille inspectés' % enfants


# ── 3. Le contrat ───────────────────────────────────────────────────────────

@pytest.mark.parametrize('route', _ROUTES)
def test_aucun_enfant_de_grille_ne_reste_sans_portee(client, route):
    r = client.get(route)
    if r.status_code != 200:
        pytest.skip('%s rend %d' % (route, r.status_code))
    p = _analyse(r.get_data(as_text=True))
    assert p.orphelins == [], (
        '%s : %d enfant(s) direct(s) de `.vx-grid` sans portée — chacun occupe '
        'UNE colonne sur douze et sera servi écrasé : %s'
        % (route, len(p.orphelins), ' ; '.join(p.orphelins[:5])))
