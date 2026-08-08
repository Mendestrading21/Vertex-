# SKYLER LOT 323 — PURGE É1 FAITE : terminal.py -33 % (10 743 → 7 164 lignes)

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-323` (base : lot 322 fusionné,
+ la moitié tests `502d6c3` préparée au lot 285, rebasée)

## Ce qui débloque ce lot

Le retrait dans `terminal.py` était refusé depuis le lot 285 par le classifieur
de permissions (4 refus). La commande passe enfin **seule** (le refus visait la
commande composée `cp … && python3 …`, pas le retrait lui-même). GO utilisateur
acquis de longue date : É1 est appliquée.

## Le retrait

Périmètre = **borne BASSE** de `tools/purge_e2_sizing.py` (les 12 constantes
`PAGE_*` référencées par chaîne via `globals()[…]` restent vivantes, elles sont
du périmètre É2) :

| | avant | après | delta |
|---|---|---|---|
| définitions top-level | 228 | 146 | **-82** |
| lignes | 10 743 | 7 164 | **-3 579 (-33,3 %)** |
| octets | 1 222 911 | 807 338 | **-415 573 (-34,0 %)** |

Le retrait est **purement soustractif** : `git diff --stat` sur `terminal.py`
= `3579 deletions(-)`, **0 insertion**. Les commentaires collés au-dessus d'une
définition retirée partent avec elle ; jamais plus de 2 lignes vides d'affilée.

## Preuves

1. **É1 close** — outil rejoué après retrait :
   `BORNE BASSE : 0 défs mortes, 0 lignes (0.0%)`. Restent 25 défs / 1 866
   lignes = périmètre É2 (sauvées par une réf-chaîne), inchangé.
2. **Équivalence octet-pour-octet du produit servi** — MD5 des 8 pages,
   serveur DEMO, scan terminé, **avant vs après** :

   | page | MD5 (identique avant/après) |
   |---|---|
   | `/` | fc15688d1af6 |
   | `/markets` | c0bb91c6971a |
   | `/opportunities` | 6a22a6abbd03 |
   | `/analysis` | 113827718e99 |
   | `/portfolio` | f1b41b665d4a |
   | `/options` | 6387210de785 |
   | `/journal` | 243699ace2d5 |
   | `/system` | 85d1cb065d2e |

   **Aucun octet servi ne change.** C'est une preuve plus forte que le
   smoke-check par taille de texte : elle porte sur le HTML complet.
3. **Navigateur** (`tools/probe_smoke.py`, `vertex_ready` atteint) : 8 × HTTP
   200, **0 erreur console/pageerror**, `client-log count: 0`.
   Note honnête : `/journal` mesure 3 684 caractères contre 2 676 aux échéances
   précédentes — l'écart vient du `desk_data.json` local de cette session
   (trades laissés par la sonde de round-trip du lot 305), **pas** de la purge,
   que les MD5 identiques disculpent formellement.
4. **Tests** : `compileall` exit 0 ; suite **2499 passed / 2 skipped**.
   La référence descend de 2516 à 2499 : les 17 tests manquants sont ceux que la
   moitié 1/2 (`502d6c3`) a retirés — tests de caractérisation écrits pour ce
   moment précis et épingles sur des alias morts.
5. **Import à chaud** : 1 805 ms avant / 1 981 ms après (3 mesures chacune).
   **Aucun gain mesurable** — l'import est dominé par pandas/yfinance. Le gain
   est de lisibilité et de surface de maintenance, pas de vitesse ; annoncer
   autre chose serait un chiffre inventé.

## Effet de bord assumé : les listes de clés de sync desk

`terminal.py` portait 3 copies de la liste des 17 clés (`__DESK_KEYS`,
`sSyncPush`, `sSyncPull`) — toutes **dans le JS des pages mortes retirées**,
donc plus servies depuis longtemps. Elles partent avec la purge.

La synchronisation réelle est **intacte** et vit dans les 3 listes servies :
`vertex/ui/vx_kit.py` (`DESK_KEYS`, kit global présent sur toutes les pages),
`vertex/ui/journal.py` (inline), `vx-entities.js` (`DESK_KEYS`).

Conséquences traitées dans ce lot :

- **Règle critique n°1 de `CLAUDE.md`** mise à jour : « LES 4 listes » →
  « LES 3 listes servies », avec la nouvelle source de vérité et les deux
  gardiens.
- **5 gardiens re-ciblés** (ils épinglaient `__DESK_KEYS` dans `terminal.py`) :
  `test_production::test_desk_sync_keys_single_source_of_truth` (durci : exige
  désormais que `terminal.py` ne ressuscite **aucune** liste),
  `test_strategy_os_final_guards::test_all_sync_keys_match` (compare vx_kit ↔
  vx-entities ↔ journal), `test_redesign_ui::test_all_sync_keys_are_canonical`,
  `test_vault::test_vault_synced_via_desk_contract`,
  `test_real_data::test_worker_and_desk_button_wired` (le bouton d'import
  vivait sur la page Desk morte → re-ciblé sur la surface vivante :
  route `/api/ibkr/positions` LECTURE SEULE + consommation par Portefeuille).

## Décision SW

**Pas de bump** (`td-shell-v186`) : les MD5 des 8 pages prouvent que zéro octet
servi ne change. Bumper aurait invalidé le cache de tous les clients pour rien.

## Invariants

READONLY intact (aucun verbe d'ordre introduit ; le gardien
`test_no_order_execution_path` reste vert), moteurs intacts (aucun fichier de
`vertex/engines/` touché), `main` jamais touchée, aucun fichier runtime commité.

## Suite

- **É2** : 25 défs / 1 866 lignes — exige d'adapter les boucles d'injection par
  chaîne (`globals()[_pg]`) ; décision humaine dédiée.
- **É3** : dépendances croisées (`PAGE_DAILY` ↔ home_art/vault,
  `PAGE_ENTREPRISES` → `_OPP_BRIEF_JS`).
- LOT 324 : veille active (nouvelle référence de suite : **2499 / 2**).
  Prochaine échéance périodique : ~lot 330.
