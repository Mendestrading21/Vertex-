# SKYLER V2 — INTELLIGENCE DES ANOMALIES

## 1. Mission

Une anomalie n’est pas automatiquement une opportunité. Elle signale qu’un comportement sort de son régime normal et mérite une enquête.

Skyler doit détecter, classer, confirmer et suivre les anomalies sans transformer un seul signal en recommandation.

Pipeline :

```text
observation anormale → contrôle qualité → contexte → confirmation → persistance → impact sur scénarios → décision éventuelle
```

## 2. Contrat d’anomalie

Chaque anomalie contient :

```json
{
  "anomaly_id": "NVDA:OPTIONS:2026-08-05:001",
  "symbol": "NVDA",
  "domain": "OPTIONS",
  "code": "CALL_OI_CONCENTRATION",
  "observed": 2.8,
  "expected": 1.0,
  "unit": "x_baseline",
  "severity": 78,
  "confidence": 0.82,
  "direction": "BULLISH_PROXY",
  "evidence_level": "F2",
  "source": "IBKR",
  "as_of": "2026-08-05T07:30:00Z",
  "freshness": "LIVE",
  "persistence": 3,
  "confirmed_by": ["PRICE", "VOLUME"],
  "contradicted_by": [],
  "limitations": ["dealer side unknown"]
}
```

## 3. Domaines

### 3.1 Marché

- rupture breadth/prix ;
- VIX contre tendance ;
- inversion ou détente rapide des taux ;
- widening crédit ;
- dispersion extrême ;
- concentration excessive de l’indice ;
- cross-asset incohérent ;
- transition de régime.

### 3.2 Secteur

- force relative inhabituelle ;
- rotation accélérée ;
- breadth sectorielle divergente ;
- leadership très concentré ;
- décorrélation secteur/indice ;
- flux ETF anormal lorsque disponible.

### 3.3 Action — prix et volume

- rendement z-score ;
- gap significatif ;
- mouvement en multiples d’ATR ;
- nouveau plus-haut/bas ;
- volume anormal ;
- dry-up ;
- accumulation/distribution ;
- rejet de niveau ;
- reconquête/perte de moyenne ;
- divergence momentum ;
- compression/expansion de volatilité ;
- décorrélation avec secteur/benchmark.

### 3.4 Fondamentaux

- révision EPS/CA anormale ;
- surprise de marge ;
- divergence bénéfice/cash-flow ;
- croissance avec dégradation du bilan ;
- changement de guidance ;
- valorisation hors distribution historique ;
- insider activity lorsque sourcée ;
- changement brutal de consensus.

### 3.5 Actualités et catalyseurs

- événement réellement nouveau ;
- plusieurs sources indépendantes ;
- contradiction entre titre et contenu ;
- intensité médiatique sans mouvement de prix ;
- mouvement de prix sans news identifiable ;
- impact sectoriel diffus ;
- retard ou avancement de calendrier ;
- langage de guidance inhabituel.

### 3.6 Options

- volume/OI anormal ;
- concentration de strikes ;
- changement de skew ;
- déplacement de term structure ;
- IV vs realized vol ;
- GEX flip ;
- call/put wall ;
- Vanna/Charm extrêmes ;
- expected move divergent de l’historique ;
- spread dégradé ;
- flow répété ;
- divergence option/sous-jacent.

### 3.7 Portefeuille

- concentration croissante ;
- corrélation cachée ;
- bêta ou duration implicite anormale ;
- exposition thématique dupliquée ;
- drawdown synchronisé ;
- P&L dominé par une seule ligne ;
- theta ou vega portefeuille excessif ;
- liquidité insuffisante en stress.

## 4. Baseline adaptative

Une anomalie doit être mesurée contre une référence appropriée :

- historique du titre ;
- historique du secteur ;
- régime actuel ;
- heure de séance ;
- jour de semaine ;
- proximité des résultats ;
- DTE ;
- liquidité habituelle ;
- taille et prix du titre.

Éviter les seuils universels lorsque le comportement normal diffère fortement.

Exemple : un RVOL de 2x peut être banal le jour des résultats mais exceptionnel sans catalyseur.

## 5. Score d’anomalie

Le score ne représente pas une probabilité de hausse.

Composantes possibles :

- magnitude ;
- rareté ;
- fraîcheur ;
- persistance ;
- confirmations indépendantes ;
- qualité des données ;
- importance financière ;
- proximité d’un catalyseur ;
- contradictions.

Forme indicative :

```text
anomaly_score = magnitude × rarity × quality × persistence × confirmation
```

Le score est borné 0–100 et versionné.

## 6. Confirmation

Une anomalie devient exploitable seulement si au moins une preuve indépendante la confirme ou si sa magnitude dépasse un seuil critique documenté.

Exemples :

- volume + cassure + force secteur ;
- révisions + hausse de marge + relative strength ;
- call flow + hausse OI + sous-jacent confirmant ;
- GEX négatif + rupture support + vol réalisée en expansion.

Une confirmation provenant du même endpoint ou du même calcul ne compte pas comme indépendante.

## 7. Persistance et cycle de vie

États :

- `NEW`
- `UNCONFIRMED`
- `CONFIRMED`
- `PERSISTENT`
- `FADING`
- `RESOLVED`
- `INVALIDATED`

Chaque mise à jour conserve l’historique. Une anomalie résolue ne disparaît pas du journal de décision.

## 8. Faux positifs à contrôler

- split ;
- dividende ;
- changement de contrat ;
- expiration options ;
- données partielles ;
- faible liquidité ;
- holiday/half-day ;
- effet résultats ;
- rééquilibrage indice/ETF ;
- changement de symbole ;
- erreur de devise ;
- duplication de news ;
- variation d’OI non finalisée intraday.

## 9. Interprétation options

Le côté dealer réel est souvent inconnu. Par conséquent :

- GEX reste une convention ;
- flow call n’est pas automatiquement haussier ;
- volume sans OI ne prouve pas l’ouverture ;
- max pain n’est pas une cible garantie ;
- wall n’est pas un support/résistance certain ;
- Vanna/Charm sont des sensibilités estimées ;
- IV élevée peut refléter un risque réel, pas une erreur de prix.

Chaque sortie affiche ces limites.

## 10. Impact sur la décision

Une anomalie peut :

- augmenter la priorité de surveillance ;
- créer une question de recherche ;
- renforcer ou affaiblir un scénario ;
- déclencher une confirmation requise ;
- plafonner la confiance ;
- activer un hard gate ;
- modifier le choix de l’instrument ;
- provoquer une réévaluation d’une position.

Elle ne peut jamais, seule, produire `ACHETER` ou `RENFORCER`.

## 11. Interface

Afficher :

- ce qui est anormal ;
- par rapport à quoi ;
- depuis quand ;
- magnitude ;
- confirmations ;
- contradictions ;
- limite de la mesure ;
- impact analytique ;
- prochaine donnée à surveiller.

Éviter les alertes rouges partout. La couleur reflète la gravité et le sens financier, pas le caractère simplement inhabituel.

## 12. Tests obligatoires

- pas d’anomalie sans baseline ;
- donnée manquante ne devient pas zéro ;
- confirmation indépendante vérifiée ;
- même source dupliquée ne compte pas deux fois ;
- faux positifs corporate actions filtrés ;
- GEX/flow toujours étiquetés comme conventions/proxies ;
- cycle de vie persistant ;
- aucune anomalie seule ne produit une décision finale ;
- seuils versionnés ;
- mode démo clairement étiqueté.
