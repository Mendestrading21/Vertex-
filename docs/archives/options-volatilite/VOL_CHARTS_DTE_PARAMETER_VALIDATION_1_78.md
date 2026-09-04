# Vertex — Validation DTE des graphiques de volatilité

La route `GET /api/options/vol-charts/<sym>?dte=…` n’interprète plus un paramètre DTE invalide comme l’absence de filtre.

| Valeur reçue | Réponse |
|---|---|
| Entier non négatif | Filtre d’échéance appliqué |
| Paramètre absent | Aucun filtre d’échéance demandé |
| Vide, illisible, négatif ou fractionnaire | HTTP 400 avec `DTE_PARAMETER_INVALID` |

Ce refus empêche qu’une requête mal formée affiche une structure de volatilité non filtrée à la place de l’échéance demandée.

> Ce contrôle ne modifie pas les données de marché, ne prédit rien et n’exécute aucun ordre. Vertex demeure en lecture seule.
