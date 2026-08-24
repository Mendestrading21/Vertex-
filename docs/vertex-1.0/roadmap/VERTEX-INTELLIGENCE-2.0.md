# Programme Vertex Intelligence 2.0

## Objectif

Faire de Vertex un comité d'investissement numérique capable de répondre à
cinq questions avec des preuves datées :

1. Que se passe-t-il maintenant ?
2. Pourquoi ce titre peut-il battre le marché ?
3. Pourquoi maintenant ?
4. Quel est le risque maximum et qu'est-ce qui invalide la thèse ?
5. La méthode a-t-elle réellement fonctionné hors échantillon ?

Vertex reste strictement **analyse uniquement**. Le programme n'ajoute aucun
ordre, aucune automatisation d'achat et aucune promesse de rendement.

## Architecture cible

```text
IBKR + SEC + FRED/BLS/CFTC + WMB + sources optionnelles
  → identité instrument canonique
  → lake point-in-time immuable
  → qualité, fraîcheur, entitlement et réconciliation
  → événements + features versionnés
  → laboratoires de validation
  → moteurs promus et gelés
  → dossier de thèse + scénarios + hard gates
  → portefeuille + options + comité contradictoire
  → décision canonique
  → narration IA sourcée
  → journal, attribution, alertes et revue
```

## Principes non négociables

- source primaire avant repli ;
- données point-in-time pour toute preuve historique ;
- temps d'observation et temps de disponibilité séparés ;
- faits, estimations, interprétations et opinions séparés ;
- probabilité publiée uniquement si calibrée ;
- signal nouveau en quarantaine avant promotion ;
- baseline simple obligatoire ;
- coût, spread et slippage intégrés ;
- aucune modification en place du profil V4 ;
- aucun nouveau code métier dans `terminal.py` ;
- une PR cohérente, une preuve, un rollback.

## Phase 0 — RC vérifiable

### Livrables

- fournir en CI `origin/main` et les pointes distantes requises par les
  gardiens de gouvernance, sans historique complet ;
- CI complète verte sur le SHA candidat ;
- smoke runtime exécuté après la suite ;
- rapport final aligné sur le vrai nombre de tests ;
- liste explicite des 7/12 skips selon local/CI ;
- avertissements Pandas 4 et boucle `ib_async` classés et corrigés ou acceptés.

### Acceptation

- aucun job rouge ;
- aucune preuve recopiée depuis un autre SHA ;
- `tests/test_no_orders.py` vert ;
- pas de fusion ni tag automatique.

## Phase 1 — Clôture G5 broker réel

Une session TWS live sur le port 7496 en lecture seule, les quatre rôles IBKR
connectés, huit espaces servis et zéro erreur client sont déjà prouvés au SHA
`d77b06d`. Le lot ne doit pas refaire cette démonstration : il doit compléter
et rendre reproductibles les cases encore absentes du protocole.

### Livrables

- rattacher la preuve live existante à `mesurer_g5_live.py` et conserver un
  artefact anonymisé ;
- matrice compte réel/papier, ports, client IDs et entitlements ;
- cotation live/frozen/delayed/frozen-delayed vérifiée ;
- chaîne options : contrat, bid/ask, IV, Greeks, OI, volume, timestamp ;
- positions et account summary réconciliés ;
- news providers réellement abonnés ;
- reconnexion, timeout, pacing et panne partielle ;
- preuve qu'aucune méthode d'ordre n'est accessible.

### Acceptation

- zéro donnée inventée ;
- type de marché capturé par requête ;
- les quatre adaptateurs IBKR à 0 % reçoivent des tests contractuels et de
  replay ;
- un enregistrement anonymisé et non sensible permet de rejouer les callbacks
  hors TWS ;
- G5 signé humainement.

## Phase 2 — Fondation point-in-time

### Nouveaux composants

- `vertex/domain/instruments.py` : conId, ticker, CIK, FIGI/ISIN si disponible,
  exchange, currency et corporate actions ;
- `vertex/storage/point_in_time.py` : observations immuables ;
- `vertex/storage/schemas.py` : versions et migrations ;
- `vertex/data_sources/contracts.py` : protocole commun des providers ;
- `vertex/data_sources/entitlements.py` : configuré, autorisé, testé, frais ;
- `vertex/data_sources/replay.py` : fixtures anonymisées.

### Modèle minimal

Chaque observation possède :

```text
instrument_id, field, value, unit, currency,
observed_at, available_at, received_at,
provider, provider_record_id, mode, quality,
revision, lineage, schema_version
```

