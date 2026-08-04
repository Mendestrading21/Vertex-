---
name: vertex-skyler-v2
description: Piloter la consolidation et le développement de Skyler V2 dans Vertex, lot par lot, avec preuves mathématiques, données traçables, analyse marché/actions/options/portefeuille et validation humaine obligatoire.
---

# VERTEX — SKYLER V2 MASTER SKILL

## 1. Mission

Tu construis **Skyler V2**, l’analyste en chef de Vertex.

Skyler doit transformer les données réelles déjà disponibles dans Vertex en une décision analytique claire, probabiliste, traçable et réversible. Il doit relier :

- régime de marché et cross-asset ;
- secteurs, breadth et leadership ;
- fondamentaux, valorisation et révisions ;
- technique, momentum et anomalies ;
- actualités et catalyseurs ;
- flux institutionnels et positionnement options ;
- calls, puts, LEAPS, volatilité et Greeks ;
- portefeuille, concentration et budget de risque ;
- journal, post-mortem et calibration.

Skyler ne passe jamais d’ordre. Il ne remplace jamais un moteur déterministe par une réponse libre d’un modèle linguistique.

Principe absolu :

> Données réelles → moteurs déterministes → SkylerPacket structuré → décision canonique → Claude explique.

Jamais :

> Données brutes → Claude invente des chiffres, des probabilités, des objectifs ou une recommandation.

## 2. Invocation

Utiliser ce skill avec une seule commande de lot à la fois :

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
- `/vertex-skyler-v2 status`
- `/vertex-skyler-v2 verify`

Une invocation exécute **un seul lot**. À la fin du lot, tu t’arrêtes et attends une validation humaine explicite. Tu ne commences jamais le lot suivant par anticipation.

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
3. Ne jamais réécrire l’historique avec un push forcé.
4. Une branche de lot = `agent/skyler-v2-lot-XX-description`.
5. Une PR de lot cible `integration/vertex-skyler-v2`.
6. Une PR reste brouillon jusqu’à validation humaine.
7. Ne pas mélanger changement de calcul, refonte visuelle et nettoyage massif dans la même PR.
8. Les branches V4/Prism historiques sont des références, pas des bases de développement.
9. Toute divergence entre la RC1 Total Rebuild et Neon Glass doit être documentée avant résolution.
10. Ne jamais supprimer une branche, un fichier ou un endpoint sans preuve d’inutilisation et accord explicite si l’action est destructive.

## 4. Sources de vérité

Ordre d’autorité :

1. `docs/refactor/VERTEX_CONSTITUTION.md`
2. `.claude/skills/vertex-skyler-v2/SKILL.md`
3. `.claude/skills/vertex-skyler-v2/references/TRADING_CONSTITUTION_V2.md`
4. `.claude/skills/vertex-skyler-v2/references/SKYLER_ARCHITECTURE.md`
5. `.claude/skills/vertex-skyler-v2/references/OPTIONS_CORRECTNESS.md`
6. `.claude/skills/vertex-skyler-v2/references/LOT_RUNBOOK.md`
7. `.claude/skills/vertex-skyler-v2/references/ACCEPTANCE_CHECKLIST.md`
8. documents de validation du lot courant ;
9. commentaires historiques du code.

Si le code contredit une règle supérieure, le code doit être corrigé. Ne jamais modifier la règle pour faire passer un comportement erroné.

## 5. Invariants absolus

### 5.1 Sécurité

- IBKR reste `readonly=True`.
- Aucun endpoint, bouton, service ou fonction d’exécution d’ordre.
- Aucun appel `placeOrder`, `submitOrder`, `transmit`, `cancelOrder` ou équivalent dans le code Vertex.
- Aucun secret, token, position réelle ou cache personnel commité.
- Aucun envoi de données privées à Claude sans réduction et filtrage explicites.

### 5.2 Intégrité des données

- Toute donnée affiche ou transporte : valeur, unité, source, période, fraîcheur et statut.
- `0`, absent, `None`, indisponible, périmé, estimé, démo et insuffisant sont des états distincts.
- Une donnée manquante reste manquante.
- Une estimation doit être étiquetée comme estimation.
- Une probabilité doit préciser le modèle, les hypothèses et la date de calcul.
- Un verdict ne doit jamais paraître plus frais que sa donnée la plus ancienne critique.
- Une valeur du navigateur ne peut pas servir de timestamp de marché.

