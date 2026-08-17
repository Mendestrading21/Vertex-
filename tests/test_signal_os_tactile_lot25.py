"""SIGNAL OS · CIBLES TACTILES — et une politique qui rate ce qu'elle ne nomme pas.

Trois contrôles jamais mesurés. **Deux rendent vide**, un trouve un défaut.

| contrôle | résultat |
| --- | --- |
| animations sous « animations réduites » | **0** sur 35 vues |
| titres de page uniques | **9 / 9**, aucun doublon |
| cibles tactiles ≥ 24×24 à 390 px | **6 familles en dessous** |

## La précision qui compte : ce n'est PAS une violation

WCAG 2.5.8 exempte les cibles suffisamment **espacées**. Mesuré : les voisins
les plus proches sont à **40 à 121 px**. L'exception s'applique, donc le produit
est conforme.

C'est un défaut de **confort sur téléphone** — 15 à 17 px de haut sous le
pouce — et l'utilisateur consulte Vertex sur iPhone. Le corriger relève du
produit, pas de la norme. Le dire autrement serait invoquer une autorité qu'on
n'a pas.

## La cause, et c'est la troisième fois

La politique de taille tactile mobile est définie **par classe** :

```css
.vx-btn,.vx-tab,.vx-chip{min-height:40px}
```

Donc **tout contrôle qui ne porte pas la classe y échappe**. Le lot 294 avait
déjà dû rattraper les contrôles segmentés — son commentaire le dit mot pour
mot : « hors de la règle ci-dessus car sans classe vx-btn ». La mesure à 390 px
en a trouvé deux familles de plus.

> Une règle qui s'applique par nom de classe ne protège que ce qu'on a pensé à
> nommer. Trois rattrapages font un motif, pas une série d'oublis.

D'où une règle qui vise le **comportement** — `role="button"`,
`data-open-analysis`, `a[onclick]` — et couvre donc aussi les contrôles à venir.

Seuil **32 px** : celui que le produit s'est déjà donné pour les actions
secondaires (`.vx-btn-sm`), pas un nombre inventé. Et `inline-flex` est
indispensable : `min-height` ne fait rien sur un élément inline.
"""

import io
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lire(*p):
    return io.open(os.path.join(_ROOT, *p), encoding='utf-8').read()


def _bloc_mobile():
    """Le bloc mobile de `responsive.css`, borné à la règle qui nous intéresse.

    Portée : `min-height:32px` figure ailleurs dans le fichier (`.vx-btn-sm`).
    Le chercher dans tout le fichier laissait passer le retrait de la règle
    visée.
    """
    css = _lire('vertex', 'static', 'vertex', 'css', 'responsive.css')
    i = css.index('[role="button"]:not(.vx-btn)')
    return css[i:css.index('}', i)]


def test_la_taille_tactile_vise_le_comportement_et_non_la_classe():
    """Le cœur du lot. Une règle par classe ne protège que ce qu'on a pensé à
    nommer — trois rattrapages l'ont montré (segmentés au lot 294, tickers et
    liens de secteur ici)."""
    bloc = _bloc_mobile()
    assert 'min-height:32px' in bloc, (
        'la hauteur tactile minimale a disparu de la règle : les tickers '
        'cliquables retombent à 17 px de haut sous le pouce.')
    # `min-height` ne fait RIEN sur un element inline : sans ce display, la
    # regle est presente et sans effet — le pire des deux mondes.
    assert 'display:inline-flex' in bloc, (
        '`min-height` sans `inline-flex` n\'a aucun effet sur un élément '
        'inline : la règle existerait sans rien changer à l\'écran.')
    assert 'align-items:center' in bloc


def test_les_trois_familles_mesurees_sont_couvertes():
    """Les sélecteurs sont nommés un par un : c'est CHAQUE famille mesurée qui
    doit rester couverte, pas « au moins un sélecteur quelque part »."""
    css = _lire('vertex', 'static', 'vertex', 'css', 'responsive.css')
    i = css.index('[role="button"]:not(.vx-btn)')
    selecteurs = css[i:css.index('{', i)]
    for s in ('[role="button"]', '[data-open-analysis]', 'a[onclick]'):
        assert s in selecteurs, (
            'la famille %s n\'est plus couverte par la règle de taille '
            'tactile.' % s)


def test_la_politique_par_classe_survit_pour_les_composants_qui_la_portent():
    """CONTRE-EXEMPLE : la nouvelle règle ne remplace pas l'ancienne, elle la
    complète. Les boutons et chips gardent leurs 40 px — les exclure de la
    nouvelle règle (`:not(.vx-btn)`) évite de les RABAISSER à 32."""
    css = _lire('vertex', 'static', 'vertex', 'css', 'responsive.css')
    assert '.vx-btn,.vx-tab,.vx-chip{min-height:40px}' in css, (
        'la politique historique a disparu : les actions primaires perdent '
        'leurs 40 px.')
    bloc_sel = css[css.index('[role="button"]:not(.vx-btn)'):]
    bloc_sel = bloc_sel[:bloc_sel.index('{')]
    assert ':not(.vx-btn)' in bloc_sel and ':not(.vx-chip)' in bloc_sel, (
        'la nouvelle règle ne s\'exclut plus des composants déjà couverts : '
        'elle RABAISSERAIT les boutons de 40 à 32 px.')


def test_le_seuil_reste_celui_que_le_produit_s_est_donne():
    """32 px n'est pas un nombre choisi par moi : c'est le seuil que le produit
    applique déjà aux actions secondaires. En inventer un autre aurait créé une
    troisième échelle dans un système qui en a déjà deux."""
    css = _lire('vertex', 'static', 'vertex', 'css', 'responsive.css')
    assert '.vx-btn-sm{min-height:32px}' in css, (
        'le seuil des actions secondaires a changé — la règle tactile du '
        'lot 25 s\'y adossait ; vérifier que les deux restent cohérents.')
