"""UN ÉTAT VIDE DOIT AVOIR UN HÔTE — sinon il ne s'affiche jamais.

## Le défaut mesuré

`markets_page.loadSectors` traitait le cas « aucun secteur » ainsi :

```js
emptyCard('vx-mk-sectors-chart', 'Secteurs non calculés par le dernier scan.', …);
VXCharts.heatmapCard('vx-mk-sectors-heat', { …, rows: sectors.map(…) });
```

Deux fautes, mesurées sur un scan sans secteurs — l'état d'un démarrage à
froid ou d'un réseau qui ne répond pas :

1. **`vx-mk-sectors-chart` n'existe pas dans le balisage.** Seuls
   `vx-mk-sectors-heat` et `vx-mk-sectors-leaders` y sont. `emptyCard` commence
   par `const el=$(host); if(!el) return;` — il sort en silence. Le message
   « Secteurs non calculés » n'a jamais été affiché à personne.
2. **À la place, une carte creuse.** Le `heatmapCard` recopié dans cette
   branche dessinait la carte avec `rows: sectors.map(…)` sur un `sectors`
   VIDE : mesuré, 196 px de haut, titrée « PERFORMANCE ET MOMENTUM PAR
   SECTEUR », posant sa question et n'y répondant par aucune ligne. Sa
   signature d'accident : `unit:'%'` y était écrit **trois fois**.

Le résultat servi était donc l'inverse exact de l'intention : le message
honnête muet, et la carte vide affichée.

## Pourquoi `tools/audit/cartes_creuses.py` ne l'a pas vu

Il l'aurait vu — il ne pouvait pas. Cet outil s'exécute sur l'application
telle qu'elle tourne, et une application PEUPLÉE ne prend jamais cette
branche. Le défaut ne vit que dans l'état dégradé, celui que l'utilisateur
rencontre au premier démarrage.

## Ce que ce banc garde

Tout `emptyCard('hôte', …)` d'une page vise un identifiant réellement présent
dans le balisage de cette page. Un état vide sans hôte est une phrase que
personne ne lira jamais, et rien ne le signale à l'exécution.
"""
from __future__ import annotations

import os
import re

import pytest

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PAGES = os.path.join(_RACINE, 'vertex', 'ui', 'pages')


def _modules() -> list[str]:
    return sorted(n for n in os.listdir(_PAGES) if n.endswith('.py'))


def _sans_commentaires(src: str) -> str:
    """Retire les commentaires JS et Python avant tout balayage.

    LA LEÇON, PAYÉE QUATRE FOIS DANS CE DÉPÔT. Un contrôle qui cherche une
    chaîne dans du source la trouve aussi dans la PROSE qui l'explique : le
    commentaire décrivant ce lot cite `emptyCard('vx-mk-sectors-chart', …)` et
    `heatmapCard`, et faisait échouer le banc sur du texte sans aucun effet.
    Le précédent nommé du dépôt est `test_la_fenetre_de_fraicheur_ne_s_elargit_pas`,
    dont la première version cherchait `'< 75' in src`.
    """
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)        # blocs JS
    src = re.sub(r'^\s*#.*$', '', src, flags=re.M)          # lignes Python
    return src


def _source(nom: str) -> str:
    with open(os.path.join(_PAGES, nom), encoding='utf-8') as f:
        return _sans_commentaires(f.read())


def _source_brute(nom: str) -> str:
    with open(os.path.join(_PAGES, nom), encoding='utf-8') as f:
        return f.read()


def _ids(src: str) -> set[str]:
    """Identifiants posés dans le balisage — guillemets simples ou doubles."""
    return set(re.findall(r"""\bid=["']([A-Za-z0-9_-]+)["']""", src))


def _cibles(src: str) -> list[str]:
    return re.findall(r"""emptyCard\(\s*['"]([A-Za-z0-9_-]+)['"]""", src)


# ── 1. Anti-vide : le lecteur trouve bien des appels et des identifiants ────

def test_le_balayage_trouve_des_appels_a_inspecter():
    """Un lecteur qui ne trouve rien déclarerait tout conforme sans rien
    mesurer — la panne que ce dépôt appelle « un gardien muet »."""
    total = sum(len(_cibles(_source(n))) for n in _modules())
    assert total >= 10, 'seulement %d appels `emptyCard` trouvés' % total