### Acceptation

- append-only ;
- migrations réversibles ;
- requête « ce que Vertex savait à T » ;
- checksum et provenance ;
- aucune dépendance UI au format du provider ;
- tests de timezone, DST, split, changement de ticker et devise.

## Phase 3 — Entreprises et macro institutionnels

### SEC / entreprise

- submissions, 10-K, 10-Q, 8-K, 20-F ;
- XBRL normalisé avec période, unité et filed date ;
- croissance, marges, FCF, dilution, dette, qualité des bénéfices ;
- Form 4 et 13F directs ;
- changements de guidance et risques textuels ;
- détection de restatement ;
- graphe entreprise : segments, pairs, dirigeants, événements.

### Macro

- FRED vintages et séries ;
- BLS CPI/emploi avec dates officielles ;
- calendrier Fed/BEA réel ;
- CFTC COT avec report date et publish date ;
- courbe de taux, crédit, dollar, pétrole, liquidité ;
- régimes calculés sans utiliser une publication avant son heure réelle.

### Acceptation

- `macro_calendar.py` ne crée plus de date exacte depuis une règle
  approximative ;
- comparaison SEC vs Yahoo/IBKR explicite ;
- backfill point-in-time sans look-ahead ;
- hard gate sur événement non confirmé.

## Phase 4 — Event Intelligence

### Taxonomie

- earnings, guidance, analyst revisions ;
- 8-K, M&A, buyback, offering, insider, litigation ;
- produits, contrats, réglementation, management ;
- macro, politique monétaire, géopolitique ;
- options flow, vol, positioning et liquidité.

### Pipeline

```text
article/dépôt/événement
  → identité et déduplication
  → horodatage et source
  → entités et type
  → faits vérifiables
  → importance et horizon
  → exposition portefeuille
  → réaction prix/volume/IV
  → statut confirmé/contesté/révisé
```

### Acceptation

- même événement consolidé sans perdre les sources ;
- article sans URL IBKR reste honnêtement sans URL ;
- sentiment séparé de l'impact ;
- historique des révisions ;
- aucune synthèse IA sans citations internes du packet.

## Phase 5 — Research OS

### Contrat d'expérience

Chaque hypothèse déclare : univers, fréquence, horizon, features, cible,
baseline, coûts, métriques, périodes train/validation/test, embargo, régimes,
seed, version de données et critères de retrait.

### Méthodes

- walk-forward ancré et roulant ;
- purged K-fold + embargo ;
- bootstrap des intervalles ;
- tests de stabilité paramètres ;
- survivorship et delisting ;
- comparaison secteur/indice ;
- calibration Brier/log-loss et reliability curves ;
- contrôle de multiplicité des essais ;
- champion/challenger/shadow ;
- drift de données, features, calibration et performance.

### Promotion

Un signal passe `IDEA → RESEARCH → SHADOW → CANDIDATE → ACTIVE`. Il retourne en
`QUARANTINED` si drift, données manquantes ou dégradation hors seuil.

### Acceptation

- aucune fonction classée F dans l'orchestrateur de recherche ;
- aucune stratégie promue sur performance in-sample seule ;
- résultats reproductibles depuis un manifest ;
- baseline naïve battue après coûts ;
- effets publiés avec intervalle, pas seulement moyenne.

## Phase 6 — Options Intelligence

### Dossier contrat

- conId/localSymbol exact ;
- bid, ask, mid, spread, sizes, OI, volume et quote age ;
- spot/forward, taux, dividendes ;
- IV et Greeks broker + modèle, avec écart ;
- skew, terme, surface sans arbitrage simple ;
- realized vol multi-fenêtres ;
- earnings et événements ;
- scénario cube spot × temps × IV ;
- probabilité de toucher, finir ITM et doubler, seulement si méthode étiquetée ;
- liquidité/slippage et coût total ;
- invalidation sous-jacent + contrat.

### Gestion

- checkpoints 2/4/6 semaines ;
- invalidation immédiate si thèse cassée ;
- aucun renforcement d'une position perdante ;
- renforcement d'un gagnant uniquement après événement de validation ;
- sorties partielles et runner paramétrés par profil versionné.

### Acceptation

- tests de parité avec valeurs indépendantes ;
- scénarios autour de dividendes, earnings, taux et IV crush ;
- borne de perte au débit total ;
- aucun contrat recommandé si quote, spread, OI, IV ou événement critique manque.

## Phase 7 — Portfolio Intelligence

### Capacités

