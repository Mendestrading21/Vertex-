# Vertex — Disponibilité DTE du plan de trade options

Le diagnostic catalyseurs et le plan de trade ne transforment plus un DTE absent en horizon par défaut.

| État du DTE | Catalyseurs | Plan de trade |
|---|---|---|
| Entier positif reporté | Score et fenêtres de résultats calculés | Calendrier de sortie et expiration affichés |
| Absent, invalide ou nul | Niveau `INCONNU` et horizon non qualifié | `TRADE_PLAN_DTE_UNAVAILABLE`, aucune échéance inférée |

Le texte de sortie devient explicitement conditionnel lorsque le DTE manque. Il ne suggère plus une fenêtre « 2–3 semaines avant expiration » sans date d’expiration prouvée.

> Le plan reste descriptif et en lecture seule. Il ne déclenche aucun ordre et ne garantit aucun résultat.
