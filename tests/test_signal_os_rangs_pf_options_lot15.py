"""SIGNAL OS · PORTEFEUILLE ET OPTIONS — les deux derniers audits de rangs.

## Portefeuille — `PAGES.md` §5

Les sept rangs sont couverts par les six vues, et la règle propre à la page
— « le portefeuille doit mettre les risques **avant** les statistiques
décoratives » — tient depuis le lot 06.

**Un défaut** : la vue `performance` n'avait **aucun titre**. Hors le `<h1>` de
la page, son seul intitulé était le `<b>` d'une note.

C'est la **deuxième** vue du produit dans ce cas après `anomalies` (lot 14) :
deux occurrences font une famille, pas un accident. Et c'est la plus gênante des
deux — c'est le **domicile** de la courbe d'équité, donc la destination du relais
posé sur le Journal au lot 11. On y arrive en cherchant explicitement sa
progression, et on tombait sur quatre états vides sans en-tête.

## Options — `PAGES.md` §6

Les six vues d'onglet sont titrées et portent toutes leur question ; les sept
rangs sont couverts.

**Le profil de lecture** — dette annoncée depuis le lot 06 — est enfin mesuré :
sur la vue qui porte des données, **6 champs sur 8**. Manquaient `spread` et
`OI`.

### Et ils étaient calculés

`liqState()` produit un champ `note` valant « OI 12 340 · spread 2,1 % » — les
deux chiffres exacts que la spécification exige — et **aucun des deux sites de
rendu ne l'affichait**. L'écran montrait « Liquidité : Excellente », sans qu'on
puisse distinguer OI 5 000 / spread 3 % de OI 50 000 / spread 0,2 %.

> Une donnée calculée puis jetée coûte plus cher qu'une donnée absente : le
> produit sait, et se tait.

## Ce que je n'ai PAS accusé, et c'est délibéré

Les vues `positions` et `leaps` d'Options rendent 1/8 et 5/8 champs du profil —
**parce qu'elles sont vides en démo** (aucune position options déclarée, aucun
LEAPS retenu par le scanner). Mesurer un profil de lecture sur une table vide
n'accuse pas le produit, ça accuse le jeu de données.
"""

import io
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lire(*parts):
    return io.open(os.path.join(_ROOT, *parts), encoding='utf-8').read()


def test_la_vue_performance_a_un_titre_de_vue():
    """C'est la destination du relais posé sur le Journal au lot 11 : on y
    arrive en cherchant sa progression. Une vue d'arrivée sans en-tête rend le
    relais décevant, même quand il pointe juste."""
    src = _lire('vertex', 'ui', 'pages', 'portfolio_page.py')
    i = src.index('pf-perf-equity')
    bloc = src[max(0, i - 1400):i]
    assert '<h2>Performance de portefeuille</h2>' in bloc, (
        'la vue Performance a reperdu son titre de vue : hors le h1 de la '
        'page, elle n\'a plus d\'en-tête — et c\'est le domicile de la courbe '
        'd\'équité, où le Journal envoie explicitement.')
    assert 'vx-sub' in bloc, (
        'l\'orientation de la vue Performance n\'emploie plus la grammaire '
        'd\'en-tête commune.')


def test_la_note_de_domicile_unique_survit_au_titre():
    """CONTRE-EXEMPLE du test précédent : en donnant un titre à la vue, il
    aurait été facile de remplacer la note. Or c'est elle qui explique
    *pourquoi* l'équité n'est pas dans le Journal — donc ce qui rend honnête le
    relais posé là-bas."""
    src = _lire('vertex', 'ui', 'pages', 'portfolio_page.py')
    assert 'Domicile unique.' in src, (
        'la note qui explique la migration depuis le Journal a disparu : le '
        'relais du Journal devient une redirection sans raison.')
    assert 'migrées depuis Journal' in src


def test_la_liquidite_montre_ses_deux_chiffres():
    """Le profil de lecture de PAGES.md §6 exige `spread` et `OI`. Ils étaient
    calculés dans `liqState().note` et jetés aux deux sites de rendu.

    Portée : on vérifie les DEUX sites — la carte-verdict et la ligne de
    tableau. N'en garder qu'un laisserait la moitié des lectures aveugle.
    """
    src = _lire('vertex', 'static', 'vertex', 'js', 'pages', 'options-structure.js')
    # Chaque site est verifie NOMMEMENT. Une assertion « au moins deux
    # occurrences de liq.note » restait verte quand on en retirait UN — et le
    # commentaire explicatif que j'ai ecrit dans le produit contient lui-meme
    # la chaine, ce qui suffisait a la satisfaire. Meme piege qu'au lot 13.
    for site, expr in (
            ('carte-verdict', "m.liq.note ? '<span class=\"vx-meta\">' + esc(m.liq.note)"),
            ('ligne de tableau', "liq.note ? '<div class=\"vx-meta\">' + esc(liq.note)")):
        assert expr in src, (
            'la note de liquidité (« OI … · spread … ») n\'est plus rendue sur '
            'le site « %s » : le produit recalcule des chiffres qu\'il '
            'n\'affiche pas.' % site)
    assert "'OI ' + nd(oi) + ' · spread '" in src, (
        'le format de la note de liquidité a changé — vérifier qu\'OI et '
        'spread y figurent toujours tous les deux.')


def test_l_etat_honnete_de_la_liquidite_est_conserve():
    """Quand `oi` et `spread` manquent tous les deux, la note dit « bid/ask ou
    OI absent — non évaluable ». Maintenant qu'elle est AFFICHÉE, cette phrase
    devient visible pour l'utilisateur : c'est exactement l'invariant « donnée
    absente → mention honnête », et il ne doit pas être remplacé par un tiret
    muet ni par un zéro."""
    src = _lire('vertex', 'static', 'vertex', 'js', 'pages', 'options-structure.js')
    assert 'bid/ask ou OI absent — non évaluable' in src, (
        'l\'état honnête de la liquidité a disparu : une liquidité non '
        'évaluable risque de s\'afficher comme une liquidité mesurée.')
