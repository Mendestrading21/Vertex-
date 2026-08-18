# Design system — Vertex 1.0

## Principe

Une interface de décision institutionnelle, sombre, calme et dense sans être
encombrée. La hiérarchie suit:

```text
signal → preuve → risque → action analytique
```

## Direction

- fonds obsidienne et surfaces mates;
- contraste élevé, effets de verre limités;
- accent d'interaction unique;
- vert/rouge/ambre réservés à la sémantique financière et aux états;
- typographie Inter pour le texte, IBM Plex Mono pour chiffres/codes;
- espaces, rayons et ombres issus d'une source de tokens unique.

## Règles

- huit espaces, une question principale par page;
- un KPI ou graphique par question, pas plusieurs variantes décoratives;
- titres courts, unités et timestamps visibles;
- chaque chiffre affiche source, fraîcheur et état lorsque nécessaire;
- aucun verdict communiqué seulement par la couleur;
- tables desktop transformées en cartes ou scroll intentionnel sur mobile;
- focus clavier, reduced motion et contraste vérifiables.

## Consolidation

Les couches Obsidian Copper, Neon Glass, V4/Prism et Signal OS sont des
références historiques. La PR Signal OS ne doit pas être fusionnée en bloc:
elle diverge fortement de `main`. Chaque composant récupéré doit:

1. résoudre une question produit;
2. utiliser les tokens canoniques;
3. remplacer, pas empiler, une implémentation;
4. conserver l'intégrité des données;
5. passer les tests de page et d'accessibilité.

## Interdictions

- nouveaux hex dispersés;
- nouveaux thèmes parallèles;
- graphiques sans résumé accessible;
- texte marketing qui dépasse la preuve;
- animation décorative sur données critiques;
- masquer `MISSING`, `STALE`, `DEMO` ou `OFFLINE`.
