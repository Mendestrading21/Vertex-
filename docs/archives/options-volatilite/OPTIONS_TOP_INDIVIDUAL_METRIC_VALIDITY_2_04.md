# Vertex — Validité des métriques des classements TOP individuels

Les classements TOP individuels ne convertissent plus une valeur absente, booléenne ou invalide en score nul. Les critères restent limités aux données réellement reportées.

| Classement | Mesure requise | Critère de validité |
|---|---|---|
| TOP High POP | POP | Nombre compris entre 0 et 100 |
| TOP Momentum | Momentum | Nombre strictement positif |
| TOP Flux | Anomalie de volume (`vol_z`) | Nombre supérieur ou égal à 1 |

Un contrat dont la mesure ne respecte pas le critère ne peut pas apparaître dans le classement concerné. Cette logique est descriptive, strictement en lecture seule et ne constitue ni un ordre ni une garantie de résultat.
