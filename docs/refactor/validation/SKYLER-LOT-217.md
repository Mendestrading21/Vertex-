# SKYLER LOT 217 — Invariant scan_state « jamais réassigné » : constat + gardien AST

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-217` (base : lot 216 fusionné)

## Objet

Poursuite de l'audit d'invariants CLAUDE.md : « État partagé :
`vertex/app/state.py` (`scan_state` muté en place — ne JAMAIS
réassigner) ». Casser cet invariant est silencieux et grave : la boucle
de fond et les routes garderaient des objets DIFFÉRENTS — pages figées
sans aucune erreur.

## Constat mesuré — invariant TENU, mais gardé par AUCUN test

Scan AST du code produit (terminal.py + vertex/**, trois formes
interdites : réassignation module-level hors state.py, affectation
d'attribut `<obj>.scan_state = …`, `global scan_state`) :

- **0 offenseur.** La seule affectation module-level est la définition
  dans `state.py` L15 (le domicile unique).
- Les 5 occurrences `scan_state = scan_state or {}` (session_snapshot,
  session_digest, market_context, skyler_sweep, copilot) sont des
  rebinds LOCAUX de paramètres de fonction — elles ne touchent pas
  l'objet partagé. Légitimes.
- Lacune : aucun des ~30 fichiers de tests utilisant scan_state ne
  vérifiait CET invariant (ils s'en servent comme fixture).

## Livré — gardien `tests/test_scan_state_invariant_lot217.py` (4 tests)

1. scan AST du code produit → 0 forme interdite (le vrai gardien) ;
2. le domicile unique existe et documente la doctrine (« jamais de
   réassignation ») ;
3. gardien du gardien : le scanner détecte bien les 3 formes interdites
   sur un exemple synthétique (s'il se cassait, il passerait à vide) ;
4. le rebind local de paramètre reste légitime (pas de faux positif).

## Décision SW

**Pas de bump** (`td-shell-v171` inchangé) : tests seulement, aucun
code produit touché.

## Preuves

- Nouveau gardien : **4/4 passed**.
- Suite complète : **2479 passed / 2 skipped** (2475 + 4).

## Suite

LOT 218 : entretien suivant utile ou directive. Purge terminal.py
toujours EN ATTENTE d'accord humain explicite.
