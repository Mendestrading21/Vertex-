"""vertex.data_sources — provenance, qualité, routage et réconciliation des données.

Invariant : chaque valeur servie à l'analyse est horodatée et porte sa source
(IBKR live / delayed, fournisseur secondaire, fallback EOD) — jamais de
mélange silencieux de sources ni de donnée inventée. Donnée absente = None
affiché « — », pas un chiffre synthétique.
"""
