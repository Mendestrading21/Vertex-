# CLAUDE CODE — EXÉCUTION VERTEX TOTAL REBUILD

## Instruction principale

Utilise obligatoirement le skill :

```text
.claude/skills/vertex-total-rebuild/SKILL.md
```

L'objectif n'est pas d'ajouter une nouvelle couche esthétique. L'objectif est de reconstruire Vertex avec une seule logique produit, une seule architecture visuelle, une seule grammaire graphique et des sources de données canoniques.

## Lot actuel autorisé

Exécute uniquement les phases 0, 1 et 2 du skill :

1. baseline mesurée ;
2. inventaire exhaustif des fichiers ;
3. cartographie pages/endpoints/moteurs/graphiques ;
4. inventaire des références visuelles ;
5. registre des contradictions et doublons.

Ne commence pas encore la refonte massive des pages.

## Travail obligatoire

- Exécute réellement tous les tests.
- Lance réellement Vertex en mode démo.
- Inspecte toutes les routes dans le navigateur.
- Vérifie console, réseau, responsive et états de données.
- Inspecte tous les fichiers suivis par Git.
- Recherche les anciens thèmes, composants, graphiques et styles locaux.
- Identifie toutes les photos, captures et références visuelles présentes dans le dépôt.
- Relie chaque graphique à son endpoint et à son moteur source.
- Compare les métriques similaires afin de détecter les contradictions.
- Ne supprime rien pendant ce premier lot.

## Documents à produire

```text
docs/refactor/VERTEX_BASELINE_AUDIT.md
docs/refactor/FILE_INVENTORY.md
docs/refactor/PAGE_DATA_GRAPH_MATRIX.md
docs/refactor/CONTRADICTIONS_REGISTER.md
docs/refactor/CHART_INVENTORY.md
docs/refactor/VISUAL_REFERENCE_MAP.md
```

## Résultat attendu

Le rapport final doit donner :

- commit et branche analysés ;
- nombre exact de tests réussis/échoués ;
- liste complète des routes ;
- liste des pages et sous-vues ;
- liste des endpoints et moteurs ;
- liste complète des graphiques ;
- sources de données de chaque graphique ;
- contradictions critiques ;
- doublons fonctionnels ;
- fichiers legacy ou morts potentiels ;
- références visuelles trouvées ;
- graphiques à garder, modifier, fusionner, remplacer ou supprimer ;
- dix problèmes prioritaires ;
- plan précis de la PR suivante.

## Exigence de preuve

Ne réponds jamais uniquement « terminé ».

Pour chaque constat, indique les fichiers, routes, fonctions, tests, captures ou commandes qui le prouvent.

## Garde-fous

- IBKR READONLY est intouchable.
- Aucune donnée ne doit être inventée.
- Aucun moteur financier ne doit être modifié pour des raisons esthétiques.
- Aucun fichier ne doit être supprimé sans preuve d'inutilisation.
- Aucun calcul ne doit être changé sans test.
- Aucune nouvelle dépendance ne doit être ajoutée pendant l'audit.
