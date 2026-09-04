# Vertex — Disponibilité du mouvement attendu dans la matrice de risques

La ligne « Volatilité du sous-jacent » de la matrice de risques n’utilise plus un mouvement attendu de 25 % lorsque `em_pct` est absent.

| État de `em_pct` | Niveau | Couverture |
|---|---|---|
| Numérique et non négatif reporté | Niveau calculé selon les seuils existants | `EXPECTED_MOVE_AVAILABLE` |
| Absent ou invalide | `INCONNU` | `EXPECTED_MOVE_UNAVAILABLE` |

Le texte précise désormais qu’aucun mouvement n’est quantifié lorsque la donnée manque. Une absence ne peut donc plus être présentée comme une volatilité médiane de 25 %.

> Ce statut est descriptif, sans prévision cachée, ordre ou garantie de résultat. Vertex demeure en lecture seule.
