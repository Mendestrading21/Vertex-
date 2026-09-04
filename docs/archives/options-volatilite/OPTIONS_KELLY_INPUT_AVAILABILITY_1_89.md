# Vertex — Disponibilité des intrants Kelly options

La fraction Kelly affichée dans les visualisations options exige désormais une POP numérique entre 0 et 100 et un potentiel de gain positif réellement reporté.

| Intrants | Résultat |
|---|---|
| POP et potentiel disponibles | Fraction Kelly calculée et bornée à 15 % |
| POP ou potentiel absent/invalide | `pct: null`, statut `KELLY_INPUT_UNAVAILABLE` |

Aucune POP de 30 % ni potentiel de 50 % n’est ajouté en secours. La couverture indique séparément la disponibilité de chaque intrant.

> Kelly est une mesure analytique conditionnelle, sans garantie de résultat ni ordre. Vertex demeure en lecture seule.
