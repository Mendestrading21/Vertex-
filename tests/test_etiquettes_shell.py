"""
LOT 369 — Les 4 étiquettes du shell : le chemin fragment échappe, le chemin
page complète n'échappe rien.

Suite directe de la faille du lot 368 (`/memory/<id>` injectait via `title=`).
Audit de **tous** les appels `render_shell(...)` du dépôt : **44 étiquettes
constantes** (sûres par construction) et **18 interpolées**. Les 18 ont été
tracées une par une jusqu'à leur source :

  · `analysis_page` — `safe = ''.join(ch for ch in sym if ch.isalnum() or ch in '.-')`
    → filtre de caractères explicite ;
  · `markets`, `opportunities`, `portfolio`, `performance`, `system`,
    `intelligence`, `options_intel` — `label`/`sub` viennent d'un **dict de vues**
    après normalisation (`if view not in dict(_VIEWS): view = '…'`) ;
  · `analysis_api` (post-mortem) — échappée depuis le lot 368.

**Verdict : 18/18 sûres.** Le seul site fautif était celui du lot 368.

**Mais l'asymétrie reste un piège** : dans `vertex/ui/shell/__init__.py`, le
rendu *fragment* échappe les quatre étiquettes
(`escape(title, quote=True)`, …) tandis que le rendu *page complète* les
interpole **brutes** :

    <title>{title} · Vertex</title>
    <b>{space_label}</b> … <span>{sub_label}</span>
    data-page-label="{page_label or space_label}"      ← dans un ATTRIBUT

Le dernier est le plus dangereux : un guillemet suffirait à sortir de
l'attribut. Aucune donnée ne l'atteint aujourd'hui — ce fichier le vérifie, et
le dira le jour où ce ne sera plus vrai.
"""
import re

import pytest

import terminal

# Routes qui interpolent une étiquette, avec le paramètre qui la nourrit.
CAS_VUE = [
    ('/markets', 'view'), ('/opportunities', 'view'), ('/portfolio', 'view'),
    ('/journal', 'view'), ('/system', 'view'), ('/intelligence', 'view'),
    ('/options', 'view'),
]
CHARGES = ('"><img src=x onerror=alert(1)>', '</title><script>alert(1)</script>',
           '" onmouseover="alert(1)')


@pytest.fixture(scope='module')
def client():
    return terminal.app.test_client()


def _titre(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    return m.group(1) if m else ''


def _attr_page_label(html):
    return re.findall(r'data-page-label="([^"]*)"', html)


# ── 1. Aucune charge ne peut atteindre les étiquettes via `?view=` ───────────

@pytest.mark.parametrize('route,param', CAS_VUE)
@pytest.mark.parametrize('charge', CHARGES)
def test_une_vue_hostile_n_atteint_aucune_etiquette(client, route, param, charge):
    html = client.get(route, query_string={param: charge}).get_data(as_text=True)
    assert charge not in html
    # Le titre reste une seule balise close, et l'attribut n'est pas cassé.
    assert html.count('<title>') == 1 and html.count('</title>') == 1
    for v in _attr_page_label(html):
        assert '"' not in v and '<' not in v


# ── 2. Le symbole filtré ne peut pas casser le titre ni l'attribut ───────────

@pytest.mark.parametrize('charge', CHARGES)
def test_un_symbole_hostile_n_atteint_aucune_etiquette(client, charge):
    html = client.get('/analysis/' + charge).get_data(as_text=True)
    assert charge not in html
    assert html.count('<title>') == 1 and html.count('</title>') == 1
    titre = _titre(html)
    assert '<' not in titre and '>' not in titre, 'balise active dans le <title>'
    for v in _attr_page_label(html):
        assert '"' not in v and '<' not in v


# ── 3. L'asymétrie du shell est documentée et surveillée ────────────────────

def test_le_chemin_fragment_echappe_bien_les_quatre_etiquettes():
    import os
    src = open(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'vertex', 'ui', 'shell', '__init__.py'),
        encoding='utf-8').read()
    for etiquette in ('title', 'space_label', 'sub_label', 'page_label'):
        assert 'escape(%s' % etiquette in src or \
               'escape(%s or space_label' % etiquette in src, (
                   'le rendu fragment n\'échappe plus %s' % etiquette)


def test_le_chemin_page_complete_reste_le_seul_non_echappe(client):
    """Contrat ASSUMÉ : la page complète interpole brut, donc chaque site
    d'appel doit filtrer. Si le shell est un jour durci (échappement centralisé,
    dossier en attente de GO), ce test doit être mis à jour — c'est son rôle."""
    import os
    src = open(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'vertex', 'ui', 'shell', '__init__.py'),
        encoding='utf-8').read()
    assert '<title>{title} · Vertex</title>' in src, (
        'le shell échappe désormais le titre : mettre à jour ce gardien et '
        'la note du lot 369')


def test_le_gardien_ne_tourne_pas_a_vide(client):
    # Une vue légitime doit produire une étiquette non vide : sinon les
    # assertions ci-dessus passeraient sur des pages sans étiquette.
    html = client.get('/portfolio', query_string={'view': 'risk'}).get_data(as_text=True)
    assert 'Portefeuille' in _titre(html)
    assert any('Portefeuille' in v for v in _attr_page_label(html))
