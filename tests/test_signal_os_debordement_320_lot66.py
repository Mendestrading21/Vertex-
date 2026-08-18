"""SIGNAL OS · LOT 66 — LE DÉTECTEUR DE DÉBORDEMENT NE POUVAIT PAS SE DÉCLENCHER.

Réserve SIGNAL-OS-65 §D3, de ma main : le balayage responsive était « la mesure
encore faisable la plus utile », parce que c'est la seule qui touche un usage
réel déclaré — la consultation sur iPhone.

Deux instruments existaient déjà. Aucun des deux n'avait de **témoin de
détection**, et l'un des deux était **structurellement aveugle**.

## L'aveuglement, mesuré des deux côtés

`mesurer_integrite_pages.py` lisait `documentElement.scrollWidth - clientWidth`.
Or `html` et `body` portent **`overflow-x: clip`** : dans ce mode, `scrollWidth`
du `documentElement` ne dépasse **jamais** `clientWidth`.

Vérifié en injectant 400 px de contenu de trop :

```text
doc.scrollWidth  : 1440  (inchangé)
body.scrollWidth : 1840  (le vrai débordement)
```

Son « 0 débordement horizontal » sur cinq largeurs, publié depuis le lot 26, ne
prouvait donc rien. **Même famille que le lot 64** : une mesure qui ne peut pas
rendre de résultat positif.

## Ce que l'aveuglement cachait

À 320 px (WCAG 1.4.10 « reflow »), le cluster droit de la barre supérieure
sortait du gabarit de 4 à 34 px selon la page. Et comme `overflow-x: clip`
**interdit tout défilement**, le bouton d'actualisation n'était pas seulement
hors écran : il était **hors d'atteinte**.

## Et ma première correction était fautive

`min-width: 0` sur le champ de recherche supprimait bien le débordement — mais le
fil d'Ariane, lui aussi en `flex: 1 1 0`, réclamait toute la place libre et
écrasait le champ à **0 px de large sur quatre pages sur cinq**. J'avais échangé
un défaut contre un autre : le bouton redevenait atteignable, la recherche
disparaissait — alors que le lot 289 a établi qu'elle est LE chemin tactile vers
la palette.

*Un plancher, pas un zéro.* 44 px.

## Le piège de mesure qui a failli me faire publier « c'est bon »

Une première sonde lisait 38 px et 73 px et me faisait croire le champ sain. Elle
mesurait **avant** que le fil d'Ariane ne se remplisse. Trois échantillons
espacés ont tranché : 0 px, stable, sur quatre pages.
"""
import pathlib

import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent
RESPONSIVE = RACINE / 'vertex' / 'static' / 'vertex' / 'css' / 'responsive.css'
MARKETS = RACINE / 'vertex' / 'ui' / 'pages' / 'markets_page.py'
INTEGRITE = RACINE / 'tools' / 'mesurer_integrite_pages.py'
ROGNAGE = RACINE / 'tools' / 'mesurer_rognage_silencieux.py'


def _lire(p):
    return p.read_text(encoding='utf-8')


@pytest.fixture(scope='module')
def integrite():
    return _lire(INTEGRITE)


def test_le_debordement_est_lu_sur_body_et_non_sur_documentElement(integrite):
    """LE DÉFAUT D'INSTRUMENT, TENU PAR SA CORRECTION.

    `overflow-x: clip` empêche `documentElement.scrollWidth` de dépasser
    `clientWidth`. Revenir à cette lecture rendrait le détecteur incapable de
    se déclencher — et son « 0 » redeviendrait une garantie creuse."""
    compact = integrite.replace(' ', '')
    assert 'document.body.scrollWidth-vp' in compact, (
        'le debordement horizontal n\'est plus lu sur `body` : avec '
        '`overflow-x:clip`, le detecteur redevient structurellement incapable '
        'de se declencher, et son « 0 » ne prouve plus rien')
    assert 'doc.scrollWidth-doc.clientWidth' not in compact, (
        'la lecture aveugle sur `documentElement` est revenue')


def test_le_balayage_couvre_le_shell_et_pas_seulement_le_contenu(integrite):
    """Le coupable — `.vx-topbar-right` — vit dans le SHELL. Chercher dans
    `#vx-content` seulement, c'était chercher la clé sous le lampadaire : 36
    vues rendaient « élément non identifié »."""
    assert "querySelectorAll('body *')" in integrite, (
        'le balayage est revenu a `#vx-content` : le debordement de la barre '
        'superieure redeviendrait invisible')


