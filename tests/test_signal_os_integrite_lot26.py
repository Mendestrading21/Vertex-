"""SIGNAL OS · LOT 26 — UN LOT QUI NE TROUVE RIEN, et pourquoi ça compte.

Quatre invariants qu'aucun test de la suite ne peut tenir, parce qu'ils
n'existent qu'une fois la page rendue et hydratée :

| invariant | 1440 px | 320 px |
| --- | --- | --- |
| identifiants dupliqués | **0** | **0** |
| erreurs de page | **0** | **0** |
| liens internes cassés (65 distincts) | **0** | **0** |
| débordement horizontal (WCAG 1.4.10) | **0** | **0** |

Le produit est propre. Il n'y a **rien à corriger**, et l'écrire est le
résultat du lot — pas son échec.

## Ce que le lot livre quand même

L'instrument, `tools/mesurer_integrite_pages.py`. Un invariant qu'on ne peut
plus re-mesurer se dégrade en silence : c'est exactement ce qui était arrivé au
rognage silencieux avant le lot 13.

## Deux pièges d'instrument, dont un qui aurait supprimé du code vivant

En mesurant la couverture CSS pour chercher du poids mort, deux fichiers sont
ressortis à **0 %** :

1. **`responsive.css`** — mesuré à 1440 px seulement. Tout son contenu vit dans
   des `@media` qui n'y matchent pas. Mesuré aussi à 390 px, il remonte à
   **35 %**. Agir sur le premier relevé aurait **supprimé la feuille mobile du
   produit**.
2. **`fonts.css`** — 0 % à toutes les largeurs, parce qu'il ne contient que des
   `@font-face`, que la couverture CSS n'attribue jamais. Les deux polices sont
   auto-hébergées et bien employées.

Et une mesure JS carrément fausse : ma première version calculait la couverture
avec `Math.max(endOffset)` — l'offset le plus lointain atteint, pas la somme des
plages exécutées — d'où des « 100 % » partout qui ne mesuraient **rien**.

> Trois fichiers auraient pu être « nettoyés » sur la foi de ces relevés. Le
> seul garde-fou a été de trouver le résultat trop beau et de refaire la mesure.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OUTIL = os.path.join(_ROOT, 'tools', 'mesurer_integrite_pages.py')


def test_l_instrument_d_integrite_est_conserve():
    """Un invariant qu'on ne peut plus re-mesurer se dégrade en silence."""
    assert os.path.isfile(_OUTIL), (
        'l\'instrument d\'intégrité a disparu : plus rien ne mesure les ids '
        'dupliqués, les liens cassés ni le reflow à 320 px.')
    src = io.open(_OUTIL, encoding='utf-8').read()
    assert 'def _vues(' in src, (
        'l\'instrument ne dérive plus ses vues de la source : il peut de '
        'nouveau visiter des URL inexistantes sans que rien ne le signale '
        '(leçon du lot 14).')
    #  LOT 42 : la garde portait sur l'appel littéral `balayer(pw, 320, 800`.
    #  Elle disait la bonne chose de la mauvaise façon — elle figeait une FORME
    #  d'écriture, pas la propriété. Passer les largeurs dans une table la
    #  faisait échouer alors que le balayage à 320 px n'avait pas bougé, et
    #  l'aurait laissée passer si quelqu'un avait gardé l'appel en supprimant
    #  la boucle. Ce qu'on garde vraiment : la MATRICE de `VALIDATION.md`.
    largeurs = set(int(n) for n in
                   re.findall(r"\((\d{3,4}),\s*\d{3,4},\s*'", src))
    assert 320 in largeurs, (
        'le balayage à 320 px a disparu : c\'est la largeur qu\'impose '
        'WCAG 1.4.10, et le seul endroit où le reflow se mesure.')
    manquantes = {1440, 1024, 768, 390, 320} - largeurs
    assert not manquantes, (
        'la matrice responsive de VALIDATION.md est incomplète — largeurs '
        'absentes : %s. Les défauts de grille naissent aux BASCULES (1024, '
        '768, 390), pas aux extrémités.' % sorted(manquantes))


def test_l_instrument_ne_suit_jamais_un_point_d_entree_interdit():
    """La liste sert DEUX fois : avorter les requêtes du navigateur, et filtrer
    les liens que l'outil irait chercher lui-même. Ne garder que la première
    laisserait l'outil appeler ce qu'il refuse au navigateur."""
    src = io.open(_OUTIL, encoding='utf-8').read()
    assert 'pg.route(motif, lambda r: r.abort())' in src, (
        'l\'instrument n\'avorte plus les points d\'entrée interdits.')
    assert '_INTERDIT_RE.search(h)' in src, (
        'l\'instrument suit de nouveau TOUS les liens : il appellerait '
        'lui-même les points d\'entrée qu\'il avorte au navigateur.')


def test_l_instrument_ne_compte_pas_ses_propres_avortements():
    """Sans ce filtre, l'outil rend 4 « erreurs de page » par vue qui sont les
    siennes — et noie le signal réel, comme au lot 13 avec les 21 à 24 faux
    positifs de `.vx-sr-only`."""
    src = io.open(_OUTIL, encoding='utf-8').read()
    assert "'ERR_FAILED' in m.text" in src, (
        'l\'instrument recompte ses propres avortements comme des erreurs du '
        'produit.')


def test_les_deux_feuilles_faussement_mortes_existent_toujours():
    """CONTRE-EXEMPLE, et le test qui compte vraiment. Deux fichiers sont
    ressortis à 0 % de couverture ; les supprimer aurait retiré la feuille
    MOBILE et les polices auto-hébergées. Ce test tient le fait qu'ils sont
    vivants, pour que le prochain relevé « 0 % » ne serve pas de preuve."""
    css = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css')
    resp = io.open(os.path.join(css, 'responsive.css'), encoding='utf-8').read()
    assert '@media' in resp and len(resp) > 2000, (
        'responsive.css a été vidé ou supprimé — or son 0 % de couverture à '
        '1440 px est un artefact : tout son contenu est sous @media, et il '
        'remonte à 35 % dès qu\'on mesure aussi à 390 px.')
    fonts = io.open(os.path.join(css, 'fonts.css'), encoding='utf-8').read()
    assert '@font-face' in fonts and 'inter-var.woff2' in fonts, (
        'fonts.css a été vidé ou supprimé — or son 0 % de couverture est un '
        'artefact : la couverture CSS n\'attribue jamais les @font-face, et '
        'les polices sont auto-hébergées pour ne dépendre d\'aucun CDN.')
