# Lot 12A — Laboratoire de stratégies reproductible (RAPPORT)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Livré

**NEUF** `vertex/research/contracts.py` :

- `StrategySpec` — 22 champs requis (identité/version, famille admise parmi
  les 10 du skill + thèse économique, univers **point-in-time**, classe
  d'actif, timeframe, entrée/sortie/invalidation, sizing théorique,
  contraintes, benchmark, calendrier de décision, données requises, coûts,
  slippage, liquidité, périodes d'entraînement ET de validation, seed,
  propriétaire moteur). `seed=0` valide (absence = sentinelles vides, jamais
  falsy). `manifest()` = JSON canonique trié + **sha256** : même spec →
  même hash, tout paramètre changé → hash changé (replay déterministe
  adressable, zéro changement silencieux).
- `StrategyEvidence` — métriques minimales co-obligatoires (rendement,
  drawdown, exposition, turnover, coûts) + population/observations/
  stabilité/qualité/biais connus ; 4 statuts ; `VALIDÉ_HORS_ÉCHANTILLON`
  **exige** `preuves.walk_forward.passed=True`.
- `tableau_comparatif()` — axes minimaux toujours co-présents, paramètre
  `tri` **refusé** (classement sur ratio unique interdit par contrat).

Existant conservé tel quel (déjà sain, mesuré) : cycle de vie + 12
contrôles de biais (`factory.py`), walk-forward avec embargo, coûts,
registre conservant les essais REJECTED.

## Preuves

- `tests/test_labo_strategies_lot12a.py` : 12 bancs — 9 **nés rouges** →
  verts ; 2 gardiens de séparation nés verts à raison (caractérisation
  AST : `vertex/research/**` ⟂ advice/skyler_core/executive_engine, dans
  les deux sens — « aucun backtest ne modifie AdviceResult ») ; 1
  contre-épreuve seed=0.
- Suite complète : **4354 passés · 153 ignorés · 0 échec** (134 s).

## Limites consignées

- Contrats purs, pas encore branchés à une UI : le labo reste une sous-vue
  d'Analyse/Simulateur, widgets (StrategyMatrix, WalkForwardTimeline…) en
  phase D.
- Registre en mémoire (pas de persistance) : ADR requis quand un usage
  réel le justifie.
- Corrections de multiplicité des essais (point 10 du pipeline
  anti-illusion) : non couvert ici, consigné.

## Rollback

`git revert` du commit du lot.
