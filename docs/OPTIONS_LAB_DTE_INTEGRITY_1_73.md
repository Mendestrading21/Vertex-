# Vertex — Intégrité DTE du laboratoire options

Les catégories `TOP LEAPS`, `TOP Long terme` et `TOP Court terme` ne classent désormais que les contrats dont le DTE est numérique, non négatif et réellement reporté.

| DTE du contrat | Catégories d’horizon |
|---|---|
| Numérique et valide | Éligible selon sa frontière DTE |
| Absent, illisible ou négatif | Exclu des catégories d’horizon |

Une valeur DTE manquante n’est plus remplacée par zéro. Elle ne peut donc plus faire apparaître artificiellement un contrat comme une opportunité court terme.

Le compteur **LEAPS** du cockpit applique la même règle. Il ne compte que les contrats disposant d’un DTE exploitable d’au moins 300 jours.

> Ce filtre décrit la disponibilité de l’échéance et ne crée aucun ordre, aucune prévision ni garantie de résultat. Vertex demeure en lecture seule.
