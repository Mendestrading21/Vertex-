"""vertex.visualization — moteur d'interprétation des graphiques (§6).

Vertex ne se contente pas d'afficher des courbes : chaque graphique répond à
UNE question et rend un verdict lisible (FAVORABLE / NEUTRE / DÉFAVORABLE /
BLOQUANT / INCONNU) accompagné de ses preuves, de ses incertitudes et de son
impact stratégique. Règle de vérité : donnée absente → statut INCONNU, jamais
un chiffre inventé. Lecture seule, aucun ordre.
"""
from .schemas import (
    STATUSES, ST_FAVORABLE, ST_NEUTRE, ST_DEFAVORABLE, ST_BLOQUANT, ST_INCONNU,
    interpretation, is_valid_interpretation,
)

__all__ = [
    'STATUSES', 'ST_FAVORABLE', 'ST_NEUTRE', 'ST_DEFAVORABLE', 'ST_BLOQUANT',
    'ST_INCONNU', 'interpretation', 'is_valid_interpretation',
]
