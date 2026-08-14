"""LOT 615 — L'ÉTIQUETTE QUI NOMME CHAQUE VALEUR SOUS 720 PX, ENFIN RENDUE.

Les lots 613 et 614 l'avaient **recensée dans le CSS et jamais mesurée** :

```css
@media (max-width:720px){
  .vx-table-cards td::before{content:attr(data-label); … color:var(--vx-text-faint)}
}
```

Aucun banc ne pouvait la voir — les tables du produit sont **vides** dans un
environnement sans positions ni opportunités, donc `.vx-table-cards td` n'existe
pas, et un pseudo-élément n'est de toute façon **pas un nœud du DOM**.

Mesurée au lot 615 par **injection DOM** d'une ligne synthétique dans une page
réelle à 390 px (on mesure le CSS, pas une donnée produit) :

| | avant 613 | après 613 | **après 615** |
| --- | --- | --- | --- |
| ratio | **2,93** | **4,50** *(exactement le seuil, zéro marge)* | **5,23** |

Le 613 avait été **borné par la position d'alors du palier `muted`** ; le 614
l'ayant remonté, le 615 a pu donner à `faint` la marge que le 614 exige de
tout palier (**614-B** : une conformité à un centième n'en est pas une).

Ce gardien tient les trois choses dont dépend cette mesure : le **seuil avec
marge**, le **token que la règle utilise**, et la **bascule** sous laquelle elle
s'applique.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TOKENS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'tokens.css')
_TABLES = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'tables.css')

_SEUIL_AA = 4.5
_MARGE_MINIMALE = 0.20          # règle 614-B
# La surface sur laquelle la carte mobile est peinte, mesurée au navigateur :
# `.vx-table-cards tbody tr{background:var(--vx-surface-elevated)}`.
_SURFACE_CARTE = '--vx-surface-elevated'
_BASCULE_CARTES = 720           # px, mesurée dans tables.css


def _lire(p):
    return io.open(p, encoding='utf-8').read()


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


def _ratio(a, b):
    l1, l2 = _luminance(a), _luminance(b)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def _bloc_cartes():
    src = _lire(_TABLES)
    i = src.index('.vx-table-cards')
    return src[max(0, i - 200):]


def test_l_etiquette_de_carte_mobile_a_une_marge_reelle():
    """Le défaut que le 615 corrige : 4,50 **exactement**.

    Conforme au centième près, donc reperdu par n'importe quel assombrissement
    de la surface — sans qu'aucun test ne bouge. C'est précisément ce que le lot
    614 avait refusé d'accepter pour le palier `muted` (614-B) ; le même
    raisonnement s'applique ici.
    """
    t = _tokens()
    faint, surface = t.get('--vx-text-faint'), t.get(_SURFACE_CARTE)
    assert faint and surface, 'token manquant — la mesure du lot 615 est périmée'
    r = _ratio(faint, surface)
    assert r >= _SEUIL_AA + _MARGE_MINIMALE, (
        'l\'étiquette de carte mobile donne %.2f sur %s (marge %+.2f, minimum '
        'exigé %+.2f). C\'est le SEUL texte qui dit de quelle colonne vient un '
        'chiffre quand la table passe en cartes : sa lisibilité n\'est pas '
        'décorative. Re-mesurer au navigateur (injection DOM à 390 px) avant de '
        'publier.' % (r, _SURFACE_CARTE, r - _SEUIL_AA, _MARGE_MINIMALE))


def test_l_etiquette_utilise_toujours_le_palier_garde():
    """La mesure du 615 vaut pour `--vx-text-faint`. Repointer la règle sur un
    autre token ferait passer les tests de palier au vert tout en changeant la
    couleur réellement peinte : le gardien mesurerait alors autre chose que ce
    qui s'affiche."""
    bloc = _bloc_cartes()
    m = re.search(r"\.vx-table-cards td::before\{[^}]*\}", bloc, re.S)
    assert m, 'la règle `.vx-table-cards td::before` a disparu de tables.css'
    regle = m.group(0)
    assert 'var(--vx-text-faint)' in regle, (
        'la règle n\'utilise plus --vx-text-faint : %s' % regle[:160])
    assert 'attr(data-label)' in regle, (
        'l\'étiquette ne reprend plus `data-label` — elle ne nomme donc plus la '
        'colonne, et la mesure du 615 porte sur autre chose')


def test_la_bascule_du_mode_cartes_est_celle_qui_a_ete_mesuree():
    """La mesure a été faite à 390 px **parce que** la bascule est à 720. Si elle
    descend, des largeurs aujourd'hui couvertes cessent de l'être, et la mesure
    ne dit plus rien de ces largeurs-là."""
    src = _lire(_TABLES)
    i = src.index('.vx-table-cards')
    entete = src[:i]
    m = re.findall(r"@media\s*\(max-width:\s*(\d+)px\)", entete)
    assert m, 'aucune requête média avant le bloc du mode cartes'
    assert int(m[-1]) == _BASCULE_CARTES, (
        'le mode cartes bascule désormais à %s px, mesuré à %d px au lot 615. '
        'Re-mesurer aux largeurs qui changent de camp.' % (m[-1], _BASCULE_CARTES))


def test_le_palier_faint_reste_sous_le_palier_muted():
    """Le 615 remonte `faint` dans la place libérée par le 614. Il ne doit pas
    la consommer entièrement : les deux paliers doivent rester distinguables,
    sinon le produit a quatre noms pour trois nuances."""
    t = _tokens()
    lf, lm = _luminance(t['--vx-text-faint']), _luminance(t['--vx-text-muted'])
    assert lf < lm, ('--vx-text-faint (L=%.4f) a rattrapé --vx-text-muted '
                     '(L=%.4f)' % (lf, lm))
    assert lm / lf >= 1.10, (
        'les paliers `faint` (L=%.4f) et `muted` (L=%.4f) ne sont plus séparés '
        'que d\'un facteur %.3f : le pas devient invisible et le vocabulaire '
        'visuel perd un niveau.' % (lf, lm, lm / lf))
