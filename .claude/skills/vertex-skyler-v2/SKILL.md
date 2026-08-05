---
name: vertex-skyler-v2
description: Piloter la consolidation et le développement de Skyler V2, analyste en chef institutionnel de Vertex, lot par lot, avec comité contradictoire, décisions probabilistes, preuves mathématiques, données traçables et validation humaine obligatoire.
---

# VERTEX — SKYLER V2 MASTER SKILL

## 1. Mission

Tu construis **Skyler V2**, l’analyste en chef et président du comité d’investissement de Vertex.

Skyler doit relier dans une seule décision traçable :

- régime de marché et cross-asset ;
- secteurs, breadth, dispersion et leadership ;
- fondamentaux, valorisation et révisions ;
- technique, momentum, prix et volume ;
- actualités, événements et catalyseurs ;
- anomalies et flux institutionnels ;
- options calls/puts/LEAPS, volatilité et Greeks ;
- GEX, Vanna, Charm, skew et term structure ;
- portefeuille, concentration et budget de risque ;
- discipline comportementale, journal et post-mortem ;
- calibration historique des probabilités et décisions.

Skyler ne cherche pas à produire beaucoup de trades. Il cherche quelques opportunités dont l’asymétrie est réellement exceptionnelle.

Il ne passe jamais d’ordre. Il ne remplace jamais un moteur déterministe par une réponse libre d’un modèle linguistique.

Pipeline absolu :

```text
Données réelles
→ normalisation et qualité
→ moteurs déterministes
→ comité spécialisé contradictoire
→ SkylerPacket validé
→ moteur de décision canonique
→ Claude explique sans modifier la décision
```

Jamais :

```text
Données brutes → prompt libre → chiffres/probabilités/recommandation inventés
```

## 2. Invocation

Une commande exécute une seule mission :

- `/vertex-skyler-v2 audit`
- `/vertex-skyler-v2 lot-0`
- `/vertex-skyler-v2 lot-1`
- `/vertex-skyler-v2 lot-2`
- `/vertex-skyler-v2 lot-3`
- `/vertex-skyler-v2 lot-4`
- `/vertex-skyler-v2 lot-5`
- `/vertex-skyler-v2 lot-6`
- `/vertex-skyler-v2 lot-7`
- `/vertex-skyler-v2 lot-8`
- `/vertex-skyler-v2 lot-9`
- `/vertex-skyler-v2 lot-10`
- `/vertex-skyler-v2 lot-11`
- `/vertex-skyler-v2 lot-12`
- `/vertex-skyler-v2 decision-review <SYMBOL>`
- `/vertex-skyler-v2 red-team <SYMBOL>`
- `/vertex-skyler-v2 status`
- `/vertex-skyler-v2 verify`

À la fin de chaque mission : rapport, PR brouillon, arrêt et validation humaine explicite.

Ne jamais commencer un autre lot par anticipation.

## 3. Branche et gouvernance Git

Branche d’intégration officielle :

```text
integration/vertex-skyler-v2
```

Base fonctionnelle :

```text
agent/vertex-neon-glass-graphs
```

Règles :

1. Ne jamais travailler directement sur `main`.
2. Ne jamais fusionner automatiquement vers `main`.
3. Ne jamais utiliser de push forcé.
4. Une branche de lot = `agent/skyler-v2-lot-XX-description`.
5. Chaque PR de lot cible `integration/vertex-skyler-v2`.
6. Chaque PR reste brouillon jusqu’à validation humaine.
7. Ne pas mélanger calcul, visuel et nettoyage massif dans une même PR.
8. Les branches V4/Prism sont historiques, pas des bases de développement.
9. Toute divergence RC1/Neon Glass est documentée avant résolution.
10. Aucun fichier, route, branche ou endpoint supprimé sans preuve d’inutilisation.
11. Un lot doit être réversible.
12. Les données runtime et privées ne sont jamais commitées.

## 4. Sources de vérité

Ordre d’autorité :

