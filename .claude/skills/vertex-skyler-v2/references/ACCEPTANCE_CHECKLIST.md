# SKYLER V2 — ACCEPTANCE CHECKLIST

## Règle

Un lot ne peut recevoir `GO` que si toutes les lignes obligatoires applicables sont prouvées.

## Git et périmètre

- [ ] branche différente de `main` ;
- [ ] branche du lot issue de `integration/vertex-skyler-v2` ;
- [ ] worktree inspecté avant modification ;
- [ ] aucun fichier étranger au lot ;
- [ ] diff relu ;
- [ ] PR brouillon ;
- [ ] pas de merge automatique ;
- [ ] rollback décrit.

## Sécurité et READONLY

- [ ] `readonly=True` intact ;
- [ ] `tests/test_no_orders.py` vert ;
- [ ] aucun endpoint d’ordre ;
- [ ] aucun bouton d’exécution ;
- [ ] aucun appel d’ordre dans le code Vertex ;
- [ ] aucun secret dans le diff ;
- [ ] aucun fichier runtime personnel dans le diff ;
- [ ] aucune donnée privée supplémentaire envoyée à l’IA.

## Données

- [ ] sources explicites ;
- [ ] unités explicites ;
- [ ] périodes explicites ;
- [ ] fraîcheur réelle ;
- [ ] timestamps cohérents ;
- [ ] absence distincte de zéro ;
- [ ] démo distincte de réel ;
- [ ] estimé distinct de broker ;
- [ ] stale/offline/missing/insufficient testés ;
- [ ] conflits de sources visibles ;
- [ ] aucune donnée inventée.

## Calculs financiers

- [ ] défaut reproduit avant correction ;
- [ ] test rouge initial ;
- [ ] unité documentée ;
- [ ] convention documentée ;
- [ ] cas manuel ;
- [ ] cas limite ;
- [ ] NaN/inf refusés ;
- [ ] entrées invalides refusées ;
- [ ] test de non-régression ;
- [ ] API/UI alignées ;
- [ ] résultat extrême expliqué.

## Options

- [ ] IV typée ;
- [ ] prime/action et prime/contrat séparées ;
- [ ] multiplicateur explicite ;
- [ ] DTE explicite ;
- [ ] taux/dividende documentés ;
- [ ] bid/ask/spread présents si liquidité analysée ;
- [ ] max profit borné/illimité correct ;
- [ ] max loss borné/illimité correct ;
- [ ] breakevens testés ;
- [ ] PoP étiquetée avec modèle ;
- [ ] doublement distinct de PoP ;
- [ ] TACTICAL/SWING/LEAPS séparés ;
- [ ] stratégies hors mandat filtrées ;
- [ ] GEX/dealer présenté comme inférence ;
- [ ] earnings/IV crush traité si pertinent.

## Décision Skyler

- [ ] décision unique canonique ;
- [ ] score total = 40 maximum ;
- [ ] niveau cohérent ;
- [ ] hard gates prioritaires ;
- [ ] pessimiste/probable/exceptionnel ;
- [ ] probabilités validées ;
- [ ] invalidation explicite ;
- [ ] catalyseur explicite ;
- [ ] objection forte ;
- [ ] inconnues visibles ;
- [ ] audit trail ;
- [ ] réponse déterministe sans Claude ;
- [ ] Claude ne modifie aucun chiffre.

## Portefeuille

- [ ] impact marginal calculé ;
- [ ] concentration après ajout ;
- [ ] corrélation/facteurs ;
- [ ] budget de risque ;
- [ ] quota options ;
- [ ] aucun renforcement perdant ;
- [ ] preuve de renforcement gagnant ;
- [ ] sizing plafonné ;
- [ ] stress après ajout ;
- [ ] provenance des positions.

## Backend

- [ ] `compileall` vert ;
- [ ] pytest complet vert ;
- [ ] routes concernées testées ;
- [ ] contrats API testés ;
- [ ] erreurs structurées ;
- [ ] état partagé non réassigné incorrectement ;
- [ ] absence de régression de cache ;
- [ ] logs sans secret.

## Frontend

- [ ] réponse visible rapidement ;
- [ ] une mission par page ;
- [ ] aucun doublon ;
- [ ] graphique utile ;
- [ ] titre/question/conclusion ;
- [ ] unité/période/source/fraîcheur ;
- [ ] loading/empty/error/stale/demo/offline/insufficient ;
- [ ] données externes échappées ;
- [ ] 0 erreur console ;
- [ ] service worker bump si requis.

## Responsive et accessibilité

- [ ] 390 px ;
- [ ] 768 px ;
- [ ] 1440 px ;
- [ ] 1920 px ;
- [ ] aucun overflow critique ;
- [ ] navigation clavier ;
- [ ] focus visible ;
- [ ] reduced-motion ;
- [ ] contraste ;
- [ ] signification sans couleur ;
- [ ] résumé accessible des graphiques.

## Documentation

- [ ] rapport du lot ;
- [ ] fichiers modifiés listés ;
- [ ] commandes exactes ;
- [ ] résultats exacts ;
- [ ] captures référencées ;
- [ ] risques restants ;
- [ ] statut mis à jour ;
- [ ] prochaine étape unique ;
- [ ] arrêt et validation humaine demandés.

## Verdict

### GO

Toutes les exigences critiques applicables sont satisfaites. Aucun risque connu ne rend le lot trompeur ou dangereux.

### GO AVEC RÉSERVES

Aucune erreur critique, mais une limite clairement documentée subsiste. Elle ne doit pas altérer les calculs, l’intégrité ou la sécurité.

### NO-GO

Utiliser si :

- test critique rouge ;
- calcul non prouvé ;
- risque illimité masqué ;
- donnée inventée ;
- source/fraîcheur trompeuse ;
- chemin d’ordre ;
- secret exposé ;
- overflow/console bloquant ;
- périmètre mélangé ;
- lot précédent non validé.
