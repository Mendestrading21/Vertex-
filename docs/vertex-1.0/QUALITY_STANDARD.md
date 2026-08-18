# Vertex 1.0 — Quality Standard

Ce document définit le niveau minimum acceptable pour toute capacité active de Vertex.

## Principe

Une fonctionnalité n'est pas terminée parce qu'elle s'affiche. Elle est terminée lorsque sa donnée est correcte, traçable, fraîche, testée, explicable, accessible, observable et réversible.

## 1. Données

Chaque valeur financière exploitable expose ou permet de retrouver :

- source canonique ;
- timestamp de la donnée ;
- timestamp de réception ;
- unité et devise ;
- état `LIVE`, `DELAYED`, `STALE`, `DEMO`, `OFFLINE` ou `MISSING` ;
- qualité/confiance distincte de la conviction d'investissement ;
- erreur ou raison de l'absence.

Interdictions : zéro de substitution silencieux, donnée fictive non marquée, fallback invisible, mélange compte réel/démo.

## 2. Décision

Une décision doit être reproductible depuis un packet versionné contenant : faits, hypothèses, thèse, contre-thèse, catalyseurs, invalidation, scénarios, risques, hard gates, compatibilité portefeuille, versions des moteurs et du profil.

Le score ne contourne jamais un hard gate. Une probabilité non calibrée est étiquetée comme telle.

## 3. Options

Pour une option candidate : contrat exact, spot, strike, expiration/DTE, bid/ask/mid, spread %, volume, OI, IV, Greeks, quote age, coût total, perte maximale, événements et scénarios spot/temps/IV doivent être disponibles ou explicitement manquants.

Le mandat de release reste : options longues, revues 2/4/6 semaines, DTE préféré 120–240 jours, cible 180 jours.

## 4. Actions

Toute recommandation analytique d'action porte un horizon explicite 3/6/12 mois, une thèse, des catalyseurs, une invalidation et une compatibilité portefeuille.

## 5. WMB

WMB fournit du contexte macro et des catalyseurs avec provenance. Il ne fournit jamais le prix canonique, les Greeks ou une autorisation de contourner les règles de risque.

## 6. IA

L'IA peut expliquer, résumer, comparer et mettre en évidence les contradictions. Elle ne devient jamais propriétaire d'un calcul financier, d'un score, d'un hard gate, d'une limite ou d'un verdict.

## 7. Interface

Chaque espace répond à une question principale. Tout chiffre important montre son unité et, lorsque pertinent, sa source/fraîcheur. Les états critiques ne sont jamais communiqués uniquement par couleur.

Exigences : desktop, mobile, clavier, focus visible, contraste, reduced motion, erreurs applicatives observables et panne partielle compréhensible.

## 8. Performance et fiabilité

Aucun worker ne démarre deux fois. Les appels réseau possèdent timeout et comportement dégradé. Les caches ont un propriétaire et une politique de fraîcheur. Les écritures utilisateur sont atomiques ou transactionnelles et sauvegardables.

## 9. Sécurité

- `READONLY=True` et `ANALYSIS_ONLY=True` ;
- IBKR `readonly=True` ;
- aucun ordre, ticket exécutable ou chemin de transmission ;
- aucun secret ou donnée de compte dans Git, logs IA ou fixtures publiques ;
- webhook TradingView authentifié, dédupliqué et anti-replay.

## 10. Définition de terminé

Une PR de production doit fournir : tests, provenance, état dégradé, observabilité, compatibilité/migration, risques et rollback. Une release nécessite toutes les preuves sur le même SHA.
