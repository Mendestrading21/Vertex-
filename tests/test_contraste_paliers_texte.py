"""LOT 613 — LES QUATRE PALIERS DE TEXTE, ET CE QUE CHACUN ATTEINT.

Mesuré en vrai Chromium sur **8 pages × 2 largeurs**, 2 700 feuilles de texte,
par deux méthodes indépendantes (composition CSS des fonds ancêtres, et lecture
des pixels réellement peints sur capture `full_page`).

Le brief visait **les bandeaux d'état**. Ils sont **tous conformes** (45 feuilles,
4,79 à 17,24). Le défaut était **à côté** : `--vx-text-faint` valait `#655d5f`,
soit **3,23:1 sur la surface la PLUS favorable du produit** — ce palier ne
pouvait atteindre 4,5:1 **nulle part**, alors qu'il porte du texte réel :

| ce que ce palier écrit | taille | avant | après |
| --- | --- | --- | --- |
| `.vx-help` — texte d'aide des formulaires (4 pages) | 11 px | **3,10** | conforme |
| `.vx-mono` / `b` — noms de fichiers sur `/system` | 11 px | **3,10** | conforme |
| `.vx-op-mom .b span` — étiquettes de momentum | 8 px | **3,15** | 4,47–4,85 *(voir plus bas)* |
| `.vx-state-icon` — pictogramme d'état vide | 16 px | **3,21** | 4,93 |
| `.vx-table-cards td::before` — **l'étiquette qui nomme chaque valeur quand la
  table passe en cartes sous 768 px** | 9,5 px | — | — |

**LA CONTRAINTE QUI REND LE CORRECTIF NON TRIVIAL** : viser la conformité sur
*toutes* les surfaces déclarées imposait `#92878a`, dont la luminance (0,2527)
**dépassait celle de `--vx-text-muted`** (0,2303 à l'époque) — la hiérarchie des paliers
s'inversait. **Les deux paliers sont couplés** : on ne peut pas rendre `faint`
conforme partout sans d'abord déplacer `muted`. D'où `#847a7c` (L = 0,2028),
conforme sur les quatre surfaces où ce texte est **effectivement servi**, et qui
reste sous `muted`.

Ce gardien épingle les deux faces : le seuil **atteint**, et la limite **assumée**.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TOKENS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'tokens.css')
_POLISH = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'polish.css')

_SEUIL_AA = 4.5

# Les surfaces opaques où le palier `faint` porte du texte, mesurées au navigateur.
_SURFACES_SERVIES = ('--vx-canvas', '--vx-shell', '--vx-surface', '--vx-surface-elevated')
# Celles où il reste sous le seuil — limite assumée, documentée, non corrigée.
# LOT 615 : `surface-selected` a ete FERMEE (4,74). Seule `warm-depth` reste.
_SURFACES_HORS_PORTEE = ('--vx-warm-depth',)

def _tokens():
    src = io.open(_TOKENS, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'(--vx-[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;', src):
        out.setdefault(m.group(1), m.group(2).lower())
    return out


def _rgb(hexa):
    h = hexa.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _canal(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _luminance(hexa):
    r, g, b = _rgb(hexa)
    return 0.2126 * _canal(r) + 0.7152 * _canal(g) + 0.0722 * _canal(b)


def _ratio_l(l1, l2):
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def _ratio(texte, fond):
    return _ratio_l(_luminance(texte), _luminance(fond))


def test_le_palier_faint_atteint_le_seuil_sur_les_surfaces_servies():
    """Le correctif du lot 613. Avant : 3,23 au mieux, donc conforme nulle part."""
    t = _tokens()
    faint = t.get('--vx-text-faint')
    assert faint, '--vx-text-faint introuvable dans tokens.css'
    manques = []
    for s in _SURFACES_SERVIES:
        fond = t.get(s)
        assert fond, '%s introuvable — la mesure du lot 613 est périmée' % s
        r = _ratio(faint, fond)
        if r < _SEUIL_AA:
            manques.append('%s : %.2f' % (s, r))
    assert not manques, (
        '--vx-text-faint (%s) retombe sous %.1f:1 sur %s. Ce palier porte du TEXTE '
        'réel (aide des formulaires, noms de fichiers, étiquettes de table en mode '
        'cartes sous 768 px) : le rendre illisible n\'est pas un choix de style. '
        'Re-mesurer au navigateur avant de publier.'
        % (faint, _SEUIL_AA, ', '.join(manques)))


def test_la_hierarchie_des_paliers_de_texte_est_preservee():
    """La contrainte qui a interdit le correctif « évident ».

    Viser la conformité sur TOUTES les surfaces imposait #92878a, plus clair que
    `--vx-text-muted` : le palier « le plus discret » serait devenu le plus
    lumineux. Un futur éclaircissement de `faint` doit s'accompagner d'un
    déplacement de `muted`, jamais le franchir en silence.
    """
    t = _tokens()
    echelle = ['--vx-text-primary', '--vx-text-secondary', '--vx-text-muted',
               '--vx-text-faint']
    lums = []
    for nom in echelle:
        assert t.get(nom), '%s introuvable' % nom
        lums.append((nom, _luminance(t[nom])))
    for (n1, l1), (n2, l2) in zip(lums, lums[1:]):
        assert l1 > l2, (
            'hiérarchie rompue : %s (L=%.4f) n\'est plus plus clair que %s (L=%.4f). '
            'Les quatre paliers sont ordonnés par intention ; les croiser rend le '
            'vocabulaire visuel du produit faux.' % (n1, l1, n2, l2))


def test_le_repli_du_token_faint_egale_le_token():
    """Défaut trouvé au 613 : `var(--vx-text-faint,#5f5a55)` — un repli ENCORE
    plus sombre que le token qu'il double. Un repli qui contredit sa valeur de
    référence est un second réglage caché, jamais relu."""
    src = io.open(_POLISH, encoding='utf-8').read()
    replis = re.findall(r'var\(--vx-text-faint\s*,\s*(#[0-9a-fA-F]{6})\)', src)
    assert replis, 'aucun repli de --vx-text-faint dans polish.css — mesure périmée'
    token = _tokens()['--vx-text-faint']
    for r in replis:
        assert r.lower() == token, (
            'repli %s ≠ token %s. Le repli ne sert que si la variable manque : '
            'divergent, il devient un réglage fantôme qui échappe à toute mesure.'
            % (r, token))


def test_la_limite_assumee_du_palier_faint_est_toujours_celle_qui_est_documentee():
    """Le lot ne prétend PAS avoir rendu ce palier conforme partout.

    Sur `--vx-surface-selected` et `--vx-warm-depth` il reste sous le seuil, et
    c'est écrit dans tokens.css. Si un jour il y passe, la documentation ment
    par excès de prudence — ce test le dira.
    """
    t = _tokens()
    faint = t['--vx-text-faint']
    encore_sous = [s for s in _SURFACES_HORS_PORTEE
                   if t.get(s) and _ratio(faint, t[s]) < _SEUIL_AA]
    assert encore_sous == list(_SURFACES_HORS_PORTEE), (
        'la limite documentée dans tokens.css ne correspond plus à la mesure : '
        'attendu encore sous le seuil sur %s, mesuré %s. Mettre à jour le '
        'commentaire du token ET le rapport du lot 613.'
        % (list(_SURFACES_HORS_PORTEE), encore_sous))


# Le test `test_le_deficit_mesure_du_palier_muted_est_epingle_tel_quel` vivait ici.
# Son message d'échec disait : « si ce palier atteint désormais le seuil, mettre à
# jour le rapport et retirer ce test ». **Le lot 614 l'a fermé** — `--vx-text-muted`
# est passé de #8A8284 (4,04) à #989092 (4,86). Le test a donc été retiré, et son
# successeur — qui garde le seuil ATTEINT au lieu d'épingler le déficit — vit dans
# `tests/test_contraste_palier_muted.py`.
