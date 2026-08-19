"""vertex/app/weekly_selection.py — LA SÉLECTION HEBDO, SON CHEMIN ET SON FILTRE.

Deux choses que `terminal.py` tenait et qui n'avaient aucune raison d'y rester :

- **où** vit le snapshot hebdomadaire figé ;
- **quels titres en sont écartés** parce que leurs résultats tombent dans la
  semaine.

## Le chemin passe par `persist.cache_path`, et ce n'est pas cosmétique

`terminal.py` calculait `os.path.join(os.path.dirname(__file__), …)`. Recopier
cette formule ici la ferait pointer vers `vertex/app/`, pas vers la racine : le
snapshot de la semaine serait écrit à côté du code et **l'ancien ne serait plus
jamais relu**. Aucune erreur ne serait levée — la sélection repartirait
simplement de zéro un lundi.

`persist.cache_path` rend exactement le même chemin qu'avant (mesuré) et refuse
toute sortie de la racine.

## Pourquoi écarter les résultats de la semaine

Une publication de résultats déplace un titre de plusieurs pour cent en une
séance, dans un sens que l'analyse technique ne prédit pas, et écrase la volatilité
implicite juste après. Garder ces titres dans une sélection *hebdomadaire*
reviendrait à parier sur l'événement plutôt que sur la thèse.

`dte` absent ⇒ le titre n'est **pas** écarté : ne pas savoir quand tombent les
résultats n'est pas savoir qu'ils tombent cette semaine.
"""
from __future__ import annotations

from vertex.app.state import cal_state
from vertex.services import persist

#: Sélection hebdo FIGÉE — le snapshot du lundi, relu toute la semaine.
CHEMIN = persist.cache_path('weekly_snapshot.json')


def carte_resultats() -> dict:
    """`{sym: dte}` depuis le calendrier de résultats collecté (`cal_state`).

    Sert à écarter les titres dont les résultats tombent dans la semaine
    (gap à l'ouverture, puis effondrement de la volatilité implicite)."""
    return {x['sym']: x['dte'] for x in (cal_state.get('items') or [])
            if x.get('sym') and x.get('dte') is not None}


__all__ = ['CHEMIN', 'carte_resultats']