- exposition nette/brute, beta, delta dollars, gamma, vega, theta ;
- concentration titre/secteur/facteur/thèse/catalyseur ;
- corrélations conditionnelles et downside ;
- stress historiques et scénarios macro ;
- marginal VaR/CVaR et contribution au drawdown ;
- risque de liquidité ;
- chevauchement d'événements ;
- compatibilité avec 8–15 lignes et 3 options maximum ;
- proposition de taille par niveau, jamais exécution.

### Acceptation

- risque portefeuille avant conviction isolée ;
- aucune allocation si données de position non réconciliées ;
- explication du risque ajouté et du risque remplacé ;
- stress reproductibles et versionnés.

## Phase 8 — Dossier de décision et mémoire

### Sortie unique

Chaque recommandation contient :

- verdict et horizon ;
- thèse et contre-thèse ;
- pourquoi maintenant ;
- catalyseurs 30/90/180 jours ;
- invalidation mesurable ;
- scénarios pessimiste/probable/exceptionnel ;
- asymétrie et perte maximale ;
- qualité des données et incertitude ;
- opinion minoritaire du comité ;
- compatibilité portefeuille ;
- contrat optionnel exact si applicable ;
- prochaine date de revue ;
- versions de données, moteurs et profil.

### Mémoire

- enregistrer le packet avant décision humaine ;
- enregistrer accepter/refuser/attendre sans réécrire le passé ;
- suivre MFE/MAE, sortie, thèse cassée ou non ;
- attribuer le résultat au marché, secteur, facteur, timing, options et gestion ;
- produire un postmortem sans réécrire la justification initiale.

### Acceptation

- track record calculé sur packets gelés ;
- aucune sélection rétrospective des gagnants ;
- performance par régime, score, horizon et qualité des données ;
- calibration des niveaux S+/S/A/B ;
- retrait automatique d'affichage d'un niveau non calibré, pas retrait de
  données.

## Phase 9 — Profil stratégique V5, décision humaine

Créer `vertex_strategy_v5.json` sans toucher à V4. Le candidat doit comparer :

- delta 0,70–0,90 pour LEAPS de conviction ;
- options tactiques 2/4/6 semaines, DTE autour de six mois ;
- asymétrie pessimiste/probable/exceptionnelle ;
- risque par position et risque portefeuille séparés ;
- tailles S+/S/A/B ;
- gestion +20/+30/+50/+75/+100 ;
- renforcement des gagnants uniquement ;
- objectifs comme cibles non garanties.

V5 reste `CANDIDATE` tant que :

- l'utilisateur n'a pas arbitré le conflit V4/V5 ;
- les données options point-in-time ne permettent pas un backtest honnête ;
- la calibration par cohorte n'est pas suffisante.

## Phase 10 — Simplification et exploitation

- extraire les workers restants de `terminal.py` ;
- réduire les captures silencieuses par budget mesuré ;
- casser les fonctions E/F avec tests de caractérisation ;
- introduire Ruff progressivement par périmètre, jamais 1 256 corrections en
  masse ;
- types sur les modèles canoniques et frontières de provider ;
- seuil de couverture critique, pas un chiffre global aveugle ;
- SBOM, audit dépendances et pins reproductibles ;
- sauvegarde, restauration, rollback et migrations ;
- politique de rétention des branches et documents historiques.

## Ordre des PR

| Lot | Branche | Dépend de | Gate |
|---|---|---|---|
| 0 | `agent/vertex-1-0-ci-proof` | RC | G6/G7 |
| 1 | `agent/vertex-1-0-g5-close` | 0 | G5 |
| 2 | `agent/vertex-1-0-point-in-time` | 1 | G2/G3 |
| 3 | `agent/vertex-1-0-sec-macro` | 2 | G2/G3 |
| 4 | `agent/vertex-1-0-event-intel` | 3 | G3 |
| 5 | `agent/vertex-1-0-research-os` | 2 | G3 |
| 6 | `agent/vertex-1-0-options-intel` | 1,2,4,5 | G3/G5 |
| 7 | `agent/vertex-1-0-portfolio-intel` | 2,5 | G3 |
| 8 | `agent/vertex-1-0-decision-memory` | 4,5,6,7 | G3 |
| 9 | `agent/vertex-1-0-strategy-v5` | 5,6,8 | décision humaine |
| 10 | `refactor/vertex-runtime-debt` | RC stable | G1/G6 |

Ne jamais ouvrir ces dix branches simultanément. Un lot commence lorsque ses
dépendances sont acceptées et intégrées dans la base de travail autorisée.
