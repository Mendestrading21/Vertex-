"""SIGNAL OS · SYSTÈME — CARACTÉRISATION : qui dit « démo », et qui se tait.

**Ce fichier ne valide rien. Il fige un constat**, comme
`tests/test_desk_perte_lot362.py` fige les pertes possibles du bureau. Il doit
être mis à jour quand le produit est corrigé — pas contourné.

## Ce qui a été mesuré

Serveur en `DEMO=1`, huit espaces chargés au navigateur, recherche d'un
`.vx-demo-banner` **rempli** ou d'un `.vx-badge-demo` :

| espace | hôte `vx-demo-banner` dans le HTML servi | étiquette visible |
| --- | --- | --- |
| `/` | 2 | **oui** |
| `/markets` | 3 | **oui** |
| `/portfolio` | 0 | **oui** *(badge posé à l'exécution)* |
| `/system` | 0 | **oui** *(badge posé à l'exécution)* |
| `/options` | **1** | **non — l'hôte existe et reste vide** |
| `/opportunities` | 0 | **non** |
| `/analysis` | 0 | **non** |
| `/journal` | 0 | **non** |

## Ce que ce constat établit — et ce qu'il n'établit pas

**Établi** : trois mécanismes différents coexistent (hôte serveur rempli en JS,
badge posé à l'exécution, rien), et `/options` porte un hôte que rien ne
remplit.

**NON établi** : que les quatre espaces silencieux servent des données
synthétiques. `/analysis` (page d'accueil) et `/journal` affichent des données
**personnelles** venant du navigateur — aucune donnée de moteur, donc aucune
étiquette démo à porter. `/opportunities` affiche bien des données de scan et
mérite l'examen ; `/options` porte un hôte vide, ce qui est un signe.

Corriger l'étiquetage sans avoir établi, espace par espace, **quelle donnée est
réellement synthétique**, reviendrait à coller une mention « démo » sur des
données personnelles — un mensonge d'un autre genre. Le constat est donc figé
ici, et la correction attend la mesure qui la fonde.

## Portée

`DEMO=1` dans cet environnement ; `/api/market/summary` répond
`source: "cloud"` et non `"demo"`. Le mode réellement actif n'est donc pas
uniforme entre les points d'entrée — c'est une pièce de plus à démêler avant de
toucher aux étiquettes.
"""

import io
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PAGES = os.path.join(_ROOT, 'vertex', 'ui', 'pages')

# Occurrences de `vx-demo-banner` dans la SOURCE de chaque page, mesurées au
# lot 08. Ce n'est pas une cible : c'est l'état constaté.
#
# ATTENTION — deux comptes différents, et je les ai d'abord mélangés : la SOURCE
# contient la déclaration de l'hôte ET le code JS qui l'écrit, donc elle en
# compte plus que le HTML SERVI (3 vs 2 sur Aujourd'hui, 4 vs 3 sur Marchés).
# Les nombres ci-dessous sont ceux de la SOURCE, puisque c'est elle que ce
# fichier lit.
_HOTES_MESURES = {
    'briefing.py': 3,
    'markets_page.py': 4,
    'opportunities_page.py': 0,
    'analysis_page.py': 0,
    'portfolio_page.py': 0,
    'options_intel_page.py': 1,
    'performance_page.py': 0,
    'system_page.py': 0,
}


def _src(nom):
    return io.open(os.path.join(_PAGES, nom), encoding='utf-8').read()


def test_le_recensement_des_hotes_demo_ne_derive_pas_en_silence():
    """Un hôte qui apparaît ou disparaît change ce que l'utilisateur peut
    croire réel. Le compte doit bouger DÉLIBÉRÉMENT."""
    ecarts = []
    for nom, attendu in _HOTES_MESURES.items():
        reel = _src(nom).count('vx-demo-banner')
        if reel != attendu:
            ecarts.append('%s : %d attendu, %d mesuré' % (nom, attendu, reel))
    assert not ecarts, (
        'le recensement des hôtes « démo » a changé sans que ce fichier suive :\n'
        '  ' + '\n  '.join(ecarts) +
        '\nSi c\'est une CORRECTION, mettre à jour _HOTES_MESURES et retirer la '
        'ligne correspondante du constat. Si c\'est un accident, le défaut est '
        'précisément là.')


def test_options_porte_un_hote_que_rien_ne_remplit():
    """LE signe le plus net du constat : `options_intel_page.py` déclare
    `<div id="vx-demo-banner">` et aucun script de cette page ne l'écrit.

    Ce test ÉCHOUERA le jour où quelqu'un le remplit — et ce sera une bonne
    nouvelle, pas une régression : il faudra alors le retirer.
    """
    src = _src('options_intel_page.py')
    assert 'vx-demo-banner' in src, (
        'l\'hôte a disparu d\'Options : soit le défaut est corrigé (retirer ce '
        'test), soit l\'étiquette démo a été supprimée au lieu d\'être remplie.')
    assert "getElementById('vx-demo-banner')" not in src \
        and 'vx-demo-banner\').innerHTML' not in src, (
        'quelque chose remplit désormais l\'hôte démo d\'Options — le constat '
        'de ce fichier est périmé, le mettre à jour.')
