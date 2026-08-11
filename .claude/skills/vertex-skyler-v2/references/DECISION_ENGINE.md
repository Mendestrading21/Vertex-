# SKYLER V2 — MOTEUR DE DÉCISION INSTITUTIONNEL

## 1. Objet

Ce document définit comment Skyler transforme des faits vérifiés en une décision analytique unique, traçable et réversible.

Skyler ne cherche pas à avoir raison sur chaque mouvement. Il cherche à :

- engager peu de capital lorsque l’incertitude domine ;
- engager davantage seulement lorsque l’asymétrie, les preuves et le timing convergent ;
- perdre peu lorsque la thèse est invalidée ;
- conserver assez longtemps les rares positions capables de produire une année exceptionnelle.

La décision ne vient jamais d’un prompt libre. Elle vient d’un pipeline déterministe, puis Claude explique le résultat.

## 2. Vocabulaire canonique

### 2.1 Décisions finales

Le moteur final conserve exactement le vocabulaire constitutionnel :

- `ACHETER`
- `RENFORCER`
- `ATTENDRE`
- `REDUIRE`
- `REFUSER`

Aucun analyste spécialisé, aucune page et aucun modèle linguistique ne peut créer un autre verdict final.

### 2.2 États opérationnels analytiques

Les états suivants peuvent préciser le contexte sans devenir des décisions finales :

- `SURVEILLER`
- `PREPARER`
- `DECLENCHEMENT_CONDITIONNEL`
- `CONFIRMATION_REQUISE`
- `SECURISATION_PARTIELLE`
- `RUNNER`
- `THESE_A_REEVALUER`
- `DONNEES_INSUFFISANTES`

Exemple :

```json
{
  "final_decision": "ATTENDRE",
  "operational_state": "DECLENCHEMENT_CONDITIONNEL",
  "trigger": "clôture au-dessus de la résistance avec volume supérieur à 1,5x"
}
```

## 3. Hiérarchie des preuves

Chaque affirmation appartient à un niveau précis.

### Niveau F1 — Fait primaire

Donnée directement observée et sourcée : prix IBKR, volume, résultats publiés, guidance, open interest, date de publication.

### Niveau F2 — Métrique dérivée

Calcul déterministe depuis des faits primaires : RSI, ATR, croissance, marge, reward/risk, Greeks, GEX.

### Niveau F3 — Estimation de modèle

Probabilité, expected move, scénario Monte Carlo, probabilité de doublement, estimation de volatilité future.

### Niveau F4 — Interprétation

Lecture analytique : accumulation probable, leadership, compression, catalyseur potentiellement sous-évalué.

Règles :

1. Une interprétation F4 ne peut jamais être affichée comme un fait F1.
2. Une décision S ou S+ ne peut pas reposer principalement sur F4.
3. Toute estimation F3 affiche modèle, hypothèses, date et intervalle d’incertitude.
4. Une contradiction entre deux faits F1 ne peut pas être résolue par une interprétation F4.

## 4. Pipeline de décision

Ordre obligatoire :

1. **Validation des données** — présence, unité, fraîcheur, cohérence des sources.
2. **Régime de marché** — environnement autorisant ou limitant le nouveau risque.
3. **Qualité de l’entreprise** — croissance, rentabilité, bilan, moat, révisions.
4. **Catalyseurs** — événement, horizon, nouveauté, crédibilité, potentiel de surprise.
5. **Technique et timing** — tendance, niveau d’entrée, invalidation, extension, confirmation.
6. **Institutions et anomalies** — volume, flux, relative strength, options, positionnement.
7. **Asymétrie** — pessimiste, probable, exceptionnel, expected value, R:R.
8. **Instrument** — action, call, put ou aucune exposition.
9. **Compatibilité portefeuille** — concentration, corrélation, budget de risque, remplacement.
10. **Avocat du diable** — objection adverse la plus forte.
11. **Décision finale** — un seul verdict, avec raisons et conditions.
12. **Audit trail** — données, versions des moteurs, règles appliquées et inconnues.

L’ordre ne peut pas être inversé pour justifier un contrat d’option séduisant sur une mauvaise thèse de sous-jacent.

## 5. Score /40 et décision

Le score mesure la qualité du dossier, pas l’autorisation d’acheter.

### 5.1 Blocs

- fondamentaux : 0–5 ;
- catalyseurs : 0–5 ;
- technique/timing : 0–6 ;
- institutions/anomalies : 0–4 ;
- régime/secteur : 0–4 ;
- asymétrie/scénarios : 0–6 ;
- option : 0–6 ;
- données : 0–4.

### 5.2 Niveaux

- S+ : 36–40 ;
- S : 32–35 ;
- A : 28–31 ;
- B : 24–27 ;
- inférieur à 24 : refus ou surveillance.

### 5.3 Règle fondamentale

```text
score élevé + hard gate actif = pas d’achat
```

Un score de 38/40 avec une invalidation absente ou des données critiques périmées doit rester `ATTENDRE` ou `REFUSER`.

## 6. Hard gates

Les hard gates sont déterministes, codés, testés et audités.

### Données

- donnée critique absente ;
- unité ambiguë ;
- source contradictoire non réconciliée ;
- donnée trop périmée pour l’horizon ;
- mode démo présenté comme réel.

### Thèse

- aucune raison claire de battre le marché ;
- catalyseur non identifiable ;
- scénario probable défavorable ;
- invalidation absente ;
- thèse déjà cassée.

### Asymétrie

