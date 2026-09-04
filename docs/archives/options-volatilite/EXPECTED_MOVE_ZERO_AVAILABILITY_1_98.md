# Vertex — Mouvement attendu nul et disponibilité

Le laboratoire options ne traite plus un `em_pct` égal à zéro comme une fourchette exploitable autour du spot. Cette valeur ne peut pas représenter un mouvement attendu calculé à partir d’une IV strictement positive et d’un DTE exploitable.

| Valeur reportée | Sortie visualisation | Sortie matrice de risques |
|---|---|---|
| Nombre strictement positif | Fourchette `lo` / `hi` calculée | Niveau de volatilité évalué |
| Absente, invalide, booléenne ou nulle | `EXPECTED_MOVE_UNAVAILABLE`, sans bande plate | `INCONNU`, sans interprétation de volatilité |

> Le statut est descriptif uniquement. Vertex n’émet aucun ordre et ne garantit aucun résultat financier.
