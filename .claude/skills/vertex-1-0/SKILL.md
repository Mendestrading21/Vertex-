---
name: vertex-1-0
description: Orchestrateur unique pour auditer, développer, valider et publier Vertex 1.0.
---

# ACTIVE_SKILL: vertex-1-0

Ce skill est la seule instruction active pour Claude Code dans ce dépôt.

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
8. `docs/vertex-1.0/audits/AUDIT-TOTAL-2026-08-24.md` pour tout chantier post-RC ;
9. `docs/vertex-1.0/roadmap/VERTEX-INTELLIGENCE-2.0.md` pour l'ordre des lots post-RC ;
10. code et tests du composant modifié.

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
- supprimer un actif legacy sans respecter `CLEANUP_POLICY.md`.

## Workflow

1. Partir du dernier `main`, relever le SHA et créer `agent/vertex-1-0-<sujet>`.
2. Exécuter la baseline et lire l'issue ciblée.
3. Cartographier propriétaires, consommateurs, routes, tests, caches et données touchés.
4. Chercher les doublons avant d'ajouter du code.
5. Implémenter avec adaptateur/rollback si une interface existante change.
6. Appliquer `QUALITY_STANDARD.md`.
7. Valider `compileall`, pytest complet et `tests/test_no_orders.py`.
8. Si runtime/UI : `/healthz`, `/api/client-log`, huit espaces, desktop/mobile et modes dégradés.
9. Ouvrir une PR brouillon avec preuves, risques, rollback et limites ; ne jamais fusionner automatiquement.

## Programme post-RC

Pour toute demande d'amélioration globale, de nouvelle source, d'API, de
stratégie, d'intelligence options, de portefeuille, de news ou de recherche :

1. lire `docs/vertex-1.0/roadmap/SOURCES-APIS-OPEN-SOURCE.md` ;
2. choisir le premier lot non terminé dont les dépendances sont satisfaites ;
3. ne jamais ouvrir plusieurs lots dépendants en parallèle ;
4. utiliser un store point-in-time avant toute nouvelle preuve historique ;
5. garder tout profil V5 candidat inactif jusqu'à décision humaine.

Le nombre de fonctionnalités n'est pas une preuve de qualité. Aucune nouvelle
source ou stratégie n'est terminée sans contrat de données, replay, état
dégradé, validation hors échantillon et attribution.

## Règles Git

- `main` = seule ligne de release ;
- une PR cohérente par chantier ;
- anciennes branches = sources historiques uniquement ;
- aucune nouvelle branche d'intégration permanente ;
- aucune preuve provenant d'un autre SHA.

## Définition de terminé

Le changement satisfait le Quality Standard et le release gate concerné. Une suite verte ne suffit pas à autoriser un tag final, un ordre ou une promesse de rendement.
