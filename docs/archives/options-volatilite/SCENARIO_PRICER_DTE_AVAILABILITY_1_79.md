# Vertex — Disponibilité DTE du moteur de scénarios

Le moteur `scenario_pricer.simulate()` ne convertit plus un DTE absent ou invalide en zéro lorsqu’il est appelé directement par un autre moteur.

| DTE transmis | Résultat |
|---|---|
| Entier non négatif reporté | Calcul poursuivi, sous réserve des autres entrées nécessaires |
| Zéro reporté | Option expirée, simulation refusée selon le comportement existant |
| Absent, illisible, négatif ou fractionnaire | Simulation refusée avec `input_coverage.status: DTE_UNAVAILABLE` |

Dans le dernier cas, le moteur renvoie `rate: null` pour ne pas suggérer qu’une échéance a été choisie par défaut.

> Le moteur est analytique et non transactionnel. Il ne crée ni ordre, ni prix observé, ni garantie de résultat.