### 5.3 Calculs

- Toute modification de calcul commence par un test rouge reproduisant le défaut.
- Toute unité d’entrée doit être explicite.
- Aucun calcul financier critique ne dépend d’une heuristique silencieuse d’unité.
- Les résultats extrêmes, NaN, infinis et entrées invalides doivent être refusés honnêtement.
- Les calculs action et option doivent inclure le multiplicateur exact.
- Les résultats doivent être validés par cas simples calculables à la main.

### 5.4 Produit

- Une page = une mission.
- Une section = une question.
- Un graphique = une conclusion exploitable.
- Réponse d’abord, justification ensuite, expertise à la demande.
- Aucun doublon de métrique ou de graphique sans justification.
- Aucun lot terminé avec tests rouges, erreur console, overflow critique ou contradiction non documentée.

## 6. Philosophie d’investissement à implémenter

Skyler recherche l’asymétrie, pas la fréquence de trades.

Pour chaque opportunité, il doit répondre :

1. Pourquoi cette société peut-elle battre le marché ?
2. Pourquoi maintenant ?
3. Quel est le catalyseur des 90 prochains jours ?
4. Les institutions accumulent-elles ?
5. Le graphique confirme-t-il ?
6. Quel est le risque maximum ?
7. Une option directionnelle peut-elle raisonnablement doubler ?

Scénarios obligatoires :

- pessimiste ;
- probable ;
- exceptionnel.

Chaque scénario doit inclure : probabilité, horizon, déclencheur, cible, rendement, invalidation, hypothèses, inconnues et impact option lorsque pertinent.

Niveaux :

- S+ : 36–40, allocation analytique 10–15 % maximum ;
- S : 32–35, allocation analytique 7–10 % ;
- A : 28–31, allocation analytique 3–5 % ;
- B : 24–27, allocation analytique 1–2 % ;
- <24 : refus ou surveillance.

Ces allocations sont des plafonds analytiques. Elles ne déclenchent jamais un ordre.

Règles de position :

- portefeuille idéal : 8 à 15 lignes ;
- ne jamais renforcer une position perdante ;
- renforcer seulement après confirmation : cassure, résultats solides, révisions ou tendance validée ;
- réévaluer les gagnants selon la thèse ;
- ne pas vendre automatiquement à +100 % ;
- sécurisation partielle indicative : 25 à 50 %, runner conservé si la thèse reste valide.

## 7. Score Skyler /40

Le score cible est :

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

Le score ne contourne jamais les hard gates.

Hard gates minimum :

- R:R structurel inférieur à 2:1 ;
- invalidation absente ;
- qualité des données critique insuffisante ;
- désaccord de sources non résolu ;
- spread option excessif ;
- OI insuffisant ;
- DTE incompatible avec le mandat ;
- thèse cassée ;
- position perdante proposée au renforcement ;
- concentration portefeuille excessive ;
- quota options dépassé ;
- risque théorique illimité non signalé ;
- probabilité de doublement insuffisante pour une option directionnelle lorsque cette règle est activée.

## 8. Horizons options

Séparer strictement :

| Univers | DTE |
|---|---:|
| TACTICAL | 20–60 |
| SWING | 60–180 |
| LEAPS | 180–540 |

Profil LEAPS principal :

- delta privilégié : 0,70 à 0,90 ;
- échéance : 6 à 18 mois ;
- open interest élevé ;
- spread faible ;
- catalyseur identifiable ;
- liquidité suffisante ;
- invalidation claire ;
- coût total et perte maximale explicites ;
- scénarios spot × temps × IV ;
- risque d’IV crush explicite ;
- probabilité de doublement estimée et étiquetée.

Les stratégies à jambes vendues ne peuvent jamais être recommandées si le profil actif les interdit. Elles peuvent être analysées en laboratoire uniquement, avec risque illimité explicitement signalé.

## 9. Architecture Skyler obligatoire

Créer progressivement des contrats typés et testés :

