# Agent — Trading Engine

## Mission

Garantir que Vertex traduit correctement la stratégie d’investissement de l’utilisateur en analyse structurée, sans transformer des préférences en ordres automatiques ni en promesses de performance.

## Cadre d’analyse

Chaque opportunité doit présenter :

- qualité de l’entreprise ;
- qualité de l’action au prix actuel ;
- qualité du timing ;
- tendance ;
- catalyseur 90 jours ;
- accumulation institutionnelle si mesurable ;
- confirmation graphique ;
- risque maximum ;
- invalidation ;
- scénario pessimiste ;
- scénario probable ;
- scénario exceptionnel ;
- asymétrie ;
- horizon ;
- fraîcheur et qualité des données.

## Niveaux

- S+ : 36–40, opportunité exceptionnelle ;
- S : 32–35, très forte conviction ;
- A : 28–31, opportunité valide ;
- B : position expérimentale ou surveillance.

Les allocations associées sont indicatives et ne doivent jamais déclencher d’action.

## Règles de risque

- ne jamais renforcer automatiquement une perte ;
- distinguer invalidation de volatilité normale ;
- renforcer seulement après confirmation documentée ;
- afficher clairement la perte théorique maximale ;
- signaler les concentrations et corrélations ;
- séparer résultat réalisé, latent, estimé et simulé.

## Règles gagnants

L’interface doit aider à réévaluer les gagnants sans sortie automatique :

- +20 % : surveillance normale ;
- +30 % : révision du stop ou de l’invalidation ;
- +50 % : conservation par défaut si la thèse reste intacte ;
- +75 % : réévaluation complète ;
- +100 % : possibilité de sécurisation partielle, jamais obligation automatique.

## LEAPS

Présenter :

- delta ;
- échéance ;
- open interest ;
- spread ;
- IV ;
- theta ;
- catalyseur ;
- tendance du sous-jacent ;
- scénario prix/temps/volatilité ;
- coût total ;
- perte maximale ;
- liquidité.

Profil recherché à signaler, pas à imposer : delta 0,70–0,90, échéance 6–18 mois, OI élevé, spread faible.

## Contradictions à empêcher

- score élevé avec scénario défavorable non expliqué ;
- verdict achat avec asymétrie médiocre ;
- potentiel exceptionnel inférieur au probable ;
- stop supérieur au prix d’entrée pour une position longue ;
- mélange entre prix par action et coût total ;
- confiance élevée avec données périmées ;
- PoP affichée sans IV ou modèle valide.

## Modification des moteurs

Toute modification exige :

1. preuve du défaut ;
2. test rouge reproduisant le défaut ;
3. correction minimale ;
4. tests de non-régression ;
5. documentation des hypothèses.

## Invariant

Aucun code d’exécution d’ordre. IBKR reste strictement READONLY.