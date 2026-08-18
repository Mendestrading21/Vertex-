"""SIGNAL OS · PASSE FINALE — UNE SEULE FAMILLE D'ICONES, ET UNE SEULE TABLE.

`VISUAL_SYSTEM.md` : « une seule famille d'icônes outline », « ne jamais mélanger
pictogrammes remplis, outline, multicolores et emojis dans la même surface ».

## Ce que le lot précédent avait manqué, et pourquoi

Le lot 09 (1/n) avait cherché des **emojis**. Un instrument plus large — *tout
élément dont le texte propre tient en un ou deux caractères non alphanumériques*
— trouve la suite : `✕` (bouton Fermer, **8 espaces sur 8**), `⋯` (boutons
« Actions », 10 sites), `★ ◎ ! ◇` (barre mobile de la fiche Analyse), `✓` (une
valeur de tuile sur Système).

**La cause n'est pas de la négligence** : `_ICONS` vit en Python et ne servait
que le HTML rendu au serveur. Les pages construisent une grande part de leur DOM
en JavaScript et n'avaient **aucun moyen d'atteindre la famille** — le caractère
était la seule option disponible. La table est donc publiée au client
(`window.VX.__icons`) et relue par `VX.icon()`.

## Portée dite

Ces tests lisent les **sources de page** et le **shell**. Un pictogramme
construit à l'exécution par un moteur (les notes du comité arrivent préfixées
d'un emoji, cf. `vertex/engines/committee.py`) leur échappe : c'est le site
d'**affichage** qui le retire, et c'est `test_signal_os_today.py` qui le garde.

`vertex/ui/sync_center.py` porte encore un `✕` et n'est **pas** dans la portée :
mesuré, il n'atteint aucun des huit espaces (il n'est injecté que dans
`_NAVJS_BLOCK` du monolithe historique ; `curl /` n'en contient aucune trace).
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PAGES_DIR = os.path.join(_ROOT, 'vertex', 'ui', 'pages')
_SHELL = os.path.join(_ROOT, 'vertex', 'ui', 'shell', '__init__.py')
_JS_DIR = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js')
_CORE = os.path.join(_JS_DIR, 'vx-core.js')

# Les huit espaces canoniques, plus les deux modules encore servis hors nav.
_PAGES = (
    'briefing.py', 'markets_page.py', 'opportunities_page.py', 'analysis_page.py',
    'portfolio_page.py', 'options_intel_page.py', 'performance_page.py',
    'system_page.py', 'intelligence_page.py',
)

# Domaine des PICTOGRAMMES : dingbats, formes géométriques, emojis.
#
# Il commence à U+2200 pour exclure le bloc des FLÈCHES (U+2190–U+21FF) :
# « Marchés → », « Ouvrir le desk → » sont le vocabulaire directionnel du
# produit, écrit DANS un libellé. Mon premier motif les accusait à tort — deux
# mesures l'ont montré avant publication.
#
# `_TEXTE` retire ensuite les caractères qui, dans ce domaine, sont du TEXTE et
# non des icônes. Chaque exclusion est justifiée, aucune n'est là pour faire
# passer le test :
#   −  U+2212 moins mathématique (« − 3,2 % », « Call GEX (+) vs Put GEX (−) »)
#   ≥ ≤ ≈ ≠  comparateurs employés dans des seuils (« |z| ≥ 2 »)
#   × ÷ ± √ ∑ ∞  opérateurs
#   ⌘  légende de touche (« ⌘K ») — c'est le nom d'une touche, pas une icône,
#      et le lot 288 l'a déjà masquée au tactile pour cette raison même.
_TEXTE = '−≥≤≈≠×÷±√∑∞⌘'
_PICTO = (r'(?![' + _TEXTE + r'])'
          r'[\u2200-\u2BFF\uFE0F\U0001F000-\U0001FAFF]')


def _lire(chemin):
    return io.open(chemin, encoding='utf-8').read()


def _sources_de_page():
    """Les sources de page, le shell, ET TOUTE LA COUCHE JAVASCRIPT SERVIE.

    La couche JS a été ajoutée après coup, et c'est la leçon de ce lot : mon
    premier balayage s'arrêtait à `vertex/ui/pages/**`, alors que les builders
    de graphiques et les modules de page construisent du DOM exactement comme
    elles. Il restait **douze** pictogrammes de l'autre côté de cette frontière
    — dont un (`▸`, devant le verdict du Catalyst Runway) que le navigateur
    affichait sur l'accueil pendant que le gardien était vert. Un gardien dont
    la portée s'arrête avant le code qui produit le défaut ne garde rien.

    `vendor/` est exclu : ce sont des bibliothèques tierces, que le produit ne
    réécrit pas.
    """
    src = {n: _lire(os.path.join(_PAGES_DIR, n)) for n in _PAGES}
    src['shell/__init__.py'] = _lire(_SHELL)
    for racine, _, fichiers in os.walk(_JS_DIR):
        if 'vendor' in racine:
            continue
        for n in sorted(fichiers):
            if n.endswith('.js'):
                chemin = os.path.join(racine, n)
                src[os.path.relpath(chemin, _JS_DIR)] = _lire(chemin)
    return src


def test_aucun_pictogramme_textuel_dans_un_noeud_de_texte():
    """LA propriété, et non la liste des cas connus.

    ### Pourquoi ce motif-ci, et pas celui que j'avais écrit d'abord

    Mon premier gardien cherchait un élément **réduit** à un glyphe
    (`<button>✕</button>`). Testé par mutation, il a laissé passer deux
    régressions sur neuf — et surtout, appliqué au produit, il ne voyait que
    ce que j'avais déjà corrigé à la main. Le motif ci-dessous — *un
    pictogramme n'importe où dans un nœud de texte* — en a trouvé **sept de
    plus**, tous COLLÉS à du texte et donc invisibles au premier :

    | site | glyphe |
    | --- | --- |
    | `opportunities_page.py` classement | `★` sur le meilleur candidat |
    | `opportunities_page.py` porte plafonnante | `✕` |
    | `analysis_page.py` préparation bloquée | `⛔` |
    | `analysis_page.py` portes non franchies | `✕` |
    | `portfolio_page.py` revues obligatoires | `⚠` |
    | `portfolio_page.py` favoris | `★` |
    | `system_page.py` avertissements | `⏳` |

    Aucun n'était rendu lors du relevé navigateur : ils vivent tous dans une
    branche conditionnelle (une porte plafonnée, un avertissement). **Un
    pictogramme latent est un pictogramme** — il apparaîtra le jour où la
    condition sera vraie, c'est-à-dire le jour où l'écran comptera le plus.

    Traitement retenu, et il n'est pas uniforme : *là où le mot dit déjà la
    chose* (« bloquée », un bandeau d'avertissement, une ligne de revue) le
    glyphe est RETIRÉ ; *là où le pictogramme était le seul marqueur* (étoile
    de favori, croix de porte) il devient un trait de la famille.
    """
    motif = re.compile(r'>[^<>\n]{0,140}?(' + _PICTO + r')[^<>\n]{0,140}?<')
    fautes = []
    for nom, src in _sources_de_page().items():
        for m in motif.finditer(src):
            ligne = src.count('\n', 0, m.start()) + 1
            fautes.append('%s:%d → %r' % (nom, ligne, m.group(0)[:80]))
    assert not fautes, (
        'un pictogramme TEXTUEL est rendu dans du contenu, alors que le produit '
        'a une famille SVG :\n  ' + '\n  '.join(fautes) +
        '\nSi c\'est une icône : icon(nom) (Python) ou VX.icon(nom) (JavaScript) ; '
        'ajouter le nom à _ICONS dans vertex/ui/shell/__init__.py au besoin. '
        'Si le mot voisin dit déjà la chose, retirer le glyphe.')


def test_la_famille_n_a_qu_une_table_et_le_client_ne_la_recopie_pas():
    """Le défaut que ce pont pouvait introduire : une SECONDE table côté JS.

    C'est exactement ce que la table de micro-copy du lot 211 avait produit —
    deux vérités pour un même libellé, dont une seule gardée. On vérifie donc
    que `VX.icon` LIT `VX.__icons` et ne déclare aucun tracé lui-même.

    Portée : le bloc `VX.icon` seul. Chercher `<path` dans TOUT le fichier
    aurait mordu sur `VX.states.ghost`, qui dessine légitimement ses
    silhouettes de chargement — une assertion trop large est le défaut que
    cette refonte a rencontré cinq fois.
    """
    core = _lire(_CORE)
    debut = core.index('VX.icon = function')
    bloc = core[debut:core.index('VX.states = {', debut)]
    assert 'VX.__icons' in bloc, (
        'VX.icon ne lit plus la table publiée par le shell : la famille a '
        'probablement été recopiée côté client.')
    for balise in ('<path', '<circle', '<rect', '<line'):
        assert balise not in bloc, (
            'VX.icon déclare un tracé (%s) : c\'est une seconde table, et une '
            'seconde table dérive en silence.' % balise)
    assert "|| ''" in bloc and '?' not in bloc.split('__icons')[1][:40], (
        'un nom inconnu doit rendre une icône VIDE. Un caractère de repli '
        'réintroduirait par la porte de derrière le pictogramme textuel que ce '
        'pont existe pour supprimer.')


def test_le_shell_publie_la_famille_entiere_au_client():
    """Le pont doit transporter TOUTE la table, pas les seuls noms du jour."""
    import sys
    sys.path.insert(0, _ROOT)
    from vertex.ui.shell import _ICONS, _icons_for_client
    publie = _icons_for_client()
    manquants = [n for n in _ICONS if '"%s"' % n not in publie]
    assert not manquants, 'noms absents du pont client : %s' % manquants
    shell = _lire(_SHELL)
    assert 'id="vx-icons"' in shell and '{icons}' in shell, (
        'le bloc #vx-icons a disparu du shell : les pages qui construisent leur '
        'DOM en JavaScript n\'ont plus accès à la famille, et retomberont sur '
        'des caractères.')


def test_les_deux_boutons_fermer_du_shell_dessinent_un_trait():
    """Ce sont les DEUX seuls pictogrammes que les huit espaces partagent :
    ils appartiennent au shell, donc une régression ici est une régression
    partout à la fois."""
    shell = _lire(_SHELL)
    bloc = shell[shell.index('_OVERLAYS'):shell.index('def _wants_fragment')]
    assert bloc.count("{icon('close')}") == 2, (
        'les boutons « Fermer » n\'utilisent plus la fabrique du shell.')

    # La SOURCE porte l'expression f-string ; ce qui compte est ce qui est
    # RENDU. On relit donc le bloc évalué — une assertion sur le texte du
    # fichier aurait été verte même si `icon()` rendait une chaîne vide.
    import sys
    sys.path.insert(0, _ROOT)
    from vertex.ui.shell import _OVERLAYS
    rendus = re.findall(r'aria-label="Fermer">(.*?)</button>', _OVERLAYS)
    assert len(rendus) == 2, (
        'le nombre de boutons « Fermer » du shell a changé (%d) — vérifier que '
        'le nouveau dessine bien une icône.' % len(rendus))
    for r in rendus:
        assert r.startswith('<svg') and 'stroke-width="1.7"' in r, (
            'un bouton « Fermer » ne dessine pas un trait de la famille : %r' % r)


def test_la_tuile_lecture_seule_porte_un_mot_et_distingue_absent_de_faux():
    """L'invariant le plus important du produit ne se dit pas avec un signe.

    Et le contre-exemple compte autant : quand le serveur ne répond pas, la
    tuile doit dire « Inconnue » — jamais « Non », qui affirmerait qu'un ordre
    est possible.
    """
    src = _lire(os.path.join(_PAGES_DIR, 'system_page.py'))
    ligne = [l for l in src.splitlines() if "_kp('Lecture seule'" in l]
    assert len(ligne) == 1, 'tuile « Lecture seule » introuvable ou dupliquée'
    ligne = ligne[0]
    assert "'Active'" in ligne, 'la valeur affirmée doit être un mot'
    assert "'Inconnue'" in ligne, (
        'le cas « le serveur n\'a pas confirmé » doit se dire « Inconnue » : '
        '« Non » affirmerait que le terminal peut passer un ordre.')
    assert '✓' not in ligne and '⚠' not in ligne, (
        'la valeur est redevenue un pictogramme.')