1. `docs/refactor/VERTEX_CONSTITUTION.md`
2. ce fichier `SKILL.md`
3. `references/TRADING_CONSTITUTION_V2.md`
4. `references/DECISION_ENGINE.md`
5. `references/ADVERSARIAL_COMMITTEE.md`
6. `references/DECISION_PACKET_SCHEMA.md`
7. `references/SCENARIO_CALIBRATION.md`
8. `references/OPTIONS_CORRECTNESS.md`
9. `references/ANOMALY_INTELLIGENCE.md`
10. `references/SKYLER_ARCHITECTURE.md`
11. `references/LOT_RUNBOOK.md`
12. `references/ACCEPTANCE_CHECKLIST.md`
13. rapport de validation du lot courant ;
14. commentaires historiques du code.

Si le code contredit une règle supérieure, corriger le code. Ne jamais affaiblir une règle pour faire passer un comportement erroné.

## 5. Agents spécialisés obligatoires

Utiliser les agents suivants lorsque leur domaine est concerné :

- `.claude/agents/skyler-market-regime.md`
- `.claude/agents/skyler-options-risk.md`
- `.claude/agents/skyler-portfolio-risk.md`
- `.claude/agents/skyler-data-auditor.md`
- `.claude/agents/skyler-devils-advocate.md`
- `.claude/agents/skyler-chair.md`

Les autres agents métier Vertex peuvent compléter le comité.

Règles :

- aucun sous-agent ne produit `final_decision` ;
- le Président Skyler est l’unique producteur du verdict final ;
- les agents retournent des claims structurés, sources, fraîcheur, confiance et inconnues ;
- plusieurs métriques issues de la même donnée ne comptent pas comme preuves indépendantes ;
- une opinion minoritaire crédible est conservée ;
- un veto qualité des données ne peut pas être annulé par vote majoritaire ;
- toute note S/S+ exige une red-team indépendante.

## 6. Invariants absolus

### 6.1 READONLY et sécurité

- IBKR reste `readonly=True`.
- Aucun endpoint, bouton, service ou fonction d’exécution d’ordre.
- Aucun appel `placeOrder`, `submitOrder`, `transmit`, `cancelOrder` ou équivalent.
- Aucun secret, token, position réelle ou cache personnel commité.
- Aucun envoi de données privées à Claude sans filtrage et réduction.
- La couche Claude ne peut modifier aucun champ canonique de décision.

### 6.2 Intégrité des données

Toute valeur critique transporte :

- valeur ;
- unité ;
- source ;
- champ source ;
- période ;
- timestamp ;
- fraîcheur ;
- mode réel/démo/simulé ;
- statut disponible/manquant/insuffisant ;
- caractère estimé ;
- méthode lorsque calculée.

`0`, absent, `None`, périmé, estimé, démo et insuffisant sont des états différents.

Une donnée manquante reste manquante. Un verdict ne paraît jamais plus frais que sa donnée critique la plus ancienne.

### 6.3 Calculs

- Toute correction commence par un test rouge.
- Toute unité d’entrée est explicite.
- Aucune heuristique silencieuse d’unité sur un calcul financier critique.
- NaN, infinis et entrées invalides sont refusés.
- Multiplicateurs actions/options exacts.
- Validation par cas manuels et tests de propriété.
- Les modèles sont versionnés.
- Les résultats historiques restent liés à la version qui les a produits.
- Aucun look-ahead dans les backtests ou calibrations.

### 6.4 Produit

- une page = une mission ;
- une section = une question ;
- un graphique = une conclusion ;
- réponse d’abord, preuve ensuite, expertise à la demande ;
- aucune donnée inventée pour remplir un écran ;
- aucun doublon de métrique sans justification ;
- aucun lot terminé avec tests rouges, erreur console, overflow ou contradiction non documentée.

## 7. Philosophie d’investissement

Pour chaque opportunité, Skyler répond :

1. Pourquoi cette société peut-elle battre le marché ?
2. Pourquoi maintenant ?
3. Quel est le catalyseur des 90 prochains jours ?
4. Les institutions accumulent-elles ?
5. Le graphique confirme-t-il ?
6. Quel est le risque maximum ?
7. Une option directionnelle peut-elle raisonnablement doubler ?
8. Pourquoi l’action ou l’option est-elle meilleure que l’alternative ?
9. Qu’est-ce qui est déjà intégré dans le prix ?
10. Quelle preuve ferait changer immédiatement la décision ?

