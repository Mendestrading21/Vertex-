# Vertex V3 — Options Swing trois à six mois

## Objet

La constitution **V3** ajoute le mandat opérationnel `SWING_3_6M` pour les options longues détenues de **une à trois semaines**. Ce mandat est analytique et en lecture seule : il ne place, ne transmet ni ne prépare aucun ordre.

> Un score classe un dossier. Il ne crée jamais une obligation d’acheter, et une probabilité ne doit jamais être affichée comme telle avant calibration hors échantillon suffisante.

## Contrat de sélection

| Élément | Règle V3 | Effet de sécurité |
|---|---:|---|
| DTE admissible | 75–210 jours | Une fenêtre de sélection explicite est appliquée. |
| DTE préféré | 90–180 jours | Alignement avec le mandat trois à six mois. |
| DTE cible de classement | 135 jours | Critère déterministe de proximité, non une promesse de performance. |
| Plans de détention | 5, 10 ou 15 séances | Le plan est présent dans le contexte et dans le sélecteur de calls. |
| Delta absolu | 0,30–0,60 | Contrôle transparent du profil de sensibilité. |
| Open interest minimal | 500 | Contrôle de liquidité minimal. |
| Volume minimal | 50 | Une valeur absente est `PARTIAL_MANDATE`, jamais conforme par défaut. |
| Spread maximal | 8 % | Les contrats trop coûteux sont étiquetés hors mandat. |
| Âge maximal de quote | 900 secondes | Une quote absente ou trop ancienne ne peut pas être déclarée fraîche. |

Les statuts d’un candidat sont `IN_MANDATE`, `PARTIAL_MANDATE`, `OUT_OF_MANDATE` ou `NOT_APPLICABLE`. Les candidats hors mandat restent visibles avec leurs motifs : VERTEX ne masque pas les informations qui ont motivé un rejet.

## Chaîne de décision

La fiche Skyler et le balayage d’univers utilisent tous deux le même contexte `SWING_3_6M`. Le contexte contient l’univers, le meilleur candidat déterministe, son statut de mandat, les raisons de non-conformité, sa distance au DTE cible et le plan de détention. Une même entrée produit donc la même base de sélection dans les deux parcours.

La route Strategy OS construit désormais un `DecisionPacket` déterministe. Trois preuves critiques doivent être fournies explicitement : la qualité de données, la réconciliation des sources et le garde-fou portefeuille. En l’absence de l’une d’elles, la règle `DECISION_PACKET_INCOMPLETE` plafonne toute décision nouvelle à `ATTENDRE`.

| Section critique | Absence de donnée | Comportement |
|---|---|---|
| Qualité de données | Une qualité seulement dérivée du scan est disponible. | Paquet incomplet, sans conformité implicite. |
| Réconciliation | Aucune preuve spot/chaîne/contrat n’est fournie. | Entrée actionnable refusée. |
| Portefeuille | Aucun calcul de risque portefeuille n’est fourni. | Entrée actionnable refusée. |

## Mémoire et calibration

Le ledger immuable fige le contexte options déjà présent au moment de la décision : univers, DTE, bucket DTE, delta, IV, open interest, volume, spread, âge de quote, statut de mandat et plan de détention. Il mesure désormais le résultat directionnel du sous-jacent aux horizons **5, 10 et 15 séances**, en plus des horizons 20 et 60 séances historiques.

Cette mesure n’est **pas** un P&L de contrat. Tant qu’une quote de sortie, avec ses coûts et son timestamp, n’est pas enregistrée, le résultat `OPTION` demeure `NON_APPLICABLE`. Les découpes par univers, bucket DTE et plan de détention sont des observations descriptives du signal directionnel ; elles ne sont pas consommées comme calibration de rendement d’option.

## Exploitation et validation

Avant d’utiliser un dossier pour une analyse actionnable, l’opérateur vérifie que le `DecisionPacket` est complet, que le contrat est `IN_MANDATE`, que les quotes sont fraîches et que les coûts bid/ask sont réalistes. Toute information manquante doit mener à `ATTENDRE`, à une surveillance ou à une recherche complémentaire, jamais à une extrapolation.

La suite de tests complète du dépôt a été exécutée après cette évolution avec le résultat suivant : **3 024 tests réussis**. Les tests couvrent notamment le scan 3–6 mois, l’absence de conformité implicite en cas de liquidité incomplète, le paquet de décision incomplet, le profil V3, la mémoire options et les horizons de 5/10/15 séances.
