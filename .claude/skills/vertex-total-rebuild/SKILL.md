---
name: vertex-total-rebuild
description: Refonte complète de Vertex, page par page, fichier par fichier et graphique par graphique, en préservant les moteurs financiers, les données réelles, les tests et IBKR READONLY.
---

# VERTEX TOTAL REBUILD

## Mission

Tu es l'architecte produit, frontend, data-visualization et qualité de Vertex. Tu ne dois pas ajouter une couche visuelle supplémentaire. Tu dois comprendre l'existant, supprimer les contradictions, simplifier l'expérience puis reconstruire le produit de manière cohérente.

Principe central :

> Une page = une mission. Une section = une question. Un graphique = une conclusion exploitable.

## Philosophie d'investissement à intégrer

Vertex doit refléter la stratégie suivante sans jamais inventer une recommandation :

- rechercher une asymétrie forte ;
- perdre peu lorsque la thèse échoue ;
- gagner beaucoup lorsque la thèse est correcte ;
- distinguer bonne entreprise, bonne action et bon timing ;
- présenter scénario pessimiste, probable et exceptionnel ;
- mesurer risque maximum, catalyseur 90 jours, invalidation et potentiel ;
- privilégier les tendances de 1 à 24 mois ;
- renforcer uniquement après validation du marché ;
- ne jamais renforcer une position perdante ;
- réserver la concentration aux opportunités réellement exceptionnelles ;
- pour les LEAPS : delta 0,70 à 0,90, échéance 6 à 18 mois, OI élevé, spread faible.

Niveaux analytiques :

- S+ : score 36–40, allocation indicative 10–15 % maximum ;
- S : score 32–35, allocation indicative 7–10 % ;
- A : score 28–31, allocation indicative 3–5 % ;
- B : allocation indicative 1–2 %.

Ces allocations sont des repères analytiques, jamais des ordres automatiques.

## Invariants absolus

1. IBKR reste strictement READONLY.
2. Aucun chemin d'exécution d'ordre ne doit exister.
3. Toute donnée affiche source, unité, période et fraîcheur.
4. Une donnée absente reste indisponible ; elle n'est jamais remplacée par zéro sans justification.
5. Les moteurs financiers restent la source de vérité.
6. Toute modification de calcul exige un test démontrant le problème et la correction.
7. Le mode démo, le mode sans IBKR et les états périmés doivent fonctionner.
8. Aucun lot n'est terminé avec des tests rouges, une erreur console ou un débordement responsive.

## Interdictions

- Ne pas créer un nouveau thème par-dessus les anciens.
- Ne pas ajouter un graphique uniquement parce qu'il est esthétique.
- Ne pas afficher deux graphiques répondant à la même question.
- Ne pas multiplier donuts, radars et jauges.
- Ne pas créer de palette locale par page.
- Ne pas construire de gros blocs HTML par concaténation JavaScript.
- Ne pas mélanger récupération de données, logique métier et rendu.
- Ne pas supprimer un fichier avant vérification des imports, routes, tests et références.
- Ne pas déclarer une page terminée sans test navigateur réel.

## Direction visuelle

Identité unique : **VERTEX OBSIDIAN — Institutional Intelligence System**.

Le produit doit être sombre, calme, institutionnel, précis et premium. Il ne doit ressembler ni à un casino crypto, ni à un dashboard SaaS générique, ni à une collection de widgets.

Palette sémantique :

- obsidienne et graphite pour les surfaces ;
- ivoire pour le texte principal ;
- gris sable pour le secondaire ;
- cuivre pour l'identité, la sélection et l'action principale ;
- émeraude pour un résultat financier positif ;
- corail pour une perte ou un risque ;
- ambre pour un avertissement ;
- violet désaturé pour options et volatilité ;
- neutre pour les données descriptives.

Une hausse n'est pas automatiquement verte et une baisse n'est pas automatiquement rouge. La couleur dépend du sens financier réel.

## Références visuelles

Avant toute refonte, inspecter tous les dossiers ou fichiers contenant : `reference`, `references`, `moodboard`, `inspiration`, `design`, `screenshots`, `assets`.

Créer `docs/refactor/VISUAL_REFERENCE_MAP.md` avec :

- fichier ;
- éléments utiles ;
- éléments à ne pas copier ;
- page Vertex concernée ;
- composant ou interaction à adapter.

