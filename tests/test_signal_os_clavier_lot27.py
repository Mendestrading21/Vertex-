"""SIGNAL OS · LES LIGNES CLIQUABLES ÉTAIENT FOCUSABLES ET INERTES.

Un contrôle **non natif** — `role="button"` sur un `<span>`, une ligne de
tableau cliquable — n'est activé au clavier que si quelqu'un l'a câblé. Le
navigateur ne le fait que pour `button`, `a[href]`, `input`, `select`.

Sonde : focus, `Entrée`, et on regarde si un clic part. **18 contrôles non
natifs testés, 3 familles muettes** — scanner LEAPS, positions options,
comparateur d'options. On pouvait les atteindre au clavier et il ne se passait
**rien** (WCAG 2.1.1).

## La cause, et c'est la même qu'au lot 25

Le gestionnaire clavier délégué n'énumérait que **trois attributs** :

```js
closest('[data-open-analysis],[data-entity-menu],[data-position-menu]')
```

Toute ligne qui n'en portait aucun était hors de sa portée.

> Une règle qui énumère des noms ne protège que ce qu'on a pensé à nommer. Au
> lot 25 c'était la taille tactile par classe ; ici c'est l'activation clavier
> par attribut. Même forme, deux endroits.

## Un second défaut, trouvé en chemin

Deux de ces familles n'ont **ni rôle ni nom accessible** : focusables et
cliquables — donc des contrôles — mais un lecteur d'écran annonce « ligne ».

L'audit du lot 24 ne les avait pas vues **parce qu'il sélectionnait
`[role="button"]`**, que justement elles n'avaient pas. Un audit ne trouve que
ce que son sélecteur admet.

## Le faux positif écarté

`.vx-heatmap-scroll` porte `role="region"` et un libellé qui annonce le
défilement horizontal : c'est un conteneur défilable focusable, motif
**correct**, où `Entrée` ne doit rien faire. C'est mon sélecteur `[tabindex="0"]`
qui l'avait ramassé — il reste « muet » à la mesure, et c'est très bien.
"""

import io
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_JS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js')


def _lire(*p):
    return io.open(os.path.join(*p), encoding='utf-8').read()


def test_l_activation_clavier_couvre_les_lignes_cliquables():
    """Le défaut fonctionnel. `[data-clickable]` est l'attribut que TOUTES les
    lignes cliquables du produit portent — le viser couvre les trois familles
    mesurées et celles à venir, là où énumérer leurs attributs propres
    (`data-candidate`, `data-ct`, `data-option-position`) aurait recommencé la
    même erreur un cran plus loin."""
    src = _lire(_JS, 'vx-entities.js')
    i = src.index("if (e.key !== 'Enter' && e.key !== ' ') return;")
    bloc = src[i:i + 400]
    assert '[data-clickable]' in bloc, (
        'les lignes cliquables sont retombées hors du gestionnaire clavier : '
        'elles redeviennent focusables et INERTES (WCAG 2.1.1).')
    for attr in ('[data-open-analysis]', '[data-entity-menu]', '[data-position-menu]'):
        assert attr in bloc, (
            'la famille %s a été retirée du gestionnaire clavier.' % attr)


def test_le_gestionnaire_laisse_les_controles_natifs_au_navigateur():
    """CONTRE-EXEMPLE : intercepter Entrée sur un `<button>` ou un `<a href>`
    déclencherait l'action DEUX fois — le navigateur le fait déjà. La garde
    qui les exclut est aussi importante que la liste qui inclut les autres."""
    src = _lire(_JS, 'vx-entities.js')
    i = src.index("if (e.key !== 'Enter' && e.key !== ' ') return;")
    bloc = src[i:i + 700]
    assert "['BUTTON', 'A', 'INPUT', 'SELECT', 'TEXTAREA'].includes(el.tagName)" in bloc, (
        'la garde des contrôles natifs a disparu : Entrée sur un bouton '
        'déclencherait son action deux fois.')


def test_les_lignes_cliquables_annoncent_leur_role_et_leur_nom():
    """Le second défaut. Focusable + cliquable = un contrôle, qui doit dire ce
    qu'il est et ce qu'il fait. Les deux fichiers sont vérifiés NOMMÉMENT : ils
    ont le même défaut mais vivent dans deux modules distincts, et n'en
    corriger qu'un laissait la moitié des lignes muettes."""
    for nom, action in (('options-structure.js', 'Ouvrir la position'),
                        ('options-scanner.js', 'Simuler')):
        src = _lire(_JS, 'pages', nom)
        assert 'role="button"' in src, (
            '%s : les lignes cliquables n\'annoncent plus leur rôle — un '
            'lecteur d\'écran dit « ligne ».' % nom)
        assert 'aria-label="' + action in src, (
            '%s : les lignes cliquables n\'annoncent plus ce qu\'elles font.'
            % nom)


def test_le_conteneur_defilable_reste_une_region_et_non_un_bouton():
    """Le faux positif, figé pour qu'on ne le « corrige » pas. Un conteneur
    défilable focusable est un motif CORRECT : lui donner `role="button"` pour
    faire taire la sonde transformerait une région lisible au clavier en un
    contrôle qui ne fait rien."""
    src = _lire(_JS, 'charts', 'heatmap.js')
    assert 'class="vx-heatmap-scroll" role="region" tabindex="0"' in src, (
        'le conteneur défilable de la heatmap a changé de rôle : vérifier '
        'qu\'on ne l\'a pas transformé en bouton pour satisfaire un '
        'instrument.')
    assert 'défilant horizontalement' in src, (
        'le libellé qui explique POURQUOI cette région est focusable a '
        'disparu.')
