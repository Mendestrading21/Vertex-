"""SIGNAL OS · LE CONTRASTE NON TEXTUEL — et trois fois le même piège d'instrument.

Suite du lot 22, côté **non textuel** : WCAG 1.4.11 demande 3:1 pour ce qui
permet d'identifier un composant **et son état**.

## Deux résultats, dont un vide

**Rien côté graphiques.** Les cinq séries et les couleurs sémantiques passent
toutes contre le fond de graphique (4,84 à 10,39), et **zéro trait SVG** sous le
seuil sur les 35 vues. Un résultat vide ne vaut que parce que l'instrument
pouvait échouer — et il a échoué ailleurs, sur la même page.

**Un défaut systémique côté contrôles.** 56 boutons, chips, champs et selects
sur 14 familles rendaient **1,15 à 1,24:1**.

## Le constat honnête sur la cause

Ce n'est **pas** « quelqu'un a cassé une valeur » : **aucun** jeton de bordure du
produit n'atteint 3:1 — même `--vx-border-strong` plafonne à **2,51**. C'est un
parti pris cohérent des deux couches, pas une régression.

La correction est donc **scopée aux contrôles** : les bordures décoratives
(cartes, séparateurs) gardent leur discrétion, parce que la règle porte sur ce
qui **identifie un composant**, pas sur tout trait. `primary`, `ghost` et `link`
restent exclus — ils n'ont pas de bordure par choix et sont identifiés par leur
fond ou leur nature de lien ; leur en donner une aurait inventé un défaut en
corrigeant l'autre.

## Trois fois le même piège, et je ne l'ai vu qu'à la troisième

L'instrument ne regardait **qu'un seul canal** à la fois :

1. **La bordure seule** — il accusait des composants dont le fond portait déjà
   la limite. Corrigé en prenant le meilleur de *bordure ou fond*.
2. **La cascade déduite au lieu d'être mesurée** — ma première correction
   empilait un override de spécificité *inférieure*. Elle n'a rien changé pour
   les champs ni les chips ; seuls les boutons passaient, parce que leur chaîne
   de `:not()` les faisait gagner. J'ai fini par **demander au moteur** quelles
   règles s'appliquaient, au lieu de raisonner sur l'ordre des feuilles — et la
   gagnante était une règle scopée que je n'avais pas lue.
3. **L'anneau `box-shadow` ignoré** — l'instrument déclarait en échec un contrôle
   que je venais de corriger. Sans ce troisième canal, il aurait poussé à
   **sur-corriger un défaut déjà résolu**.

## L'état sélectionné, mesuré plutôt que supposé

Le segment pressé ne se distinguait que par un fond violet à `.12` — 1,17:1. Son
libellé change bien de couleur (`#F5F3F0` contre `#989092`), mais cet écart vaut
**2,81:1** : il porte *presque* l'état, pas tout à fait. D'où un anneau interne,
qui franchit le seuil des deux côtés (3,72 contre le groupe, 3,17 contre le fond
du segment) sans décaler la mise en page.

## Trouvé en chemin, et c'est moi qui l'avais causé

Deux `C.colors.series[i % 6]` sur un tableau de **cinq** entrées, hérités du
retrait d'`OPTION` de la série que j'ai fait moi-même. Latents aujourd'hui
(aucun graphique n'atteint six séries, et les overlays portent tous une couleur
explicite), mais silencieusement hors palette dès qu'une sixième série
apparaît : `series[5]` vaut `undefined`.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CSS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css')
_JS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js', 'charts')


def _lire(*p):
    return io.open(os.path.join(*p), encoding='utf-8').read()


def _jetons():
    src = _lire(_CSS, 'tokens.css') + _lire(_CSS, 'signal-os.css')
    brut = dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', src))
    out = {}
    for k in brut:
        v = brut[k].strip()
        for _ in range(8):
            m = re.fullmatch(r'var\((--[a-z0-9-]+)\)', v)
            if not m:
                break
            s = (brut.get(m.group(1)) or '').strip()
            if not s or s == v:
                break
            v = s
        out[k] = v
    return out


def _rgba(v):
    v = v.strip()
    m = re.fullmatch(r'#([0-9a-fA-F]{6})', v)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.fullmatch(r'rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)', v)
    if m:
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)),
                1.0 if m.group(4) is None else float(m.group(4)))
    raise AssertionError('couleur non analysable : %r' % v)


def _sur(t, f):
    return (t[0] * t[3] + f[0] * (1 - t[3]), t[1] * t[3] + f[1] * (1 - t[3]),
            t[2] * t[3] + f[2] * (1 - t[3]), 1.0)


def _lum(c):
    def f(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def _ratio(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# Les fonds réels sur lesquels un contrôle peut reposer, dérivés des jetons.
_FONDS = ('--vx-canvas', '--vx-surface', '--vx-surface-elevated')


def test_la_limite_d_un_controle_est_perceptible():
    """Le défaut mesuré, tenu par le CALCUL : le jeton pourrait être renommé ou
    ramené à sa valeur d'origine, les deux cassent ce test."""
    j = _jetons()
    c = _rgba(j['--vx-border-control'])
    for f in _FONDS:
        fond = _rgba(j[f])
        r = _ratio(_sur(c, fond), fond)
        assert r >= 3.0, (
            'la limite des contrôles repasse sous 3:1 sur %s (%.2f). Les '
            'boutons, chips et champs redeviennent des zones sans contour.'
            % (f, r))


