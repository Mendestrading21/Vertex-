# SKYLER V2 — ACCEPTANCE CHECKLIST

## Règle

Un lot ne reçoit `GO` que si toutes les exigences critiques applicables sont prouvées.

## Git et périmètre

- [ ] branche différente de `main` ;
- [ ] branche issue de `integration/vertex-skyler-v2` ;
- [ ] worktree inspecté ;
- [ ] aucun fichier étranger au lot ;
- [ ] diff relu ;
- [ ] PR brouillon ;
- [ ] pas de merge automatique ;
- [ ] rollback décrit ;
- [ ] lot précédent validé humainement.

## Sécurité et READONLY

- [ ] `readonly=True` intact ;
- [ ] `tests/test_no_orders.py` vert ;
- [ ] aucun endpoint/bouton/appel d’ordre ;
- [ ] aucun secret ou runtime personnel dans le diff ;
- [ ] aucune donnée privée supplémentaire envoyée à l’IA ;
- [ ] packet externe filtré ;
- [ ] Claude ne peut modifier les champs canoniques.

## Données

- [ ] source et champ source explicites ;
- [ ] unité/devise/multiplicateur explicites ;
- [ ] période et timestamp réels ;
- [ ] fraîcheur cohérente ;
- [ ] absence distincte de zéro ;
- [ ] démo/simulé distincts du réel ;
- [ ] estimé distinct du broker ;
- [ ] stale/offline/missing/insufficient testés ;
- [ ] conflits visibles ;
- [ ] NaN/infini refusés ;
- [ ] aucune donnée future en backtest ;
- [ ] aucune donnée inventée.

## Calculs financiers

- [ ] défaut reproduit ;
- [ ] test rouge initial ;
- [ ] unités et conventions documentées ;
- [ ] cas manuel ;
- [ ] cas limites ;
- [ ] entrées invalides refusées ;
- [ ] test de non-régression ;
- [ ] API/UI alignées ;
- [ ] résultat extrême expliqué ;
- [ ] version moteur enregistrée ;
- [ ] déterminisme prouvé.

## Options

- [ ] IV typée ;
- [ ] prime/action et prime/contrat séparées ;
- [ ] multiplicateur/DTE/taux/dividende explicites ;
- [ ] bid/ask/spread/slippage présents lorsque requis ;
- [ ] max profit borné/illimité correct ;
- [ ] max loss borné/illimité correct ;
- [ ] breakevens testés ;
- [ ] PoP étiquetée avec modèle ;
- [ ] doublement distinct de PoP ;
- [ ] TACTICAL/SWING/LEAPS séparés ;
- [ ] stratégies hors mandat filtrées ;
- [ ] GEX/flow/max pain étiquetés comme inférences ;
- [ ] earnings/IV crush traité ;
- [ ] comparaison action/option/attendre ;
- [ ] scénario spot × temps × IV.

## Comité contradictoire

- [ ] sous-agents limités à leur domaine ;
- [ ] aucun sous-agent ne produit `final_decision` ;
- [ ] Président unique ;
- [ ] claims structurés avec sources/fraîcheur ;
- [ ] groupes de preuves indépendantes ;
- [ ] opinion minoritaire conservée ;
- [ ] avocat du diable exécuté ;
- [ ] veto data quality prioritaire ;
- [ ] dossier S/S+ red-teamé ;
- [ ] accord mesuré sans double-compter une source.

## Décision Skyler

- [ ] décision finale dans l’enum canonique ;
- [ ] état opérationnel séparé ;
- [ ] score ≤ 40 et niveau cohérent ;
- [ ] hard gates prioritaires ;
- [ ] pessimiste/probable/exceptionnel ;
- [ ] probabilités cohérentes ;
- [ ] EV calculée avec unités correctes ;
- [ ] invalidation et catalyseur explicites ;
- [ ] déclencheur explicite ;
- [ ] instrument préféré justifié ou aucun ;
- [ ] objection forte ;
- [ ] inconnues visibles ;
- [ ] confidence factors et plafonds ;
- [ ] audit trail ;
- [ ] réponse déterministe sans Claude ;
- [ ] texte Claude séparé du packet.

