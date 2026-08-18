# Vertex — diagnostic de rupture de régime

## Objectif

Le champ `decision.regime_break` complète les indicateurs existants de tendance, de volatilité et de structure. Il compare 60 rendements journaliers de référence aux 20 rendements ultérieurs, depuis la même série de clôtures **datée**. Il est strictement descriptif : le score Skyler, les gates, le verdict et la mémoire décisionnelle ne le consomment pas.

> Une rupture statistique observée signale une revue analytique. Elle ne prédit pas le régime futur et ne déclenche ni ordre, ni allocation, ni modification automatique de la stratégie.

## Méthode et garde-fous

| Élément | Règle | Garanties |
|---|---|---|
| Donnée | Clôtures positives, finies et accompagnées de dates ISO strictement croissantes. | Aucune série non datée ou réordonnée n’est analysée. |
| Référence | 60 rendements immédiatement antérieurs. | Les rendements récents restent postérieurs à la référence. |
| Fenêtre récente | 20 rendements ultérieurs. | Pas de chevauchement de rendements avec la référence. |
| Volatilité | Alerte si l’écart-type récent / référence est supérieur ou égal à 1,80. | Seuil visible ; la variabilité nulle rend le résultat indisponible. |
| Direction | Alerte si le déplacement de moyenne normalisé atteint 2,50 ; renversement explicite si les rendements cumulés changent de signe. | Un déplacement statistique est séparé d’une affirmation économique ou prédictive. |

Le diagnostic retourne `TEMPORAL_EVIDENCE_REQUIRED` pour une date, une clôture, un ordre chronologique ou une variabilité de référence non exploitable. Il retourne `INSUFFICIENT_SAMPLE` sous 81 clôtures datées. L’absence de preuve ne devient jamais une continuité supposée.

## Statuts

| Statut | Signification de présentation |
|---|---|
| `REGIME_CONTINUITY` | Aucune rupture ne dépasse les seuils publiés dans l’échantillon. Ce n’est pas une prévision de stabilité. |
| `REGIME_BREAK_WATCH` | Une expansion de volatilité, un déplacement de rendement moyen ou une inversion directionnelle a été observé. Présenter une revue analytique requise. |
| `TEMPORAL_EVIDENCE_REQUIRED` | Les preuves chronologiques ne permettent pas de calculer le diagnostic. |
| `INSUFFICIENT_SAMPLE` | La série datée n’atteint pas la longueur minimale. |

Les indicateurs `VOLATILITY_REGIME_BREAK`, `MEAN_RETURN_REGIME_BREAK` et `DIRECTIONAL_REGIME_REVERSAL` sont des causes descriptives. Ils ne sont ni des signaux d’achat ou de vente, ni des garanties de perte ou de performance.