- `MarketContext`
- `CompanyContext`
- `CatalystContext`
- `TechnicalContext`
- `InstitutionalContext`
- `OptionsContext`
- `PortfolioContext`
- `DataQualityContext`
- `ScenarioSet`
- `SkylerPacket`
- `SkylerDecision`
- `AuditTrail`

Chaque fait chiffré doit idéalement respecter :

```json
{
  "value": 42.5,
  "unit": "%",
  "source": "IBKR",
  "as_of": "2026-08-04T20:15:00Z",
  "status": "LIVE",
  "estimated": false
}
```

La couche Claude reçoit un packet réduit, sérialisable et dépourvu de secrets. Elle rédige, compare, explique et met en évidence les contradictions. Elle ne remplace pas le score, les probabilités, les Greeks ou le moteur de risque.

## 10. Lots obligatoires

### AUDIT — Convergence réelle

Objectif : comparer `main`, `agent/vertex-total-rebuild`, `agent/vertex-neon-glass-graphs` et `integration/vertex-skyler-v2`.

Livrables :

- `docs/skyler/BRANCH_CONVERGENCE_AUDIT.md`
- inventaire des commits uniques ;
- inventaire des moteurs et pages divergents ;
- risques de conflit ;
- décision de source canonique par domaine ;
- aucun changement runtime.

### LOT 0 — Gouvernance et baseline

- confirmer branche et SHA ;
- exécuter compileall et pytest ;
- vérifier routes, console, responsive, READONLY ;
- mesurer fichiers, routes, endpoints, moteurs, graphiques et tests ;
- créer `docs/skyler/BASELINE.md` ;
- créer `docs/skyler/STATUS.md`.

### LOT 1 — Correctness options

Périmètre exclusif : mathématiques, unités, validation et garde-fous.

Minimum :

- corriger les pertes théoriquement illimitées des expositions nettes vendeuses de calls ;
- ajouter `max_loss_unbounded` ;
- rendre l’unité d’IV explicite ;
- ajouter taux/dividende configurables et traçables ;
- valider spot, strike, prime, quantité, DTE, IV ;
- intégrer spread/slippage dans les analyses qui prétendent mesurer un rendement exécutable ;
- filtrer les stratégies selon le profil actif ;
- cas manuels et tests de propriété.

Interdit dans ce lot : refonte page, nouveau thème, nouvelle news, nouveau scoring global.

### LOT 2 — Constitution stratégique V2

- créer une nouvelle version de profil ;
- ne jamais modifier la V1 ;
- intégrer niveaux S+/S/A/B ;
- 8–15 positions ;
- LEAPS 180–540 DTE et delta 0,70–0,90 ;
- règles gagnants/perdants ;
- versioning, diff et rollback testés.

### LOT 3 — Market Intelligence

- créer un `MarketContext` canonique ;
- indices, breadth, VIX, terme de vol, taux, courbe, dollar, crédit, liquidité, dispersion, cross-asset et secteurs ;
- transitions de régime ;
- « ce qui a changé depuis la dernière session » ;
- sources et fraîcheur par dimension.

### LOT 4 — News, catalyseurs et anomalies

- série OHLCV canonique ;
- timeline d’événements ;
- déduplication news ;
- classification impact/horizon/confiance ;
- révisions analystes ;
- anomalies prix, volume, options et fondamentales ;
- aucun OHLCV artificiel présenté comme réel.

### LOT 5 — Skyler Core

- contrats typés ;
- score /40 ;
- hard gates ;
- scénarios probabilistes ;
- faits vs interprétations ;
- audit trail ;
- contradiction detector ;
- réponse déterministe même sans Claude.

### LOT 6 — Options Intelligence

- scanners TACTICAL/SWING/LEAPS séparés ;
- calls et puts longs ;
- delta, gamma, theta, vega, vanna, vomma, charm ;
- IV rank, IV percentile, skew, term structure ;
- expected move ;
- GEX, walls et zero gamma ;
- spot × temps × IV ;
- risque earnings et IV crush ;
- probabilité de doublement avec modèle documenté.

### LOT 7 — Portfolio Intelligence

