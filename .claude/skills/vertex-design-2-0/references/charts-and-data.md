# Graphiques et présentation des données

## Contrat

Chaque graphique répond à une question métier et produit une conclusion lisible en cinq secondes. Il expose la source, la période, l'unité, le timestamp, la fraîcheur, les limites et son état.

Consolider `VXCharts`, Chart.js et TradingView Lightweight Charts derrière un thème et des wrappers communs. Ne pas créer une quatrième bibliothèque ou un second registre de couleurs.

## Palette

- Série principale : argent clair.
- Benchmark : gris moyen ou gris chaud.
- Positif/négatif : vert/rouge uniquement quand la direction porte ce sens.
- Seuil ou prudence : ambre.
- Options : violet discret, motif ou dash lorsque possible.
- Séries multiples neutres : variations de luminance, épaisseur, dash et marqueurs avant d'ajouter une teinte.

Le registre Python `vertex/visualization/palette.py`, le thème JS, les tokens CSS et les tests doivent converger vers les mêmes valeurs. Le cuivre, le cyan technique et le Signal Green ne sont plus des identités.

## Choix du visuel

- Tendance : ligne ou aire très légère.
- Prix : chandeliers + volume + niveaux réels.
- Comparaison précise : barres triées ou table avant donut.
- Composition : donut limité à cinq catégories, sinon treemap/table.
- Risque borné avec seuils réels : jauge ; sinon barres ou distribution.
- Performance : equity curve + benchmark + drawdown séparé.
- Options : payoff, spot × temps, smile/skew, term structure, OI par strike.
- Densité ou calendrier : heatmap avec légende et fallback tabulaire.

Supprimer, fusionner ou remplacer tout graphique qui ne répond à aucune décision ou répète exactement une table voisine.

## Honnêteté visuelle

- Zéro visible sur barres signées et drawdown.
- Axes non tronqués de manière trompeuse.
- Comparaisons normalisées sur une base commune.
- Seuils affichés seulement s'ils viennent d'une règle réelle.
- Une couleur de marché n'est pas automatiquement positive : hausse du VIX, des taux ou de l'IV doit être interprétée selon la métrique.
- Ne jamais relier des points manquants comme s'ils existaient.
- Fallback accessible et textuel pour toute visualisation critique.

## Implémentation

- Les couleurs sont résolues depuis les tokens au rendu.
- Tooltip, axes, grille, formatters, resize, destruction, reduced motion et états sont centralisés.
- Le canvas reste transparent ; la surface appartient à `ChartCard`.
- Une instance est détruite avant recréation ; aucun listener ou ResizeObserver orphelin.
- Les graphiques respectent le mode de densité sans masquer source, unité ou conclusion.

