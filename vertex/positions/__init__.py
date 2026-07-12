"""vertex.positions — Position Intelligence (cycle de vie analytique).

Détection → Validation → Réconciliation → Enrichissement → Calcul →
Analyse → Contrôle stratégique → Risque → Verdict → Explication →
Alerte → Snapshot → Historique → Interface.

⛔ LECTURE SEULE ABSOLUE : ce paquet lit, calcule, compare, alerte et
historise. Il ne contient AUCUNE méthode d'exécution — un verdict RÉDUIRE
ou SORTIE_ANALYTIQUE_PROPOSÉE est une recommandation, jamais un ordre, et
aucune position réelle n'est clôturée automatiquement.
"""
from vertex.positions.repository import load_positions  # noqa: F401
from vertex.positions.detector import startup_position_report  # noqa: F401
from vertex.positions.audit import audit_positions  # noqa: F401
