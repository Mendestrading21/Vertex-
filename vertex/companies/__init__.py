"""vertex.companies — Company Intelligence (§16).

Façade unique du « jumeau analytique » d'une entreprise : profil, pairs,
fondamentaux, valorisation relative — le tout depuis les moteurs existants
(`vertex/data/company.py`, `vertex/data_sources/fundamentals.py`), sans
duplication de calcul. Le détecteur de changement compare deux snapshots
et déclenche un recalcul de décision (jamais un ordre).
"""
from vertex.companies.company_twin import company_twin  # noqa: F401
from vertex.companies.change_detector import detect_changes  # noqa: F401
