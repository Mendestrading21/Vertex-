# Vertex — Structure temporelle IV Skyler

Le contexte `iv_term_structure` compare les médianes de volatilité implicite (`iv`) réellement observées parmi les contrats du board options du symbole. Il sépare un horizon court de **60 DTE ou moins** et un horizon long de **90 DTE ou plus**.

| Champ | Signification | Condition |
|---|---|---|
| `short_median_iv` | Médiane IV des contrats courts observés | Au moins une IV positive avec DTE ≤ 60 |
| `long_median_iv` | Médiane IV des contrats longs observés | Au moins une IV positive avec DTE ≥ 90 |
| `long_minus_short_iv_points` | Médiane long terme moins médiane court terme, en points d’IV | Deux horizons disponibles |
| `coverage` | Nombre de contrats retenus et frontières DTE appliquées | Toujours présent |

Lorsque l’un des horizons ne fournit aucune IV exploitable, le contexte retourne `INSUFFICIENT_SHORT_LONG_IV`. Il expose alors les nombres de contrats disponibles par horizon, sans imputer une valeur manquante.

> Ce contexte ne reconstruit aucune surface de volatilité, n’interpole aucune échéance, ne prédit pas la volatilité future et ne modifie ni score, ni gate, ni verdict. Vertex demeure un outil d’analyse en lecture seule ; toute décision comporte un risque de perte.
