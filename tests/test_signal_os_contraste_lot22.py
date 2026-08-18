"""SIGNAL OS · LE CONTRASTE RÉEL — mesuré, et tenu par le calcul.

## L'audit qui n'avait jamais été fait

Ratio WCAG de **chaque** élément portant du texte, contre son fond **effectif**
— composition des couches semi-transparentes en remontant les ancêtres. Lire le
`backgroundColor` de l'élément seul rend `rgba(0,0,0,0)` partout et un ratio
faux : c'est ce qui rend ce défaut invisible à l'inspection ordinaire.

**2 309 éléments sur 35 vues. 3 familles en échec.**

## Un seul mécanisme derrière les trois

> Une teinte sémantique **éclaircit** le fond ; le texte qui la traverse perd le
> contraste qu'il avait sur le fond nominal.

### 1. Le négatif comme texte sur sa propre teinte

| fond | `--vx-negative` (#E9555F) |
| --- | --- |
| canevas | 5,69 |
| carte | 5,12 – 5,30 |
| **sa propre teinte** | **4,20 – 4,39** |

Des trois couleurs sémantiques, c'est **la seule** dans ce cas — l'avertissement
rend 7,28 et le positif 6,02 sur leur teinte. D'où un jeton dédié,
`--vx-negative-text`, et **surtout pas** un éclaircissement de `--vx-negative` :
il sert de couleur de perte partout ailleurs, où il passe, et le repeindre
changerait chaque chiffre rouge du produit.

### 2. Le texte assourdi dans un insight

cyan **4,26** · avertissement **4,11** — sous le seuil ; violet 4,66, soit moins
de 0,2 de marge. Les trois teintes sont traitées par une règle unique : sur une
surface teintée, le texte discret monte d'un cran.

Les deux teintes non listées par l'audit ne l'étaient pas parce qu'elles
tenaient, mais parce qu'aucune vue visitée ne rendait de texte assourdi dessus.

## Ce que ce gardien fait, et pourquoi il calcule

Épingler `color:var(--vx-negative-text)` ne prouve rien : le jeton pourrait
valoir n'importe quoi. Le gardien **recalcule** le ratio depuis `tokens.css`,
en composant la teinte sur le fond de carte. Un changement de valeur qui casse
le contraste échoue, même si aucune règle CSS n'a bougé.

## Le focus clavier — mesuré, rien trouvé

109 familles d'éléments atteintes au clavier sur les 8 espaces : **toutes** ont
un indicateur de focus visible. Mesuré en comparant l'état focalisé au même
sélecteur non focalisé — sans cette référence, une carte portant déjà une ombre
passerait pour « focus visible » alors que rien ne change.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CSS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css')


def _lire(nom):
    return io.open(os.path.join(_CSS, nom), encoding='utf-8').read()


def _jetons():
    """Les propriétés personnalisées de `tokens.css`, chaînes `var()` résolues."""
    src = _lire('tokens.css')
    brut = dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', src))
    out = {}
    for k in brut:
        v = brut[k].strip()
        for _ in range(8):                      # borne : un alias circulaire
            m = re.fullmatch(r'var\((--[a-z0-9-]+)\)', v)
            if not m:
                break
            suivant = (brut.get(m.group(1)) or '').strip()
            if not suivant or suivant == v:
                break
            v = suivant
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
        a = 1.0 if m.group(4) is None else float(m.group(4))
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)), a)
    raise AssertionError('couleur non analysable : %r' % v)


def _sur(teinte, fond):
    """La teinte composée sur un fond opaque."""
    tr, tg, tb, a = teinte
    fr, fg, fb, _ = fond
    return (tr * a + fr * (1 - a), tg * a + fg * (1 - a), tb * a + fb * (1 - a), 1.0)


def _lum(c):
    def f(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def _ratio(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# Les deux fonds de carte réels du produit, dérivés des jetons — pas écrits à la
# main : si la surface change, le calcul suit.
_SURFACES = ('--vx-surface', '--vx-surface-elevated')


def test_le_negatif_de_texte_est_lisible_sur_sa_propre_teinte():
    """Le défaut mesuré, tenu par le CALCUL et non par une chaîne. Le jeton
    pourrait être renommé, redirigé, ou revenir à la valeur d'origine : les
    trois cassent ce test, parce qu'il recompose la couleur."""
    j = _jetons()
    texte = _rgba(j['--vx-negative-text'])
    teinte = _rgba(j['--vx-negative-soft'])
    for s in _SURFACES:
        fond = _sur(teinte, _rgba(j[s]))
        r = _ratio(texte, fond)
        assert r >= 4.5, (
            'la bannière d\'erreur repasse sous le seuil AA sur %s : %.2f:1. '
            'Le texte négatif doit rester lisible sur sa propre teinte.' % (s, r))


