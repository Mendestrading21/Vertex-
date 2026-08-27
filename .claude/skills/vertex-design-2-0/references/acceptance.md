# Acceptation Vertex Design 2.0

## Produit et données

- READONLY et ANALYSIS_ONLY restent vrais ; aucun chemin d'ordre.
- Aucune donnée, courbe, source ou fraîcheur inventée.
- LIVE, DELAYED, STALE, DEMO, OFFLINE, MISSING/PARTIAL restent distingués.
- Les clés localStorage/desk sync, endpoints et contrats JS sont préservés ou migrés avec tests.

## Cohérence visuelle

- Une seule identité Black Glass — Signal Light sur toutes les pages.
- Geist/Geist Mono chargées avec fallback ; chiffres tabulaires.
- Aucun bleu identitaire, cuivre legacy, Signal Green de marque ou arc-en-ciel de séries.
- Vert, rouge, ambre et violet respectent strictement leur sens.
- Pas de bordures lourdes, glow permanent, gradient coloré ou carte opaque grise.
- Un seul système de cartes, métriques, contrôles, tables, états et charts.
- Tout texte visible est en français, sauf terme financier utile et explicable.

## UX et accessibilité

- Objectif et point focal compris en moins de cinq secondes.
- Navigation stable ; aucune impasse ni double destination ambiguë.
- Focus visible, ordre de tabulation logique, nom accessible pour icônes.
- Le sens ne dépend jamais uniquement de la couleur.
- Contraste AA pour les contenus essentiels.
- `prefers-reduced-motion` respecté.

## Responsive

Vérifier au minimum 390, 430, 768, 1024, 1280, 1440 et 1600 px, plus un écran large si disponible. Aucun débordement horizontal global, texte tronqué essentiel, contrôle inaccessible ou canvas déformé.

## Graphiques

- Question, conclusion, unité, période, source et fraîcheur.
- Axes honnêtes, benchmark cohérent, tooltip commun et fallback.
- Resize et destruction sans fuite ; console vide.
- Aucun graphique purement décoratif ou redondant.

## Vérifications techniques

```bash
python -m compileall -q terminal.py vertex
python -m pytest -q
python -m pytest tests/test_no_orders.py -q
```

Pour le runtime/UI : `/healthz`, `/api/client-log`, huit espaces principaux, utilitaires, sous-vues, desktop/tablette/mobile, données réelles et états dégradés. Tout changement visible du shell ou des statiques exige le bump du service worker et l'adaptation des tests associés.

## Contenu de la PR

- objectif et périmètre ;
- propriétaires modifiés ;
- avant/après aux largeurs pertinentes ;
- tests et vérifications navigateur ;
- impact données/fraîcheur ;
- risques, rollback et dette restante ;
- décisions humaines encore nécessaires.

