---
name: vertex-2-0
description: Piloter l'audit, la consolidation et le développement complet de Vertex comme centre de trading IA en lecture seule, en réutilisant toutes les capacités existantes et en faisant converger produit, données, moteurs, portefeuille, options, opportunités, interface et qualité.
---

# Vertex 2.0 — Centre de trading IA

## Mission

Transformer le dépôt existant en une plateforme personnelle complète d'intelligence de marché et d'aide à la décision. Vertex doit relier les données réelles, les moteurs déterministes, l'analyse actions/ETF/options, les opportunités, le portefeuille, le risque, la performance, le suivi et l'explication IA dans une expérience unique, cohérente et auditable.

Ce skill est l'orchestrateur racine. Pour toute demande globale, lancer uniquement `/vertex-2-0`. Il charge les autorités spécialisées selon le lot :

- `.claude/skills/vertex-1-0/SKILL.md` pour données, moteurs, stratégie, sécurité et release ;
- `.claude/skills/vertex-design-2-0/SKILL.md` pour architecture des pages, UX, composants, graphiques et identité visuelle.

En cas de conflit : sécurité et lecture seule → vérité financière → contrats de données et moteurs → produit → design.

## Boucle produit

**OBSERVER → COMPRENDRE → DÉTECTER → ÉVALUER → DÉCIDER → SURVEILLER → MESURER → APPRENDRE.**

Chaque moteur, page, tableau, graphique et texte IA doit servir explicitement une étape. Une fonctionnalité sans place dans cette boucle est fusionnée, déplacée ou supprimée après preuve qu'elle n'a plus de consommateur.

## Invariants absolus

- Vertex reste `READONLY=True` et `ANALYSIS_ONLY=True` ; IBKR reste `readonly=True`.
- Aucun ordre, ticket broker, bouton achat/vente, transmission ou automatisation d'exécution.
- L'IA explique et relie les faits ; elle ne calcule ni ne modifie prix, Greeks, score, scénario, risque, sizing, hard gate ou verdict canonique.
- Aucune donnée, source, fraîcheur, courbe ou performance inventée. L'absence est affichée honnêtement.
- Les positions IBKR, positions déclarées, idées suivies, simulations et signaux théoriques restent séparés.
- Toute décision conserve faits, sources, timestamps, qualité, contradictions, scénarios, invalidation, version des moteurs et limites.
- Les fonctionnalités existantes sont inventoriées et consolidées avant tout ajout parallèle.

## Règle « tout ce qui existe déjà »

Avant chaque chantier, cartographier routes, modules, moteurs, services, jobs, stores, endpoints, composants, tests et documents liés. Produire ou mettre à jour un registre de capacités indiquant : propriétaire canonique, entrées, sorties, consommateurs, état réel, doublons, dette, données manquantes et décision conserver/fusionner/migrer/retirer.

Ne jamais repartir de zéro si une capacité saine existe. Ne jamais garder deux propriétaires actifs pour le même score, cache, route, widget, chaîne d'options ou registre de portefeuille.

Lire [platform-architecture.md](references/platform-architecture.md) pour la carte cible et [capability-convergence.md](references/capability-convergence.md) pour la méthode d'inventaire.

## Routage des domaines

- Opportunités, screener, classements, catalyseurs, alertes : [opportunity-center.md](references/opportunity-center.md).
- Analyse actions/ETF et dossiers : [analysis-center.md](references/analysis-center.md).
- Chaînes, volatilité, contrats et scénarios options : [options-center.md](references/options-center.md).
- Portefeuille, exposition, risque, watchlist et suivi : [portfolio-center.md](references/portfolio-center.md).
- Intelligence, assistant, comité, mémoire et audit trail : [ai-center.md](references/ai-center.md).
- Performance, journal, tracking, apprentissages : [performance-center.md](references/performance-center.md).
- Calendrier économique, résultats, dividendes, expirations, revues et alertes : [calendar-and-alerts.md](references/calendar-and-alerts.md).
- Données, IBKR, TradingView, WMB, news, jobs et santé : [data-and-integrations.md](references/data-and-integrations.md).
- Programme complet, lots et conditions de sortie : [delivery-program.md](references/delivery-program.md).
- Pour toute interface, charger aussi `vertex-design-2-0` et seulement ses références pertinentes.

## Architecture fonctionnelle

1. **Aujourd'hui** synthétise le contexte, les risques, les opportunités et les éléments à revoir.
2. **Marchés** explique le régime macro et cross-asset.
3. **Opportunités** détecte et classe ce qui mérite une analyse.
4. **Analyse** construit le dossier canonique actions/ETF/options.
5. **Portefeuille** relie positions, thèses, exposition, risque et actions de surveillance.
6. **Options** explore chaînes, volatilité, contrats et scénarios.
7. **Performance** mesure trades, signaux, suivi et apprentissages sans les confondre.
8. **Intelligence** rend le raisonnement, les contradictions, la mémoire et la recherche auditables.
9. **Système** prouve la santé des sources, intégrations, jobs, sécurité et préférences.

Journal, watchlist, calendrier, alertes, tracking et détails sont des surfaces transversales rattachées à un propriétaire clair. Le Calendrier possède une vue plein écran accessible globalement, mais ne duplique pas les calendriers spécialisés de Marchés, Options ou Portefeuille : il les agrège avec filtres et liens vers leurs propriétaires.

## Méthode de livraison

1. Partir du dernier `main`, relever CI/PR/SHA et ne pas baser le travail sur une ancienne branche de redesign.
2. Auditer le domaine et ses dépendances ; identifier le premier lot canonique non terminé.
3. Écrire le contrat du lot : question, propriétaire, entrées, sorties, états, consommateurs, budget, tests, rollback.
4. Consolider backend et modèle de présentation avant la page si les données sont fragmentées.
5. Développer l'expérience complète, y compris états réels et dégradés.
6. Vérifier calculs, provenance, navigateur, responsive, clavier, console, performance et tests.
7. Livrer une PR brouillon cohérente avec preuves ; ne jamais fusionner automatiquement.

## Définition de terminé

Vertex 2.0 n'est pas terminé parce que toutes les pages existent. Il est terminé lorsqu'une idée peut traverser la boucle complète — observation, détection, dossier, décision canonique, impact portefeuille, suivi et mesure — avec données réelles, provenance, états honnêtes, aucun doublon actif, aucune erreur navigateur et aucune capacité d'exécution d'ordre.
