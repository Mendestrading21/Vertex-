"""SIGNAL OS · L'ÉTIQUETAGE DÉMO — le constat du lot 08, instruit et corrigé.

Le lot 08 avait **figé un constat plutôt que de corriger au jugé** : quatre
espaces muets, un hôte vide sur Options, et une pièce qui ne collait pas —
`/api/market/summary` répondait `source: "cloud"` alors que `DEMO=1`. Il refusait
d'étiqueter avant d'avoir établi quelle donnée est réellement synthétique.

Ce fichier remplace cette caractérisation. L'instruction est faite.

## Le défaut que la pièce manquante cachait

| endpoint | disait | sert |
| --- | --- | --- |
| `/scan` | `source: 'demo'` | données synthétiques |
| `/api/market/summary` | **`source: 'cloud'`** | **les mêmes**, dérivées du scan |

Cause : `feeds.py` écrivait `'source': 'ibkr' if IBKR_ENABLED else 'cloud'` —
un **binaire** qui ignore `DEMO_MODE`, alors qu'il y a **trois** états. En démo
il annonçait donc « cloud », c'est-à-dire de la donnée de marché **réelle**,
pour des chiffres fabriqués.

C'est l'invariant produit n°4 pris à revers : « jamais de chiffre inventé
affiché comme réel ». Et le bon calcul **existait déjà à côté** —
`status_service.py` fait le trois-états depuis toujours ; ce site-ci ne l'avait
simplement pas suivi.

## Le trou d'Options

`options_intel_page.py` déclare `<div id="vx-demo-banner">` et **rien** ne le
remplissait. Chaque carte de l'espace savait pourtant qu'elle était en démo —
`d.demo` traverse le hero, les compteurs, le scanner, le payoff. Seul l'espace
se taisait.

## Ce qui reste délibérément muet

`/analysis` (accueil) et `/journal` n'affichent **aucune donnée de moteur** :
ils lisent le bureau du navigateur, données **personnelles**. Y coller « démo »
serait un mensonge d'un autre genre — c'était déjà la conclusion du lot 08, et
elle tient.
"""

import io
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lire(*parts):
    return io.open(os.path.join(_ROOT, *parts), encoding='utf-8').read()


def test_la_source_du_marche_a_trois_etats_et_non_deux():
    """LE défaut de fond. Un binaire `ibkr | cloud` ne peut pas dire « démo » :
    il range forcément la donnée synthétique dans l'une des deux cases
    RÉELLES."""
    src = _lire('vertex', 'app', 'routes', 'feeds.py')
    assert "'source': 'demo' if DEMO_MODE else ('ibkr' if IBKR_ENABLED else 'cloud')" in src, (
        '/api/market/summary est revenu à une source binaire : en démo il '
        'annoncera « cloud », donc de la donnée de marché réelle, pour des '
        'chiffres fabriqués.')
    assert 'from vertex.app.config import DEMO_MODE, IBKR_ENABLED' in src, (
        'DEMO_MODE n\'est plus importé — la source ne peut plus être honnête.')


def test_le_calcul_a_trois_etats_reste_coherent_avec_son_precedent():
    """`status_service.py` faisait déjà le bon calcul. Les deux doivent rester
    d'accord : deux réponses différentes sur le mode réel, c'est le défaut du
    lot 08 réinstallé ailleurs."""
    st = _lire('vertex', 'services', 'status_service.py')
    assert "'demo' if demo_mode else ('ibkr' if ibkr_enabled else 'cloud')" in st, (
        'le précédent correct a changé de forme — vérifier que les deux sites '
        'donnent toujours le même mode.')


def test_l_espace_options_remplit_enfin_son_hote_demo():
    """L'hôte existait depuis toujours et personne ne l'écrivait. Le lot 08
    l'avait figé comme « le signe le plus net » du constat."""
    page = _lire('vertex', 'ui', 'pages', 'options_intel_page.py')
    assert 'vx-demo-banner' in page, 'l\'hôte démo d\'Options a disparu'
    js = _lire('vertex', 'static', 'vertex', 'js', 'pages', 'options-intel.js')
    # La fonction ET ses deux APPELS. Chercher le nom seul restait vert sur un
    # renommage en `remplirBandeauDemoX` — la chaîne cherchée en est un
    # PRÉFIXE. Même piège qu'au lot 13 avec `td.vx-truncate` ; c'est la
    # neuvième fois qu'une portée d'assertion me trompe dans cette refonte.
    assert 'function remplirBandeauDemo(' in js, (
        'la fabrique du bandeau démo d\'Options a disparu ou changé de nom.')
    assert js.count('remplirBandeauDemo(d') >= 2, (
        'le bandeau démo d\'Options n\'est plus appelé sur les DEUX chemins '
        '(tableau vide et tableau plein) : l\'espace redevient muet dans un '
        'des deux cas.')
    assert "getElementById('vx-demo-banner')" in js
    assert 'Données synthétiques clairement identifiées' in js, (
        'le libellé démo d\'Options a divergé de celui de Marchés et '
        'Opportunités — un seul fait doit avoir un seul libellé.')


def test_le_meme_libelle_sert_les_trois_espaces_qui_etiquettent():
    """Trois espaces affichent une donnée de moteur en démo ; ils doivent le
    dire de la même façon. Un libellé par page, c'est trois vérités."""
    textes = [
        _lire('vertex', 'ui', 'pages', 'markets_page.py'),
        _lire('vertex', 'static', 'vertex', 'js', 'pages', 'options-intel.js'),
    ]
    for t in textes:
        assert 'Données synthétiques clairement identifiées' in t


def test_analyse_et_journal_restent_muets_et_c_est_voulu():
    """CONTRE-EXEMPLE, et le plus important du fichier : la correction ne doit
    PAS s'étendre aux deux espaces qui n'affichent aucune donnée de moteur.

    `/analysis` (accueil) et `/journal` lisent le bureau du navigateur —
    données personnelles. Un bandeau « démo » y serait faux.
    """
    for page in ('analysis_page.py', 'performance_page.py'):
        src = _lire('vertex', 'ui', 'pages', page)
        assert 'vx-demo-banner' not in src, (
            '%s a reçu un hôte « démo » : ses données viennent du navigateur, '
            'pas d\'un moteur — l\'étiquette y serait un mensonge d\'un autre '
            'genre.' % page)
