# SKYLER V2 — LOT 46 : restauration étendue (séances + journal)

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-46-full-restore`
(base : `integration/vertex-skyler-v2` @ `118d191`) · Mode : développement
continu (directive utilisateur).

## 1. Choix du lot — justification

Backlog proposé : (a) restauration étendue séances + journal, (b) bouton
« Importer » UI, (c) autre. Choix : **(a)** — le lot 45 disait
honnêtement son périmètre partiel (« séances/journal au backlog ») ;
le compléter d'abord rend le bundle ENTIÈREMENT restaurable avant de
poser un bouton UI dessus (l'UI du lot 47 s'appuiera sur un import
complet, pas partiel).

## 2. Périmètre livré

### 2.1 Moteurs — rejeu honnête, la donnée LOCALE gagne

- **`session_log.merge_log(current, imported)`** : n'ajoute que les
  séances (symbole, date) ABSENTES du log local — la clôture locale
  n'est JAMAIS remplacée par l'archive (le scan local est l'observation
  de référence ; nuance importante : `record_close` seul aurait laissé
  la « dernière observation » importée écraser la locale — le merge
  filtre AVANT rejeu). Dates malformées, clôtures non finies ou ≤ 0,
  entrées non-dict, listes manquantes → comptées, jamais fatales ;
- **`skyler_journal.merge_journal(current, imported)`** : n'ajoute que
  les entrées absentes, identifiées par le **même triple de dédup que
  `record`** — (symbol, as_of, decision), source unique de la règle —
  l'entrée locale gagne ; borné `MAX_ENTRIES` ; corrompues comptées.

### 2.2 Route — `POST /api/skyler/memory/import` étendue

Le MÊME bundle (même contrat d'empreinte, vérifiée AVANT toute
écriture — falsification d'une séance → 400 et AUCUN des trois magasins
écrit, prouvé) restaure désormais les TROIS magasins : mémoire (lot 45)
+ séances + journal. `stats` gagne les sous-objets `sessions` et
`journal` (comptes exacts par magasin) ; la note dit le périmètre
COMPLET — le mot « backlog » en a disparu (gardé par test).

## 3. Méthode — rouge d'abord

`tests/test_import_full_lot46.py` (7 tests) écrit AVANT ; confirmé
rouge : **5 failed / 2 passed** (les 2 verts : contrats du lot 45 déjà
tenus — locale gagne par absence de merge, empreinte déjà vérifiée).
Après : **7 passed**, et les 9 gardiens du lot 45 restent verts
(16 passed sur l'import au total).

Couverture : séances absentes ajoutées / locales jamais remplacées
(999.0 importée vs 100.0 locale → 100.0 gardée) ; corrompues comptées ;
journal même règle sur le triple de `record` ; sinistre simulé →
round-trip complet des trois magasins ; clôture locale divergente
intacte au niveau route ; falsification → rien écrit sur les trois.

## 4. Preuves

```text
python -m pytest tests/test_import_full_lot46.py \
                 tests/test_sovereign_import_lot45.py -q → 16 passed
python -m compileall -q terminal.py vertex               → exit 0
python -m pytest tests/ -q → 1622 passed, 2 skipped      (baseline 1615 → +7)
```

Moteur 0.9.0 et SW v106 inchangés (API/moteurs seulement — aucune règle
de décision, aucun champ figé, aucun shell).

## 5. Invariants tenus

- la donnée LOCALE gagne dans les trois magasins (prouvé contre archives
  falsifiées et divergentes) ; append-only intact ;
- empreinte vérifiée avant TOUTE écriture (aucun magasin touché sur
  refus — prouvé sur les trois) ;
- règles de dédup en source unique (triple de `record` réutilisé) ;
- entrées corrompues comptées, jamais fatales ; jamais 500 ;
- READONLY absolu ; fichiers runtime jamais commités ; `main` intacte.

## 6. Backlog (candidats lot 47)

1. Bouton « Importer » dans la carte Mémoire (upload fichier → POST →
   stats/erreur honnêtes ; SW v107 + 4 gardiens + preuve navigateur) ;
2. Toute amélioration constatée pendant le travail.

**Arrêt après ce lot — validation humaine requise.**
