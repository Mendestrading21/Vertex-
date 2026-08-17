"""SIGNAL OS · MOBILE ET SÉMANTIQUE — deux angles que les audits précédents ne couvraient pas.

## Ce qui manquait aux lots 22-23

Ils ne mesuraient qu'à **1440**. À 390, le texte tient (2 274 éléments, 0 échec)
— mais une famille non textuelle apparaît : les **lignes de tableau cliquables
en mode cartes** (`role="button"`, `tabindex`, `aria-label`), dont la carte
**est** la limite, à 1,20:1.

> Un défaut ne se voit que dans la forme où il existe. À 1440 ces lignes sont
> des lignes, pas des cartes : il n'y avait rien à trouver.

## L'audit de sémantique, jamais fait — et le produit est propre

Sur les 35 vues : **0 contrôle sans nom accessible**, **0 tableau sans `<th>`**,
**0 image sans `alt`**. Deux défauts réels seulement.

### 1. L'ossature de titres de Marchés sautait de h1 à h3

Sur les **cinq** vues. Cause exacte, mesurée : les titres de cartes de tête sont
des `<span>` — aucun titre de niveau 2 n'existait — et le `h3` venait du Chart
Shell. Sur `macro`, `sectors` et `breadth`, c'est même un **graphique** qui ouvre
la vue : promouvoir un titre de carte plus bas n'y changeait rien.

D'où `titleLevel` sur le Chart Shell : quand un graphique **ouvre** une vue, son
titre **est** le titre de section. L'option ne change rien au rendu — le style
vient de la classe, pas de la balise.

### 2. La racine du treemap d'allocation était muette

Chaque tuile porte déjà `role="img"` et son libellé, mais on entrait dans un
graphique **anonyme** avant de les rencontrer. Nommée en `role="group"` — et non
`img`, qui aurait rendu le sous-arbre opaque et fait perdre le détail par tuile.
Le résumé est **dérivé** : nombre de postes, dominant et sa part.

## Quatrième fois qu'une portée d'instrument me fait crier au loup

L'instrument accusait la jauge de Système. Or `chart-core.js` la nomme déjà sur
son conteneur, avec `role="img"` — ce qui rend le sous-arbre **opaque** pour un
lecteur d'écran. L'instrument ne regardait que l'élément lui-même.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lire(*p):
    return io.open(os.path.join(_ROOT, *p), encoding='utf-8').read()


def test_le_chart_shell_sait_ouvrir_une_section():
    """Sans `titleLevel`, un graphique qui ouvre une vue force un saut h1→h3 :
    aucun titre de niveau 2 n'existe avant lui. Le défaut se produisait sur
    quatre vues du produit."""
    src = _lire('vertex', 'static', 'vertex', 'js', 'charts', 'chart-core.js')
    assert 'const niv = (opts.titleLevel === 2) ? 2 : 3;' in src, (
        'le Chart Shell ne sait plus ouvrir une section : le titre de '
        'graphique redevient un h3 figé.')
    assert '<h${niv} class="vx-chart-title" id="${id}-title">' in src, (
        'le niveau calculé n\'est plus employé à l\'émission du titre.')
    # Le DEFAUT par defaut reste h3 : un graphique est le plus souvent une
    # sous-section. Passer tout le monde en h2 aurait juste deplace le saut.
    assert '? 2 : 3' in src


def test_les_graphiques_qui_ouvrent_une_vue_portent_le_niveau_2():
    """Les quatre sites MESURÉS au navigateur. Les nommer un par un plutôt que
    d'exiger « au moins un titleLevel quelque part » : c'est chaque vue qui
    doit tenir, pas le fichier."""
    marches = _lire('vertex', 'ui', 'pages', 'markets_page.py')
    for titre in ('Courbe des taux US', 'Rotation sectorielle — force relative × momentum',
                  'Tendance de participation'):
        i = marches.index("'" + titre + "'")
        assert 'titleLevel:2' in marches[i:i + 200], (
            'le graphique « %s » ouvre sa vue mais a reperdu son niveau 2 : '
            'l\'ossature y saute de h1 à h3.' % titre)
    op = _lire('vertex', 'ui', 'pages', 'opportunities_page.py')
    i = op.index("'Qualité × timing'")
    assert 'titleLevel:2' in op[i:i + 200], (
        'le graphique d\'ouverture du radar a reperdu son niveau 2.')


def test_les_titres_de_tete_de_marches_sont_des_titres():
    """CONTRE-EXEMPLE : il aurait suffi de poser `titleLevel` partout et de
    laisser les cartes en `<span>`. Or sur `overview` et `volatility`, c'est
    une CARTE qui ouvre la vue — son titre doit donc être un vrai titre."""
    src = _lire('vertex', 'ui', 'pages', 'markets_page.py')
    for titre in ('Régime', 'VIX', 'Leaders', 'Participation actuelle',
                  'Qualité des données'):
        motif = r'<h2 class="vx-card-title">%s</h2>' % re.escape(titre)
        assert re.search(motif, src), (
            'le titre de tête « %s » est redevenu un <span> : il ne compte '
            'plus dans l\'ossature des titres.' % titre)


def test_la_racine_du_treemap_est_nommee_sans_masquer_ses_tuiles():
    """Le détail par tuile est la vraie richesse de ce graphique : le nommer en
    `role="img"` l'aurait effacé. `group` nomme sans rendre opaque."""
    src = _lire('vertex', 'static', 'vertex', 'js', 'charts', 'chart-core.js')
    i = src.index('C.treemap = function')
    bloc = src[i:src.index('C.waterfall = function', i)]
    assert 'role="group" aria-label="${resume' in bloc, (
        'la racine du treemap a reperdu son nom : un lecteur d\'écran entre '
        'de nouveau dans un graphique anonyme.')
    assert 'role="img" aria-label="${aria' in bloc, (
        'les tuiles ont perdu leur libellé individuel.')
    # Le resume est DERIVE, pas une phrase fixe.
    assert 'rects.reduce((a, b) => (b.d.value > a.d.value ? b : a))' in bloc, (
        'le résumé du treemap n\'est plus dérivé des données tracées.')


def test_la_ligne_cliquable_en_mode_cartes_a_une_limite_visible():
    """Défaut visible SEULEMENT en mobile : à 1440 ces lignes sont des lignes
    de tableau, pas des cartes. Les lignes NON cliquables gardent leur bordure
    discrète — elles n'identifient aucun contrôle."""
    css = _lire('vertex', 'static', 'vertex', 'css', 'tables.css')
    i = css.index('.vx-table-cards tbody tr[data-clickable]')
    bloc = css[i:css.index('}', i)]
    assert 'border-color:var(--vx-border-control)' in bloc, (
        'la ligne cliquable en mode cartes reperd son contour : sa carte EST '
        'sa limite, et elle retombe à 1,20:1.')


def test_l_instrument_connait_l_opacite_d_un_ancetre_role_img():
    """Quatrième portée trop étroite de cette refonte, gardée pour qu'on ne la
    refasse pas : un ancêtre `role="img"` rend le sous-arbre opaque, donc un
    SVG à l'intérieur est DÉJÀ nommé. Sans cette règle, l'instrument accuse la
    jauge de Système, que `chart-core.js` nomme correctement."""
    src = _lire('vertex', 'static', 'vertex', 'js', 'charts', 'chart-core.js')
    assert 'class="vx-gauge" role="img" aria-label=' in src, (
        'la jauge a perdu le nom porté par son conteneur — et cette fois '
        'l\'accusation serait juste.')