Scénarios obligatoires : pessimiste, probable, exceptionnel.

Chaque scénario inclut : probabilité, horizon, déclencheur, cible, rendement, invalidation, hypothèses, inconnues, impact action et impact option.

Niveaux :

- S+ : 36–40, allocation analytique maximale 10–15 % ;
- S : 32–35, 7–10 % ;
- A : 28–31, 3–5 % ;
- B : 24–27, 1–2 % ;
- inférieur à 24 : refus ou surveillance.

Les allocations sont des plafonds analytiques, jamais des ordres.

Règles :

- portefeuille idéal 8–15 lignes ;
- ne jamais renforcer une position perdante ;
- renforcer seulement après nouveau fait positif et confirmation ;
- réévaluer les gagnants selon la thèse ;
- ne pas vendre automatiquement à +100 % ;
- sécurisation partielle indicative 25–50 % si la thèse reste valide ;
- conserver un runner lorsque l’asymétrie résiduelle reste exceptionnelle.

## 8. Décision canonique

Décisions finales autorisées uniquement :

- `ACHETER`
- `RENFORCER`
- `ATTENDRE`
- `REDUIRE`
- `REFUSER`

États opérationnels possibles :

- `SURVEILLER`
- `PREPARER`
- `DECLENCHEMENT_CONDITIONNEL`
- `CONFIRMATION_REQUISE`
- `SECURISATION_PARTIELLE`
- `RUNNER`
- `THESE_A_REEVALUER`
- `DONNEES_INSUFFISANTES`

Le score ne contourne jamais les hard gates.

## 9. Score Skyler /40

| Bloc | Points |
|---|---:|
| Fondamentaux et qualité | 5 |
| Catalyseurs | 5 |
| Technique et timing | 6 |
| Institutions, flux et anomalies | 4 |
| Régime marché et secteur | 4 |
| Asymétrie et scénarios | 6 |
| Qualité de l’option | 6 |
| Qualité et fraîcheur des données | 4 |
| **Total** | **40** |

Hard gates minimum :

- R:R inférieur à 2:1 ;
- EV négative ;
- invalidation absente ;
- donnée critique insuffisante ou unité ambiguë ;
- désaccord de sources non résolu ;
- catalyseur non démontré ;
- spread ou liquidité option insuffisants ;
- DTE hors mandat ;
- thèse cassée ;
- renforcement perdant ;
- concentration excessive ;
- quota options dépassé ;
- perte illimitée non signalée ;
- événement binaire non traité ;
- red-team absente pour S/S+.

## 10. Confiance

La confiance n’est jamais la moyenne des scores.

Elle combine :

- qualité et complétude ;
- fraîcheur ;
- indépendance et accord des preuves ;
- robustesse aux hypothèses ;
- calibration historique ;
- contradictions ;
- dépendance à un événement binaire.

Forme cible :

```text
confidence = data_quality × agreement × robustness × calibration
```

Plafonds obligatoires :

- donnée critique estimée : maximum 70 % ;
- régime `UNKNOWN` : maximum 55 % ;
- contradiction majeure non résolue : maximum 50 % ;
- données insuffisantes : décision non actionnable.

## 11. Options

Univers distincts :

| Mandat | DTE |
|---|---:|
| TACTICAL | 20–60 |
| SWING | 60–180 |
| LEAPS | 180–540 |

Profil LEAPS :

- delta 0,70–0,90 ;
- échéance 6–18 mois ;
- OI élevé ;
- spread faible ;
- catalyseur identifiable ;
- perte maximale et coût total explicites ;
- scénarios spot × temps × IV ;
- risque IV crush ;
- probabilité de doublement distincte de PoP.

Les stratégies à jambes vendues sont interdites à la recommandation si le profil actif les interdit. Elles peuvent être analysées en laboratoire avec risque explicite.

GEX, max pain, flow, walls, Vanna et Charm restent des modèles/conventions et ne sont jamais présentés comme certitudes.

## 12. SkylerPacket

Créer progressivement des contrats typés et testés :

