# Plan d'exécution Vertex Design 2.0

## Phase 0 — Baseline et convergence documentaire

- Relever SHA, CI, PR ouvertes, routes, propriétaires et captures actuelles.
- Identifier toutes les identités concurrentes et les consommateurs réels.
- Établir la matrice page × données × widgets × graphiques × états.
- Ne pas utiliser la PR historique Signal OS comme base de vérité.

## Phase 1 — Fondations

- Installer/self-héberger Geist et Geist Mono avec fallback sûr.
- Unifier tokens CSS, palette Python, thème JS et `.interface-design/system.md`.
- Retirer l'identité Signal Green/cuivre/cyan des chemins actifs sans casser les alias legacy nécessaires.
- Mettre `/design-system` au niveau de la cible et ajouter les tests de contrat.

## Phase 2 — Shell et navigation

- Unifier sidebar, topbar, recherche, statut marché, drawers, modales, toasts et mobile bar.
- Appliquer l'architecture principale/utilitaire cible.
- Préserver routes et préférences avec redirects/migrations.
- Éliminer double navigation et styles inline du shell.

## Phase 3 — Primitives

- Consolider cartes, métriques, badges, boutons, tabs, filtres, tables, formulaires et états.
- Migrer les variantes page par page vers les primitives ; ne pas supprimer une classe avant son dernier consommateur.
- Documenter chaque primitive sur `/design-system`.

## Phase 4 — Graphiques

- Unifier palette, thème, wrappers, tooltip, axes, formatters, registry, resize et fallbacks.
- Auditer chaque graphique par question, source, unité, période, fraîcheur et conclusion.
- Supprimer seulement les visualisations prouvées redondantes ou décoratives.

## Phases 5 à 14 — Pages

Ordre : Aujourd'hui → Marchés → Opportunités → Analyse → Portefeuille → Options et chaîne complète → Performance/Journal/Centre de suivi → Intelligence → Système → routes secondaires.

Pour chaque page : baseline, question, hiérarchie, composants partagés, états, responsive, clavier, tests, captures et rollback. Une page ne crée pas de nouveau token ou composant si l'équivalent existe.

## Phase 15 — Nettoyage contrôlé

- Chercher les consommateurs avant toute suppression.
- Retirer CSS/JS/documents historiques uniquement lorsqu'un remplacement testé existe.
- Conserver un journal de migration et des redirects temporaires.
- Bumper le service worker pour chaque livraison visible concernée.

## Phase 16 — QA et release

- Suite complète, tests garde-fous, healthz et console.
- Captures représentatives avec données réelles, sans IBKR, demo, stale, partial et offline.
- Audit visuel, a11y, responsive et performance.
- PR brouillon avec preuves. Aucune fusion, activation ou promesse « 100 % terminé » sans décision humaine.

## Commande de démarrage Claude

```text
/vertex-design-2-0 phase:fondations
```

Claude commence par la première phase non terminée. Il n'ouvre pas plusieurs phases dépendantes simultanément et ne saute pas les fondations pour retoucher une page visible.
