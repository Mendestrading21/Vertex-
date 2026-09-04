# Vertex — Disponibilité DTE de la surface de volatilité

La surface de volatilité construit désormais une expiration uniquement si les contrats qui la composent fournissent un unique DTE numérique entier et non négatif.

| DTE par expiration | Effet |
|---|---|
| Valeur valide unique | Point ATM, structure de terme et mouvement attendu observé produits |
| Absent ou invalide | Expiration exclue avec une note explicite |
| Plusieurs valeurs contradictoires | Expiration exclue avec une note explicite |

L’exclusion évite de représenter une expiration incomplète comme un point à zéro jour. Aucune interpolation ou prévision n’est ajoutée.

> Cette surface reste une lecture descriptive des IV disponibles ; elle ne crée ni ordre ni garantie de résultat.
