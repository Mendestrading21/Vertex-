"""Lot 29 — la vue Options du Calendrier ne rend plus de filtres inertes.

`calendar.js` sort de `boot()` AVANT de câbler le moindre filtre quand la vue
est `options` : cette vue ne lit pas `/cal-feed`, sa donnée est le desk local.
Les neuf commandes de la barre de contexte — cinq horizons, trois types,
« Mes positions seulement » — s'affichaient donc exactement comme sur les six
autres vues et **ne faisaient rien**.

Relevé en les CLIQUANT (`tools/audit/boutons_morts.py`), pas en lisant le
code : aucune mutation du DOM, aucune requête, aucun défilement, aucune
écriture de stockage. Une commande qui ne peut rien produire est une fausse
fonctionnalité, que la doctrine produit interdit.

Ce banc garde les deux moitiés de la correction : les filtres disparaissent
là où ils ne peuvent pas agir, et restent là où ils agissent.
"""
from __future__ import annotations

import re

import pytest

from vertex.ui.pages import calendar_page

#: Les attributs par lesquels `calendar.js` retrouve les filtres. Écrits
#: littéralement des deux côtés : si l'un change, ce banc doit le voir.
_MARQUEURS = ('data-cal-horizon', 'data-cal-cat', 'data-cal-mine')

#: Les vues qui lisent `/cal-feed` — celles où les filtres ont un sens.
_VUES_FLUX = ('today', 'week', 'month', 'agenda', 'portfolio', 'macro')


def _barre(view: str) -> str:
    return calendar_page._filtres(view)


@pytest.mark.parametrize('marqueur', _MARQUEURS)
def test_la_vue_options_ne_rend_aucun_filtre(marqueur):
    """Aucune commande de filtre sur la vue que le script ne câble pas."""
    assert marqueur not in _barre('options'), (
        'la vue Options rend « %s » alors que `calendar.js` sort de boot() '
        'avant de le câbler : la commande s\'afficherait et ne ferait rien.'
        % marqueur
    )


def test_la_vue_options_dit_ce_qu_elle_mesure_a_la_place():
    """Retirer une commande sans rien dire est une perte, pas une correction."""
    barre = _barre('options')
    assert 'contrats déclarés' in barre, (
        'la barre de contexte doit nommer sa source réelle — les contrats '
        'déclarés — puisqu\'elle ne filtre plus un flux.'
    )
    assert 'vx-cal-fraicheur' in barre, (
        'la fraîcheur reste due : elle est remplie par `calendar.js` même sur '
        'cette vue.'
    )


@pytest.mark.parametrize('vue', _VUES_FLUX)
@pytest.mark.parametrize('marqueur', _MARQUEURS)
def test_les_vues_de_flux_gardent_leurs_filtres(vue, marqueur):
    """La correction ne doit pas déborder sur les vues où les filtres agissent."""
    assert marqueur in _barre(vue), (
        'la vue %s a perdu « %s » : elle lit `/cal-feed` et `calendar.js` y '
        'câble ce filtre.' % (vue, marqueur)
    )


def test_le_script_sort_bien_tot_sur_la_vue_options():
    """Le motif que ce banc suppose doit exister dans le script servi."""
    import pathlib
    js = (pathlib.Path(__file__).resolve().parents[1] / 'vertex' / 'static'
          / 'vertex' / 'js' / 'pages' / 'calendar.js').read_text(encoding='utf-8')
    bloc = re.search(r"if \(vue === 'options'\) \{(.*?)\n    \}", js, re.S)
    assert bloc, (
        "`calendar.js` ne sort plus tôt sur la vue Options : si elle câble "
        "désormais les filtres, il faut les lui rendre — et retirer ce banc."
    )
    assert 'return;' in bloc.group(1), (
        'la branche Options doit toujours sortir avant le câblage des filtres.'
    )
