# Vertex — Disponibilité DTE du score de contrat

Le scoreur de contrat exige désormais un DTE numérique entier et non négatif. Un DTE absent, illisible, négatif ou fractionnaire n’est plus remplacé par zéro.

| DTE du contrat | Effet sur le score |
|---|---|
| Entier non négatif reporté | Ajustement habituel selon la fenêtre de la catégorie |
| Absent, illisible, négatif ou fractionnaire | Multiplicateur DTE nul et pénalité explicite |

Cette règle rend le contrat non classable lorsque son échéance n’est pas prouvée, même si les autres facteurs semblent favorables.

> Cette protection ne produit ni ordre, ni estimation de marché, ni garantie de résultat. Vertex demeure en lecture seule.
