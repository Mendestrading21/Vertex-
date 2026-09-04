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

# Marqueur de version — visible dans /healthz, /readyz et la page Système.
#
# DÉRIVÉ de `vertex/version.py`, seul propriétaire canonique de la version.
# La valeur était recopiée à la main (`'VERTEX-1.0'`) : au renommage du produit
# en Vertex Test 1.0, elle a cessé de correspondre sans que rien ne le signale,
# et l'opérateur lisait dans « Build » une version qui n'existait plus. Deux
# propriétaires pour une même métrique, c'est la dérive garantie.
# `vertex/version.py` n'importe rien : aucun cycle possible.
from vertex.version import RELEASE_NAME as _RELEASE_NAME

BUILD = _RELEASE_NAME

# Intervalle (secondes) entre deux scans complets de l'univers en boucle de fond.
# MODÈLE « SESSION D'ANALYSE 30 MIN » : le premier scan (démarrage à froid) calcule
# tout l'univers en ~2-3 min, puis la session reste STABLE 30 min — les verdicts et
# chiffres ne bougent pas, les changements de page sont instantanés (aucun recalcul).
# Toutes les 30 min, un nouveau scan republie → bascule atomique côté client
# (session_id dérivé de scan_ts). Cadence voulue par l'utilisateur : une analyse
# posée, pas un ticker qui clignote. (Le prix live éventuel IBKR reste un overlay séparé.)
REFRESH_SEC = 1800          # 30 min : cadence de la session d'analyse
DEMO_UNIVERSE_N = 20        # mode démo : la boucle scanne UNIVERSE[:N] (vitrine rapide)

# Seuils de fraîcheur des données (secondes) pour /api/system-status.
# Alignés sur la cadence de 30 min : une donnée n'est « rassise » que si le
# rafraîchissement de session est EN RETARD (au-delà de la fenêtre de 30 min + marge),
# jamais pendant la session courante — sinon le badge crierait « à actualiser » à tort.
STALE_SCAN_SEC = 2100       # scan « rassis » seulement si le cycle 30 min est dépassé (>35 min)
STALE_QUOTES_SEC = 120      # cotations live rassies au-delà de 2 min (overlay live, indépendant)
STALE_OPTIONS_SEC = 2100    # board d'options rassis au-delà du cycle de session (>35 min)

__all__ = ['BENCH', 'R', 'BUILD', 'REFRESH_SEC', 'DEMO_UNIVERSE_N',
           'STALE_SCAN_SEC', 'STALE_QUOTES_SEC', 'STALE_OPTIONS_SEC']
