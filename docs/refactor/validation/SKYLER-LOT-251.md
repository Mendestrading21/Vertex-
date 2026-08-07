# SKYLER LOT 251 — Smoke-check santé post-tranche (conditions réelles)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-251` (base : lot 250 fusionné)

## Objet

Cinq lots docs-only viennent d'être fusionnés (246-250). Entretien
périodique légitime : re-mesurer en VRAI navigateur que la base
intégrée reste saine — pas une supposition, une mesure.

## Protocole

Serveur `DEMO=1 NO_IBKR=1 START_ON_IMPORT=1` port 5002 ; Playwright
(chromium-1194, 1440×900, `domcontentloaded` + 4 500 ms) ; écoute des
événements `console` (type error) et `pageerror` sur toute la session ;
puis `/api/client-log` et `/healthz`.

## Résultat — SAIN sur toute la ligne

| Page | HTTP | Titre | Texte rendu |
|---|---|---|---|
| / | 200 | Aujourd'hui · Vertex | 3 371 c. |
| /markets | 200 | Marchés · Vertex | 2 795 c. |
| /opportunities | 200 | Opportunités · Radar · Vertex | 4 680 c. |
| /analysis | 200 | Analyse · Vertex | 924 c. |
| /portfolio | 200 | Portefeuille · Synthèse · Vertex | 1 610 c. |
| /options | 200 | Options · Vertex | 2 956 c. |
| /journal | 200 | Journal · Vertex | 2 677 c. |
| /system | 200 | Système · Vertex | 3 898 c. |

- **0 erreur** console/pageerror sur les 8 chargements.
- `/api/client-log` : `{count: 0, errors: []}`.
- `/healthz` : `status ok`, `data_source demo`, 8 moteurs, scan 20/517.

**0 défaut → 0 changement de code** (la règle « jamais de changement
gratuit » s'applique aussi aux correctifs sans défaut).

## Décision SW

**Pas de bump** (`td-shell-v173`) : aucun octet servi modifié.

## Preuves

- Script rejouable : `smoke251.py` (scratchpad de session).
- Suite complète : **2486 passed / 2 skipped**.

## Suite

LOT 252 : entretien ou directive. La purge attend « GO purge étape 1 ».
