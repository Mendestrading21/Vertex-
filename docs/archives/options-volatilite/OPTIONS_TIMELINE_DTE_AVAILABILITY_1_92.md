# Vertex — Disponibilité DTE de la timeline options

La timeline options ne remplace plus un DTE absent par 90 jours.

| État du DTE | Timeline |
|---|---|
| Entier positif reporté | Checkpoints, fenêtre TP1, résultats, sortie et expiration datés |
| Absent, invalide ou nul | Point de départ et avertissement `TIMELINE_DTE_UNAVAILABLE` uniquement |

Les événements calendaires réellement fournis continuent d’être ajoutés, mais aucun checkpoint de gestion ou date d’expiration n’est calculé par défaut.

> La timeline est informative et en lecture seule. Elle ne déclenche aucun ordre et ne garantit aucun résultat.
