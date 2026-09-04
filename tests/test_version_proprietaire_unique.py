"""UN SEUL PROPRIÉTAIRE POUR LA VERSION — l'opérateur lisait un numéro périmé.

Deux endroits déclaraient la version du produit, sans lien entre eux :

| endroit | valeur | servi où |
|---|---|---|
| `vertex/version.py` | `RELEASE_NAME` | contrat produit, CI |
| `vertex/data/constants.py` | `BUILD = 'VERTEX-1.0'` (recopié) | `/healthz`, `/readyz`, champ « Build » de la page Système |

Au renommage du produit en **Vertex Test 1.0**, seul le premier a suivi. Le
second est resté figé sur `VERTEX-1.0` : la page Système et `/healthz`
affichaient donc une version que le code ne déclarait plus, et rien n'échouait.
Une constante recopiée à la main ne reste juste que tant que personne ne
renomme.

`BUILD` est désormais **dérivé** de `vertex/version.py`. Ce banc empêche le
retour en arrière : il vérifie l'égalité, il vérifie qu'elle vient d'un import
et non d'une nouvelle copie, et il vérifie sur les **octets réellement servis**
plutôt que sur la seule constante.

Portée : la version affichée, pas le contenu de la release. Ce banc ne dit pas
que la version est la bonne — il dit qu'il n'en existe qu'une.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
CONSTANTES = RACINE / 'vertex' / 'data' / 'constants.py'


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


# ── 1. Anti-vide : la mesure porte-t-elle sur quelque chose ? ────────────────

def test_la_version_declaree_n_est_pas_vide():
    """Sans version déclarée, les égalités ci-dessous seraient vraies pour rien."""
    from vertex import version
    assert version.RELEASE_NAME.strip(), 'RELEASE_NAME vide'
    assert version.__version__.strip(), '__version__ vide'
    assert version.PRODUCT_NAME.strip(), 'PRODUCT_NAME vide'
    #  `__version__` est un numéro sémantique (`1.0.0`) ; `RELEASE_NAME` est le
    #  nom affiché (`Vertex Test 1.0`). On n'exige donc pas l'égalité des
    #  chaînes — seulement que la majeure.mineure soit la même, sinon le nom
    #  lu par l'opérateur annoncerait une autre release que le code.
    majeure_mineure = '.'.join(version.__version__.split('.')[:2])
    assert majeure_mineure in version.RELEASE_NAME, (
        'RELEASE_NAME (%r) ne porte pas la version %s tirée de %r — le nom '
        'affiché et le numéro peuvent alors diverger sans que rien ne le voie'
        % (version.RELEASE_NAME, majeure_mineure, version.__version__))
    assert version.PRODUCT_NAME in version.RELEASE_NAME, (
        'RELEASE_NAME (%r) ne porte pas le nom du produit (%r)'
        % (version.RELEASE_NAME, version.PRODUCT_NAME))


# ── 2. Un seul propriétaire, prouvé sur la constante ────────────────────────

def test_le_marqueur_de_build_egale_la_version_declaree():
    from vertex.data.constants import BUILD
    from vertex.version import RELEASE_NAME
    assert BUILD == RELEASE_NAME, (
        'BUILD (%r) et RELEASE_NAME (%r) ont divergé : la page Système '
        'afficherait une version que le code ne déclare pas' % (BUILD, RELEASE_NAME))


def test_le_marqueur_de_build_est_IMPORTE_et_non_recopie():
    """L'égalité seule ne suffit pas : deux littéraux identiques la satisfont
    aujourd'hui et divergent au prochain renommage. On exige le lien."""
    arbre = ast.parse(CONSTANTES.read_text(encoding='utf-8'))
    importe = any(
        isinstance(n, ast.ImportFrom) and n.module == 'vertex.version'
        for n in ast.walk(arbre))
    assert importe, ('vertex/data/constants.py n\'importe plus vertex.version : '
                     'BUILD est redevenu une copie, elle dérivera au prochain '
                     'renommage')
    for n in ast.walk(arbre):
        if isinstance(n, ast.Assign) and any(
                isinstance(c, ast.Name) and c.id == 'BUILD' for c in n.targets):
            assert not isinstance(n.value, ast.Constant), (
                'BUILD est réassigné à un littéral (%r) — le lien avec '
                'vertex/version.py est rompu' % getattr(n.value, 'value', None))


def test_aucun_numero_de_version_recopie_dans_les_constantes():
    """Un `VERTEX-1.0` retapé ailleurs dans le fichier recréerait le défaut."""
    texte = CONSTANTES.read_text(encoding='utf-8')
    code = '\n'.join(l for l in texte.splitlines()
                     if not l.lstrip().startswith('#'))
    fautes = re.findall(r"['\"][^'\"]*VERTEX-\d[^'\"]*['\"]", code)
    assert fautes == [], ('numéro de version recopié dans les constantes : %s'
                          % fautes)


# ── 3. Sur les OCTETS SERVIS, pas seulement sur la constante ────────────────

def test_healthz_sert_la_version_declaree(client):
    from vertex.version import RELEASE_NAME
    charge = client.get('/healthz').get_json()
    assert charge['build'] == RELEASE_NAME, (
        '/healthz sert build=%r alors que le produit declare %r'
        % (charge.get('build'), RELEASE_NAME))


def test_la_page_systeme_sert_la_version_declaree(client):
    """Le champ « Build » de la page Système vient de `/api/system-status`."""
    from vertex.version import RELEASE_NAME
    reponse = client.get('/api/system-status')
    assert reponse.status_code == 200, reponse.status_code
    charge = reponse.get_json() or {}
    assert charge.get('build') == RELEASE_NAME, (
        'la page Système afficherait build=%r pour un produit nomme %r'
        % (charge.get('build'), RELEASE_NAME))
