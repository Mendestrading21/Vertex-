"""LOT 616 — LE TEXTE DES GRAPHIQUES, MESURÉ AU LIEU D'ÊTRE RAISONNÉ.

Le lot 614 a changé `VXCharts.colors.muted` (#8A8284 → #989092) **sur un
raisonnement** — « éclaircir sur fond sombre ne peut pas dégrader la
lisibilité » — et l'a écrit noir sur blanc : *« l'argument retenu est un
raisonnement, PAS une mesure »*. C'est la limite que le 614 publie lui-même.

Ce lot la ferme. Deux sites peignent ce token **comme texte** sur `<canvas>` :

```js
chart-core.js:445     ctx.fillStyle = C.colors.muted;  ctx.font = '10px …'
markets_page.py:722   g.fillStyle = …colors.muted;     g.font  = '9px …'
```

Un `<canvas>` n'expose **aucun nœud de texte** : la composition CSS ne peut rien
dire ici, seuls les pixels peints existent. Mesure au navigateur sur les 8 pages
servies, en sondant **les régions où le texte est réellement peint** (centre de
l'anneau, bande d'axes, bande haute) et en appliquant le critère du 613/614 —
la **part de la dominante** dit si l'échantillon est un fond :

| | régions | pire ratio |
| --- | --- | --- |
| sondées | 12 | — |
| **retenues** *(part ≥ 55 %, mesurée 59 à 84 %)* | **5** | — |
| `colors.muted` sur fond de graphique | | **6,16** |
| `colors.text` sur fond de graphique | | **9,89** |

**Le raisonnement du 614 est confirmé par la mesure.** Aucun octet servi n'a
changé — ce lot ne corrige rien, il **transforme une dette en fait**.

Ce gardien encode le modèle que la mesure a validé : les canvas n'ont pas de
fond opaque propre, donc le texte des graphiques est peint sur **les surfaces de
carte**, et le calcul redevient dérivable des tokens sur disque.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TOKENS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'tokens.css')
_CORE = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js', 'charts', 'chart-core.js')
_MARKETS = os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'markets_page.py')
_CSS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css')

_SEUIL_AA = 4.5
_MARGE_MINIMALE = 0.20                     # règle 614-B
# Les surfaces opaques sur lesquelles une carte de graphique peut reposer.
_SURFACES = ('--vx-canvas', '--vx-shell', '--vx-surface', '--vx-surface-elevated')
# Pire ratio mesuré au navigateur, régions retenues uniquement.
_MESURE_MUTED = 6.16
_MESURE_TEXTE = 9.89


def _lire(p):
    return io.open(p, encoding='utf-8').read()


def _tokens():
    out = {}
    for m in re.finditer(r'(--vx-[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;', _lire(_TOKENS)):
        out.setdefault(m.group(1), m.group(2).lower())
    return out


def _couleurs_graphiques():
    src = _lire(_CORE)
    out = {}
    for cle in ('text', 'muted'):
        m = re.search(r"\b%s:\s*'(#[0-9a-fA-F]{6})'" % cle, src)
        assert m, '%s introuvable dans chart-core.js' % cle
        out[cle] = m.group(1).lower()
    return out


def _canal(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _luminance(hexa):
    h = hexa.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _canal(r) + 0.7152 * _canal(g) + 0.0722 * _canal(b)


def _ratio(a, b):
    l1, l2 = _luminance(a), _luminance(b)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def test_le_texte_des_graphiques_atteint_le_seuil_avec_marge():
    """Ce que la mesure du 616 a établi, rendu vérifiable sur disque."""
    t, c = _tokens(), _couleurs_graphiques()
    manques = []
    for role, valeur in c.items():
        for s in _SURFACES:
            assert t.get(s), '%s introuvable — la mesure du lot 616 est périmée' % s
            r = _ratio(valeur, t[s])
            if r < _SEUIL_AA + _MARGE_MINIMALE:
                manques.append('colors.%s sur %s : %.2f' % (role, s, r))
    assert not manques, (
        'le texte des graphiques retombe sous %.1f + %.2f de marge :\n  %s\n'
        'Ce texte est peint en canvas : AUCUN outil DOM ne le verra, et aucun '
        'balayage de contraste ne le signalera. Re-mesurer au navigateur '
        '(échantillonnage de pixels, critère de la part de dominante) avant de '
        'publier.' % (_SEUIL_AA, _MARGE_MINIMALE, '\n  '.join(manques)))


def test_la_mesure_du_navigateur_et_le_modele_sur_disque_concordent():
    """Le modèle ne vaut que s'il retrouve ce que le navigateur a mesuré.

    Pire ratio mesuré : 6,16 pour `muted`, 9,89 pour `text`. Le modèle calcule
    sur `--vx-surface-elevated`, la plus claire des surfaces de carte ; les fonds
    réellement échantillonnés allaient de (6,6,7) à (14,15,15), donc le modèle
    doit tomber dans la même zone. Un écart signifie que l'un des deux ment.
    """
    t, c = _tokens(), _couleurs_graphiques()
    fond = t['--vx-surface-elevated']
    for role, attendu in (('muted', _MESURE_MUTED), ('text', _MESURE_TEXTE)):
        calcule = _ratio(c[role], fond)
        assert abs(calcule - attendu) < 0.60, (
            'colors.%s : le modèle sur disque donne %.2f, le navigateur avait '
            'mesuré %.2f. Soit une couleur a bougé, soit les surfaces ont '
            'changé : re-mesurer et mettre à jour SKYLER-LOT-616.md.'
            % (role, calcule, attendu))


def test_les_sites_qui_peignent_le_texte_utilisent_toujours_ce_token():
    """La mesure porte sur `colors.muted`. Repointer un site de peinture sur une
    autre couleur ferait passer ce gardien au vert tout en changeant ce qui est
    réellement peint — et personne ne le verrait, faute de nœud DOM."""
    core = _lire(_CORE)
    m = re.search(r"ctx\.fillStyle\s*=\s*C\.colors\.muted;\s*\n\s*ctx\.font\s*=\s*'(\d+)px", core)
    assert m, ("le site de peinture d'étiquette de `chart-core.js` n'utilise plus "
               "`C.colors.muted` immédiatement avant sa police — la mesure du 616 "
               "ne porte plus sur ce qui est peint")
    marches = _lire(_MARKETS)
    assert 'VXCharts.colors.muted' in marches and "font='9px" in marches.replace(' ', ''), (
        "le site de peinture d'axes de `markets_page.py` a changé de couleur ou "
        'de police — re-mesurer')


def test_aucun_canvas_ne_peint_un_fond_opaque_qui_casserait_le_modele():
    """LE MODÈLE REPOSE LÀ-DESSUS.

    Le calcul sur disque suppose que le texte des graphiques est peint sur **la
    surface de la carte**. C'est vrai tant qu'aucun `<canvas>` ne pose son propre
    fond opaque. Un seul en pose un — `#op-scatter canvas{background:rgba(0,0,0,.14)}`
    — et c'est du **noir transparent** : il ne peut qu'assombrir, donc
    qu'augmenter le contraste d'un texte clair. Un fond CLAIR, lui, invaliderait
    le modèle **sans qu'aucun test de token ne bouge**.
    """
    # Découpage en blocs `sélecteur { déclarations }`. Chercher la sous-chaîne
    # « canvas » ne suffit pas : `--vx-canvas` apparaît dans des déclarations et
    # ferait remonter des blocs qui ne visent aucun `<canvas>` (faux positif
    # rencontré en écrivant ce test).
    suspects = []
    for nom in sorted(os.listdir(_CSS)):
        if not nom.endswith('.css'):
            continue
        src = _lire(os.path.join(_CSS, nom))
        for m in re.finditer(r'([^{}]*)\{([^{}]*)\}', src):
            selecteur = m.group(1)
            if not re.search(r'(^|[\s>,+~])canvas($|[\s{,:\[])', selecteur):
                continue
            for bg in re.findall(r'background(?:-color)?\s*:\s*([^;}]+)', m.group(2)):
                bg = bg.strip()
                if bg in ('none', 'transparent') or bg.startswith('var('):
                    continue
                rgba = re.match(r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,', bg)
                if rgba and all(int(x) <= 24 for x in rgba.groups()):
                    continue          # noir (ou quasi) transparent : assombrit
                suspects.append('%s : %s' % (nom, bg[:60]))
    assert not suspects, (
        'un `<canvas>` peint un fond qui n\'est pas du noir transparent :\n  %s\n'
        'Le modèle du lot 616 — « le texte des graphiques repose sur la surface '
        'de la carte » — ne tient plus, et la mesure du navigateur doit être '
        'refaite sur ce fond.' % '\n  '.join(suspects))
