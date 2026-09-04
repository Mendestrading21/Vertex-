# Vertex — Disponibilité DTE des véhicules recommandés

Les véhicules d’horizon `LEAPS`, `COVERED_CALL` et `PROTECTIVE_PUT` exigent désormais un DTE numérique, non négatif et effectivement reporté.

| Rôle | Fenêtre DTE | Donnée absente ou invalide |
|---|---:|---|
| LEAPS | ≥ 300 jours | Exclu |
| Covered call | 20–90 jours | Exclu |
| Protective put | 25–180 jours | Exclu |

Une échéance manquante n’est plus remplacée par zéro lors de la sélection. Les contrats peuvent rester visibles au board, mais ne reçoivent pas un rôle d’horizon non prouvé.

> Vertex reste un système d’analyse en lecture seule. Cette règle ne crée ni ordre, ni garantie de résultat.
