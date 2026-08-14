"""LOT 614 — LE PALIER `muted` PASSE LE SEUIL, ET LES DEUX RÔLES DE #8A8284
RESTENT SÉPARÉS.

Le lot 613 avait mesuré `--vx-text-muted` **#8A8284 à 4,04:1** sous `.vx-meta`,
`.vx-kpi-label`, `.vx-card-footer` et `.vx-muted` — **11 combinaisons page ×
largeur** — et l'avait **refusé** (60 littéraux, décision de design). L'humain a
tranché : le lot 614 le porte à **#989092** (ratio **4,86**, marge **+0,36** ; le
minimum strict #938a8c ne laissait que **+0,01**, soit aucune marge).

Mesuré au navigateur, 8 pages × 2 largeurs, avant/après : les **sept** familles
qui étaient sous le seuil **par les deux méthodes** l'ont toutes quitté
(combinaisons sous seuil : **23 → 16**).

**LE PIÈGE QUE CE GARDIEN EXISTE POUR TENIR** : `#8A8284` portait **deux rôles**.

| rôle | ce qu'il colore | a suivi le correctif ? |
| --- | --- | --- |
| **texte discret** | token, 39 replis, `palette.TEXT_MUTED`, `VXCharts.colors.muted` | **oui → #989092** |
| **série neutre acier** | `--vx-steel-3`, `palette.COPPER`, dernière série des graphiques, lignes support/résistance | **non → #8A8284** |

Un `sed` aveugle aurait changé **la couleur d'une série de données** au prétexte
de rendre du texte lisible. Ce gardien empêche que les deux rôles se rejoignent
par accident dans un sens comme dans l'autre.
"""

import glob
import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TOKENS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'tokens.css')
_PALETTE = os.path.join(_ROOT, 'vertex', 'visualization', 'palette.py')
_CHART_CORE = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js', 'charts',
                           'chart-core.js')

_SEUIL_AA = 4.5

# Fond composé sous `.vx-meta` / `.vx-kpi-label`, MESURÉ au navigateur (luminance
# relative WCAG) : le pire fond réel du produit pour ce palier. Plus clair que
# toute surface opaque déclarée — c'est un empilement de voiles de verre.
_PIRE_FOND_MESURE = 0.01939
# Ratio mesuré après correctif.
_RATIO_ATTENDU = 4.86


def _lire(chemin):
    return io.open(chemin, encoding='utf-8').read()


def _tokens():
    out = {}
    for m in re.finditer(r'(--vx-[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;', _lire(_TOKENS)):
        out.setdefault(m.group(1), m.group(2).lower())
    return out


