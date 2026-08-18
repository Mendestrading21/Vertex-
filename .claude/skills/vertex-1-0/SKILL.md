---
name: vertex-1-0
description: Orchestrateur unique pour auditer, développer, valider et publier Vertex 1.0.
---

# ACTIVE_SKILL: vertex-1-0

Ce skill est la seule instruction active pour Claude Code dans ce dépôt.
Les anciens skills Skyler V2, Total Rebuild, V4 et Signal OS sont des archives
de recherche; ils ne définissent plus le produit.

## Mission

Construire un système institutionnel d'intelligence de marché et d'aide à la
décision, mesurable, explicable et strictement en lecture seule.

Vertex sert trois mandats distincts:

1. options longues tactiques, détenues typiquement 2/4/6 semaines, DTE préféré
   120–240 jours et cible 180 jours;
2. actions analysées aux horizons 3/6/12 mois;
3. WMB Brief quotidien comme contexte macro avec date et provenance.

## Sources de vérité

Lire dans cet ordre:

1. `CLAUDE.md`
2. `docs/vertex-1.0/README.md`
3. `docs/vertex-1.0/PRODUCT_CONTRACT.md`
4. `docs/vertex-1.0/ARCHITECTURE.md`
5. `vertex/strategy/profiles/vertex_strategy_v4.json`
6. le code et les tests du composant modifié

Un ancien document ne peut jamais contredire ces sources.

## Pipeline obligatoire

Sources réelles et horodatées
→ normalisation, qualité, fraîcheur et provenance
→ moteurs déterministes
→ packet de décision versionné et immuable
→ hard gates
→ scénarios, score et compatibilité portefeuille
→ décision canonique
→ explication IA
→ interface et audit.

## Limites de l'IA

Claude peut résumer, comparer, expliciter les contradictions, formuler une
thèse et rédiger l'explication finale. Claude ne peut jamais:

- inventer un prix, un Greek, une prime, une probabilité ou une source;
- modifier un score, un hard gate ou la décision canonique;
- transformer un signal TradingView ou WMB en ordre;
- rendre une donnée absente « conforme »;
- préparer ou transmettre un ordre;
- modifier automatiquement la constitution stratégique.

## Workflow obligatoire

1. **Préflight**
   - partir du dernier `main`;
   - créer une branche `agent/vertex-1-0-<sujet>`;
   - lire les contrats et identifier le propriétaire canonique de chaque donnée.
2. **Audit ciblé**
   - cartographier appels, endpoints, pages, tests et données touchés;
   - rechercher les doublons avant d'ajouter un nouveau module;
   - écrire le risque de régression et le plan de rollback.
3. **Implémentation**
   - une responsabilité par module;
   - conserver les adaptateurs de compatibilité jusqu'à preuve de non-usage;
   - aucune valeur financière silencieusement remplacée par zéro;
   - états `LIVE`, `DELAYED`, `STALE`, `DEMO`, `OFFLINE`, `MISSING` explicites.
4. **Validation**
   - `python -m compileall -q terminal.py vertex`;
   - `python -m pytest -q`;
   - `python -m pytest tests/test_no_orders.py -q`;
   - vérifier `/healthz`, `/api/client-log` et les huit espaces lorsque le
     changement touche le runtime ou l'interface;
   - documenter les limites non vérifiées.
5. **Publication**
   - commit intentionnel;
   - PR brouillon vers `main`;
   - résumé, preuves, risques, rollback et décisions humaines restantes;
   - ne jamais fusionner automatiquement.

## Règles d'architecture

- `python -m vertex` est l'entrée locale canonique.
- `vertex.runtime:app` est l'entrée WSGI canonique.
- `terminal.py` est un adaptateur historique à réduire progressivement, pas
  une destination pour de nouvelles fonctionnalités.
- `vertex.product` et le profil stratégique actif portent les horizons.
- un endpoint/métrique/page doit avoir un seul propriétaire canonique.
- les anciennes branches de lots ne sont jamais des bases de développement.

## Définition de terminé

Un changement n'est terminé que lorsque le code, les tests, les docs actives,
la provenance des données, le comportement dégradé et le rollback concordent.
Une suite verte n'autorise ni l'exécution d'ordres ni la promesse de rendement.
