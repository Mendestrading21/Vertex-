"""SIGNAL OS · LOT 59 — LES HUIT ESPACES DÉGRADENT HONNÊTEMENT, ET UN NE LE FAISAIT PAS.

Réserve SIGNAL-OS-53 §5.1, de ma main : *« Une seule page. Les sept autres
espaces ont leurs propres hôtes et ne sont pas balayés. »*

`tools/mesurer_hotes_resolus.py --tous` les balaie désormais, en nominal **et**
sous coupure totale des données — seize passages. Quinze étaient sains. Le
seizième a trouvé un défaut réel, et d'un genre qu'aucun gardien d'octets ne
pouvait voir.

## Le défaut, et pourquoi il était invisible

Sous coupure, `/options` gardait `#vx-os-verdict` à l'état de **squelette
au-delà de 45 secondes** — le plafond de l'outil — là où la fiche Analyse
dégrade entièrement en 5 s.

Le plus instructif : `loadStructure()` porte un `.catch` parfaitement honnête,
qui peint « Analyse indisponible ». **Il n'était jamais atteint.** La vue amorce
son symbole depuis le tableau d'options ; quand `/api/options` échoue, `board()`
avale l'erreur et rend `[]`, aucun symbole n'est choisi, et la garde
`if (!input.value && (pre || syms.length))` reste fausse. `loadStructure` n'est
donc **jamais appelé**, et le squelette du HTML initial reste à l'écran, pour
toujours.

*L'état honnête existait ; le produit n'y arrivait jamais.* On ne trouve cela
ni en lisant le code — le `catch` est là, bien visible — ni dans les octets
servis. Il faut couper les données et regarder l'écran.

## Ce que le correctif ajoute, et ce qu'il refuse d'inventer

Un `else` : quand aucun symbole ne peut être choisi, la page **le dit**. Et elle
distingue deux causes que `board()` confondait en rendant `[]` :

| cause | ce que la page affiche |
| --- | --- |
| tableau injoignable | « Tableau d'options injoignable — aucun titre à analyser » |
| tableau vide | « Aucun titre à options dans le tableau courant » |

Les deux invitent à saisir un symbole à la main — le chemin qui reste ouvert.
"""
import pathlib
import re

import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent
SOURCE = RACINE / 'vertex' / 'static' / 'vertex' / 'js' / 'pages' / 'options-structure.js'


@pytest.fixture(scope='module')
def js():
    return SOURCE.read_text(encoding='utf-8')


def test_l_amorce_sans_symbole_a_desormais_une_branche(js):
    """LE DÉFAUT MESURÉ, TENU PAR SA CORRECTION.

    Sans ce `else`, `load()` n'était jamais appelé et la vue Structure gardait
    son squelette de départ pour toujours — 45 s au plafond de l'instrument,
    contre 5 s pour la fiche Analyse."""
    compact = js.replace(' ', '').replace('\n', '')
    assert 'elseif(!input.value&&typeofonVide===\'function\'){onVide(_boardEchec);}' in compact, (
        'la branche « aucun symbole a charger » a disparu : quand le tableau '
        'd\'options est vide ou injoignable, la vue Structure redevient un '
        'squelette perpetuel — l\'etat honnete existe dans loadStructure mais '
        'le produit n\'y arrive jamais')


def test_la_cause_de_l_absence_est_distinguee(js):
    """`board()` rendait `[]` aussi bien pour « aucun titre » que pour « serveur
    injoignable ». Deux états très différents, une seule apparence : la page ne
    pouvait annoncer qu'un vide sans cause."""
    assert '_boardEchec' in js, (
        'la cause de l\'absence de tableau n\'est plus retenue : la page ne '
        'peut plus distinguer « vide » de « injoignable »')
    assert 'Tableau d’options injoignable' in js, 'le message de panne a disparu'
    assert 'Aucun titre à options dans le tableau courant' in js, (
        'le message de vide honnete a disparu')


def test_les_deux_messages_laissent_le_chemin_manuel_ouvert(js):
    """Un état honnête qui laisse l'utilisateur sans recours n'est qu'à moitié
    honnête. Les deux messages nomment la sortie : saisir un symbole."""
    for message in ('Saisir un symbole ci-dessus pour forcer l’analyse',
                    'Saisir un symbole ci-dessus pour lancer l’analyse'):
        assert message in js, (
            'le recours manuel n\'est plus propose : « %s »' % message[:40])


def test_le_verdict_garde_son_chemin_d_erreur_propre(js):
    """La correction ajoute une branche, elle n'en retire aucune : le `.catch`
    de `loadStructure` reste le filet quand le chargement démarre et échoue."""
    assert re.search(r"catch\(function \(e\) \{ vHost\.innerHTML = VX\.states\.error", js), (
        'le filet d\'erreur de loadStructure a disparu — il couvre le cas ou le '
        'chargement DEMARRE et echoue, l\'autre branche celui ou il ne demarre '
        'jamais. Les deux sont necessaires')


def test_l_instrument_couvre_bien_les_huit_espaces():
    """L'outil lit les espaces du registre au lieu de les recopier. Une liste
    écrite à la main diverge dès le premier ajout de page — et le lot 56 a
    montré le coût d'une liste incomplète : « jamais peint » sur un produit
    correct."""
    from tools.mesurer_hotes_resolus import espaces
    vus = espaces()
    assert len(vus) == 8, (
        'le registre PRIMARY_NAV ne porte plus huit espaces (%d) : le balayage '
        'du lot 59 ne couvre plus le produit entier' % len(vus))
    idents = {i for i, _ in vus}
    assert {'briefing', 'markets', 'opportunities', 'analysis', 'portfolio',
            'options', 'journal', 'system'} <= idents, (
        'un espace canonique a disparu du registre : %s' % sorted(idents))