def test_le_balayage_ecarte_bien_les_COMMENTAIRES():
    """Contre-épreuve de la leçon ci-dessus : une mention en prose ne doit pas
    compter comme un appel."""
    faux = ("/* on a retiré emptyCard('hote-disparu') d'ici */\n"
            "emptyCard('hote-reel', 'raison');")
    assert _cibles(_sans_commentaires(faux)) == ['hote-reel']
    assert 'hote-disparu' not in _sans_commentaires(faux)


def test_le_lecteur_d_identifiants_voit_les_deux_ecritures():
    """Contre-épreuve : les pages mélangent `id="x"` et `id='x'`. Ne lire
    qu'une forme ferait passer l'autre pour absente, et le banc crierait sur
    des hôtes qui existent."""
    assert _ids('<div id="alpha"></div>') == {'alpha'}
    assert _ids("<div id='beta'></div>") == {'beta'}
    assert _ids('<div class="x"></div>') == set()


# ── 2. Le contrat ───────────────────────────────────────────────────────────

@pytest.mark.parametrize('module', _modules())
def test_chaque_etat_vide_vise_un_hote_existant(module):
    src = _source(module)
    cibles = _cibles(src)
    if not cibles:
        pytest.skip('%s n’appelle pas emptyCard' % module)
    ids = _ids(src)
    orphelins = sorted({c for c in cibles if c not in ids})
    assert orphelins == [], (
        '%s : `emptyCard` vise %s, mais aucun élément de cette page ne porte '
        'cet identifiant. `emptyCard` sort en silence sur un hôte introuvable : '
        'le message ne sera JAMAIS affiché, et rien ne le signalera.'
        % (module, orphelins))


# ── 3. La branche « aucun secteur » ne dessine plus de carte creuse ─────────

def _branche_vide_des_secteurs() -> str:
    src = _source('markets_page.py')
    debut = src.index('function loadSectors(')
    fin = src.index('return;', debut)
    return src[debut:fin]


def test_la_branche_sans_secteur_ne_dessine_aucune_carte_de_donnees():
    """Le cœur du défaut : rendre un `heatmapCard` sur une liste vide produit
    une carte qui pose sa question et n'y répond pas."""
    branche = _branche_vide_des_secteurs()
    assert 'heatmapCard' not in branche, (
        'la branche « aucun secteur » dessine de nouveau une carte de données '
        'sur une liste vide — elle rendra 196 px de titre sans une seule ligne')


def test_la_branche_sans_secteur_dit_bien_quelque_chose():
    """Dénominateur : ne rien dessiner ne suffit pas ; il faut DIRE pourquoi.
    Sans ce contrôle, supprimer les deux appels passerait pour un correctif."""
    branche = _branche_vide_des_secteurs()
    assert 'emptyCard(' in branche, 'la branche ne pose plus aucun état vide'
    assert 'Secteurs non calculés' in branche, (
        'l’état vide ne nomme plus sa raison')
    assert 'SCAN_ACTION' in branche, (
        'l’état vide n’offre plus de chemin vers Système / Données')


def test_l_hote_de_cet_etat_vide_existe_vraiment():
    """La faute exacte de départ, gardée nommément."""
    src = _source('markets_page.py')
    branche = _branche_vide_des_secteurs()
    vises = _cibles(branche)
    assert vises, 'plus aucun hôte visé dans la branche'
    for v in vises:
        assert v in _ids(src), (
            '`emptyCard(%r)` vise de nouveau un identifiant absent du balisage '
            '— le message redeviendrait muet' % v)


def test_l_unite_n_est_plus_ecrite_trois_fois():
    """La signature de l'accident. Trois `unit:` dans le même objet littéral
    ne change rien au rendu — JavaScript garde la dernière — mais dit qu'une
    édition s'est mal passée à cet endroit."""
    src = _source('markets_page.py')
    assert "unit:'%',unit:'%'" not in src.replace(' ', ''), (
        'une clé `unit` est de nouveau répétée dans le même objet')
