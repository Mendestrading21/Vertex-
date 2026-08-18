# Vertex 1.0 — Release gates

## G0 — Fondation

État : PASS au merge `bf49f9b49d5325a0f0264ad609264b020e06a7c2`.

Preuves : 3 247 tests, safety vert, runtime canonique, V4 activé, `/healthz` 200.

## G1 — Runtime modulaire

PASS lorsque factory Flask, routes, lifecycle/workers et scheduler ont un propriétaire modulaire, avec parité et sans double démarrage. `terminal.py` n'est plus le centre de nouvelles responsabilités.

## G2 — Données et domaines

PASS lorsque les doublons entreprise/data/portfolio sont convergés, les états de fraîcheur sont uniformes et la persistance/sauvegarde est prouvée.

## G3 — Intelligence

PASS lorsque le packet décisionnel est reproductible/versionné, WMB est ingéré avec provenance, les scénarios et probabilités sont étiquetés/calibrés et la mémoire des résultats est exploitable sans look-ahead.

## G4 — Expérience

PASS lorsqu'une seule couche de design est servie, les huit espaces sont validés desktop/mobile/clavier/contraste, `/api/client-log` est propre et aucune surface ne masque une donnée manquante ou périmée.

## G5 — Live read-only

PASS après test TWS/IB Gateway réel : connexion/reconnexion, market data, chaîne options, portefeuille et erreurs, avec preuve que l'API reste Read-Only et qu'aucun ordre n'est possible.

## G6 — Exploitation

PASS après audit secrets/dépendances, sauvegarde/restauration, observabilité, procédure d'installation, rollback testé et gouvernance de `main`.

## G7 — Release

`v1.0.0` uniquement lorsque G0–G6 sont PASS sur le même SHA candidat et acceptés humainement. Sinon le statut reste RC/NO-GO.
