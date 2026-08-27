---
name: vertex-2-0
description: Auditer et refondre intégralement l'interface visible de Vertex comme centre de trading IA clair, cohérent et premium, page par page, en réutilisant toutes les capacités existantes sans modifier moteurs, calculs, données, API, intégrations ou règles financières.
---

# Vertex 2.0 — Centre de trading IA

## Mission

Transformer l'interface existante en un centre de trading IA complet, clair et simple à utiliser. La refonte relie visuellement toutes les capacités déjà présentes — marchés, opportunités, analyse, options, calendrier, portefeuille, risque, performance, suivi et IA — sans modifier leur fonctionnement interne.

Ce skill est l'orchestrateur unique et la doctrine finale de la refonte visuelle. Pour ce chantier, lancer uniquement `/vertex-2-0`. Il lit l'autorité financière existante pour connaître les invariants, mais ne modifie jamais ses propriétaires :

- `.claude/skills/vertex-1-0/SKILL.md` pour les données, moteurs, stratégies, règles financières, sécurité et release ;
- `.claude/skills/vertex-design-2-0/SKILL.md` est seulement un alias historique vers ce skill.

Les anciennes instructions de design sont des preuves historiques. Les références internes de ce skill définissent désormais directement l'architecture des pages, l'UX, les composants, les graphiques et l'identité visuelle.

En cas de conflit : sécurité et lecture seule → vérité financière → contrats existants → clarté d'usage → design.

## Périmètre verrouillé : interface uniquement

Autorisé :

- réorganiser la navigation, les pages, sous-vues et sections ;
- modifier templates/HTML de présentation, CSS, tokens, classes et responsive ;
- consolider les composants visuels, tables, drawers, formulaires et états ;
- modifier le thème et les options de rendu des graphiques sans changer leurs données ;
- reformuler toute la microcopy visible en français ;
- créer une nouvelle vue visuelle uniquement avec routes, fonctions, endpoints et données déjà présents ;
- ajouter tests visuels, a11y, responsive et garde-fous de présentation.

Interdit :

- modifier moteur, score, formule, scénario, gate, stratégie ou verdict ;
- modifier schéma métier, store, persistance, desk sync ou donnée utilisateur ;
- ajouter ou changer provider, API, endpoint financier, worker, job ou intégration ;
- modifier les connexions IBKR, TradingView, WMB, news ou Claude ;
- fabriquer une donnée pour remplir une nouvelle page ;
- déplacer une logique financière dans JavaScript ou un template ;
- supprimer une fonction existante parce qu'elle est difficile à présenter.

Si la maquette exige une donnée ou fonction absente, noter le besoin dans le rapport de lot et afficher un état manquant honnête. Ne pas développer le backend dans cette refonte.

Ce verrou de périmètre prévaut sur toute formulation plus ambitieuse présente dans une référence de domaine.

## Boucle produit

**OBSERVER → COMPRENDRE → DÉTECTER → ÉVALUER → DÉCIDER → SURVEILLER → MESURER → APPRENDRE.**

Chaque page, tableau, graphique et texte IA doit servir explicitement une étape. Une fonctionnalité existante sans place évidente reste fonctionnelle : déplacer ou regrouper uniquement sa présentation, sans supprimer sa logique, sa route, ses données ni ses consommateurs.

## Invariants absolus

- Vertex reste `READONLY=True` et `ANALYSIS_ONLY=True` ; IBKR reste `readonly=True`.
- Aucun ordre, ticket broker, bouton achat/vente, transmission ou automatisation d'exécution.
- L'IA explique et relie les faits ; elle ne calcule ni ne modifie prix, Greeks, score, scénario, risque, sizing, hard gate ou verdict canonique.
- Aucune donnée, source, fraîcheur, courbe ou performance inventée. L'absence est affichée honnêtement.
- Les positions IBKR, positions déclarées, idées suivies, simulations et signaux théoriques restent séparés.
- Toute décision conserve faits, sources, timestamps, qualité, contradictions, scénarios, invalidation, version des moteurs et limites.
- Les fonctionnalités existantes sont inventoriées et consolidées avant tout ajout parallèle.

## Règle « tout ce qui existe déjà »

Avant chaque page, cartographier en lecture seule routes, modules, moteurs, services, jobs, stores, endpoints, composants, tests et documents liés. Produire ou mettre à jour un registre visuel indiquant : source existante, consommateur, bloc actuel, état réel, doublon d'affichage, donnée manquante et décision conserver/regrouper/déplacer/masquer visuellement.

