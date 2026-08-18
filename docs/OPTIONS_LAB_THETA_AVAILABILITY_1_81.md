# Vertex — Disponibilité du thêta dans le laboratoire options

La matrice de risques ne remplace plus l’érosion `theta_burn` absente par une valeur par défaut.

| État de `theta_burn` | Niveau de risque | Couverture |
|---|---|---|
| Valeur numérique non négative reportée | Faible, moyen ou élevé selon la mesure | `THETA_BURN_AVAILABLE` |
| Absente ou invalide | `INCONNU` | `THETA_BURN_UNAVAILABLE` |

La matrice conserve le risque structurel du passage du temps, mais ne le quantifie pas si aucune mesure n’est disponible. Le champ `coverage` est purement descriptif.

> Cette transparence ne crée aucun ordre, aucune estimation de thêta et aucune garantie de résultat. Vertex demeure en lecture seule.
