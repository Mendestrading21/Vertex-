# Lot 12A — Laboratoire de stratégies reproductible (WORK_MANIFEST)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Objectif unique

Contrats `StrategySpec` / `StrategyEvidence` + manifeste point-in-time à
replay déterministe + preuve de séparation stricte d'avec le conseil
canonique. Aucun classement sur un ratio unique.

## Constat mesuré

Existant sain (conservé tel quel) : `vertex/research/factory.py` — cycle
IDEA→…→APPROVED avec 12 contrôles de biais obligatoires, walk-forward avec
embargo anti look-ahead, coûts documentés ; `registry.py` conserve les
essais (y compris REJECTED). Manquent : les contrats NOMMÉS du skill
(champs requis exhaustifs : univers point-in-time, sizing, calendrier de
décision, slippage, liquidité, seed, propriétaire moteur…), le manifeste
immuable haché (replay), le statut d'évidence 4-états avec exigence
hors-échantillon, le tableau comparatif qui refuse le ratio unique, et le
gardien d'imports research ⟂ advice.

## Fichiers propriétaires

- **NEUF** `vertex/research/contracts.py` — `StrategySpec` (validation,
  familles admises, `manifest()` haché sha256), `StrategyEvidence`
  (métriques minimales, statuts, VALIDÉ_HORS_ÉCHANTILLON exige un
  walk-forward réussi), `tableau_comparatif()` (jamais un ratio seul).
- **NEUF** `tests/test_labo_strategies_lot12a.py` — bancs rouges + gardien
  de séparation (AST) : `vertex/research/**` n'importe jamais
  advice/skyler_core/executive_engine, et réciproquement.

## Contrat de données

Aucune route ni page nouvelle (le labo reste une sous-vue d'Analyse/
Simulateur, branchée en phase D). Aucun store persisté. Pur et testable.

## Hors périmètre (consigné)

Widgets du labo (StrategyMatrix, WalkForwardTimeline…) : phase D.
Persistance du registre : quand un usage réel le justifie (ADR sinon).

## Rollback

`git revert` du commit du lot.
