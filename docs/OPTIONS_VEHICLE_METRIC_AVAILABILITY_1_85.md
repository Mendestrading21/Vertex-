# Vertex — Disponibilité des métriques de véhicules options

La matrice de véhicules ne crée plus de probabilité de profit (POP) ou de point mort lorsque la valeur n’est pas réellement reportée par une jambe options disponible.

| Métrique | Condition de présence | Sinon |
|---|---|---|
| POP du CALL ATM | POP numérique reportée par le contrat vedette | `null` avec couverture indisponible |
| Point mort CALL/LEAPS | Point mort numérique reporté par la jambe correspondante | `null` avec couverture indisponible |
| POP et points morts des autres véhicules | Aucune donnée de contrat dédiée | `null`, sans approximation stratégique |

Chaque ligne porte un champ `coverage` distinguant disponibilité et provenance observée. Les coûts et primes calculés restent explicitement des sorties de modèle, pas des observations de marché.

> Vertex reste en lecture seule. Cette transparence ne constitue ni une recommandation personnalisée, ni une garantie de résultat.
