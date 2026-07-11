"""vertex.ui.pages — pages du Vertex Master Redesign (8 espaces).

Chaque module expose `render(...) -> str` (HTML complet via le shell).
Convention : squelette HTML serveur + rendu client depuis les APIs existantes
(l'UI consomme les moteurs, ne recalcule rien), états LOADING/READY/EMPTY/
STALE/ERROR systématiques, provenance et horodatage visibles partout.
"""
