"""L'OUTIL QUI CHERCHE LES BOUTONS MORTS DOIT SAVOIR CE QU'EST UN EFFET.

## Deux faux positifs, mesurés

`tools/audit/boutons_morts.py` a déclaré morts **quatorze boutons qui
marchent**, en deux familles :

  · **cinq tuiles d'options** sur `/`. Leur `onclick` fait
    `location.href='/options/dossier/ACN'`. Le relevé supposait qu'une page qui
    navigue ferait LEVER `page.evaluate` ; elle ne lève pas — l'appel réussit
    sur le NOUVEAU document, où `window.__vxEffet` n'existe pas, et le repli
    `{dom:0, stockage:0, …}` se lisait « aucun effet ». Vérifié une par une :
    l'URL passe bien de `/` à `/options/dossier/ACN` ;

  · **neuf boutons** sur `/intelligence` — les quatre exemples de questions et
    les cinq pastilles de tickers. Leur handler fait `champ.value = …`. Or la
    `value` d'un input est une **propriété**, pas un attribut : le
    MutationObserver ne la voit pas, rien ne part sur le réseau, rien ne
    défile. Remplir un formulaire est pourtant l'effet le plus courant d'un
    produit fait de filtres.

Un instrument qui crie faux finit par ne plus être cru — et c'est alors le
vrai bouton mort qu'on rate.

## Ce que ce banc garde

Les deux sondes de l'outil, éprouvées sur une page FABRIQUÉE dont on connaît
la réponse : un bouton vraiment mort doit ressortir, un bouton qui ne fait que
remplir un champ ne doit pas, et la navigation doit se lire sur l'URL.

Le témoin NÉGATIF compte autant que le positif : c'est lui qui manquait.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

import pytest

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SONDE = os.path.join(_RACINE, 'tests', 'aides', 'sonde_boutons_morts.py')


def _navigateur_dispo() -> bool:
    from tools.mesures.mesurer_qa_espaces import navigateur_pret
    return navigateur_pret()


@pytest.fixture(scope='module')
def releve() -> dict:
    """Les cinq témoins, mesurés DANS UN SOUS-PROCESSUS.

    Nécessaire : `ib_async` applique `nest_asyncio`, ce qui fait croire à
    Playwright qu'une boucle asyncio tourne — son API synchrone refuse alors
    de démarrer dans le processus de test. Mesuré : le banc échouait sur
    « Playwright Sync API inside the asyncio loop » avant d'ouvrir un
    navigateur. La page témoin est en outre SERVIE par un vrai serveur, car
    `set_content` produit une origine opaque où `localStorage` est refusé —
    et la sonde instrumente justement le stockage.
    """
    if not _navigateur_dispo():
        pytest.skip('Chromium absent — la mesure porterait sur rien')
    r = subprocess.run([sys.executable, _SONDE], capture_output=True,
                       text=True, timeout=240)
    assert r.returncode == 0, 'la sonde a échoué :\n%s' % r.stderr[-800:]
    derniere = [l for l in r.stdout.splitlines() if l.strip().startswith('{')]
    assert derniere, 'la sonde n’a rien rendu :\n%s' % r.stdout[-400:]
    return json.loads(derniere[-1])


def _rien(e: dict) -> bool:
    """Le critère de l'outil, effets externes mis à part."""
    return not (e.get('dom') or e.get('stockage') or e.get('defile')
                or e.get('champs') or e.get('a_navigue'))


# ── 1. Le témoin POSITIF : un bouton vraiment mort ressort ──────────────────

def test_un_bouton_qui_ne_fait_RIEN_ressort_mort(releve):
    """Sans lui, un détecteur devenu aveugle passerait tous les bancs
    suivants en déclarant le produit sain."""
    assert _rien(releve['mort']), (
        'un bouton sans le moindre effet n’est plus détecté : %s'
        % releve['mort'])


# ── 2. Les témoins NÉGATIFS : ceux qui manquaient ───────────────────────────

def test_remplir_un_CHAMP_compte_comme_un_effet(releve):
    """Le faux positif des neuf boutons de Vertex IA. `champ.value = …` ne
    touche aucun attribut : sans sonde dédiée, l'outil enterre tout bouton
    qui remplit un formulaire — et un produit fait de filtres en est plein."""
    e = releve['remplit']
    assert e['champs'], 'la valeur du champ a changé et rien ne l’a vu'
    assert not _rien(e)


def test_cocher_une_CASE_compte_aussi(releve):
    """Même famille : `checked` est une propriété. Une sonde qui ne lirait
    que `value` manquerait toutes les cases du produit."""
    assert releve['coche']['champs'], 'l’état coché a changé et rien ne l’a vu'


def test_la_NAVIGATION_est_vue(releve):
    """Le faux positif des cinq tuiles d'options : elles naviguent, et
    l'outil les enterrait."""
    e = releve['va']
    assert e['a_navigue'], 'le clic n’a pas navigué : ce témoin ne prouve rien'
    assert not _rien(e)


def test_une_mutation_du_DOM_reste_detectee(releve):
    """Contre-épreuve : la sonde historique doit continuer de mordre — on
    ajoute une capacité, on n'en retire pas."""
    assert releve['mute']['dom'], 'une insertion de nœud n’est plus vue'


def test_les_temoins_ne_se_confondent_pas(releve):
    """Chaque témoin doit être vu par SA sonde et pas par une autre : sinon
    le banc passerait sur un détecteur qui crie sur tout."""
    assert not releve['remplit']['dom'], 'remplir un champ compte comme une mutation'
    assert not releve['mute']['champs'], 'une mutation compte comme un remplissage'
    assert not releve['mort']['a_navigue']


# ── 3. Les deux correctifs, gardés dans la source de l'outil ───────────────

def _source_outil() -> str:
    with open(os.path.join(_RACINE, 'tools', 'audit', 'boutons_morts.py'),
              encoding='utf-8') as f:
        src = f.read()
    #  Commentaires écartés : ils citent les motifs qu'on cherche.
    return re.sub(r'^\s*#.*$', '', src, flags=re.M)


def test_l_outil_compare_bien_les_URL():
    """La navigation ne LÈVE pas : `page.evaluate` réussit sur le nouveau
    document et rend le repli à zéro. S'appuyer sur une exception pour la
    détecter était l'erreur."""
    src = _source_outil()
    assert 'url_avant = page.url' in src
    assert 'if page.url != url_avant:' in src, (
        'la navigation n’est plus lue sur l’URL — les boutons qui naviguent '
        'redeviendraient des faux morts')


def test_le_critere_de_l_outil_inclut_bien_les_champs():
    src = _source_outil()
    assert "interne.get('champs')" in src, (
        'le remplissage de champ ne compte plus dans le critère')
    assert '__vxChamps' in src, 'la sonde des champs a disparu'
