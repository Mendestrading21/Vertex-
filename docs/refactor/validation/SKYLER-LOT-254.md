# SKYLER LOT 254 — Audit de l'invariant « fichiers runtime jamais commités »

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-254` (base : lot 253 fusionné)

## Objet

La règle Git de CLAUDE.md (« données runtime : gitignorées, jamais
commitées ») est le seul invariant de la liste jamais audité
formellement pendant la campagne de preuve. Ce lot le mesure.

## Protocole (3 volets)

1. `git ls-files` × motifs runtime interdits (edge_ledger, desk_backup,
   desk_data, track_meta, alerts_fired, .env, .vertex_secret,
   skyler_*, caches, pyc) ;
2. `git ls-files -ci --exclude-standard` — fichiers traqués qui
   seraient ignorés (incohérences) ;
3. Croisement .gitignore ↔ sites d'ÉCRITURE réels de l'app (grep des
   `_save_json`/constantes de fichiers dans terminal.py et
   vertex/engines/*).

## Résultat — INVARIANT TENU (0 correctif nécessaire)

- **Volet 1 : 0 fichier runtime traqué.** L'unique match textuel est
  `tests/test_desk_backup_lot178.py` — un fichier de TEST dont le nom
  contient le motif, pas une donnée.
- **Volet 2 : 0 incohérence** traqué/ignoré.
- **Volet 3 : couverture 100 % des sites d'écriture réels.** L'app
  écrit exactement `skyler_memory.json` (decision_memory.py),
  `skyler_sessions.json` (session_log.py), `skyler_decisions.json`
  (skyler_journal.py) et `alerts_fired.json` (terminal.py L10599/
  10638) — tous les quatre listés dans .gitignore. Les caches
  (`constituents_cache`, `session_digest_cache`, `analyst_cache`) sont
  couverts par le motif générique `*_cache.json` (l. 20). Les jokers
  du rituel de nettoyage (`skyler_*.json`, `alerts_fired*.json`) sont
  de la ceinture-bretelles : aucun fichier réel ne correspond aux
  variantes.

Gardiens existants confirmés en place : `test_session_log_lot15` et
`test_decision_memory_lot10` vérifient déjà la présence de leurs
entrées dans .gitignore.

**0 défaut → 0 changement** (la règle « jamais de changement gratuit »
tient). Docs seulement.

## Décision SW

**Pas de bump** (`td-shell-v173`).

## Preuves

- Commandes des 3 volets rejouables telles quelles.
- Suite complète : **2486 passed / 2 skipped**.

## Suite

LOT 255 : mini-bilan 251-255 attendu. La purge attend « GO purge
étape 1 ».
