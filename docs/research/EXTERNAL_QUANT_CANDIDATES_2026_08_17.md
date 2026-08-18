# Veille externe — candidats quantitatifs pour Vertex

## Périmètre

Cette veille identifie des composants open source susceptibles d’améliorer les diagnostics de Vertex. Aucune dépendance n’est installée à ce stade. Toute adoption exige une vérification ultérieure de la licence, de la surface de dépendances, de la compatibilité des données, de la sécurité et des tests de non-régression.

| Candidat | Intérêt observé | Risque ou limite | Décision provisoire |
|---|---|---|---|
| `awesome-quant` | Catalogue de projets quantitatifs utile à la découverte ; activité de maintenance visible. | C’est un index, pas une bibliothèque à intégrer. | Utiliser uniquement comme source de sélection. |
| `QuantStats` | Bibliothèque Python de métriques de séries de rendements, drawdown et risque ; licence Apache-2.0 confirmée via l’API GitHub ; maintenance récente visible. | Les métriques portent sur des périodes de rendement, pas directement sur les trades discrétionnaires ni les contrats options. Dépendances scientifiques supplémentaires. | Évaluer certaines formules isolées face aux métriques Vertex existantes ; ne pas importer le package sans audit. |
| `Riskfolio-Lib` | Méthodes de risque et de portefeuille nombreuses, activité récente visible, licence BSD-3-Clause confirmée via l’API GitHub. | Orientée optimisation/allocation et dépendances potentiellement lourdes ; Vertex ne doit ni proposer ni exécuter une allocation. | Ne pas intégrer l’optimiseur. Évaluer seulement des métriques descriptives si elles apportent une preuve supplémentaire. |
| `VectorBT` | Moteur vectorisé de recherche, métriques de portefeuille et tests de robustesse ; activité récente et version publiée visibles. | La licence renvoyée par l’API GitHub est `NOASSERTION`, tandis que le projet expose une surface et des dépendances étendues (Numba/Rust, accès données, automatisation). | Exclure toute installation tant que la licence n’est pas explicitement résolue et que l’isolation du sous-ensemble lecture seule n’est pas démontrée. |
| `Frouros` | Bibliothèque de détection de dérive conceptuelle et de données ; licence BSD-3-Clause affichée ; tests, CI et maintenance visible. | Conçue pour les flux de modèles de ML ; ses détecteurs ne valident pas automatiquement la pertinence économique ni la stabilité d’une stratégie financière. | Évaluer les statistiques de dérive non paramétriques comme référence ; préférer une implémentation locale minimale si les entrées et seuils Vertex sont clairement établis. |
| `ruptures` | Bibliothèque de détection de points de rupture temporels ; licence BSD-2-Clause affichée ; tests et activité de maintenance visibles. | Un changement statistique ne constitue pas à lui seul un régime économique ni une prévision ; une intégration introduirait une dépendance supplémentaire. | Retenir le principe de rupture avec seuils et données datées explicites ; comparer une implémentation locale minimale avant toute dépendance. |
| `vollib` | Calcul de prix, volatilité implicite et grecques Black/Black-Scholes/Black-Scholes-Merton ; licence MIT affichée ; version 1.0.7 récente visible. | Vertex possède déjà un moteur Black-Scholes ; le gain ne justifie pas encore une nouvelle dépendance. Les entrées de marché manquantes restent non inférables. | Préférer un jeu de tests croisés sur le moteur existant ; n’adopter que si un écart numérique démontré exige le solveur de volatilité implicite. |

## Principe de sélection

Vertex privilégie les algorithmes purs, déterministes, à dépendances limitées et compatibles avec des séries datées réellement disponibles. Les composants qui optimisent automatiquement un portefeuille, exigent des données absentes, cachent leur méthodologie ou augmentent la surface d’exécution sont exclus par défaut.

## Priorisation retenue

| Priorité | Amélioration | Décision |
|---|---|---|
| P1 | Diagnostic local de rupture de régime sur volatilité et tendance réalisées. | À développer sans dépendance externe, avec fenêtres datées, seuils publiés et état indisponible si l’historique est incomplet. Cette approche reprend le principe de `ruptures` sans transformer un point de rupture en prédiction. |
| P2 | Test croisé de précision de la volatilité implicite et des grecques du moteur options existant. | À préparer contre une référence vérifiée avant toute dépendance `vollib`; la couverture options réelle reste la condition d’évaluation. |
| P3 | Métriques de risque complémentaires de séries de rendements. | À étudier à partir de formules explicables inspirées de QuantStats et Riskfolio-Lib, jamais via un optimiseur d’allocation. |
| Exclu pour l’instant | Import direct de VectorBT, Riskfolio-Lib ou d’optimiseurs. | Surface de dépendances, mécanismes d’optimisation/allocation ou licence insuffisamment certaine incompatibles avec l’objectif actuel. |

## Sources consultées

1. https://github.com/wilsonfreitas/awesome-quant
2. https://github.com/ranaroussi/quantstats
3. https://github.com/dcajasn/Riskfolio-Lib
4. https://github.com/polakowo/vectorbt
5. https://github.com/IFCA-Advanced-Computing/frouros
6. https://github.com/deepcharles/ruptures
7. https://github.com/vollib/py_vollib
