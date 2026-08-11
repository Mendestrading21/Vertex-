# SKYLER LOT 301 — Robustesse : API coupées → états honnêtes ; sondeurs outillés

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-301` (base : lot 300 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — couper des API en vol (angle neuf)

7 cas testés en navigateur réel (interception réseau, abort, attente
9 s) : `/` sans editorial, `/` sans command, `/markets` sans
market/summary, `/opportunities` sans /scan, `/system` sans
system-status (+2 approfondissements).

**Verdict : SAIN sur les 7 cas.**
- États HONNÊTES quand la donnée manque : « indisponible » (briefing,
  command), « ERREUR / indisponible » ×5 (system) ;
- **0 squelette éternel**, 0 texte cassé (NaN/undefined), 0 erreur
  console inattendue ;
- Deux faits d'architecture mesurés : `/markets` n'appelle PAS
  `/api/market/summary` au chargement (0 requête interceptée — la page
  vit d'autres endpoints) ; `/opportunities` privée de `/scan` reste
  complète (le radar vit de `/api/command`) — résilience par
  endpoint réel, pas par invention.

Aucun défaut → aucun changement produit (changement gratuit refusé).

## Livré — les sondeurs deviennent des OUTILS commités

Les sondeurs vivaient dans le scratchpad (effacé entre conteneurs) et
ont été réécrits à chaque campagne. Commités en outils officiels,
en-têtes d'usage + références :

- `docs/refactor/validation/tools/probe_smoke.py` — protocole lot 251
  (8 pages, erreurs, client-log, tailles vs référence lot 300) ;
- `docs/refactor/validation/tools/probe_error_states.py` — le sondeur
  de ce lot (cas + verdict de référence documentés).

(compileall vert ; outils hors runtime — aucun octet servi ne change.)

## Preuves

- Sortie complète des 7 cas dans ce rapport (section calibrage).
- Suite complète : **2514 passed / 2 skipped** (référence maintenue).

## Décision SW

**Pas de bump** (`td-shell-v185`) : outils/docs seulement.

## Suite

LOT 302 : purge É1 en PRIORITÉ dès déblocage ; sinon développement.
