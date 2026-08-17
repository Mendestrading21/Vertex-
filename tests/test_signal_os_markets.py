"""SIGNAL OS · MARCHÉS — quatre pastilles coupées en plein mot à 390 px.

Le lot Shell avait signalé « 2 éléments coupés d'environ 40 px » sur `/markets`.
La mesure de ce lot corrige ce chiffre : **quatre**, et de 25 à 66 px.

Le premier compte n'avait retenu que ce qui dépassait le **viewport**. Or
`.vx-mk-idx` porte `overflow:hidden` : deux cartes de la colonne de gauche
débordaient de leur **carte** sans atteindre le bord de l'écran, donc sans être
comptées — alors qu'elles étaient tout autant coupées.

## Ce que la capture à 390 px montrait

| élément | attendu | rendu |
| --- | --- | --- |
| pastille de plage | `près du haut` | `près du h` |
| pastille de plage | `milieu de plage` | `milie` |
| nom de l'indice | `S&P 500` | sur deux lignes, comprimé à 25 px |
| variation | `+1,67 %` | `+1,67` puis `%` seul sur la ligne suivante |

**Trois symptômes, un mécanisme** : une rangée `flex` en `nowrap` contenant une
pastille en `white-space:nowrap` que rien ne peut réduire. La pastille prend ce
qu'il lui faut, le nom se fait écraser, et le débord est **rogné en silence**
par l'`overflow:hidden` de la carte — pas de points de suspension, pas de barre
de défilement, rien qui signale qu'un mot est tronqué.

## Le correctif

Sous **720 px** — bascule déjà présente dans le recensement mesuré du lot 611,
donc aucune bande de largeur neuve — la rangée passe à la ligne.

La pastille n'est **pas** masquée : « près du haut » situe le prix dans sa plage,
c'est une lecture. La cacher au mobile reviendrait à retirer une information
parce qu'elle gêne la mise en page.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_NEON = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'neon-glass.css')
_MARKETS = os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'markets_page.py')

# Bascule choisie, et déjà mesurée par le banc des neuf bandes du lot 611.
_BASCULE = 720


def _css():
    return io.open(_NEON, encoding='utf-8').read()


def _bloc_mobile():
    """Le bloc `@media (max-width:720px)` qui corrige la carte d'indice."""
    src = _css()
    for m in re.finditer(r'@media\s*\(max-width:\s*(\d+)px\)\s*\{', src):
        if int(m.group(1)) != _BASCULE:
            continue
        i = m.end()
        prof = 1
        while prof and i < len(src):
            if src[i] == '{':
                prof += 1
            elif src[i] == '}':
                prof -= 1
            i += 1
        bloc = src[m.end():i - 1]
        if _regle(bloc, 'vx-mk-idx-top') is not None:
            return bloc
    return None


def _regle(bloc, classe):
    """Déclarations de LA règle dont le sélecteur se termine par `.classe`.

    Chercher la sous-chaîne ne suffit pas, et c'est ce lot qui l'a prouvé :
    deux mutations ont d'abord passé au vert. `.vx-mk-idx-topX` contient
    `vx-mk-idx-top`, et `flex-wrap:wrap` cherché dans le BLOC entier était
    satisfait par la règle voisine `.vx-mk-idx-foot`. Une règle se lit,
    elle ne se devine pas (même famille que 616-B).
    """
    for m in re.finditer(r'([^{}]+)\{([^}]*)\}', bloc):
        sel = m.group(1).strip()
        if re.search(r'\.%s\s*$' % re.escape(classe), sel):
            return m.group(2).replace(' ', '').replace('\n', '')
    return None


