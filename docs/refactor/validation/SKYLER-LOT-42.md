# SKYLER V2 — LOT 42 : intégrité de l'export souverain

Date : 2026-08-05 · Branche : `agent/skyler-v2-lot-42-export-integrity`
(base : `integration/vertex-skyler-v2` @ `12b00dd`) · Mode : travail continu
(directive utilisateur « go sans validation humaine », 24h/24).

## 1. Choix du lot (backlog) — justification

Backlog proposé au réveil : (a) intégrité de l'export (checksum et/ou
ledger_health embarqué), (b) fuzz clés encodées /memory/cell, (c) biais
par type de catalyseur dans detect_patterns. Choix : **(a), les deux
volets** — ils forment UNE propriété cohérente d'archive :

- l'export (lot 29) est la sauvegarde de la donnée la plus précieuse du
  desk, mais un fichier de sauvegarde muet sur sa propre cohérence et
  sans empreinte n'est qu'à moitié souverain : impossible de savoir des
  mois plus tard s'il a été altéré ou s'il était déjà incohérent ;
- (c) vérifié honnêtement : `by_catalyst_type` (lot 30) donne déjà la
  découpe d'observation en cellules ; un « pattern » dédié n'apporterait
  aujourd'hui aucune information nouvelle sans échantillons mesurés
  réels — reporté, dit franchement ; (b) patrons voisins déjà couverts
  (lot 34).

## 2. Périmètre livré — `GET /api/skyler/memory/export`

- **`ledger_health` embarqué** : la santé du ledger (lot 35) calculée AU
  MOMENT de l'export — l'archive dit elle-même si elle était cohérente ;
  un magasin corrompu est **fidèlement empreinté, jamais maquillé**
  (prouvé : export d'un magasin corrompu → `ANOMALIES` dit + empreinte
  exacte) ;
- **`content_sha256`** : sha256 du JSON CANONIQUE du bundle (clés
  triées, `separators=(',',':')`, contenu SANS le champ d'empreinte) —
  **vérifiable HORS LIGNE** par quiconque détient le fichier, sans le
  serveur ; la méthode de vérification est documentée dans la `note` du
  bundle lui-même ;
- toujours strictement lecture seule (octets identiques avant/après —
  gardien du lot 29 re-prouvé avec les nouveaux champs).

Aucun changement de shell → **SW v106 inchangé** (API seulement).

## 3. Méthode — rouge d'abord

`tests/test_export_integrity_lot42.py` (6 tests) écrit AVANT ; confirmé
rouge : **5 failed / 1 passed** (le passant : lecture seule, déjà vraie).
Après : **6 passed**, et les 7 gardiens du lot 29 restent verts.

Couverture : ledger_health SAIN embarqué ; ledger incohérent (outcome
orphelin) → ANOMALIES dit dans l'archive ; empreinte vérifiée hors ligne
par recalcul indépendant dans le test ; note documente la vérification ;
lecture seule stricte re-prouvée ; magasin corrompu → empreinte exacte +
ANOMALIES.

## 4. Preuves

```text
python -m pytest tests/test_export_integrity_lot42.py \
                 tests/test_memory_export_lot29.py -q → 13 passed
python -m compileall -q terminal.py vertex            → exit 0
python -m pytest tests/ -q → 1599 passed, 2 skipped   (baseline 1593 → +6)
```

Moteur 0.9.0 inchangé (l'export lit et empreinte, ne décide rien).

## 5. Invariants tenus

- lecture seule stricte (octets identiques, re-prouvé) ; READONLY absolu ;
- données réelles uniquement : l'archive corrompue est empreintée telle
  quelle et son incohérence DITE — jamais maquillée ;
- vérification souveraine : hors ligne, sans le serveur, méthode
  documentée dans le fichier même ;
- fichiers runtime jamais commités ; gardiens prospectifs ; `main`
  intacte ; SW inchangé.

## 6. Backlog restant (candidats lot 43)

1. Bilan périodique 38→42 (si le rythme de consolidation le justifie) ;
2. Pattern biais par type de catalyseur — QUAND des échantillons mesurés
   réels existeront (reporté honnêtement ce lot) ;
3. Toute amélioration constatée pendant le travail.

**Arrêt après ce lot — validation humaine requise.**
