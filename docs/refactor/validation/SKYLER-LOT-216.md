# SKYLER LOT 216 — Invariants n° 2 + IBKR : constat mesuré + gardien du timeout anti-blocage

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-216` (base : lot 215 fusionné)

## Objet

Poursuite de l'audit d'invariants CLAUDE.md (entamé au lot 214) sur les
deux règles restantes mesurables sans TWS : la règle n° 2 (apostrophes
françaises / syntaxe du JS généré) et la règle IBKR
(readonly=True + RequestTimeout=45).

## Constat 1 — Règle n° 2 (JS généré valide) : TENUE et déjà gardée

`tests/test_js_syntax_sweep_lot182.py` couvre l'invariant en entier :
chaque bloc `<script>` inline de **16 routes HTML** passe au vrai
parseur (`node --check`), plus les chaînes JS des modules
(sync_center.JS, heatmap du vault), avec un garde-fou de volume
(≥ 12 blocs réellement contrôlés) et un test de l'extracteur lui-même.
Une apostrophe non échappée casse la suite — rien à ajouter.

## Constat 2 — IBKR readonly : TENU et gardé 3 fois… mais PAS le timeout

- `readonly=True` : codé EN DUR dans `ibkr_gateway.py` (attribut de
  classe `READONLY = True` + `connect(..., readonly=True)`), inspecté
  par **3 gardiens** (test_no_orders — balayage dépôt entier,
  test_strategy_os_final_guards, test_data_sources L217). TENU.
- **Lacune réelle mesurée** : `grep RequestTimeout|TIMEOUT tests/` →
  **0 occurrence**. L'invariant CLAUDE.md « RequestTimeout=45 (ne pas
  retirer — anti-blocage) » n'était épinglé par AUCUN test : on pouvait
  retirer `ib.RequestTimeout = REQUEST_TIMEOUT_S` ou changer 45 sans
  rien casser, alors qu'un worker IBKR bloqué gèle l'app.

## Livré — gardien `tests/test_ibkr_timeout_lot216.py` (3 tests)

1. `REQUEST_TIMEOUT_S == 45` (la valeur de l'invariant) ;
2. la connexion applique les DEUX bornes (`ib.RequestTimeout = …` +
   `readonly=True, timeout=REQUEST_TIMEOUT_S`) et `READONLY is True` —
   source inspectée, aucun TWS requis ;
3. `ibkr_scheduler.DEFAULT_TIMEOUT_S == ibkr_gateway.REQUEST_TIMEOUT_S`
   (le scheduler se documente « aligné » — si l'un bouge sans l'autre,
   le test casse au lieu de laisser dériver).

## Décision SW

**Pas de bump** (`td-shell-v171` inchangé) : tests seulement, aucun
code produit touché, rien à déployer.

## Preuves

- Nouveau gardien : **3/3 passed**.
- Suite complète : **2475 passed / 2 skipped** (2472 + 3).

## Suite

LOT 217 : entretien suivant utile ou directive. Purge terminal.py
toujours EN ATTENTE d'accord humain explicite.