def _canal(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _luminance(hexa):
    h = hexa.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _canal(r) + 0.7152 * _canal(g) + 0.0722 * _canal(b)


def _ratio_l(l1, l2):
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def _sources_servies():
    fichiers = []
    for motif in ('vertex/**/*.py', 'vertex/**/*.css', 'vertex/**/*.js'):
        fichiers += glob.glob(os.path.join(_ROOT, motif), recursive=True)
    fichiers.append(os.path.join(_ROOT, 'terminal.py'))
    return sorted(set(f for f in fichiers if os.path.isfile(f)))


def test_le_palier_muted_atteint_le_seuil_sur_le_pire_fond_mesure():
    """Le correctif du lot 614. Avant : 4,04 — sous le seuil sur 11 combinaisons."""
    muted = _tokens().get('--vx-text-muted')
    assert muted, '--vx-text-muted introuvable dans tokens.css'
    r = _ratio_l(_luminance(muted), _PIRE_FOND_MESURE)
    assert r >= _SEUIL_AA, (
        '`--vx-text-muted` (%s) donne %.2f sur le pire fond mesuré du produit, sous '
        'le seuil de %.1f. Ce palier porte les métadonnées, les étiquettes de KPI et '
        'les pieds de carte — le texte qui dit D\'OÙ vient un chiffre. Re-mesurer au '
        'navigateur avant de publier.' % (muted, r, _SEUIL_AA))


def test_la_marge_du_palier_muted_n_est_pas_symbolique():
    """Le minimum strict (#938a8c) donnait +0,01. Une conformité qui tient à un
    centième n'est pas une conformité : le moindre ajustement de surface la
    reperd, en silence, sans qu'aucun test ne bouge."""
    muted = _tokens()['--vx-text-muted']
    r = _ratio_l(_luminance(muted), _PIRE_FOND_MESURE)
    assert abs(r - _RATIO_ATTENDU) < 0.10, (
        'ratio mesuré %.2f, le lot 614 avait mesuré %.2f. Soit le token a bougé, '
        'soit le fond a changé : re-mesurer et mettre à jour SKYLER-LOT-614.md, qui '
        'affirme un chiffre qui ne serait plus vrai.' % (r, _RATIO_ATTENDU))
    assert r - _SEUIL_AA >= 0.20, (
        'marge de seulement %+.2f au-dessus du seuil. Le lot 614 a délibérément '
        'écarté le minimum strict pour cette raison.' % (r - _SEUIL_AA))


def test_aucun_repli_de_muted_ne_diverge_du_token():
    """Le défaut du 613 (`var(--vx-text-faint,#5f5a55)`), à 39×.

    Un repli n'agit que si la variable manque. Divergent, c'est un second
    réglage que personne ne relit — et le lot 613 a montré qu'il dérive.
    """
    token = _tokens()['--vx-text-muted']
    divergents = []
    for f in _sources_servies():
        for val in re.findall(r'var\(--vx-text-muted\s*,\s*(#[0-9a-fA-F]{6})\)',
                              _lire(f)):
            if val.lower() != token:
                divergents.append('%s : %s' % (os.path.relpath(f, _ROOT), val))
    assert not divergents, (
        'replis divergents du token %s :\n  %s' % (token, '\n  '.join(sorted(set(divergents)))))


def test_les_miroirs_du_role_texte_suivent_le_token():
    """`palette.TEXT_MUTED` et `VXCharts.colors.muted` sont des COPIES du token
    dans deux autres langages. Les laisser derrière créerait un produit où le
    texte des pages et celui des graphiques ne disent pas la même chose."""
    token = _tokens()['--vx-text-muted']
    m = re.search(r"TEXT_MUTED\s*=\s*'(#[0-9a-fA-F]{6})'", _lire(_PALETTE))
    assert m, 'TEXT_MUTED introuvable dans palette.py'
    assert m.group(1).lower() == token, (
        'palette.TEXT_MUTED (%s) ≠ token (%s)' % (m.group(1), token))
    m = re.search(r"muted:\s*'(#[0-9a-fA-F]{6})'", _lire(_CHART_CORE))
    assert m, 'VXCharts.colors.muted introuvable dans chart-core.js'
    assert m.group(1).lower() == token, (
        'VXCharts.colors.muted (%s) ≠ token (%s)' % (m.group(1), token))


def test_le_role_serie_acier_n_a_pas_suivi_le_role_texte():
    """LE PIÈGE PRINCIPAL DU LOT.

    #8A8284 portait deux rôles. Le rôle « série neutre acier » colore des
    DONNÉES : `--vx-steel-3`, `palette.COPPER`, la dernière série des graphiques,
    les lignes support/résistance. Le faire suivre un correctif de LISIBILITÉ DE
    TEXTE changerait la couleur d'une série sans qu'aucune mesure ne le demande.
    """
    t = _tokens()
    steel = t.get('--vx-steel-3')
    assert steel, '--vx-steel-3 introuvable'
    assert steel == '#8a8284', (
        '--vx-steel-3 vaut %s. Ce token colore une SÉRIE DE DONNÉES, pas du texte : '
        's\'il a bougé avec le palier de texte, les deux rôles ont été confondus.'
        % steel)
    assert steel != t['--vx-text-muted'], (
        'le rôle « série acier » et le rôle « texte discret » ont repris la même '
        'valeur. Ils ont été séparés au lot 614 précisément pour ne plus l\'être : '
        'les rejoindre rend impossible de corriger l\'un sans déplacer l\'autre.')
    m = re.search(r"COPPER\s*=\s*'(#[0-9a-fA-F]{6})'", _lire(_PALETTE))
    assert m and m.group(1).lower() == '#8a8284', (
        'palette.COPPER a suivi le correctif de texte — c\'est la série neutre acier.')


def test_la_hierarchie_des_quatre_paliers_tient_toujours():
    """Le lot 613 avait établi que `faint` et `muted` sont couplés : remonter
    l'un sans regarder l'autre inverse l'échelle. Le 614 remonte `muted`, donc
    l'écart s'ouvre — ce test vérifie qu'il ne s'est pas ouvert dans le mauvais
    sens, et que `muted` n'a pas rattrapé `secondary`."""
    t = _tokens()
    echelle = ['--vx-text-primary', '--vx-text-secondary', '--vx-text-muted',
               '--vx-text-faint']
    lums = [(n, _luminance(t[n])) for n in echelle if t.get(n)]
    assert len(lums) == 4, 'un palier de texte a disparu de tokens.css'
    for (n1, l1), (n2, l2) in zip(lums, lums[1:]):
        assert l1 > l2, ('hiérarchie rompue : %s (L=%.4f) n\'est plus plus clair '
                         'que %s (L=%.4f)' % (n1, l1, n2, l2))
