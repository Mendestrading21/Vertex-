"""SIGNAL OS · PORTEFEUILLE — le risque passe devant les statistiques.

`PAGES.md` §5 donne à cette page une règle qu'aucune autre n'a :

> Le portefeuille doit mettre les risques avant les statistiques décoratives.

**Mesuré à 1440 px** dans la vue Synthèse :

| bloc | position |
| --- | --- |
| tuiles valeur / P&L / cash | 603 px |
| **journal « depuis ta dernière visite »** | **746 px** |
| concentration du capital | 852 px |
| positions exigeant une décision | 1292 px |

Un delta depuis la dernière visite est intéressant. Ce n'est pas ce qui menace
le capital. Il passait pourtant **avant** la concentration et avant les
positions à revoir.

## Le contre-exemple

Le journal n'est pas **supprimé** — il descend. Le retirer ferait passer la même
règle et retirerait une lecture réelle (« la valeur nette a bougé de X depuis ma
dernière visite »). `test_le_journal_est_deplace_et_non_supprime` refuse cette
sortie.

## Une incohérence que j'ai moi-même introduite

Au lot précédent, l'onglet `Watchlist` est devenu `Surveillance` — et le bouton
d'ajout, à quarante pixels de là, disait toujours `+ Watchlist`. Deux noms pour
la même chose sur le même écran. C'est le risque exact d'un renommage partiel,
et c'est pourquoi le nom est désormais gardé **des deux côtés**.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PF = os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'portfolio_page.py')
_BRIEF = os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'briefing.py')


def _src():
    return io.open(_PF, encoding='utf-8').read()


def _sans_commentaires(src):
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    return re.sub(r'<!--.*?-->', '', src, flags=re.S)


def test_le_risque_precede_le_journal_des_changements():
    """L'ordre d'assemblage EST l'ordre de lecture : `pf-body` est composé par
    concaténation, donc la position dans la chaîne décide de la position à
    l'écran."""
    code = _sans_commentaires(_src())
    i_diff = code.index("id=\"pf-diff\"")
    i_alloc = code.index('aria-label="Allocation et concentration"')
    i_dec = code.index('aria-label="Positions exigeant une décision"')
    assert i_alloc < i_diff, (
        'le journal des changements repasse avant la concentration du capital : '
        'une statistique avant le risque, ce que la règle de cette page '
        'interdit explicitement.')
    assert i_dec < i_diff, (
        'le journal repasse avant les positions qui exigent une décision.')


def test_le_journal_est_deplace_et_non_supprime():
    """CONTRE-EXEMPLE. Supprimer le journal ferait passer le test ci-dessus —
    et retirerait une lecture réelle."""
    code = _sans_commentaires(_src())
    assert 'id="pf-diff"' in code, (
        'l\'hôte du journal des changements a disparu : la règle « le risque '
        'd\'abord » a été satisfaite en retirant l\'information, pas en la '
        'replaçant.')
    assert 'vxPortfolioBaseline' in code, (
        'la référence de comparaison n\'est plus posée : le journal ne peut '
        'plus rien montrer.')


def test_l_onglet_et_le_bouton_disent_le_meme_mot():
    """Le renommage partiel du lot précédent : onglet « Surveillance », bouton
    « + Watchlist », à quarante pixels d'écart."""
    code = _sans_commentaires(_src())
    assert "('watchlist', 'Surveillance')" in code
    assert '+ Watchlist' not in code, (
        'le bouton d\'ajout dit de nouveau « Watchlist » alors que l\'onglet dit '
        '« Surveillance » : deux noms pour la même chose sur le même écran.')
    assert '+ Surveillance' in code


def test_le_meme_objet_porte_le_meme_nom_sur_les_deux_pages():
    """« Ce qui a changé » sur Aujourd'hui, « Depuis ta dernière visite » sur
    Portefeuille : même objet, deux noms. `VALIDATION.md` — labels cohérents."""
    pf = _sans_commentaires(_src())
    brief = io.open(_BRIEF, encoding='utf-8').read()
    assert 'Ce qui a changé' in brief
    assert 'Ce qui a changé' in pf, (
        'Portefeuille ne nomme plus son journal comme Aujourd\'hui nomme le sien.')
    assert 'Depuis ta dernière visite' not in pf, (
        'l\'ancien nom est revenu : deux libellés pour un même objet selon la '
        'page où on se trouve.')


def test_le_titre_de_l_allocation_ne_repete_pas_la_page():
    """« du capital » est vrai de toute la page Portefeuille."""
    code = _sans_commentaires(_src())
    assert '<span class="vx-chart-title">Allocation &amp; concentration</span>' in code \
        or '<span class="vx-chart-title">Allocation & concentration</span>' in code
    assert 'concentration du capital</span>' not in code