Ne jamais copier aveuglément. Extraire hiérarchie, densité, espacements, interactions, cartes, tableaux et qualité graphique, puis les adapter à Vertex.

## Phase 0 — Baseline

Avant toute modification :

- confirmer la branche ;
- exécuter tous les tests ;
- relever le nombre exact de tests ;
- lancer Vertex en mode démo ;
- relever toutes les routes ;
- relever erreurs console, réseau et Python ;
- prendre des captures desktop, laptop, tablette et mobile ;
- créer `docs/refactor/VERTEX_BASELINE_AUDIT.md`.

## Phase 1 — Inventaire exhaustif

Inspecter tous les fichiers suivis par Git.

Créer `docs/refactor/FILE_INVENTORY.md` avec, pour chaque fichier significatif : rôle, page, moteur, imports, dépendances, statut actif/legacy/doublon/mort potentiel, action proposée et niveau de risque.

Rechercher routes, graphiques, styles inline, HTML injecté, palettes locales, TODO, FIXME, legacy, deprecated, old, backup, v2, v3 et v4.

## Phase 2 — Cartographie et contradictions

Créer `docs/refactor/PAGE_DATA_GRAPH_MATRIX.md`.

Pour chaque page : route, mission, question principale, endpoints, moteurs, composants, graphiques, tableaux, actions, états vides, erreurs, fraîcheur, doublons et priorité.

Créer `docs/refactor/CONTRADICTIONS_REGISTER.md`.

Rechercher :

- scores différents pour un même titre ;
- verdicts divergents ;
- définitions différentes du régime de marché ;
- calculs différents du reward/risk ;
- unités incohérentes ;
- coûts actions/options mal normalisés ;
- heure d'affichage utilisée comme fraîcheur ;
- mêmes métriques provenant de plusieurs endpoints ;
- périodes différentes non indiquées ;
- couleurs positives/négatives sans sens financier.

Pour chaque contradiction : identifier les sources, choisir la source canonique, documenter, corriger et tester.

## Architecture informationnelle cible

Limiter Vertex à huit espaces :

1. Aujourd'hui — état du marché, alertes, opportunités et actions prioritaires.
2. Marchés — indices, breadth, secteurs, macro, cross-asset, volatilité.
3. Opportunités — screener, ranking, watchlist, catalyseurs, comparaison.
4. Analyse — synthèse titre, technique, fondamentaux, scorecard, scénarios, risques.
5. Portefeuille — positions, allocation, concentration, risque, performance, sorties.
6. Options — positions, LEAPS, stratégies, payoff, volatilité et Greeks.
7. Journal — décisions, hypothèses, erreurs, statistiques et apprentissage.
8. Système — IBKR, fraîcheur, moteurs, diagnostics, paramètres, design system.

Aucun nouvel espace principal ne peut être ajouté sans fusion ou suppression justifiée.

## Hiérarchie obligatoire de chaque page

Niveau 1 — Réponse : que se passe-t-il, importance, confiance, risque et prochaine action analytique.

Niveau 2 — Justification : facteurs, graphiques essentiels, scénarios, catalyseurs et invalidations.

Niveau 3 — Expertise : données brutes, méthodologie, diagnostics et métriques avancées dans des panneaux dépliables.

Limites par vue initiale : un message principal, quatre KPI, trois graphiques majeurs, trois alertes, trois actions et un tableau principal maximum.

## Audit de tous les graphiques

Créer `docs/refactor/CHART_INVENTORY.md`.

Pour chaque graphique : identifiant, fichier, page, titre, type, données, endpoint, unité, période, question, conclusion, source, fraîcheur, interactions, mobile, doublons, contradictions et décision garder/modifier/fusionner/remplacer/supprimer.

Un graphique doit répondre à ces questions :

1. Quelle question précise résout-il ?
2. Un KPI ou une phrase suffirait-il ?
3. Est-il redondant ?
4. La période et les unités sont-elles explicites ?
5. La couleur a-t-elle un sens ?
6. Peut-il induire une mauvaise décision ?
7. Fonctionne-t-il avec peu de données et sur mobile ?
8. Sa conclusion est-elle expliquée ?

## Grammaire graphique officielle

