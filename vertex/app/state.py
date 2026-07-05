"""
vertex/app/state.py — ÉTAT PARTAGÉ DE L'APPLICATION (Ch. II).

`scan_state` est LE dictionnaire vivant du scan : rempli et muté EN PLACE par la
boucle de fond, lu par les routes. Lui donner un domicile unique permet à
terminal.py ET aux Blueprints d'importer le MÊME objet — plus besoin de
l'injecter partout. On mute toujours en place (`.update(...)`, `state['x']=…`),
jamais de réassignation, pour que la référence reste partagée.

Lecture seule côté métier : cet état ne contient que de l'analyse, aucun ordre.
"""

# Le dict est délibérément « vide » ici ; terminal.py le remplit au démarrage
# (caches disque) puis la boucle de scan le met à jour en continu.
scan_state = {
    'rows': [], 'detail': {}, 'portfolio': None, 'options_board': [], 'daily': None,
    'anomalies': [], 'sectors': [], 'market_ctx': None, 'fundamentals': None,
    'indices': [], 'commodities': [], 'macro': [], 'edge': None, 'internals': None,
    'radar': None, 'recommendations': [], 'strategy': None, 'committee': None,
    'updated': None, 'error': None,
}

# Watchlist de la semaine : sélection figée le lundi (régénérée en fond).
weekly_state = {'data': None, 'updated': None, 'regenerated': False}


__all__ = ['scan_state', 'weekly_state']