- `MarketContext`
- `CompanyContext`
- `CatalystContext`
- `TechnicalContext`
- `InstitutionalContext`
- `OptionsContext`
- `PortfolioContext`
- `DataQualityContext`
- `EvidenceClaim`
- `Contradiction`
- `ScenarioSet`
- `InstrumentCandidate`
- `SkylerPacket`
- `SkylerDecision`
- `AuditTrail`

Le packet est versionné, JSON-sérialisable, sans secret, sans NaN/Infinity et immuable après décision.

Claude reçoit uniquement un packet réduit. Il explique, compare et vulgarise. Il ne recalcule pas les probabilités, scores, Greeks ou risques.

## 13. Lots obligatoires

### AUDIT — Convergence réelle

Comparer `main`, RC1, Neon Glass et Skyler V2.

Livrable : `docs/skyler/BRANCH_CONVERGENCE_AUDIT.md`.

Aucun changement runtime.

### LOT 0 — Gouvernance et baseline

- branche/SHA ;
- compileall/pytest ;
- routes, endpoints, moteurs, graphes ;
- READONLY ;
- console et responsive ;
- baseline documentée.

### LOT 1 — Correctness options

- perte illimitée ;
- `max_loss_unbounded` ;
- unités IV explicites ;
- taux/dividende ;
- validations ;
- spread/slippage ;
- profils autorisés ;
- tests manuels et de propriété.

Aucun visuel ni scoring global dans ce lot.

### LOT 2 — Constitution V2

- nouvelle version de profil ;
- V1 immuable ;
- S+/S/A/B ;
- 8–15 positions ;
- LEAPS ;
- gagnants/perdants ;
- versioning/diff/rollback.

### LOT 3 — Market Intelligence

- `MarketContext` canonique ;
- indices, breadth, VIX, terme de vol, taux, crédit, dollar, liquidité, dispersion, cross-asset, secteurs ;
- transitions de régime ;
- changement depuis dernière session.

### LOT 4 — News, catalyseurs et anomalies

- OHLCV canonique ;
- timeline événements ;
- déduplication news ;
- révisions ;
- anomalies marché/secteur/action/options/fondamentaux ;
- cycle de vie et confirmations.

### LOT 5 — Skyler Core

- contrats typés ;
- preuves ;
- comité contradictoire ;
- score /40 ;
- hard gates ;
- scénarios ;
- contradiction detector ;
- décision déterministe sans Claude ;
- audit trail.

### LOT 6 — Options Intelligence

- scanners TACTICAL/SWING/LEAPS ;
- calls et puts longs ;
- Greeks complets ;
- IV rank/percentile/skew/term structure ;
- expected move ;
- GEX/walls/zero gamma ;
- spot × temps × IV ;
- earnings/IV crush ;
- probabilité de doublement.

### LOT 7 — Portfolio Intelligence

- sizing ;
- budget de risque ;
- corrélations ;
- remplacement ;
- ajout aux gagnants uniquement ;
- sécurisation partielle ;
- stress tests ;
- exposition Greeks portefeuille.

### LOT 8 — Expérience Neon Glass

Ordre : Aujourd’hui, Marchés, Opportunités, Analyse, Portefeuille, Options, Journal, Système.

Chaque page répond en moins de dix secondes : changement, importance, risque, invalidation, prochaine action analytique.

### LOT 9 — Scénarios et calibration

- ledger de décisions ;
- probabilités versionnées ;
- Brier score, log loss, calibration bins ;
- MAE/MFE ;
- résultats par régime/niveau/instrument ;
- benchmark SPY ;
- absence de look-ahead.

### LOT 10 — Mémoire et discipline décisionnelle

- figer chaque décision et sa version ;
- comparer thèse initiale et résultat ;
- détecter erreurs récurrentes ;
- séparer erreur de modèle, erreur de données et erreur de discipline ;
- recommandations d’amélioration soumises à validation humaine ;
- aucune auto-modification de la Constitution.

### LOT 11 — Knowledge Graph et recherche institutionnelle

- relier sociétés, secteurs, thèmes, catalyseurs, fournisseurs, clients, concurrents et risques ;
- propagation d’impact explicable ;
- provenance de chaque relation ;
- détection de dépendances cachées ;
- questions de recherche automatiques, sans invention de relation.

### LOT 12 — Red-team, sécurité et release candidate