def test_la_rangee_de_la_carte_indice_passe_a_la_ligne_en_mobile():
    """Sans `flex-wrap`, la pastille reste sur la rangée et rogne le nom."""
    bloc = _bloc_mobile()
    assert bloc, (
        'plus de bloc `@media (max-width:%dpx)` corrigeant `.vx-mk-idx-top` : '
        'les pastilles de plage redeviennent coupées en plein mot à 390 px.'
        % _BASCULE)
    top = _regle(bloc, 'vx-mk-idx-top')
    assert top and 'flex-wrap:wrap' in top, (
        'la rangée de la carte d\'indice ne passe plus à la ligne : %r' % top)
    nom = _regle(bloc, 'vx-mk-idx-name')
    assert nom and 'min-width:0' in nom, (
        'le nom de l\'indice ne peut plus se réduire : il sera comprimé au lieu '
        'de passer à la ligne (%r).' % nom)


def test_la_variation_ne_se_casse_plus_entre_le_nombre_et_son_unite():
    """« +1,67 % » laissait le « % » seul sur la ligne suivante."""
    chg = _regle(_bloc_mobile() or '', 'vx-mk-idx-chg')
    assert chg and 'white-space:nowrap' in chg, (
        'la variation peut de nouveau se couper entre le nombre et son unité '
        '(%r).' % chg)


def test_la_pastille_de_plage_n_est_pas_masquee_en_mobile():
    """CONTRE-EXEMPLE. La solution paresseuse — `display:none` sous 720 px —
    ferait passer tous les tests de débordement. Elle retirerait une lecture
    (« où est le prix dans sa plage ») parce qu'elle gêne la mise en page."""
    bloc = _bloc_mobile() or ''
    rel = _regle(bloc, 'vx-mk-idx-rel')
    assert rel is not None, '`.vx-mk-idx-rel` n\'est plus traitée dans le bloc mobile'
    assert 'display:none' not in rel, (
        'la pastille de plage est masquée en mobile : le débordement disparaît '
        'des mesures, et l\'information avec.')


def test_la_bascule_reste_une_bascule_deja_mesuree():
    """Anti-dérive : choisir 700 ou 640 px créerait une bande de largeur que le
    banc des neuf bandes du lot 611 n'a jamais exercée."""
    import importlib.util
    chemin = os.path.join(_ROOT, 'tests', 'test_bascules_mesurees_lot611.py')
    spec = importlib.util.spec_from_file_location('g611', chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert _BASCULE in mod._BASCULES, (
        '%d px n\'est plus dans le recensement mesuré du lot 611.' % _BASCULE)


def test_les_titres_de_marches_viennent_du_serveur():
    """La micro-copy de Marchés était réécrite dans le DOM après le rendu :
    le serveur envoyait « VIX — volatilité implicite du marché », l'écran
    affichait « VIX ». Deux vérités, et les gardiens gardaient la mauvaise."""
    src = io.open(_MARKETS, encoding='utf-8').read()
    # AGNOSTIQUE A LA BALISE, volontairement. Ce test garde le fait que le
    # titre VIENT DU SERVEUR, pas la balise qui le porte : le premier titre de
    # chaque vue est passé de `span` à `h2` au lot 24 pour réparer une ossature
    # qui sautait de h1 à h3. Épingler `<span>` revenait à interdire une
    # correction d'accessibilité au nom d'une règle de micro-copy.
    for classe, titre in (('vx-card-title', 'VIX'),
                          ('vx-card-title', 'Leadership'),
                          ('vx-card-title', 'Risque principal'),
                          ('vx-chart-title', 'Santé du marché')):
        motif = r'<(span|h2|h3) class="%s">%s</\1>' % (classe, re.escape(titre))
        assert re.search(motif, src), (
            'titre non écrit à la source : %s (classe %s)' % (titre, classe))


def test_les_libelles_longs_restent_pour_les_lecteurs_d_ecran():
    """Raccourcir un titre visible ne doit pas appauvrir le nom accessible :
    « VIX » seul ne dit pas de quoi parle la région."""
    src = io.open(_MARKETS, encoding='utf-8').read()
    for aria in ('aria-label="Régime de marché"',
                 'aria-label="Leadership sectoriel"',
                 'aria-label="Entonnoir de sélection"'):
        assert aria in src, (
            'nom accessible perdu en même temps que le titre visible : %s' % aria)
