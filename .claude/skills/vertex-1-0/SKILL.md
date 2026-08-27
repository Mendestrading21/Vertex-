---
name: vertex-1-0
description: Orchestrateur unique pour auditer, développer, valider et publier Vertex 1.0 puis Vertex Intelligence 2.0, page par page, sans exécution d'ordre.
---

# ACTIVE_SKILL: vertex-1-0

Ce skill est l'autorité spécialisée pour le produit, les données, les moteurs, la sécurité et la release. Il est orchestré par `.claude/skills/vertex-2-0/SKILL.md`. Pour toute interface, page, navigation, widget, tableau, graphique, typographie ou refonte visuelle, l'orchestrateur charge aussi `vertex-design-2-0`, qui hérite de tous les invariants ci-dessous.

## Mission

Faire converger Vertex vers un système institutionnel d'intelligence de marché et d'aide à la décision, mesurable, explicable, sobre et strictement en lecture seule.

Mandats :

1. options longues tactiques, revues 2/4/6 semaines, DTE préféré 120–240 jours, cible 180 ;
2. actions aux horizons 3/6/12 mois ;
3. WMB Brief quotidien comme contexte macro daté et sourcé.

## Sources de vérité

Lire dans cet ordre :

1. `CLAUDE.md` ;
2. `docs/vertex-1.0/README.md` ;
3. `docs/vertex-1.0/PRODUCT_CONTRACT.md` ;
4. `docs/vertex-1.0/QUALITY_STANDARD.md` ;
5. `docs/vertex-1.0/ARCHITECTURE.md` ;
6. `docs/vertex-1.0/RELEASE_GATES.md` ;
7. `vertex/strategy/release_profiles/vertex_strategy_v4.json` ;
8. `docs/vertex-1.0/audits/AUDIT-TOTAL-2026-08-25.md` pour les risques, pages et priorités actuels ;
9. `docs/vertex-1.0/audits/AUDIT-TOTAL-2026-08-24.md` pour la preuve RC antérieure ;
10. `docs/vertex-1.0/roadmap/VERTEX-INTELLIGENCE-2.0.md` pour l'ordre des lots post-RC ;
11. `docs/vertex-1.0/roadmap/SOURCES-APIS-OPEN-SOURCE.md` et `USER-REPOSITORIES-2026-08-25.md` avant toute source ou dépendance ;
12. code, migrations et tests du composant modifié.

## Pipeline obligatoire

sources réelles et horodatées → normalisation/provenance/fraîcheur → moteurs déterministes → packet versionné → hard gates → scénarios/score/portefeuille → décision canonique → explication IA → UI/journal/audit.

## Interdictions absolues

- inventer prix, Greek, prime, probabilité ou source ;
- modifier un score, hard gate ou verdict depuis l'IA ;
- transformer TradingView ou WMB en ordre ;
- rendre une donnée absente conforme ;
- préparer ou transmettre un ordre ;
- ajouter une nouvelle doctrine, architecture parallèle ou couche de thème ;
- ajouter une nouvelle fonctionnalité métier dans `terminal.py` ;
- effectuer une collecte réseau lourde dans le chemin synchrone d'une page ;
- créer un second propriétaire d'une route, d'un score, d'un cache ou d'un registre ;
- copier ou importer un bot, un moteur d'exécution ou un MCP capable d'agir sur IBKR ;
- supprimer un actif legacy sans respecter `CLEANUP_POLICY.md`.

## Workflow

1. Relever le SHA, l'état CI, les PR ouvertes et la pile de dépendances avant de choisir une base.
2. Continuer le premier lot canonique non terminé ; ne jamais recréer un lot déjà ouvert.
3. Exécuter la baseline et écrire le contrat du lot : problème mesuré, propriétaire, entrées, sorties, budgets et témoins négatifs.
4. Cartographier producteurs, consommateurs, routes, jobs, tests, caches, persistance et données touchés.
5. Chercher doublons et chemins legacy ; choisir un propriétaire unique avant d'ajouter du code.
6. Implémenter derrière modèle Vertex canonique, feature flag, migration et rollback si une frontière change.
7. Appliquer `QUALITY_STANDARD.md`, puis compiler, tester et mesurer sur le même SHA.
8. Si data/provider : contrat, licence, entitlement, replay, point-in-time, timeout, pacing et panne partielle.
9. Si runtime/UI : `/healthz`, `/api/client-log`, budgets p95, huit espaces, desktop/mobile/clavier et états loading/empty/stale/offline/error.
10. Ouvrir ou mettre à jour une PR brouillon avec preuves, risques, rollback et limites ; ne jamais fusionner automatiquement.

## Programme post-RC

Pour toute demande d'amélioration globale, de nouvelle source, d'API, de
stratégie, d'intelligence options, de portefeuille, de news ou de recherche :

1. lire `docs/vertex-1.0/roadmap/SOURCES-APIS-OPEN-SOURCE.md` et la matrice des dépôts utilisateur ;
2. choisir le premier lot non terminé dont les dépendances sont satisfaites ;
3. ne jamais ouvrir plusieurs lots dépendants en parallèle ;
4. utiliser un store point-in-time avant toute nouvelle preuve historique ;
5. garder tout profil V5 candidat inactif jusqu'à décision humaine.

Le nombre de fonctionnalités n'est pas une preuve de qualité. Aucune nouvelle
source ou stratégie n'est terminée sans contrat de données, replay, état
dégradé, validation hors échantillon et attribution.

## Contrats produit V2

- actions : thèse et scénarios 3/6/12 mois ;
- ETF : holdings point-in-time, look-through, overlap, liquidité, tracking et frais ;
- options : risque borné, DTE préféré 120–240 jours, cible 180, revues 2/4/6 semaines ;
- TradingView : contexte/alerte seulement, jamais source canonique ni ordre ;
- IBKR : cotations/chaînes/positions/P&L en lecture seule, avec source du mark et réconciliation ;
- IA : narration sourcée depuis un packet immuable, jamais calculateur ou décideur.

Pour une page, partir de sa question définie dans l'audit du 25 août. Réduire
les doublons avant d'ajouter un onglet. `Intelligence` et `Tracking` restent des
surfaces secondaires tant qu'un propriétaire produit unique n'est pas arbitré.

## Règles Git

- `main` = seule ligne de release ;
- une PR cohérente par chantier ;
- anciennes branches = sources historiques uniquement ;
- aucune nouvelle branche d'intégration permanente ;
- aucune preuve provenant d'un autre SHA.

## Définition de terminé

Le changement satisfait le Quality Standard et le release gate concerné. Une suite verte ne suffit pas à autoriser un tag final, un ordre ou une promesse de rendement.
