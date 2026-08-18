# Vertex — Volume relatif Skyler

Le contexte `relative_volume` compare le volume réellement observé de la dernière séance à la médiane des volumes observés sur les **20 séances précédentes** de la série de scan canonique.

| Champ | Signification | Condition |
|---|---|---|
| `current_volume` | Volume de la dernière séance | Volume courant strictement positif et fini |
| `prior_median_volume` | Médiane des 20 volumes antérieurs | Les 20 observations antérieures sont toutes exploitables |
| `current_to_prior_median_ratio` | Ratio du volume courant sur la médiane antérieure | Contexte disponible |
| `coverage` | Taille de fenêtre et nombre de volumes antérieurs valides | Toujours présent |

Le contexte retourne `CURRENT_VOLUME_UNAVAILABLE` lorsque la dernière observation est absente, nulle ou invalide. Il retourne `INCOMPLETE_PRIOR_VOLUME_WINDOW` lorsque l’une des 20 observations antérieures nécessaires manque, et `INSUFFICIENT_VOLUME_HISTORY` lorsque la série n’est pas assez longue. Aucun volume manquant n’est remplacé et aucune observation antérieure n’est sélectionnée comme valeur courante.

> Le volume relatif est une mesure descriptive observée. Il ne prédit pas l’activité future, ne modifie ni score, ni gate, ni verdict, et ne constitue pas un ordre ou une recommandation. Vertex reste un outil d’analyse en lecture seule ; toute décision financière comporte un risque de perte.