- red-team de tous les niveaux S/S+ ;
- tests adversariaux ;
- audit mathématique options ;
- audit données et sécurité ;
- audit performance/accessibilité ;
- mode démo/sans IBKR/stale/offline ;
- rollback ;
- validation humaine sur appareil physique ;
- aucun merge `main` sans accord explicite.

## 14. `decision-review`

Pour un symbole :

1. construire le packet sans modifier le runtime ;
2. exécuter les analystes ;
3. produire les contradictions ;
4. construire les scénarios ;
5. comparer action/call/put/attendre ;
6. consulter le portefeuille ;
7. exécuter l’avocat du diable ;
8. produire une décision déterministe ;
9. séparer faits, estimations et interprétations ;
10. ne jamais passer d’ordre.

Cette commande est une analyse, pas une implémentation de lot.

## 15. `red-team`

Pour un symbole ou une décision :

- construire le meilleur dossier adverse ;
- tester choc marché, retard catalyseur, IV crush, spread, gap et corrélation ;
- identifier la preuve la plus fragile ;
- proposer les conditions exactes de dégradation du score ou de la confiance ;
- conserver la décision initiale séparément ;
- ne jamais réécrire silencieusement l’historique.

## 16. Procédure obligatoire pour chaque lot

1. Lire toutes les références.
2. Confirmer branche et SHA.
3. Vérifier validation du lot précédent.
4. Auditer avant code.
5. Écrire les tests rouges pour tout défaut de calcul.
6. Implémenter le minimum nécessaire.
7. Exécuter validations ciblées et suite complète.
8. Tester navigateur si UI.
9. Produire le rapport `templates/LOT_REPORT.md`.
10. Mettre à jour `docs/skyler/STATUS.md`.
11. Committer uniquement le lot.
12. Ouvrir ou mettre à jour une PR brouillon.
13. S’arrêter.

## 17. Validation minimale

```bash
python -m compileall -q terminal.py vertex
python -m pytest tests/ -q
python -m pytest tests/test_no_orders.py -q
```

Puis vérifier :

- `/healthz` ;
- `/api/client-log` = 0 erreur ;
- `DEMO=1 NO_IBKR=1` ;
- mode sans IBKR ;
- missing/stale/demo/insufficient/offline ;
- 390/768/1440/1920 px si UI ;
- clavier/focus/reduced-motion si UI ;
- service worker bump si shell visible ;
- aucun secret/runtime dans le diff ;
- déterminisme des décisions ;
- schéma packet valide ;
- opinion minoritaire et audit trail conservés.

## 18. Interdictions explicites

- pas de refonte big-bang ;
- pas de plusieurs lots dans une session ;
- pas de moteur modifié pour embellir un visuel ;
- pas de test affaibli pour accepter un résultat faux ;
- pas de fallback silencieux ;
- pas de confusion force relative/sentiment ;
- pas de score catalyseur basé uniquement sur une date ;
- pas de stratégie contraire au profil ;
- pas de GEX/flow/max pain présenté comme vérité ;
- pas de probabilité sans méthode ;
- pas de confiance à 100 % ;
- pas d’auto-recalibration ;
- pas d’auto-modification de Constitution ;
- pas de disparition d’une contradiction ;
- pas de décision S/S+ sans red-team ;
- pas de continuation après échec critique ;
- jamais « terminé » sans preuves.

## 19. Rapport obligatoire

Chaque rapport contient :

- Constat ;
- Problème ;
- Décision ;
- Implémentation ;
- Fichiers modifiés ;
- Tests et résultats exacts ;
- Validation navigateur ;
- Invariants ;
- Contradictions ;
- Opinion minoritaire ;
- Risques restants ;
- Diff avec lot précédent ;
- verdict `GO`, `GO AVEC RÉSERVES` ou `NO-GO` ;
- prochaine étape autorisée ;
- phrase : `Arrêt après ce lot — validation humaine requise.`

## 20. Première mission

La première exécution reste :

```text
/vertex-skyler-v2 audit
```

Elle ne modifie aucun moteur ni page. Elle produit uniquement l’audit de convergence, la source canonique par domaine et le plan de Lot 0.

Après validation humaine, exécuter `lot-0`, puis s’arrêter de nouveau.
