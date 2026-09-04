# Vertex — validation walk-forward de la mémoire Skyler

## Objectif

La route `GET /api/skyler/validation?horizon=H5|H10|H15|H20|H60` examine les résultats déjà mesurés du ledger append-only de **la version active du moteur uniquement**. Elle ne modifie ni scores, ni gates, ni décision, ni poids de stratégie. Son rôle est de rendre visible une différence répétée entre les décisions anciennes, utilisées comme entraînement, et des décisions plus récentes, observées comme hors échantillon.

> Le diagnostic est une vérification descriptive de cohérence historique. Un statut favorable ne démontre ni rendement futur ni robustesse définitive, et un statut défavorable impose une revue humaine plutôt qu’un changement automatique de stratégie.

## Chronologie et anti-fuite

| Étape | Règle | Protection apportée |
|---|---|---|
| Source | Uniquement les décisions et résultats MESURÉS portant la même `engine_version`. | Évite le mélange de versions de modèle. |
| Ordre | Classement par `session_date` figée dans le record, jamais par ordre d’écriture. | Évite une chronologie artificielle du ledger. |
| Embargo | Entre train et test, un nombre de séances égal à l’horizon mesuré est exclu. | Empêche de confondre une information postérieure à une décision d’entraînement avec le bloc test. |
| Évaluation | Le hit suit la taxonomie `classify_error` de la mémoire. | Conserve la même définition de résultat que les post-mortems. |

Une décision mesurée sans `session_date` n’est pas repositionnée par approximation : le diagnostic retourne `TEMPORAL_EVIDENCE_REQUIRED` jusqu’à ce que la preuve de chronologie soit disponible.

## Seuils et statuts

Par défaut, Vertex requiert au moins deux fenêtres complètes, chacune composée de 20 séances datées d’entraînement, d’un embargo égal à l’horizon, puis de 10 séances datées hors échantillon. Les résultats sont interprétés exclusivement comme suit.

| Statut | Signification | Attente de présentation |
|---|---|---|
| `INSUFFICIENT_SAMPLE` | Le nombre de séances datées ne suffit pas aux deux fenêtres complètes. | Afficher l’absence de preuve ; ne pas déduire une robustesse. |
| `TEMPORAL_EVIDENCE_REQUIRED` | Au moins un résultat mesuré n’a pas de date de séance figée. | Demander une meilleure traçabilité ; ne pas ordonner arbitrairement le ledger. |
| `OOS_CONSISTENT` | La dégradation du hit rate n’atteint pas 20 points de pourcentage dans une majorité de fenêtres. | Présenter une cohérence provisoire, jamais une prédiction. |
| `OOS_DEGRADED` | La dégradation atteint 20 points ou plus dans une majorité de fenêtres. | Présenter une revue humaine requise ; ne jamais désactiver ou recalibrer automatiquement le moteur. |

Chaque fenêtre expose ses bornes de train, d’embargo et de test ainsi que les hit rates et l’expectancy observés. Aucune quote de contrat ou P&L options n’est inféré : il s’agit d’un rendement du sous-jacent tel que la mémoire le mesure déjà.
