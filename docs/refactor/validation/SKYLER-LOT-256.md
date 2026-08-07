# SKYLER LOT 256 — Baseline de performance serveur (avant-purge)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-256` (base : lot 255 fusionné)

## Objet

La performance SERVEUR n'a jamais été chiffrée formellement (le lot 72
avait mesuré le client : DCL, budgets JS). Ce lot établit la baseline —
utile en soi, et référence AVANT/APRÈS pour la purge : terminal.py fait
aujourd'hui 10 743 lignes toutes parsées et exécutées à l'import, dont
~5 200 mortes (chiffrage lot 249) qui construisent des pages que
personne ne sert.

## Mesures (DEMO=1 NO_IBKR=1, machine de la session)

### Import de terminal.py (3 passes)

| Passe | Temps |
|---|---|
| 1 (à froid) | **11,68 s** |
| 2 (cache chaud) | 1,77 s |
| 3 (cache chaud) | 2,19 s |

### TTFB des 8 pages racines (curl, 3 mesures chacune, serveur chaud)

| Page | TTFB (3 passes) | Taille HTML |
|---|---|---|
| / | 1,9 / 1,7 / 1,6 ms | 40 057 o. |
| /markets | 1,6 / 1,7 / 1,7 ms | 71 089 o. |
| /opportunities | 1,7 / 1,7 / 1,5 ms | 67 278 o. |
| /analysis | 1,4 / 1,3 / 1,4 ms | 22 359 o. |
| /portfolio | 1,6 / 1,8 / 1,5 ms | 85 645 o. |
| /options | 1,4 / 1,4 / 1,4 ms | 24 686 o. |
| /journal | 1,4 / 1,5 / 1,6 ms | 56 093 o. |
| /system | 1,6 / 1,6 / 1,5 ms | 79 997 o. |

`/healthz` : 3,0 ms.

## Lecture honnête

- **Le service est instantané** : TTFB 1,3-1,9 ms partout — les pages
  sont des chaînes préconstruites, aucun problème à corriger.
- **Le coût du code mort est à l'IMPORT** : ~2 s à chaud, 11,7 s à
  froid, payés à chaque démarrage pour construire notamment des pages
  héritées jamais servies. C'est LA métrique que la purge devrait
  améliorer — à re-mesurer avec ce même protocole après É1/É2.
- Aucun changement de code : baseline documentée, rien à corriger.

## Décision SW

**Pas de bump** (`td-shell-v173`) : docs seulement.

## Preuves

- Protocole rejouable tel quel (3× import chronométré ; curl -w
  time_total ×3 sur les 8 pages, serveur DEMO chaud).
- Suite complète : **2486 passed / 2 skipped**.

## Suite

LOT 257 : entretien espacé ou directive. La purge attend « GO purge
étape 1 » — avec désormais sa baseline avant/après.
