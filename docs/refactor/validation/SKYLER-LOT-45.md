# SKYLER V2 — LOT 45 : restauration souveraine vérifiée

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-45-sovereign-import`
(base : `integration/vertex-skyler-v2` @ `f691cb9`) · Mode : développement
continu — REPRIS sur directive utilisateur (« continue à développer le
projet »), qui prime sur le cycle RC périodique.

## 1. Choix du lot — justification

L'export souverain (lots 29/42) est une sauvegarde **sans chemin de
retour** : une archive qu'on ne peut pas restaurer n'est souveraine qu'à
moitié. Si le disque meurt, le trader détient un fichier intègre… et
aucun moyen outillé de le réinjecter. Ce lot ferme le cycle
export → vérification → **restauration**.

## 2. Périmètre livré

### 2.1 Moteur — `decision_memory.merge_memory(current, imported)`

Restauration par **REJEU APPEND-ONLY** — la discipline du ledger
s'applique à l'import lui-même :

- chaque décision repasse par `append_decision` → un `decision_id` déjà
  présent n'est **JAMAIS remplacé** (l'historique local gagne — prouvé
  contre une archive falsifiée « RÉÉCRITURE HOSTILE ») ;
- chaque outcome repasse par `append_outcome` → monotone (seule une
  mesure couvrant STRICTEMENT plus de séances remplace) ;
- entrées non-dict comptées (`corrupted_entries`), jamais fatales ;
  import dégénéré → rien d'ajouté ; stats exactes retournées.

### 2.2 Route — `POST /api/skyler/memory/import`

- **l'empreinte `content_sha256` est VÉRIFIÉE AVANT toute écriture** :
  archive altérée → 400 `empreinte_invalide` et RIEN n'est écrit
  (prouvé : le magasin n'existe même pas après le refus) ; empreinte
  absente → 400 `empreinte_absente` ;
- bundle sans magasin mémoire → 400 `memoire_absente` ; corps
  dégénérés (non-JSON, liste, objet vide) → 400/415, jamais 500 ;
- succès → `stats` du rejeu + `ledger_health` du ledger fusionné +
  versions du bundle + note disant le périmètre : **ledger mémoire
  uniquement** (séances/journal restent au backlog — dit, pas caché).

Round-trip prouvé : un bundle produit par le VRAI export (empreinte
exacte) restaure la décision dans un magasin vide, et un magasin peuplé
garde sa version locale (« VÉRITÉ LOCALE ») face au même id importé.

Aucun changement de shell → **SW v106 inchangé** (API seulement ; un
bouton « Importer » UI est un candidat du prochain lot).

## 3. Méthode — rouge d'abord

`tests/test_sovereign_import_lot45.py` (9 tests) écrit AVANT ; confirmé
rouge : **9 failed**. Après : **9 passed** (un oubli d'import Flask
`request` attrapé par les tests en cours de lot — corrigé avant tout
commit).

## 4. Preuves

```text
python -m pytest tests/test_sovereign_import_lot45.py -q → 9 passed
python -m compileall -q terminal.py vertex               → exit 0
python -m pytest tests/ -q → 1615 passed, 2 skipped      (baseline 1606 → +9)
```

Moteur 0.9.0 inchangé (le rejeu réutilise les primitives append-only
existantes — aucune règle nouvelle, aucun champ figé nouveau).

## 5. Invariants tenus

- append-only INTACT jusque dans la restauration (l'historique local
  gagne, jamais de réécriture — prouvé contre falsification) ;
- empreinte vérifiée AVANT écriture ; archive altérée refusée et DIT ;
- périmètre honnête (mémoire seulement, dit dans la réponse) ;
- jamais 500 ; READONLY absolu (aucun ordre) ; fichiers runtime jamais
  commités ; `main` intacte ; SW inchangé.

## 6. Backlog (candidats lot 46)

1. Restauration étendue aux séances + journal (même rejeu honnête :
   `record_close` par jour, dédup journal) ;
2. Bouton « Importer » dans la carte Mémoire (upload fichier → POST,
   SW v107 + gardiens + preuve navigateur) ;
3. Toute amélioration constatée pendant le travail.

**Arrêt après ce lot — validation humaine requise.**
