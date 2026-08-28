# Décision, sources et IA

## Responsabilités

Les sources apportent des faits. Les moteurs déterministes calculent. Le moteur
exécutif assemble une orientation analytique. Claude explique et questionne.
L'utilisateur décide.

```text
faits sourcés
→ normalisation + qualité + point-in-time
→ moteurs spécialisés
→ scénarios + hard gates
→ DecisionPacket versionné
→ orientation analytique
→ explication Claude validée
→ décision humaine
```

## Packet canonique

Le packet conserve au minimum : instrument, identité, date d'observation,
sources, qualité, fondamentaux, technique, catalyseurs, sentiment qualifié,
contexte institutionnel, régime, anomalies, portefeuille déclaré, options,
scénarios, inconnues, contradictions, règles bloquantes, scores, orientation,
versions des moteurs et journal d'audit.

Chaque section peut être absente. Une absence réduit la couverture ; elle ne
devient pas un score neutre implicite.

Chaque champ conserve `value`, `kind` (`FACT`, `CALCULATION`, `ESTIMATE`,
`INTERPRETATION`), `unit`, `source`, `observed_at`, `age`, `quality`,
`fallback`, `citations` et `lineage`. Chaque packet porte `snapshot_id`,
versions de profil/moteurs et empreinte des intrants.

## Autorité unique

La cible publique est une seule fonction :

```text
AdviceEngine.evaluate(snapshot) -> AdviceResult
```

Executive, DecisionStack, Skyler, comité, scorecard, quant et moteurs
spécialisés convergent : un seul devient propriétaire du conseil ; les autres
produisent preuves, métriques ou contexte. Migrer chaque route et page, tester
la parité, mesurer l'usage, puis retirer l'ancien verdict. Un mapping de mots
ne résout pas des décisions contradictoires.

`AdviceResult` contient orientation, horizon, confiance décomposée, preuves,
contradictions, inconnues, bloqueurs, invalidation, scénarios, couverture,
versions et audit. Tous les endpoints et pages projettent ce même objet.

## Orientation

Les libellés `ACHETER`, `RENFORCER`, `ATTENDRE`, `RÉDUIRE`, `REFUSER` du
moteur existant sont des sorties analytiques et non des actes. L'interface doit
les présenter comme `Orientation Vertex`, avec date, horizon, confiance,
preuves, bloqueurs, invalidation et limites. Aucun ordre ou allocation n'en
découle automatiquement.

Un hard gate inconnu ou non implémenté échoue fermé. `UNKNOWN` ne vaut jamais
faux, neutre ou conforme. Utiliser un seul R:R structurel et interdire toute
cible artificielle. Une probabilité n'est publiée que si elle est calibrée hors
échantillon, versionnée, avec taille d'échantillon et incertitude ; sinon
employer `estimation de modèle`.

## Rôle de Claude

Autorisé : résumer, comparer, expliquer, relier, nommer les contradictions,
poser des questions, produire un brief et proposer une note/alerte/règle en
statut `PROPOSÉ`.

Interdit : collecter sans contrat, recalculer un indicateur, inventer un
chiffre, modifier un score/gate/verdict, activer une règle, écrire dans le
portefeuille, affirmer une certitude ou commander une action financière.

Toute sortie IA — analyste, copilote, brief ou enrichissement — passe par une
gateway unique : schéma strict, validation des nombres, citations, défense
contre prompt injection, redaction, consentement, outils autorisés, budget de
temps/coût/débit, cancellation, audit et fallback déterministe. Une troncature
de contexte possède un manifeste des éléments omis. Les prompts et réponses ne
contiennent ni secret ni donnée de compte ; le portefeuille est exclu par
défaut et minimisé seulement après action explicite.

## Pureté et temps de réponse

Une lecture GET ne journalise, ne mémorise et ne modifie rien. Geler une
orientation ou écrire une note emploie un POST explicite. Sources et IA sont
collectées hors du chemin de réponse ; la route sert un snapshot daté avec
état `LOADING/MISSING/STALE` au lieu d'attendre le réseau.

## Hiérarchie de confiance

1. publications officielles et documents d'émetteur ;
2. données de marché autorisées et horodatées ;
3. calculs des moteurs Vertex versionnés ;
4. sources éditoriales qualifiées et dédupliquées ;
5. alertes TradingView comme événement de réévaluation ;
6. saisies utilisateur ;
7. interprétation IA, toujours étiquetée.

Une source de rang inférieur ne remplace pas silencieusement une source plus
forte. Les désaccords restent visibles.

## Automatisation acceptable

Automatiser collectes, validation, recalculs, alertes, briefs, revues et
comparaisons. Ne jamais automatiser la décision humaine, l'exécution, la
modification d'une position ou l'activation d'une règle stratégique.
