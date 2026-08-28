# Lot 12 — Pipeline opportunités (WORK_MANIFEST)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Objectif unique

Entonnoir point-in-time, budgets explicites à chaque étage, déduplication,
delta depuis le scan précédent, et **aucun candidat ne contourne les gates
canoniques**.

## Constat mesuré

1. **Contournement de gate** : `funnel.is_actionable` = score ≥ 72 + `rr_ok`
   + verdict d'achat. Or le verdict de scan (`config.verdict`, strategy/config.py:51)
   ne rétrograde que le régime `CHOP` — un titre au régime **inconnu** garde
   son BUY et passe l'entonnoir, alors que le hard gate canonique
   (`decide.py:99` « régime de marché inconnu → pas de nouveau risque »,
   aligné ExecutiveEngine) l'interdit.
2. **Pas de point-in-time** : la réponse `/api/opportunities/funnel` n'a ni
   `as_of` ni delta — « changements depuis le dernier scan » (contrat Radar)
   impossible à afficher honnêtement.
3. **Pas de déduplication** : un symbole présent deux fois dans
   `scan_state['rows']` compte deux fois à chaque étage.
4. **Budgets implicites** : `actionable_symbols` coupé à 5 sans le déclarer.

## Fichiers propriétaires

- `vertex/opportunities/funnel.py` — gate régime inconnu, dedup + compte,
  budgets déclarés, `as_of`, memo de delta (`observe`, `reset_for_test`).
- `vertex/app/routes/opportunities_api.py` — passe `scan_ts`, expose le delta.
- **NEUF** `tests/test_entonnoir_lot12.py` — bancs rouges d'abord.

## Contrat de données

- Champs AJOUTÉS à la réponse (aucun retiré) : `as_of`, `duplicates_dropped`,
  `delta {entrants, sortants, baseline_ts, premier_scan}`, `budget` sur les
  listes surfacées. Premier scan → `premier_scan: true`, listes vides,
  JAMAIS un delta inventé.
- Le memo de delta est en mémoire processus (rotation par `scan_ts`) : GET
  sans effet de bord persisté ; `reset_for_test()` garde les bancs isolés.

## Hors périmètre (consigné)

- Priorisation calendrier portefeuille/watchlist : contrat de la page
  Calendrier, vérifiée en phase D.
- Vues Actions/ETF/Anomalies du centre Opportunités : page livrée au
  checkpoint graphique, re-validée en phase D contre le blueprint.

## Rollback

`git revert` du commit du lot — memo en mémoire seulement, aucun store.
