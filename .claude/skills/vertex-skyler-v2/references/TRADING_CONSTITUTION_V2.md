# SKYLER V2 — TRADING CONSTITUTION

## Philosophie

L’objectif n’est pas d’avoir raison souvent.

L’objectif est :

- gagner beaucoup lorsque la thèse est correcte ;
- perdre peu lorsqu’elle est incorrecte ;
- refuser les asymétries médiocres ;
- réserver la taille aux rares opportunités exceptionnelles.

## Questions obligatoires avant validation

1. Pourquoi l’entreprise peut-elle battre le marché ?
2. Pourquoi maintenant ?
3. Quel catalyseur existe dans les 90 prochains jours ?
4. Existe-t-il des signes d’accumulation institutionnelle ?
5. Le prix confirme-t-il la thèse ?
6. Quelle est la perte maximale réaliste ?
7. Quel événement invalide la thèse ?
8. Quel est le scénario pessimiste ?
9. Quel est le scénario probable ?
10. Quel est le scénario exceptionnel ?
11. Le trade est-il compatible avec le portefeuille ?
12. Pour une option directionnelle, le doublement est-il raisonnablement possible ?

## Niveaux et allocation analytique

| Niveau | Score | Allocation maximale indicative |
|---|---:|---:|
| S+ | 36–40 | 10–15 % |
| S | 32–35 | 7–10 % |
| A | 28–31 | 3–5 % |
| B | 24–27 | 1–2 % |
| Refus/Watch | <24 | 0 % nouvelle exposition |

Contraintes :

- l’allocation est plafonnée par le budget de risque ;
- la concentration existante peut réduire l’allocation à zéro ;
- une qualité de données insuffisante peut plafonner à `ATTENDRE` ;
- le score ne déclenche jamais un ordre ;
- un S+ n’est possible que si les blocs critiques sont disponibles et cohérents.

## Portefeuille

- cible : 8 à 15 lignes ;
- pas de 40 à 50 petites positions sans impact ;
- concentration autorisée seulement avec données, probabilités et risque explicites ;
- aucune nouvelle position ne doit créer une dépendance excessive à un secteur, facteur ou catalyseur unique ;
- toute nouvelle position doit montrer son impact marginal sur le portefeuille.

## Règles de renforcement

Interdit :

- renforcer parce que le prix a baissé ;
- renforcer pour réduire artificiellement le prix moyen ;
- renforcer une thèse invalidée ;
- renforcer sans nouveau fait confirmant.

Autorisé seulement après :

- cassure confirmée ;
- retest réussi ;
- résultats supérieurs et guidance solide ;
- révisions positives ;
- amélioration du régime ou du secteur ;
- hausse de la qualité de la thèse ;
- amélioration mesurable du reward/risk.

Le moteur doit enregistrer la preuve de renforcement.

## Gestion des gagnants

- +20 % : aucune vente automatique ;
- +30 % : réévaluation du risque et de l’invalidation ;
- +50 % : conserver si thèse et asymétrie restent valides ;
- +75 % : revue complète ;
- +100 % : ne pas sortir automatiquement.

Sécurisation indicative :

- vendre 25 à 50 % ;
- conserver un runner ;
- adapter selon la liquidité, le catalyseur, la résistance, le temps restant et la convexité.

Une règle de gain ne peut jamais remplacer une analyse de thèse.

## Scénarios

Pour chaque opportunité :

### Pessimiste

- événement déclencheur ;
- probabilité ;
- cible ;
- perte action ;
- perte option ;
- invalidation ;
- vitesse possible du mouvement.

### Probable

- hypothèse centrale ;
- probabilité ;
- cible ;
- rendement ;
- catalyseur ;
- horizon.

### Exceptionnel

- catalyseur non linéaire ;
- probabilité ;
- cible ;
- potentiel ;
- conditions nécessaires ;
- risques de surchauffe.

Les probabilités doivent être calibrées, datées et attribuées à un modèle.

## Reward/Risk

Hard gate minimal :

```text
Reward/Risk structurel >= 2.0
```

Un ratio élevé construit sur une cible arbitraire est invalide.

Le moteur doit montrer :

- méthode de cible ;
- prix d’invalidation ;
- distance au stop ;
- coûts et slippage ;
- horizon ;
- scénario source.

## LEAPS

Profil principal :

- call long ;
- 180 à 540 DTE ;
- delta 0,70 à 0,90 ;
- open interest élevé ;
- spread faible ;
- liquidité suffisante ;
- catalyseur et tendance ;
- temps utilisé pour survivre aux fluctuations, pas comme justification unique.

Une option LEAPS doit être refusée si :

- spread ou OI insuffisant ;
- prime non fiable ;
- perte maximale incompatible ;
- delta hors mandat sans justification ;
- catalyseur absent ;
- tendance non confirmée ;
- probabilité de doublement trop faible selon le modèle actif ;
- IV anormalement chère sans scénario justifiant la convexité ;
- earnings/IV crush non modélisé lorsque pertinent.

## Puts

Les puts longs sont autorisés de manière rare et tactique lorsque :

- régime ou structure clairement baissiers ;
- catalyseur baissier identifié ;
- timing confirmé ;
- asymétrie forte ;
- spread/OI corrects ;
- risque explicite.

Aucune option vendeuse n’est autorisée par défaut dans le profil d’investissement. Les stratégies vendeuses peuvent rester disponibles dans un laboratoire d’analyse uniquement, clairement étiquetées comme hors mandat.

## Hard gates

Décision maximale `ATTENDRE` ou `REFUSER` en présence de :

- données critiques manquantes ;
- sources en conflit ;
- R:R <2 ;
- invalidation absente ;
- régime inconnu si le risque nouveau est bloqué ;
- thèse cassée ;
- renforcement d’un perdant ;
- concentration excessive ;
- quota options dépassé ;
- risque théorique illimité non signalé ;
- liquidité insuffisante ;
- modèle non calibré présenté comme certitude.

## Vocabulaire final

Décisions autorisées :

- `ACHETER`
- `RENFORCER`
- `ATTENDRE`
- `REDUIRE`
- `REFUSER`

Les sous-moteurs peuvent produire des observations, jamais une décision finale concurrente.
