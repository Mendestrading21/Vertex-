# SKYLER LOT 214 — Audit d'invariants CLAUDE.md : desk sync + sanitize_news (constat)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-214` (base : lot 213 fusionné)

## Objet

Vérifier par CONSTAT MESURÉ (pas sur parole) deux invariants critiques de
CLAUDE.md : la règle n° 1 (clés de sync desk dans les 4 listes) et la
règle n° 5 (tout texte news externe passe par `sanitize_news` avant d'être
servi — XSS, rendus en innerHTML).

## Constat 1 — Desk sync : invariant TENU

- Gardien `test_desk_sync_keys_single_source_of_truth` relancé isolément :
  **1 passed**.
- Comptage direct : `__DESK_KEYS` (terminal.py) = **17 clés** ;
  `DESK_KEYS` (vx_kit.py) = **17 clés identiques** ; journal.py ne porte
  pas de liste Python nommée mais les 17 clés inline dans le JS
  `jvSyncPush` (L152) — c'est exactement ce que le gardien vérifie
  (`assert full in journal.JS` pour chaque clé).

## Constat 2 — sanitize_news : invariant TENU (faux positif écarté)

Cartographie exhaustive des sorties de news :

| Point de sortie | Verdict |
|---|---|
| `vertex/app/routes/content.py` L32 | SANITIZED ✔ |
| `vertex/app/routes/analysis_api.py` L120 (`api_skyler`) | SANITIZED ✔ |
| `vertex/app/routes/analysis_api.py` L740 (`api_events`) | SANITIZED ✔ |
| `vertex/services/skyler_sweep.py` L46 | SANITIZED ✔ |
| `terminal.py` L1157 et L1589 | SANITIZED ✔ |
| `vertex/app/routes/system.py` (`system_status_ep`) | **FAUX POSITIF** |

Le scan avait signalé `system_status_ep` (« contient 'news' + jsonify sans
sanitize_news »). Vérification du corps réel : le champ `'news'` y est un
**seuil de fraîcheur interne** (`thresholds = {..., 'news': 3600}`) et
`build_system_status` (status_service.py L44-45, L83) ne sert pour news
que `age_s` (nombre) et `state` (enum calculé par `_freshness`). **Aucun
titre ni texte externe ne transite par cette route** — rien à assainir.

Gardien XSS existant relancé : `test_xss_exits_lot177.py` → **6 passed**.

## Décision SW

**Pas de bump** (`td-shell-v171` inchangé) : lot de constat pur — aucun
code produit touché, rien à déployer. Conforme à la doctrine (lots
204/205/206/207/208/210 idem).

## Preuves

- Suite complète : **2472 passed / 2 skipped** (référence maintenue).
- Aucun fichier produit modifié — diff limité aux docs.

## Suite

LOT 215 : MINI-BILAN 211-215 + entretien suivant. Purge terminal.py
toujours EN ATTENTE d'accord humain explicite.
