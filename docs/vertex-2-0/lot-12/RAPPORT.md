# Lot 12 — Pipeline opportunités (RAPPORT)

Date : 2026-08-28 · Branche : `agent/vertex-2-0-integration-20260828`

## Livré

`vertex/opportunities/funnel.py` + route `/api/opportunities/funnel` :

1. **Gate canonique dans l'entonnoir** : un candidat au régime inconnu
   (`None`/`''`/`UNKNOWN`/`INCONNU`) n'est plus jamais « actionnable »,
   quel que soit son score — aligné sur le hard gate de `decide.py`
   (« régime de marché inconnu → pas de nouveau risque ») ; un score de 99
   ne contourne pas non plus `rr_ok` (contre-épreuve au banc).
2. **Point-in-time** : la réponse porte `as_of` (= `scan_state['scan_ts']`).
3. **Delta depuis le scan précédent** : `delta {entrants, sortants,
   baseline_ts, premier_scan}` — memo en mémoire à rotation par `scan_ts`
   (GET sans écriture persistée ; deux GET du même scan → même delta).
   Premier scan → listes vides et `premier_scan: true`, jamais un delta
   inventé ; `scan_ts` absent → `disponible: false` honnête.
4. **Déduplication** : symbole en double compté une fois (meilleur score
   conservé), `duplicates_dropped` déclaré.
5. **Budgets déclarés** : `budgets {actionable_symbols: 5, entrants: 10,
   sortants: 10}` — les coupes de surfaçage ne sont plus implicites.

## Preuves

- `tests/test_entonnoir_lot12.py` : 11 bancs **nés rouges** → verts
  (gates, dedup, budgets, delta, stabilité intra-scan, route).
- Banc historique `test_opportunity_funnel.py` réécrit vers le contrat
  cible (jamais écarté) : `_row` porte désormais un régime connu par
  défaut, intention documentée dans le code.
- Suite complète : **4342 passés · 153 ignorés · 0 échec** (137 s).

## Contrats

Champs ajoutés seulement (`as_of`, `delta`, `duplicates_dropped`,
`budgets`) — aucun champ retiré, page existante intacte. Aucun store
persisté nouveau ; pas de changement de shell → pas de bump SW.

## Limites consignées

- L'affichage du delta (« changements depuis le dernier scan ») dans la
  vue Radar de la page Opportunités : branchement UI en phase D.
- Priorisation calendrier portefeuille/watchlist : contrat de la page
  Calendrier, phase D.
- Le memo delta est par processus : sous plusieurs workers WSGI, chaque
  worker a sa baseline (même limite que les caches mémoire existants).

## Rollback

`git revert` du commit du lot.