def test_ce_qui_defile_n_est_pas_accuse(integrite):
    """Une table large dans un conteneur `overflow-x:auto` sort du gabarit et
    reste ATTEIGNABLE. L'accuser noierait le signal réel sous le patron le plus
    courant du produit."""
    compact = integrite.replace(' ', '').replace('\n', '')
    assert 'rattrape=true' in compact and 'a.scrollWidth-a.clientWidth>2' in compact, (
        'l\'exclusion des ancetres defilants a disparu : chaque table du produit '
        'redevient un faux positif, et le vrai defaut se noie dedans')


def test_les_trois_temoins_de_detection_existent(integrite):
    """« TOUT PROPRE » sur quatre détecteurs jamais mis à l'épreuve et « je ne
    sais pas voir » rendent exactement le même résultat."""
    for ancre in ('_TEMOIN_ID', '_TEMOIN_LIEN', "vx-temoin-id-duplique"):
        assert ancre in integrite, (
            'le temoin de detection « %s » a disparu' % ancre)
    #  On vise la VERIFICATION, pas seulement la fabrication : injecter un
    #  defaut sans exiger qu'il soit vu ne prouve rien.
    assert "'debordement H': bool(reflow)" in integrite, (
        'l\'outil n\'exige plus de VOIR le debordement fabrique : il pourrait '
        'rendre « propre » en etant aveugle')


def test_le_rognage_silencieux_a_lui_aussi_un_temoin():
    """Même règle pour le second instrument, et deux largeurs de plus (768,
    1920) que la réserve D3 signalait comme jamais balayées."""
    src = _lire(ROGNAGE)
    #  ON VISE L'AFFECTATION, PAS LE NOM — la mutation l'a dit. Chercher
    #  `TEMOIN_TXT` laissait le test vert : renommer la variable a sa
    #  DEFINITION conserve le nom dans ses deux usages plus bas. Neuvieme
    #  gardien creux de la serie, toujours le meme mecanisme.
    assert "TEMOIN_TXT = 'TEMOIN ROGNAGE" in src, (
        'le texte du temoin de rognage a disparu de sa definition : « 0 rogne » '
        'cesse de vouloir dire quelque chose')
    assert 'DENONCE — le detecteur mord' in src and 'PASSE INAPERCU' in src, (
        'l\'outil n\'annonce plus le verdict de son temoin')
    assert 'LARGEURS = ((1920, 1080), (1440, 900), (768, 1024), (390, 844))' in src, (
        'les quatre largeurs ne sont plus balayees')


def test_le_champ_de_recherche_a_un_plancher_et_non_un_zero():
    """MA PROPRE CORRECTION ÉTAIT FAUTIVE.

    `min-width:0` supprimait le débordement mais laissait le fil d'Ariane
    écraser le champ à 0 px sur quatre pages sur cinq — en supprimant le chemin
    tactile vers la palette que le lot 289 a établi."""
    css = _lire(RESPONSIVE).replace(' ', '')
    assert '.vx-topbar-search{max-width:none;min-width:44px}' in css, (
        'le plancher du champ de recherche a change : a `min-width:0` il est '
        'ecrase a zero par le fil d\'Ariane ; sans `min-width` du tout, sa '
        'taille intrinseque (~98 px) fait deborder la barre a 320 px et rend le '
        'bouton d\'actualisation HORS D\'ATTEINTE (rien ne defile sous '
        '`overflow-x:clip`)')


def test_la_table_des_secteurs_est_dans_le_patron_maison():
    """La seule `<table class="vx-table">` du dépôt sans `.vx-table-wrap` : à
    320 px elle sortait de 21 px, et la colonne « Leader » était coupée sans
    recours."""
    src = _lire(MARKETS)
    assert '`<div class="vx-table-wrap"><table class="vx-table"><thead><tr><th>Secteur</th>' in src, (
        'la table des secteurs a perdu son enveloppe defilante : sa derniere '
        'colonne redevient coupee et inatteignable a 320 px')
    assert "</tbody></table></div>'" in src, (
        'l\'enveloppe de la table des secteurs n\'est plus refermee')