- R:R structurel inférieur à 2:1 ;
- expected value négative ;
- scénario exceptionnel inférieur ou égal au scénario probable ;
- perte pessimiste supérieure au budget de risque ;
- hypothèses incompatibles entre elles.

### Options

- DTE hors mandat ;
- spread trop large ;
- OI ou liquidité insuffisants ;
- perte illimitée non signalée ;
- IV inconnue pour un calcul qui la requiert ;
- stratégie interdite par la Constitution ;
- contrat ne survivant pas au scénario pessimiste réaliste ;
- risque earnings/IV crush non traité.

### Portefeuille

- renforcement d’une position perdante ;
- concentration au-delà du plafond ;
- corrélation excessive ;
- quota options dépassé ;
- drawdown portefeuille bloquant ;
- absence de budget de risque disponible.

## 7. Confiance

La confiance ne doit pas être la moyenne des scores.

Elle dépend de :

- complétude des données ;
- fraîcheur ;
- qualité des sources ;
- accord entre analystes ;
- stabilité du résultat aux hypothèses ;
- calibration historique du moteur dans ce régime ;
- nombre et gravité des contradictions ;
- dépendance à une seule hypothèse.

Forme recommandée :

```text
confidence = base_quality × agreement × robustness × calibration
```

Chaque facteur est borné entre 0 et 1. Le détail est conservé dans l’audit trail.

Plafonds :

- donnée critique estimée : confiance maximale 70 % ;
- régime `UNKNOWN` : confiance maximale 55 % ;
- contradiction majeure non résolue : confiance maximale 50 % ;
- catalyseur binaire proche : confiance réduite selon l’incertitude événementielle.

## 8. Matrice instrument

### Action

Préférer l’action lorsque :

- horizon long ;
- volatilité implicite chère ;
- timing moins précis ;
- besoin de survivre à plusieurs catalyseurs ;
- dividendes ou structure du capital importants ;
- probabilité de doublement de l’option trop faible.

### Call long

Préférer un call lorsque :

- biais haussier confirmé ;
- catalyseur et horizon identifiables ;
- perte maximale acceptable ;
- liquidité suffisante ;
- delta/DTE compatibles ;
- scénario probable couvre le coût et le theta ;
- scénario exceptionnel produit une convexité réellement supérieure à l’action.

### Put long

Préférer un put uniquement lorsque :

- thèse baissière rare mais claire ;
- catalyseur négatif crédible ;
- tendance et institutions confirment ;
- IV et skew ne rendent pas le contrat excessivement cher ;
- risque de rebond violent documenté.

### Attendre

`ATTENDRE` est une décision active lorsque :

- le prix est poursuivi ;
- la cassure n’est pas confirmée ;
- les résultats sont trop proches ;
- l’IV est anormalement chère ;
- le portefeuille est plein ;
- les preuves sont bonnes mais le timing mauvais.

## 9. Renforcement

`RENFORCER` exige simultanément :

- position en gain ou au minimum thèse validée sans détérioration ;
- nouveau fait positif depuis l’entrée ;
- confirmation technique ;
- risque total encore acceptable ;
- nouvelle asymétrie calculée depuis le prix actuel ;
- absence de concentration bloquante.

Un prix inférieur n’est jamais une raison suffisante.

## 10. Gestion des gagnants

Le moteur ne vend pas automatiquement à cause d’un pourcentage de gain.

Il réévalue :

- thèse ;
- valorisation ;
- catalyseurs restants ;
- tendance ;
- accélération institutionnelle ;
- concentration ;
- risque événementiel ;
- asymétrie depuis le cours actuel.

États analytiques :

- +20 % : suivi normal ;
- +30 % : révision invalidation/stop ;
- +50 % : conservation par défaut si thèse intacte ;
- +75 % : réévaluation complète ;
- +100 % : sécurisation partielle possible, runner conservé si asymétrie restante.

## 11. Contradictions

Le moteur produit un registre explicite :

```json
{
  "code": "FUNDAMENTAL_TECHNICAL_CONFLICT",
  "severity": "MAJOR",
  "positive_evidence": ["révisions EPS en hausse"],
  "negative_evidence": ["tendance sous MM200"],
  "resolution": "ATTENDRE_CONFIRMATION",
  "confidence_cap": 0.60
}
```

Types minimum :

- fondamental vs technique ;
- catalyseur vs valorisation ;
- prix vs volume ;
- action vs options ;
- marché vs secteur ;
- score vs scénario ;
- confiance vs qualité des données ;
- recommandation vs portefeuille ;
- sources divergentes.

## 12. Sortie canonique

Toute décision contient :

- symbole ;
- date et fraîcheur ;
- décision finale ;
- état opérationnel ;
- score /40 et niveau ;
- confiance et facteurs ;
- thèse en une phrase ;
- pourquoi maintenant ;
- catalyseur ;
- déclencheur ;
- invalidation ;
- scénarios ;
- expected value ;
- instrument préféré et raisons ;
- risque maximum ;
- compatibilité portefeuille ;
- objection adverse la plus forte ;
- inconnues ;
- conditions de réévaluation ;
- audit trail.

## 13. Tests obligatoires

- un hard gate bloque un score S+ ;
- une position perdante ne peut jamais recevoir `RENFORCER` ;
- une donnée périmée plafonne la confiance ;
- les probabilités des scénarios sont cohérentes ;
- un R:R inférieur à 2 bloque `ACHETER` ;
- une contradiction majeure apparaît dans la sortie ;
- la même entrée produit la même décision ;
- l’absence de Claude produit toujours une décision déterministe ;
- le texte Claude ne peut modifier aucun champ canonique ;
- tout changement de règle met à jour la version du moteur de décision.
