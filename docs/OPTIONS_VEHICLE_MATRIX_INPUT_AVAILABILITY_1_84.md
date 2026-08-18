# Vertex — Disponibilité des intrants de matrice de véhicules

La matrice de comparaison des véhicules options exige désormais un spot positif et une IV positive réellement reportés pour le contrat vedette.

| Intrants | Résultat |
|---|---|
| Spot et IV disponibles | Matrice de véhicules calculée selon les formules existantes |
| Spot ou IV absent/invalide | Matrice indisponible, `rows: []`, statut `VEHICLE_MATRIX_INPUT_UNAVAILABLE` |

La matrice ne crée plus un spot à 100 ou une IV à 35 % afin de présenter des prix, points morts ou probabilités de véhicules théoriques.

> La réponse reste descriptive, sans exécution d’ordre, prix observé inventé ni garantie de résultat. Vertex demeure en lecture seule.