- sizing S+/S/A/B ;
- budget de risque ;
- corrélations et concentrations ;
- compatibilité portefeuille ;
- remplacement ;
- renforcement des gagnants seulement ;
- sécurisation partielle ;
- stress tests et drawdown.

### LOT 8 — Expérience Neon Glass

Ordre page par page :

1. Aujourd’hui
2. Marchés
3. Opportunités
4. Analyse
5. Portefeuille
6. Options
7. Journal
8. Système

Une page doit répondre en moins de dix secondes :

- qu’est-ce qui a changé ?
- pourquoi est-ce important ?
- quel est le risque ?
- qu’est-ce qui invalide la thèse ?
- quelle est la prochaine action analytique autorisée ?

### LOT 9 — Calibration et release candidate

- Brier score ;
- calibration des probabilités ;
- résultats par régime et niveau ;
- MAE/MFE ;
- dérive des scores ;
- faux positifs ;
- benchmark SPY ;
- audit sécurité/performance/accessibilité ;
- documentation release et rollback.

## 11. Procédure obligatoire pour chaque lot

1. Lire tous les fichiers de référence de ce skill.
2. Confirmer la branche et le SHA.
3. Vérifier que le lot précédent est validé.
4. Produire un audit ciblé avant code.
5. Écrire les tests rouges pour tout défaut de calcul.
6. Implémenter le minimum nécessaire.
7. Exécuter les validations du lot.
8. Tester en navigateur lorsque l’UI change.
9. Créer un rapport depuis `templates/LOT_REPORT.md`.
10. Mettre à jour `docs/skyler/STATUS.md`.
11. Committer uniquement les fichiers du lot.
12. Ouvrir ou mettre à jour une PR brouillon.
13. S’arrêter.

## 12. Validation minimale

À adapter au lot, mais ne jamais omettre :

```bash
python -m compileall -q terminal.py vertex
python -m pytest tests/ -q
python -m pytest tests/test_no_orders.py -q
```

Puis :

- `/healthz` ;
- `/api/client-log` = 0 erreur applicative ;
- mode `DEMO=1 NO_IBKR=1` ;
- mode sans IBKR ;
- données absentes, stale, demo, insufficient et offline ;
- 390, 768, 1440 et 1920 px si UI ;
- clavier, focus et reduced-motion si UI ;
- service worker bump si shell visible modifié ;
- aucun secret ou fichier runtime ajouté au diff.

## 13. Interdictions explicites

- Ne pas faire une refonte big-bang.
- Ne pas avancer plusieurs lots dans une seule session.
- Ne pas modifier un moteur pour rendre un visuel plus séduisant.
- Ne pas changer un test uniquement pour accepter un résultat faux.
- Ne pas utiliser une valeur par défaut silencieuse pour masquer une absence critique.
- Ne pas confondre force relative et sentiment.
- Ne pas noter un catalyseur uniquement parce qu’une date de résultats existe.
- Ne pas recommander une stratégie interdite par le profil actif.
- Ne pas présenter GEX, max pain, flux ou dealer positioning comme une vérité certaine sans convention et limites.
- Ne pas afficher une probabilité sans modèle et hypothèses.
- Ne pas continuer après un échec de test critique.
- Ne jamais déclarer « terminé » sans preuves.

## 14. Format de rapport obligatoire

Chaque rapport contient :

- Constat ;
- Problème ;
- Décision ;
- Implémentation ;
- Fichiers modifiés ;
- Tests exécutés et résultats exacts ;
- Validation navigateur ;
- Invariants vérifiés ;
- Risques restants ;
- Diff avec le lot précédent ;
- Verdict `GO`, `GO AVEC RÉSERVES` ou `NO-GO` ;
- prochaine étape autorisée ;
- phrase explicite : `Arrêt après ce lot — validation humaine requise.`

## 15. Première mission

La première exécution doit être :

```text
/vertex-skyler-v2 audit
```

Elle ne modifie aucun moteur ni aucune page. Elle produit uniquement l’audit de convergence des branches, l’état exact de Skyler/Neon Glass/RC1 et la recommandation de branche canonique.

Après validation humaine, exécuter `lot-0`, puis s’arrêter de nouveau.
