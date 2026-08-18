"""SIGNAL OS · LE CONTRAT DE FOCUS DES SURCOUCHES, et une réserve levée.

## Deux résultats vides, et un vide qui vaut

**Les surcouches tiennent le focus.** Six critères, deux surcouches, tous verts :
ouverture, focus déplacé dedans, focus **piégé** (25 `Tab` restent dedans),
`Échap` ferme, `inert` reposé, et focus **rendu au déclencheur**.

Ce dernier point mérite d'être dit : je ne l'avais pas vu en lisant le code, et
la mesure l'a montré vrai. J'ai alors cherché **pourquoi** plutôt que de me
contenter du « oui » — `lastFocus` est capturé à l'ouverture et restauré à la
fermeture. Un résultat vert qu'on n'explique pas est un résultat qu'on n'a pas
compris.

**La réserve du lot 27 est levée.** Elle disait : sonde limitée à `Entrée` et à
six contrôles par vue. Refait sur **les deux touches** et **tous les
contrôles** — **45** au lieu de 18 — même résultat. Le plafond ne cachait rien.

## Ce que ce fichier garde

Rien de tout cela n'était protégé. `lastFocus?.focus?.()` pouvait disparaître
sans qu'un seul test bronche, et le focus serait retombé sur `<body>` à chaque
fermeture — une régression qu'aucune relecture ne remarque.
"""

import io
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SHELL = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js', 'vx-shell.js')


def _src():
    return io.open(_SHELL, encoding='utf-8').read()


def test_le_focus_est_capture_a_l_ouverture_et_rendu_a_la_fermeture():
    """Mesuré vrai au navigateur, puis expliqué dans le code. Sans la capture,
    la restauration ne peut rien rendre ; sans la restauration, le focus
    retombe sur `<body>` et l'utilisateur au clavier repart du haut de la
    page."""
    src = _src()
    assert 'let lastFocus = null;' in src, (
        'la mémoire du déclencheur a disparu : plus rien ne peut rendre le '
        'focus à la fermeture d\'une surcouche.')
    assert src.count('lastFocus = document.activeElement;') >= 2, (
        'le déclencheur n\'est plus mémorisé à l\'ouverture des DEUX '
        'surcouches (modale et tiroir).')
    assert src.count('lastFocus?.focus?.()') >= 2, (
        'le focus n\'est plus rendu au déclencheur : après Échap, il retombe '
        'sur <body> et la navigation clavier repart du haut de la page.')


def test_les_surcouches_sont_inertes_quand_elles_sont_fermees():
    """`inert` + `aria-hidden` : sans eux, une modale fermée reste dans l'ordre
    de tabulation — on tabule dans du vide invisible."""
    src = _src()
    assert "el.setAttribute('inert', '')" in src and "el.removeAttribute('inert')" in src, (
        'les surcouches ne sont plus rendues inertes à la fermeture : on peut '
        'tabuler dans une modale invisible.')
    assert "el.setAttribute('aria-hidden', 'true')" in src


def test_le_focus_est_piege_dans_la_surcouche_ouverte():
    """WCAG 2.4.3 : la tabulation ne doit pas sortir d'une modale ouverte. Le
    cycle se fait dans LES DEUX SENS — retirer la branche `shiftKey` laisserait
    le focus s'échapper vers l'arrière, ce qu'un essai qui ne tabule que vers
    l'avant ne verrait jamais."""
    src = _src()
    i = src.index("if (e.key !== 'Tab') return;")
    bloc = src[i:i + 700]
    assert 'e.shiftKey && document.activeElement === first' in bloc, (
        'le cycle ARRIÈRE a disparu : Maj+Tab depuis le premier élément sort '
        'de la surcouche.')
    assert '!e.shiftKey && document.activeElement === last' in bloc, (
        'le cycle AVANT a disparu : Tab depuis le dernier élément sort de la '
        'surcouche.')


def test_echap_ferme_toutes_les_surcouches():
    """Une seule touche, tous les niveaux — modale, tiroir, palette, menu
    contextuel. Fermer la modale sans la palette laisserait un piège ouvert."""
    src = _src()
    assert "if (e.key === 'Escape') { shell.closeAll(); return; }" in src, (
        'Échap ne ferme plus les surcouches.')
    i = src.index('closeAll() {')
    bloc = src[i:src.index('},', i)]
    # `mobileNav` a ete ajoute apres coup : je l'avais laisse hors du test comme
    # temoin de mutation, et il a SURVECU. Un temoin qui survit est soit une
    # limite assumee, soit un trou — ici c'est un trou : la nav mobile est une
    # surcouche, et si Echap cesse de la fermer, un utilisateur au telephone
    # reste bloque dedans.
    for cible in ('closeDrawer()', 'closeModal()', 'vx-palette', 'vx-context-menu',
                  'mobileNav'):
        assert cible in bloc, (
            'closeAll ne ferme plus %s : Échap laisserait ce niveau ouvert.'
            % cible)


def test_l_instrument_clavier_est_conserve_avec_son_faux_positif():
    """Le conteneur défilable ressort « muet » à chaque exécution, et c'est
    correct. L'outil le dit lui-même — sinon quelqu'un finira par « corriger »
    une région lisible au clavier en un bouton qui ne fait rien."""
    outil = os.path.join(_ROOT, 'tools', 'mesurer_clavier.py')
    assert os.path.isfile(outil), 'l\'instrument clavier a disparu'
    src = io.open(outil, encoding='utf-8').read()
    assert "mesurer_controles(pg, ' ')" in src, (
        'l\'instrument ne teste plus Espace : c\'est la moitié du contrat '
        'clavier, et la réserve du lot 27 portait précisément là-dessus.')
    assert 'for i in range(n)' in src, (
        'l\'instrument réechantillonne les contrôles au lieu de tous les '
        'tester — la réserve du lot 27 serait rouverte.')
    assert "'vx-heatmap-scroll' not in k" in src, (
        'le faux positif attendu n\'est plus écarté du verdict : l\'outil '
        'conclura « défauts trouvés » sur un motif correct.')
