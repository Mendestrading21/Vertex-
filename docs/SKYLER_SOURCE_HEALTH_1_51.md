# Vertex — santé non sensible des sources

`GET /api/skyler/health` expose `source_health`, une synthèse bornée aux statuts `AVAILABLE`, `DEGRADED`, `UNAVAILABLE`, `NOT_COLLECTED` et `UNKNOWN` pour le scan, le marché, les options et les fondamentaux.

La réponse ne contient ni nom de fournisseur détaillé, ni requête, ni adresse réseau, ni jeton, ni détail d’exception. Les statuts restent descriptifs et n’altèrent aucun verdict ou calcul de marché.
