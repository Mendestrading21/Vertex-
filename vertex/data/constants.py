"""
vertex/data/constants.py — Constantes globales de VERTEX (valeurs pures, nommées).

Aucune valeur « magique » ne doit vivre dans le code métier : toute constante
importante est nommée et documentée ici. Extrait de terminal.py (refonte
institutionnelle — responsabilité unique : les constantes du domaine).
"""

# Indice de référence pour la force relative et le régime de marché.
BENCH = 'SPY'

# Taux sans risque annualisé utilisé par les modèles d'options (Black-Scholes).
R = 0.045

# Marqueur de version — visible dans /healthz et /api/system-status.
BUILD = 'VERTEX-1.0'

# Intervalle (secondes) entre deux scans complets de l'univers en boucle de fond.
REFRESH_SEC = 120

# Seuils de fraîcheur des données (secondes) pour /api/system-status.
STALE_SCAN_SEC = 900        # un scan de plus de 15 min est considéré « rassis »
STALE_QUOTES_SEC = 120      # cotations live rassies au-delà de 2 min
STALE_OPTIONS_SEC = 1800    # board d'options rassis au-delà de 30 min

__all__ = ['BENCH', 'R', 'BUILD', 'REFRESH_SEC',
           'STALE_SCAN_SEC', 'STALE_QUOTES_SEC', 'STALE_OPTIONS_SEC']