- courbe : évolution temporelle ;
- chandeliers : OHLC, volume, moyennes et niveaux ;
- barres horizontales : classement et comparaison précise ;
- barres divergentes : positif/négatif ou risk-on/risk-off ;
- waterfall : attribution et décomposition de score ;
- heatmap : matrices et corrélations ;
- scatter : risque contre potentiel, score contre valorisation ;
- donut : composition simple de 3 à 5 catégories seulement ;
- radar : une fois maximum par vue et accompagné de valeurs ;
- jauge : métrique réellement bornée uniquement ;
- funnel : étapes successives réelles ;
- payoff options : spot, zéro, breakevens, gain/perte max, zones de profit/perte et hypothèses.

Chaque graphique utilise un shell commun : titre, question, conclusion, période, source, fraîcheur, aide, état vide, erreur, skeleton, légende et résumé accessible.

## Reconstruction page par page

Ordre obligatoire :

1. Aujourd'hui ;
2. Marchés ;
3. Opportunités ;
4. Analyse titre ;
5. Portefeuille ;
6. Options ;
7. Journal ;
8. Système.

Pour chaque page : constater, définir la mission, supprimer les répétitions, choisir la source canonique, reconstruire la hiérarchie, reconstruire les graphiques, tester desktop/mobile et documenter.

La fiche titre doit montrer en premier : verdict, score /40, niveau, confiance, prix, entrée, invalidation, scénario pessimiste, probable, exceptionnel, asymétrie et catalyseur 90 jours.

La page Options doit montrer d'abord : stratégie, biais, coût, gain/perte max, breakevens, PoP, rendement/risque, échéance, delta et theta. Gamma, vega, vanna et vomma restent dans un niveau expert.

## Frontend

Créer une couche unique de composants réutilisables pour cartes, KPI, badges, boutons, tableaux, états, scénarios, positions, stratégies et graphiques.

Séparer chargement, normalisation, état, logique de vue, rendu, événements et graphiques.

Réduire les styles inline et interdire les gros blocs HTML concaténés. Toute donnée externe doit être échappée.

## Architecture Python

Réduire progressivement `terminal.py` et converger vers :

- `vertex/app` pour factory et configuration ;
- `vertex/api` par domaine ;
- `vertex/services` pour IBKR, quotes, fraîcheur, fondamentaux et IA ;
- `vertex/engines` pour scoring, marché, risque, options et recherche ;
- `vertex/ui` pour layouts, pages et composants ;
- `vertex/static/js` pour core, components, charts et pages.

Pas de migration big-bang.

## Responsive et accessibilité

Tester au minimum 390×844, 768×1024, 1024×768, 1366×768, 1440×900 et 1920×1080.

Vérifier : aucun débordement, focus visible, clavier, contraste, reduced-motion, tooltips, zones tactiles, résumés textuels des graphiques et compréhension sans couleur.

## Stratégie de livraison

Découper en PR indépendantes :

1. audit et cartographie ;
2. design system et chart system ;
3. navigation et architecture des pages ;
4. Aujourd'hui et Marchés ;
5. Opportunités et Analyse ;
6. Portefeuille ;
7. Options ;
8. Journal et Système ;
9. nettoyage, performance, accessibilité et documentation.

Chaque PR doit être compréhensible, testée et réversible.

## Validation obligatoire

Après chaque lot :

- tests Python et JavaScript disponibles ;
- tests des routes ;
- vérification READONLY ;
- mode démo ;
- mode sans IBKR ;
- données manquantes et périmées ;
- console ;
- responsive ;
- clavier ;
- unités ;
- dates ;
- sources.

Créer `docs/refactor/validation/PR-XX.md` avec changements, fichiers, tests, captures, erreurs restantes, décisions, risques et prochaine étape.

## Format de compte rendu obligatoire

Pour chaque étape :

- Constat ;
- Problème ;
- Décision ;
- Implémentation ;
- Validation ;
- Reste à faire.

Ne jamais répondre seulement « terminé ».

## Première mission

Commencer uniquement par les phases 0, 1 et 2.

À la fin, fournir : résultats des tests, pages, graphiques, endpoints, moteurs, contradictions critiques, doublons, fichiers legacy potentiels, références visuelles trouvées, graphiques à supprimer/fusionner/reconstruire et plan détaillé de la PR suivante.
