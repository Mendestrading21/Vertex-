# SKYLER V2 — COMITÉ D’INVESTISSEMENT CONTRADICTOIRE

## 1. Mission

Le comité Skyler empêche une seule narration séduisante de dominer la décision.

Chaque analyste travaille sur un domaine limité, produit des preuves structurées et expose ses inconnues. Aucun analyste spécialisé ne peut publier la décision finale.

Le Président Skyler synthétise les avis, applique les hard gates, conserve les opinions minoritaires et produit une décision canonique unique.

## 2. Composition du comité

### A1 — Market Regime Analyst

Analyse :

- indices ;
- breadth ;
- VIX et structure à terme ;
- volatilité réalisée ;
- taux et courbe ;
- dollar ;
- crédit ;
- liquidité ;
- cross-asset ;
- transition de régime.

Il répond : le marché autorise-t-il un nouveau risque, et quel type de setup est favorisé ?

### A2 — Sector & Leadership Analyst

Analyse :

- force relative sectorielle ;
- rotation ;
- dispersion ;
- participation ;
- leadership ;
- comparaison industrie/secteur/indice.

Il répond : le titre est-il porté par une tendance collective ou isolé ?

### A3 — Fundamental Quality Analyst

Analyse :

- croissance ;
- marges ;
- free cash-flow ;
- bilan ;
- dette ;
- qualité des bénéfices ;
- moat ;
- valorisation ;
- comparaison historique et sectorielle.

Il distingue bonne entreprise, bonne action et bon prix.

### A4 — Catalyst & Revisions Analyst

Analyse :

- résultats ;
- guidance ;
- révisions EPS/CA ;
- lancements ;
- réglementation ;
- contrats ;
- M&A ;
- buybacks ;
- événements sectoriels ;
- horizon 30/90/180 jours.

Il ne note jamais un catalyseur seulement parce qu’une date existe.

### A5 — Technical Timing Analyst

Analyse :

- tendance multi-horizons ;
- structure de prix ;
- moyennes ;
- momentum ;
- ATR ;
- extension ;
- supports/résistances ;
- cassure, pullback, invalidation ;
- volume et confirmation.

Il répond : pourquoi maintenant, à quel niveau, avec quelle invalidation ?

### A6 — Institutional & Anomaly Analyst

Analyse :

- relative strength ;
- volume anormal ;
- accumulation/distribution ;
- gaps ;
- divergences ;
- flux options ;
- short interest ;
- anomalies fondamentales et news ;
- persistance du signal.

Il doit séparer donnée certaine, proxy et hypothèse.

### A7 — Options & Volatility Analyst

Analyse :

- chaîne ;
- liquidité ;
- delta/gamma/theta/vega ;
- vanna/vomma/charm ;
- IV rank et percentile ;
- skew ;
- term structure ;
- expected move ;
- GEX ;
- walls ;
- zero gamma ;
- scénarios spot × temps × IV ;
- risque d’IV crush ;
- probabilité de doublement.

Il peut conclure qu’aucune option n’est adaptée même si le sous-jacent est intéressant.

### A8 — Portfolio & Risk Analyst

Analyse :

- concentration ;
- corrélation ;
- exposition sectorielle ;
- bêta ;
- drawdown ;
- budget de risque ;
- nombre de lignes ;
- remplacement ;
- compatibilité S+/S/A/B ;
- stress tests.

Il répond : le portefeuille peut-il absorber ce risque maintenant ?

### A9 — Data Quality Auditor

Analyse :

- source ;
- unité ;
- fraîcheur ;
- complétude ;
- cohérence ;
- mode démo ;
- valeurs estimées ;
- divergences entre endpoints ;
- NaN/infini/default silencieux.

Il possède un droit de veto lorsque les données critiques sont insuffisantes.

### A10 — Behavioral Discipline Analyst

Analyse :

- poursuite du prix ;
- renforcement perdant ;
- surconfiance ;
- fréquence excessive ;
- concentration émotionnelle ;
- incohérence avec le journal ;
- erreurs récurrentes ;
- respect des règles gagnants/perdants.

Il répond : cette décision est-elle rationnelle ou influencée par un biais comportemental détectable ?

### A11 — Devil’s Advocate

Mission unique : construire le meilleur dossier opposé.

Il doit répondre :

- pourquoi la thèse peut être fausse ;
- quelle donnée positive est déjà intégrée ;
- quel catalyseur peut décevoir ;
- quel risque n’est pas suffisamment rémunéré ;
- quelle corrélation cachée peut invalider l’analyse ;
- quel scénario extrême est sous-estimé ;
- quelle preuve ferait changer immédiatement la décision.

Il ne cherche pas à être négatif. Il cherche à éviter une conviction fragile.

### A12 — Skyler Chair