def test_le_negatif_de_base_n_est_pas_eclairci_pour_faire_passer_le_test():
    """CONTRE-EXEMPLE, et c'est lui qui compte. La correction « évidente » du
    test précédent est d'éclaircir `--vx-negative` jusqu'à ce qu'il passe. Ce
    serait faux : ce jeton est la couleur de PERTE dans tout le produit, où il
    rend déjà 5,12 à 5,69:1. L'éclaircir repeindrait chaque chiffre rouge pour
    résoudre un problème qui n'existe que sur une surface teintée."""
    j = _jetons()
    assert j['--vx-negative'].lower() == '#e9555f', (
        '`--vx-negative` a changé de valeur (%s). Si c\'était pour corriger un '
        'contraste, vérifier d\'abord OÙ il manquait : sur le canevas et sur '
        'une carte il passait déjà — seule sa propre teinte échouait, et c\'est '
        '`--vx-negative-text` qui existe pour ça.' % j['--vx-negative'])
    # Et la valeur de base DOIT rester lisible là où elle sert vraiment.
    for s in _SURFACES:
        r = _ratio(_rgba(j['--vx-negative']), _rgba(j[s]))
        assert r >= 4.5, (
            '`--vx-negative` n\'est plus lisible sur %s (%.2f:1) : les chiffres '
            'de perte deviennent illisibles sur une carte ordinaire.' % (s, r))


def test_la_banniere_d_erreur_emploie_le_jeton_de_texte():
    """Le calcul ci-dessus ne vaut que si la bannière emploie RÉELLEMENT ce
    jeton. Sans cette assertion, on pourrait garder un jeton parfait et ne
    l'utiliser nulle part."""
    css = _lire('signal-os.css')
    i = css.index('.vx-error-banner{')
    bloc = css[i:css.index('}', i)]
    assert 'color:var(--vx-negative-text)' in bloc, (
        'la bannière d\'erreur est revenue à `--vx-negative`, illisible sur '
        'son propre fond teinté (4,38:1).')


def test_le_texte_discret_monte_d_un_cran_sur_une_surface_teintee():
    """La règle, et la preuve qu'elle suffit : `--vx-text-secondary` est
    recalculé sur les TROIS teintes d'insight, pas seulement celle qui a
    échoué à la mesure."""
    css = _lire('signal-os.css')
    assert '.vx-insight .vx-meta' in css and '.vx-insight .vx-kpi-label' in css, (
        'la règle qui relève le texte discret dans un insight a disparu : le '
        'texte assourdi y retombe à 4,11-4,26:1.')
    i = css.index('.vx-insight .vx-meta')
    bloc = css[i:css.index('}', i)]
    assert 'color:var(--vx-text-secondary)' in bloc

    j = _jetons()
    secondaire = _rgba(j['--vx-text-secondary'])
    for teinte in ('--vx-cyan-soft', '--vx-violet-soft', '--vx-warning-soft'):
        for s in _SURFACES:
            fond = _sur(_rgba(j[teinte]), _rgba(j[s]))
            r = _ratio(secondaire, fond)
            assert r >= 4.5, (
                'le texte discret d\'un insight %s repasse sous AA (%.2f:1) '
                'sur %s.' % (teinte, r, s))


def test_le_texte_assourdi_reste_lisible_la_ou_il_sert_vraiment():
    """Pourquoi la règle est SCOPÉE aux insights plutôt qu'appliquée partout :
    sur les surfaces nominales, `--vx-text-muted` passe. Relever le jeton
    global aurait aplati la hiérarchie typographique de tout le produit pour
    un défaut qui n'apparaît que sur une teinte."""
    j = _jetons()
    muted = _rgba(j['--vx-text-muted'])
    for s in ('--vx-canvas',) + _SURFACES:
        r = _ratio(muted, _rgba(j[s]))
        assert r >= 4.5, (
            '`--vx-text-muted` n\'est plus lisible sur %s (%.2f:1) — cette fois '
            'le défaut est global et le jeton lui-même doit changer.' % (s, r))