## Scénarios et calibration

- [ ] probabilités totalisent 100 % ;
- [ ] méthode et version enregistrées ;
- [ ] population historique comparable ;
- [ ] sample quality affichée ;
- [ ] aucun look-ahead ;
- [ ] seed/reproductibilité si simulation ;
- [ ] Brier/log loss/calibration disponibles lorsque pertinent ;
- [ ] résultats séparés par version ;
- [ ] décision historique immuable ;
- [ ] recalibration non automatique ;
- [ ] échantillon minimum respecté.

## Anomalies

- [ ] baseline appropriée ;
- [ ] magnitude/rareté/qualité documentées ;
- [ ] confirmations indépendantes ;
- [ ] persistance et cycle de vie ;
- [ ] faux positifs corporate actions contrôlés ;
- [ ] limites options/dealer visibles ;
- [ ] aucune anomalie seule ne produit une décision finale.

## SkylerPacket

- [ ] schéma versionné ;
- [ ] JSON round-trip ;
- [ ] enums validés ;
- [ ] timestamps UTC ;
- [ ] unités critiques présentes ;
- [ ] aucun NaN/infini ;
- [ ] probabilités valides ;
- [ ] hash d’entrée stable ;
- [ ] packet immuable après décision ;
- [ ] migration de version testée ;
- [ ] champs sensibles filtrés.

## Portefeuille

- [ ] impact marginal ;
- [ ] concentration après ajout ;
- [ ] corrélations/facteurs ;
- [ ] budget de risque ;
- [ ] quota options ;
- [ ] aucun renforcement perdant ;
- [ ] preuve de renforcement gagnant ;
- [ ] sizing plafonné ;
- [ ] stress après ajout ;
- [ ] exposition Greeks portefeuille ;
- [ ] provenance positions ;
- [ ] remplacement explicite si portefeuille plein.

## Backend

- [ ] `compileall` vert ;
- [ ] pytest complet vert ;
- [ ] routes/contrats testés ;
- [ ] erreurs structurées ;
- [ ] état partagé correct ;
- [ ] caches sans régression ;
- [ ] logs sans secret ;
- [ ] versioning moteurs ;
- [ ] performance mesurée si chemin critique.

## Frontend

- [ ] réponse visible rapidement ;
- [ ] une mission par page ;
- [ ] aucun doublon ;
- [ ] graphique utile ;
- [ ] titre/question/conclusion ;
- [ ] unité/période/source/fraîcheur ;
- [ ] états loading/empty/error/stale/demo/offline/insufficient ;
- [ ] données externes échappées ;
- [ ] faits/estimations/interprétations distincts ;
- [ ] 0 erreur console ;
- [ ] service worker bump si requis.

## Responsive et accessibilité

- [ ] 390/768/1440/1920 px ;
- [ ] aucun overflow critique ;
- [ ] navigation clavier ;
- [ ] focus visible ;
- [ ] reduced-motion ;
- [ ] contraste ;
- [ ] compréhension sans couleur ;
- [ ] résumé accessible des graphiques.

## Documentation

- [ ] rapport du lot ;
- [ ] fichiers et commandes exacts ;
- [ ] résultats exacts ;
- [ ] captures ;
- [ ] contradictions et opinion minoritaire ;
- [ ] risques restants ;
- [ ] statut mis à jour ;
- [ ] prochaine étape unique ;
- [ ] arrêt et validation humaine demandés.

## Verdict

### GO

Toutes les exigences critiques applicables sont satisfaites. Aucun risque connu ne rend le lot trompeur ou dangereux.

### GO AVEC RÉSERVES

Aucune erreur critique, mais une limite documentée subsiste sans altérer calculs, intégrité ou sécurité.

### NO-GO

Utiliser notamment si : test critique rouge, calcul non prouvé, risque illimité masqué, donnée inventée, source/fraîcheur trompeuse, chemin d’ordre, secret exposé, décision S/S+ sans red-team, packet invalide, look-ahead, probabilité sans modèle, périmètre mélangé ou lot précédent non validé.