Ne jamais repartir de zéro si une capacité saine existe. Les doublons de présentation peuvent converger ; les propriétaires métier restent intacts.

Lire [product-contract.md](references/product-contract.md), puis [platform-architecture.md](references/platform-architecture.md) pour la carte cible et [capability-convergence.md](references/capability-convergence.md) pour la méthode d'inventaire.

## Routage des domaines

- Organisation définitive, routes, pages, sous-vues et premier écran : [navigation-and-pages.md](references/navigation-and-pages.md).
- Identité, tokens, typographie, profondeur, densité et motion : [design-system-final.md](references/design-system-final.md).
- Cartes, widgets, tables, drawers, formulaires et états : [components-tables-and-states.md](references/components-tables-and-states.md).
- Choix et implémentation des graphiques : [chart-system-final.md](references/chart-system-final.md).
- Catalogue des widgets trading, licences et règles d'adoption : [trading-widget-catalog.md](references/trading-widget-catalog.md).
- Simulateur multi-actifs de positions et scénarios : [position-simulator.md](references/position-simulator.md).
- Français, accessibilité, responsive et performance : [ux-copy-a11y-performance.md](references/ux-copy-a11y-performance.md).
- Opportunités, screener, classements, catalyseurs, alertes : [opportunity-center.md](references/opportunity-center.md).
- Analyse actions/ETF et dossiers : [analysis-center.md](references/analysis-center.md).
- Chaînes, volatilité, contrats et scénarios options : [options-center.md](references/options-center.md).
- Portefeuille, exposition, risque, watchlist et suivi : [portfolio-center.md](references/portfolio-center.md).
- Intelligence, assistant, comité, mémoire et audit trail : [ai-center.md](references/ai-center.md).
- Performance, journal, tracking, apprentissages : [performance-center.md](references/performance-center.md).
- Calendrier économique, résultats, dividendes, expirations, revues et alertes : [calendar-and-alerts.md](references/calendar-and-alerts.md).
- Données, IBKR, TradingView, WMB, news, jobs et santé : [data-and-integrations.md](references/data-and-integrations.md).
- Programme complet, lots et conditions de sortie : [delivery-program.md](references/delivery-program.md).
- Sources méthodologiques GitHub et principes retenus : [methodology-sources.md](references/methodology-sources.md).
- Contrôle final page, domaine et plateforme : [definition-of-done.md](references/definition-of-done.md).
- Revue exhaustive avant livraison : [audit-150.md](references/audit-150.md).

## Architecture fonctionnelle

La sidebar est organisée par travail, pas par architecture technique :

- **Piloter** : Aujourd'hui, Calendrier.
- **Explorer** : Marchés, Opportunités, Analyse, Options, Simulateur.
- **Gérer** : Portefeuille, Suivi, Performance.
- **Intelligence** : Vertex IA.
- **Utilitaire épinglé** : Système.

Alertes et recherche globale restent dans la topbar. Journal appartient à Performance. Watchlist appartient au Suivi/Portefeuille. Les détails sont des routes secondaires ou drawers avec deep links, jamais de nouvelles entrées de sidebar par défaut.

## Méthode de livraison

1. Partir du dernier `main`, relever CI/PR/SHA et ne pas baser le travail sur une ancienne branche de redesign.
2. Auditer le domaine et ses dépendances ; identifier le premier lot canonique non terminé.
3. Écrire le contrat visuel du lot : question, données consommées sans modification, hiérarchie, composants, états, responsive, tests et rollback.
4. Consolider uniquement le modèle de présentation et les composants visuels ; ne pas consolider le backend.
5. Développer l'expérience visuelle complète, y compris états réels et dégradés.
6. Vérifier que calculs, données et provenance sont inchangés, puis contrôler navigateur, responsive, clavier, console, performance et tests.
7. Livrer une PR brouillon cohérente avec preuves ; ne jamais fusionner automatiquement.

Pour une surface UI, appliquer quatre critiques avant livraison : test de permutation, test de hiérarchie à distance, test de signature sur cinq emplacements précis et test des tokens. Avant le lot d'acceptation, exécuter aussi les 150 contrôles de `references/audit-150.md` et joindre les preuves. Corriger avant de montrer.

## Définition de terminé

Vertex 2.0 visuel est terminé lorsque toutes les capacités existantes sont retrouvables dans une architecture cohérente, que chaque page répond à une question claire en cinq secondes, que les données et comportements sont strictement inchangés, que les états sont honnêtes, que desktop et mobile sont utilisables, et qu'aucune erreur navigateur ni régression de test n'est introduite.