Le Président :

- reçoit les preuves ;
- élimine les doublons ;
- résout ou expose les contradictions ;
- applique les hard gates ;
- construit les scénarios ;
- choisit action/call/put/attendre ;
- consulte le portefeuille ;
- conserve l’opinion minoritaire ;
- produit le verdict final ;
- écrit l’audit trail.

## 3. Contrat de preuve

Chaque analyste retourne uniquement une structure du type :

```json
{
  "analyst": "OPTIONS_VOLATILITY",
  "as_of": "2026-08-05T07:00:00Z",
  "status": "COMPLETE",
  "claims": [
    {
      "id": "opt-iv-001",
      "statement": "l’IV est supérieure à sa médiane 1 an",
      "polarity": "NEGATIVE",
      "strength": 0.72,
      "confidence": 0.88,
      "evidence_level": "F2",
      "sources": ["IBKR_OPTIONS_CHAIN"],
      "freshness": "LIVE",
      "estimated": false
    }
  ],
  "unknowns": [],
  "blocking_findings": [],
  "recommended_followups": []
}
```

Interdictions :

- pas de verdict final ;
- pas d’allocation ;
- pas d’ordre ;
- pas de chiffre absent des sources ;
- pas de confiance à 100 % ;
- pas de disparition silencieuse d’une contradiction.

## 4. Agrégation

Les preuves sont agrégées par domaine et non par simple vote majoritaire.

Une majorité d’analystes positifs ne peut pas annuler :

- un veto de qualité des données ;
- une perte illimitée ;
- une invalidation absente ;
- une concentration bloquante ;
- une thèse cassée ;
- un R:R insuffisant.

Les poids peuvent varier selon le régime, mais doivent être versionnés et testés.

Exemples :

- en `TREND_UP`, technique et leadership gagnent du poids ;
- en `CHOP`, momentum perd du poids et asymétrie/mean reversion gagnent du poids ;
- en `RISK_OFF`, risque, bilan et liquidité dominent ;
- avant résultats, catalyseur, IV et historique de réaction gagnent du poids.

## 5. Mesure de l’accord

L’accord ne se limite pas au nombre de verdicts.

Mesurer :

- accord directionnel ;
- accord sur l’horizon ;
- accord sur le catalyseur ;
- accord sur l’invalidation ;
- accord sur le risque ;
- accord sur l’instrument ;
- dispersion des confiances ;
- dépendance à une même source.

Un comité peut sembler unanime parce que tous les analystes utilisent la même donnée. Ce n’est pas une indépendance réelle.

## 6. Opinion minoritaire

La sortie finale conserve obligatoirement :

- l’objection la plus forte ;
- l’analyste minoritaire le plus crédible ;
- la donnée qui ferait changer la décision ;
- le risque non résolu ;
- la prochaine vérification requise.

## 7. Modes de comité

### Fast Review

Pour le Briefing : faits essentiels, hard gates, changement depuis la session précédente.

### Full Review

Pour une nouvelle opportunité : tous les analystes, scénarios, instrument, portefeuille.

### Position Review

Pour une position existante : thèse depuis l’entrée, nouveau fait, gagnant/perdant, renforcement/réduction.

### Event Review

Avant/après résultats ou catalyseur : expected move, IV crush, scénarios événementiels.

### Post-Mortem

Après clôture : décision, exécution hypothétique, résultat, erreur de modèle, erreur de discipline.

## 8. Red-team obligatoire S/S+

Tout dossier S ou S+ doit subir une passe red-team indépendante.

Questions minimum :

1. Qu’est-ce qui est déjà dans le prix ?
2. Quel chiffre peut être trompeur ?
3. Quelle hypothèse unique porte trop de poids ?
4. Que se passe-t-il si le catalyseur est retardé de 90 jours ?
5. Que se passe-t-il si l’IV baisse de 10 points ?
6. Que se passe-t-il si le marché passe risk-off ?
7. Le portefeuille possède-t-il déjà la même exposition cachée ?
8. Pourquoi l’option est-elle meilleure que l’action ?
9. Quel est le chemin plausible vers la perte maximale ?
10. Quelle preuve invalide immédiatement la note S/S+ ?

Une note S+ sans red-team complétée est invalide.

## 9. Tests obligatoires

- aucun sous-agent ne peut produire `final_decision` ;
- le Président est l’unique producteur du verdict canonique ;
- un veto data quality bloque la décision ;
- l’opinion minoritaire est conservée ;
- le même paquet de preuves produit la même synthèse ;
- les poids de régime sont versionnés ;
- une source unique répliquée n’augmente pas artificiellement l’accord ;
- un dossier S/S+ sans red-team est refusé ;
- les claims sans source ou fraîcheur échouent à la validation.
