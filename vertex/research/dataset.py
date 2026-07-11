"""vertex.research.dataset — jeux de données de recherche avec embargo (§29).

Contrôles honnêtes : l'univers actuel souffre d'un biais du survivant
(constituants ACTUELS des indices) — tout dataset le documente.
"""
from .factory import walk_forward_splits  # noqa: F401

KNOWN_BIASES = {
    'survivorship': 'univers = constituants actuels des indices — les titres '
                    'disparus/délistés manquent ; les résultats sont optimistes',
    'close_only': 'stops/TP évalués sur clôtures — les mèches intrajournalières '
                  'manquent ; taux de stop sous-estimé',
}


def make_dataset(returns, meta=None):
    return {'returns': list(returns), 'n': len(returns),
            'meta': dict(meta or {}), 'documented_biases': dict(KNOWN_BIASES)}
