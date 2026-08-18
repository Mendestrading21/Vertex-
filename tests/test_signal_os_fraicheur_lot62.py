"""SIGNAL OS · LOT 62 — UN CHIFFRE VRAI HIER, AFFICHÉ SANS LE DIRE.

Réserve SIGNAL-OS-61 §6.2, de ma main : *« La fraîcheur n'est pas jugée. Un
nombre présent dans une réponse périmée paraît tracé. »*

C'est la moitié la plus sournoise de la réserve du lot 60. Un chiffre inventé est
faux tout de suite ; un chiffre **périmé** a été vrai, il reste plausible, et rien
à l'écran ne le distingue d'un chiffre frais.

## Le défaut trouvé, sur la page qui compte le plus

`vertex/ui/pages/briefing.py`, avant ce lot :

```js
const m = b.demo ? 'demo' : 'delayed';
```

**Une constante.** L'étiquette d'Aujourd'hui affichait « Différé » que la donnée
ait trois minutes ou trois jours, et les branches `live` et
`stale: ['frozen', 'Périmé']` de `freshBadge` étaient **inatteignables**. Un badge
qui occupe la place d'un indicateur de fraîcheur sans porter la moindre
information d'âge est un mensonge par omission — et Aujourd'hui est justement la
page où l'on décide vite.

Mesuré après correctif, branche non-démo forcée :

```text
scan_age=10    → Live
scan_age=600   → Différé
scan_age=7200  → Périmé
```

## Ce que le premier verdict accusait à tort

Mon instrument rendait un verdict binaire (DIT / MUET) et accusait **cinq pages
sur huit**. Trois ne mentaient pas :

- le mode **démonstration** court-circuite l'évaluation (`if(demo){…DÉMO…}`) : la
  page annonce « DÉMO », ce qui est honnête ;
- sur Système, un `data-state="live"` porte la classe `vx-freshness` et le texte
  « **Système opérationnel** » — il décrit l'état du système, pas l'âge ;
- et il existe **deux grammaires** de fraîcheur, pas une : `.vx-fresh-chip[data-state]`
  émise par `VX.freshness.chip()`, et `.vx-freshness[data-live]` émise par
  `freshBadge()`, où `frozen` veut dire « Périmé ». N'en connaître qu'une faisait
  rendre « sans vocabulaire » sur une page qui en a bien un.

*Confondre un mot avec son sens aurait accusé des pages honnêtes.*
"""
import pathlib

import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent
BRIEFING = RACINE / 'vertex' / 'ui' / 'pages' / 'briefing.py'
OUTIL = RACINE / 'tools' / 'mesurer_fraicheur_dite.py'


@pytest.fixture(scope='module')
def page():
    return BRIEFING.read_text(encoding='utf-8')


@pytest.fixture(scope='module')
def outil():
    return OUTIL.read_text(encoding='utf-8')


def test_l_etiquette_d_aujourdhui_n_est_plus_une_constante(page):
    """LE DÉFAUT, TENU PAR SA CORRECTION.

    `const m = b.demo ? 'demo' : 'delayed'` ne dépendait d'aucun âge. Si cette
    forme revient, l'étiquette redevient décorative."""
    compact = page.replace(' ', '').replace('\n', '')
    assert "constm=b.demo?'demo':'delayed';" not in compact, (
        'l\'etiquette de fraicheur d\'Aujourd\'hui est redevenue une CONSTANTE : '
        'elle affichera « Differe » que la donnee ait trois minutes ou trois '
        'jours, et « Perime » redeviendra inatteignable')
    assert 'scan_age' in page, (
        'la page ne lit plus `scan_age` : elle n\'a plus aucune source d\'age')


def test_les_seuils_sont_empruntes_et_non_recopies(page):
    """DEUX TABLES DE SEUILS DIVERGENT AU PREMIER AJUSTEMENT.

    Si Aujourd'hui recopiait 20 s / 30 min au lieu de lire
    `VX.freshness.THRESH`, l'écran finirait par dire « Différé » là où Marchés
    dit « À actualiser » — sur la même donnée."""
    #  ON VISE L'EXPRESSION, PAS LE NOM — et la mutation l'a dit. Ma premiere
    #  version cherchait `VX.freshness.THRESH` : la chaine apparait AUSSI dans
    #  le commentaire que j'avais ecrit juste au-dessus du code. Supprimer
    #  l'emprunt reel laissait donc le test vert. Sixieme gardien creux de la
    #  serie, toujours le meme mecanisme : une sous-chaine qui existe ailleurs.
    compact = page.replace(' ', '').replace('\n', '')
    assert '(window.VX&&VX.freshness&&VX.freshness.THRESH)||' in compact, (
        'les seuils de fraicheur ne sont plus empruntes a VX.freshness : deux '
        'tables vont diverger, et deux pages diront des choses differentes de '
        'la meme donnee')


def test_les_trois_etats_sont_atteignables(page):
    """`live`, `delayed` et `stale` doivent tous pouvoir sortir. Mesuré au
    navigateur : 10 s → Live, 600 s → Différé, 7 200 s → Périmé."""
    compact = page.replace(' ', '').replace('\n', '')
    assert "m=ageMs<T.live?'live':(ageMs<T.snapshot?'delayed':'stale')" in compact, (
        'la derivation des trois etats a change : verifier que « live » et '
        '« stale » restent atteignables, sinon le badge redevient decoratif')


def test_l_outil_connait_les_deux_grammaires_de_fraicheur(outil):
    """La faute de mesure qui accusait une page honnête : ne connaître que
    `.vx-fresh-chip[data-state]` et ignorer `.vx-freshness[data-live]`."""
    assert "querySelectorAll('.vx-freshness[data-live]')" in outil, (
        'l\'outil ne reconnait plus la seconde grammaire de fraicheur : il '
        'rendra « sans vocabulaire » sur des pages qui en ont bien un')
    assert "frozen: 'stale'" in outil, (
        'l\'equivalence `frozen` = « Perime » = stale a disparu : un badge qui '
        'dit correctement « Perime » serait compte comme muet')


def test_l_outil_distingue_les_quatre_verdicts(outil):
    """DIT / MUET / non observable (démo) / sans vocabulaire. Un verdict binaire
    accusait cinq pages sur huit, dont trois honnêtes."""
    for mot in ('NON OBSERVABLE', 'SANS VOCABULAIRE', 'MUET —', 'DIT —'):
        assert mot in outil, 'le verdict « %s » a disparu de l\'outil' % mot
    assert 'pire = max(pire, code if code == 1 else 0)' in outil, (
        '« non observable » ou « sans vocabulaire » remontent de nouveau comme '
        'des defauts, ou bien un vrai MUET ne remonte plus')


def test_l_experience_reste_un_avant_apres(outil):
    """Une seule photo ne prouve rien : voir « Analyse » ne dit pas si
    l'étiquette réagit. Seul l'écart entre nominal et vieilli est une mesure."""
    assert 'avant, texte_avant, _ = _une_visite(nav, base, url)' in outil, (
        'la visite nominale a disparu : il ne reste qu\'une photo, et une photo '
        'ne dit pas si l\'etiquette REAGIT')
    assert 'if not modifiees:' in outil, (
        'le refus de conclure quand aucune reponse n\'a ete vieillie a disparu')
