# Protocole d'exécution Claude

## Démarrage

1. Charger le skill maître et les références du mode.
2. Lire `CLAUDE.md`, état Git, dernier `main`, PR ouvertes, CI et décisions
   récentes liées au périmètre.
3. Refuser une ancienne branche comme base sans preuve qu'elle est canonique.
4. Exécuter la baseline en lecture seule et publier les constats avant écriture.
5. Sélectionner un seul lot non terminé.

## Contrat de lot

Écrire avant modification : objectif, non-objectifs, propriétaires, données,
invariants, fichiers prévus, migration, risques, tests, budgets, captures et
rollback. Une découverte élargissant significativement le lot provoque une
pause et un nouveau contrat.

## Implémentation

- test rouge pour un défaut reproductible ;
- correction minimale dans le propriétaire le plus bas ;
- adaptateur temporaire seulement avec date/condition de retrait ;
- pas de logique financière dans template/JS de présentation ;
- pas de nouvelle source, bibliothèque ou schéma sans contrat dédié ;
- préserver les changements utilisateur et ne pas nettoyer hors périmètre.

## Page par page

Pour chaque page modifiée :

1. capture avant au même état de données ;
2. mission, question et inventaire des fonctions ;
3. desktop 1600, tablette 1024, mobile 390 ;
4. loading, empty, partial, delayed, stale, offline, demo et error applicables ;
5. interactions, clavier, focus, zoom et reduced motion ;
6. console, réseau, `/api/client-log`, `/healthz` et routes consommées ;
7. capture après, comparaison et liste de ce qui reste ;
8. accord utilisateur possible avant la page suivante en mode interactif.

## Revue et PR

Relire le diff depuis zéro : sécurité, données, logique, performance, UI et
tests. Lancer contrôles ciblés puis suite complète. Documenter résultats exacts,
skips, limites non vérifiées, métriques avant/après et rollback. Ouvrir une PR
brouillon ; aucune fusion, déploiement ou suppression distante automatique.

## Arrêts obligatoires

Stopper sur secret, donnée de compte IBKR, migration ambiguë, store utilisateur
non sauvegardé, formule financière non spécifiée, permission nouvelle,
dépendance externe non auditée, tests de vérité rouges, cible destructive
incertaine ou conflit avec une modification utilisateur.