def test_la_limite_de_marque_tient_aussi_l_etat_selectionne():
    """Le même jeton sert deux rôles mesurés : la bordure du bouton `soft` et
    l'anneau du segment pressé. Les deux ont été calculés sur leur fond réel."""
    j = _jetons()
    c = _rgba(j['--vx-border-control-brand'])
    for f in _FONDS:
        fond = _rgba(j[f])
        r = _ratio(_sur(c, fond), fond)
        assert r >= 3.0, (
            'la limite de marque repasse sous 3:1 sur %s (%.2f) : le segment '
            'sélectionné et le bouton « soft » reperdent leur contour.' % (f, r))


def test_la_correction_est_posee_ou_la_bordure_est_declaree():
    """CONTRE-EXEMPLE de ma propre erreur. Un jeton parfait ne sert à rien s'il
    est appliqué par une règle de spécificité inférieure : ma première version
    n'a rien changé pour les champs ni les chips. On vérifie donc les DEUX
    déclarations réellement gagnantes, mesurées au moteur, pas déduites."""
    css = _lire(_CSS, 'signal-os.css')
    i = css.index('.vx-content :is(input:not([type="checkbox"])')
    bloc = css[i:css.index('}', i)]
    assert 'border:1px solid var(--vx-border-control)' in bloc, (
        'la règle scopée des champs est revenue à `--vx-border-soft` : c\'est '
        'ELLE qui gagne, un override plus faible ailleurs ne suffit pas.')
    # Ancre sur LA règle des chips, pas sur la première déclaration qui lui
    # ressemble : `backdrop-filter:none` figure aussi dans une autre règle plus
    # haut, et le test échouait sur un bloc qui n'était pas celui corrigé.
    i = css.index('"]) .vx-chip{')
    bloc = css[i:css.index('}', i)]
    assert 'border:1px solid var(--vx-border-control)' in bloc, (
        'la règle scopée des chips est revenue à `--vx-border-soft`.')


def test_l_etat_selectionne_du_controle_segmente_porte_un_anneau():
    """WCAG 1.4.11 couvre les ÉTATS. Le libellé seul portait 2,81:1 — presque,
    pas assez."""
    css = _lire(_CSS, 'signal-os.css')
    i = css.rindex('.vx-segmented button[aria-pressed="true"]')
    bloc = css[i:css.index('}', i)]
    assert 'inset 0 0 0 1px var(--vx-border-control-brand)' in bloc, (
        'le segment sélectionné a reperdu son anneau : son état ne tient plus '
        'qu\'à un fond à 1,17:1 et à un libellé à 2,81:1.')


def test_aucune_longueur_de_serie_figee():
    """Le défaut trouvé en chemin, et que j'ai moi-même causé en retirant
    `OPTION` de la série : deux `series[i % 6]` sur un tableau de cinq. Latent
    — donc invisible jusqu'au jour où une sixième série apparaît, et
    silencieux ce jour-là (`series[5]` vaut `undefined`, pas une erreur)."""
    for nom in ('chart-core.js', 'price-chart.js'):
        src = _lire(_JS, nom)
        fautes = re.findall(r'colors\.series\[[^\]]*%\s*\d+\s*\]', src)
        assert not fautes, (
            '%s indexe la palette de séries avec une longueur FIGÉE : %s. '
            'Employer `C.colors.series.length` — la série a changé de taille '
            'une fois, elle rechangera.' % (nom, fautes))


def test_les_series_de_graphique_restent_visibles_sur_leur_fond():
    """Le résultat VIDE de ce lot, figé pour qu'il reste vrai. Les cinq séries
    passaient déjà ; rien n'a été touché, et c'est justement ce qu'on garde."""
    theme = _lire(_JS, 'chart-theme.js')
    m = re.search(r'series:\s*\[([^\]]+)\]', theme)
    assert m, 'la palette de séries a disparu du thème'
    series = re.findall(r'#[0-9a-fA-F]{6}', m.group(1))
    assert len(series) >= 4, 'palette de séries anormalement courte'
    fond = _rgba(re.search(r'backgroundColor:\s*\'(#[0-9a-fA-F]{6})\'', theme).group(1))
    for c in series:
        r = _ratio(_rgba(c), fond)
        assert r >= 3.0, (
            'la série %s n\'est plus visible sur le fond de graphique '
            '(%.2f:1).' % (c, r))
