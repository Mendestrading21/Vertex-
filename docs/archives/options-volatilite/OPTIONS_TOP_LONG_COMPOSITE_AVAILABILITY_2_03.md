# Vertex — Disponibilité du classement composite TOP Long terme

Le classement « TOP Long terme » requiert un DTE d’au moins 150 jours, une qualité numérique valide et une POP numérique valide. La qualité ou la POP manquante ne sont plus remplacées par zéro dans son score composite.

| Contrat à long terme | Traitement |
|---|---|
| DTE, qualité et POP exploitables | Classé avec `quality + 0,3 × POP` |
| Qualité ou POP absente/invalide | Exclu du score composite, compté dans la couverture |
| Aucun contrat éligible | Liste vide servie avec `TOP_LONG_COMPOSITE_UNAVAILABLE` |

> Cette sortie reste analytique et en lecture seule. Elle ne constitue pas un ordre ni une garantie de performance.
